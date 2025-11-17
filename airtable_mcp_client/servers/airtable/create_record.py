"""Create a new record in a table."""
from typing import Any, Dict
from airtable_mcp_client.airtable_client import call_mcp_tool


async def create_record(
    base_id: str,
    table_id: str,
    fields: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new record in a table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        fields: Dictionary of field names and values
    
    Returns:
        Created record dictionary
    
    Example:
        record = await create_record(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            fields={
                'Name': 'John Doe',
                'Email': 'john@example.com',
                'Status': 'Active'
            }
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "fields": fields
    }
    
    return await call_mcp_tool("create_record", arguments)