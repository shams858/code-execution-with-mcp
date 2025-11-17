"""Get detailed information about a specific table."""
from typing import Any, Dict, Literal, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def describe_table(
    base_id: str,
    table_id: str,
    detail_level: Optional[Literal["tableIdentifiersOnly", "identifiersOnly", "full"]] = "full"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        detail_level: Level of detail to return (default: "full")
    
    Returns:
        Table information dictionary
    
    Example:
        table_info = await describe_table(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "detailLevel": detail_level
    }
    
    return await call_mcp_tool("describe_table", arguments)