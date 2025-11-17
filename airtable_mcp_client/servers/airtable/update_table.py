"""Update a table's name or description."""
from typing import Any, Dict, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def update_table(
    base_id: str,
    table_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a table's name or description.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        name: New name for the table (optional)
        description: New description for the table (optional)
    
    Returns:
        Updated table dictionary
    
    Example:
        table = await update_table(
            base_id='appXXXXXXXXXXXXXX',
            table_id='tblXXXXXXXXXXXXXX',
            name='Updated Table Name',
            description='Updated description'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id
    }
    
    if name is not None:
        arguments["name"] = name
    if description is not None:
        arguments["description"] = description
    
    return await call_mcp_tool("update_table", arguments)