"""
Airtable MCP Agent using LangChain
Generates and executes Python code to interact with Airtable via MCP.
"""

import os
import json
from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from code_executor import CodeExecutor


class AirtableMCPAgent:
    """Agent that generates and executes code for Airtable operations."""
    
    def __init__(self, api_key: str, mcp_url: str = "http://localhost:8000/mcp"):
        """
        Initialize the agent.
        
        Args:
            api_key: Anthropic API key
            mcp_url: URL of the Airtable MCP server
        """
        self.llm = ChatAnthropic(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            temperature=0
        )
        self.executor = CodeExecutor(timeout=60)
        self.mcp_url = mcp_url
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the agent."""
        return f"""You are an Airtable automation expert using the MCP (Model Context Protocol) code execution pattern.

CRITICAL RULES:
1. ALWAYS generate Python code that uses the Airtable MCP client wrappers
2. Process data IN CODE, not in context - this is the key to efficiency!
3. Return only summaries/results via print() statements
4. Use async/await for all Airtable operations
5. Handle errors gracefully with try/except

AVAILABLE TOOLS (from airtable_mcp_client.servers.airtable):
- list_bases() → List all Airtable bases
- list_tables(base_id, detail_level="full") → List tables in a base
- describe_table(base_id, table_id) → Get table schema
- list_records(base_id, table_id, max_records=None, filter_by_formula=None, sort=None, view=None)
- search_records(base_id, table_id, search_term, field_ids=None, max_records=None)
- get_record(base_id, table_id, record_id) → Get single record
- create_record(base_id, table_id, fields) → Create new record
- update_records(base_id, table_id, records) → Update up to 10 records (batch)
- delete_records(base_id, table_id, record_ids) → Delete records (batch)
- create_comment(base_id, table_id, record_id, text) → Add comment
- list_comments(base_id, table_id, record_id) → List comments

CODE TEMPLATE:
```python
from airtable_mcp_client.airtable_client import airtable_client

async with airtable_client("{self.mcp_url}") as client:
    from airtable_mcp_client.servers import airtable

    # Your code here
    # Process data in code, print only summaries

    print(json.dumps({{"result": "your summary here"}}))
```

CONTEXT EFFICIENCY EXAMPLE (KEY PATTERN):
```python
# Get ALL records (could be thousands)
records = await airtable.list_records(base_id, table_id)

# Process in code - NOT in context!
active = [r for r in records if r['fields'].get('Status') == 'Active']
inactive = [r for r in records if r['fields'].get('Status') == 'Inactive']

# Only print summary
print(json.dumps({{
    "total": len(records),
    "active": len(active),
    "inactive": len(inactive)
}}))
```

RESPONSE FORMAT:
Generate ONLY the Python code inside the async with block. No markdown formatting.
Start with: from airtable_mcp_client.airtable_client import airtable_client
"""
    
    async def run(self, user_input: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Run the agent on user input.
        
        Args:
            user_input: User's request
            max_retries: Maximum retry attempts for failed code
            
        Returns:
            Dictionary with result and execution details
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        attempt = 0
        last_error = None
        
        while attempt <= max_retries:
            try:
                # Generate code
                code = await self._generate_code(user_input, last_error)
                
                print(f"\n{'='*60}")
                print(f"Generated Code (Attempt {attempt + 1}):")
                print(f"{'='*60}")
                print(code)
                print(f"{'='*60}\n")
                
                # Execute code
                result = await self.executor.execute(code)
                
                if result["success"]:
                    # Success! Add to history and return
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": f"Generated and executed code successfully. Output:\n{result['stdout']}"
                    })
                    
                    return {
                        "success": True,
                        "output": result["stdout"],
                        "code": code,
                        "attempts": attempt + 1
                    }
                else:
                    # Execution failed
                    last_error = result["stderr"]
                    print(f"❌ Execution failed: {last_error}")
                    
                    if attempt == max_retries:
                        return {
                            "success": False,
                            "error": last_error,
                            "code": code,
                            "attempts": attempt + 1
                        }
                    
                    attempt += 1
                    print(f"🔄 Retrying (attempt {attempt + 1}/{max_retries + 1})...\n")
            
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "attempts": attempt + 1
                }
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "attempts": attempt + 1
        }
    
    async def _generate_code(self, user_input: str, error_context: str = None) -> str:
        """Generate Python code for the user's request."""
        # Build messages
        messages = [
            SystemMessage(content=self.system_prompt)
        ]
        
        # Add conversation history
        for msg in self.conversation_history[-5:]:  # Last 5 messages for context
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # Add current request with error context if retrying
        if error_context:
            current_msg = f"""{user_input}

PREVIOUS ATTEMPT FAILED WITH ERROR:
{error_context}

Please fix the code and try again. Focus on:
1. Correct syntax
2. Proper async/await usage
3. Correct field names and IDs
4. Error handling
"""
        else:
            current_msg = user_input
        
        messages.append(HumanMessage(content=current_msg))
        
        # Generate code
        response = await self.llm.ainvoke(messages)
        
        # Extract code from response
        code = response.content.strip()
        
        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code.split("```python")[1]
            code = code.split("```")[0]
        elif code.startswith("```"):
            code = code.split("```")[1]
            code = code.split("```")[0]
        
        return code.strip()
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []


# Quick test
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ Please set ANTHROPIC_API_KEY environment variable")
            return
        
        agent = AirtableMCPAgent(api_key)
        
        # Test query
        result = await agent.run("List all my Airtable bases")
        
        if result["success"]:
            print("\n✅ Success!")
            print(f"Output:\n{result['output']}")
        else:
            print(f"\n❌ Failed: {result['error']}")
    
    asyncio.run(test())
