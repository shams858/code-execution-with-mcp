"""List all tables in a specific base."""
from typing import Any, Dict, List, Literal, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def list_tables(
    base_id: str,
    detail_level: Optional[Literal["tableIdentifiersOnly", "identifiersOnly", "full"]] = "full"
) -> List[Dict[str, Any]]:
    """
    List all tables in a specific base.
    
    Args:
        base_id: The ID of the base
        detail_level: Level of detail to return (default: "full")
            - "tableIdentifiersOnly": Only table IDs and names
            - "identifiersOnly": Table and field IDs/names
            - "full": Complete schema information
    
    Returns:
        List of table dictionaries
    
    Example:
        tables = await list_tables(
            base_id='appXXXXXXXXXXXXXX',
            detail_level='full'
        )
    """
    arguments = {
        "baseId": base_id,
        "detailLevel": detail_level
    }
    
    return await call_mcp_tool("list_tables", arguments)