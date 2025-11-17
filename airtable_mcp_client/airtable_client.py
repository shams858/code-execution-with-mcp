"""
Airtable MCP Client for Existing Server
Connects to your running Airtable MCP server at http://localhost:8000/mcp
"""

import json
import asyncio
import aiohttp
from typing import Any, Dict, Optional, TypeVar
from contextlib import asynccontextmanager

T = TypeVar('T')


class AirtableMCPClient:
    """Client for connecting to the Airtable MCP Server."""
    
    def __init__(self, url: str = "http://localhost:8000/mcp"):
        """
        Initialize the MCP client.
        
        Args:
            url: URL of the MCP server
        """
        self.url = url
        self.session: Optional[aiohttp.ClientSession] = None
        self._request_id = 0
    
    async def connect(self):
        """Create HTTP session."""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
    
    async def _parse_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """
        Parse response from MCP server, handling both JSON and SSE formats.
        
        Args:
            response: The HTTP response object
            
        Returns:
            Parsed JSON response as a dictionary
        """
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'text/event-stream' in content_type:
            # Parse Server-Sent Events format
            text = await response.text()
            # SSE format: "event: message\ndata: {...}\n\n"
            # Extract JSON from data: lines
            lines = text.strip().split('\n')
            json_data = None
            
            for line in lines:
                if line.startswith('data: '):
                    json_str = line[6:]  # Remove "data: " prefix
                    try:
                        json_data = json.loads(json_str)
                        break
                    except json.JSONDecodeError:
                        continue
            
            if json_data is None:
                raise RuntimeError(f"Could not parse SSE response: {text}")
            
            return json_data
        else:
            # Standard JSON response
            return await response.json()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool and return the result.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments for the tool
            
        Returns:
            The tool's response
        """
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        self._request_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        async with self.session.post(self.url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
            
            result = await self._parse_response(response)
            
            if "error" in result:
                raise RuntimeError(f"MCP Error: {result['error']}")
            
            # Extract content from MCP response
            if "result" in result and "content" in result["result"]:
                content = result["result"]["content"]
                if content and len(content) > 0:
                    # Return the text content, parsed as JSON if possible
                    text = content[0].get("text", "")
                    try:
                        return json.loads(text)
                    except:
                        return text
            
            return result.get("result")
    
    async def list_tools(self):
        """List all available tools."""
        if not self.session:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        self._request_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": "tools/list",
            "params": {}
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        async with self.session.post(self.url, json=payload, headers=headers) as response:
            # Check status code first
            if response.status != 200:
                response_text = await response.text()
                content_type = response.headers.get('Content-Type', 'unknown')
                raise RuntimeError(
                    f"HTTP {response.status}: {response_text}\n"
                    f"Content-Type: {content_type}\n"
                    f"URL: {self.url}"
                )
            
            result = await self._parse_response(response)
            return result.get("result", {}).get("tools", [])


# Global client instance
_global_client: Optional[AirtableMCPClient] = None


def set_global_client(client: AirtableMCPClient):
    """Set the global MCP client instance."""
    global _global_client
    _global_client = client


def get_global_client() -> AirtableMCPClient:
    """Get the global MCP client instance."""
    if _global_client is None:
        raise RuntimeError("No global client set. Use airtable_client() context manager.")
    return _global_client


async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> T:
    """Call an MCP tool using the global client."""
    client = get_global_client()
    return await client.call_tool(tool_name, arguments)


@asynccontextmanager
async def airtable_client(url: str = "http://localhost:8000/mcp"):
    """
    Context manager for Airtable MCP client.
    
    Usage:
        async with airtable_client() as client:
            from servers import airtable
            bases = await airtable.list_bases()
    """
    client = AirtableMCPClient(url)
    await client.connect()
    set_global_client(client)
    
    try:
        yield client
    finally:
        await client.close()


# ============================================================================
# Quick test
# ============================================================================

async def test_connection():
    """Test connection to the MCP server."""
    print("Testing connection to Airtable MCP Server...")
    
    async with airtable_client() as client:
        # List available tools
        tools = await client.list_tools()
        print(f"\n[OK] Connected! Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")


if __name__ == "__main__":
    asyncio.run(test_connection())
