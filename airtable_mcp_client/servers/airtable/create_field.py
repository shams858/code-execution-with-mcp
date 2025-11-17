"""Create a new field in a table."""
from typing import Any, Dict
from airtable_mcp_client.airtable_client import call_mcp_tool


async def create_field(
    base_id: str,
    table_id: str,
    field: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new field in a table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        field: Field definition dictionary
            Example: {"name": "New Field", "type": "singleLineText"}
    
    Returns:
        Created field dictionary
    
    Example:
        field = await create_field(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            field={
                'name': 'Phone',
                'type': 'phoneNumber'
            }
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "nested": {
            "field": field
        }
    }
    
    return await call_mcp_tool("create_field", arguments)