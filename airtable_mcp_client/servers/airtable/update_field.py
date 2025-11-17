"""Update a field's name or description."""
from typing import Any, Dict, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def update_field(
    base_id: str,
    table_id: str,
    field_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a field's name or description.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        field_id: The ID of the field
        name: New name for the field (optional)
        description: New description for the field (optional)
    
    Returns:
        Updated field dictionary
    
    Example:
        field = await update_field(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            field_id='fldXXXXXXXXXXXXXX',
            name='Updated Field Name',
            description='Updated description'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "fieldId": field_id
    }
    
    if name is not None:
        arguments["name"] = name
    if description is not None:
        arguments["description"] = description
    
    return await call_mcp_tool("update_field", arguments)
