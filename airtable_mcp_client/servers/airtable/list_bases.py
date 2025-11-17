"""List all accessible Airtable bases."""
from typing import Any, Dict, List
from airtable_mcp_client.airtable_client import call_mcp_tool


async def list_bases() -> List[Dict[str, Any]]:
    """
    List all accessible Airtable bases.
    
    Returns:
        List of base dictionaries
    
    Example:
        bases = await list_bases()
        for base in bases:
            print(f"{base['name']}: {base['id']}")
    """
    return await call_mcp_tool("list_bases", {})