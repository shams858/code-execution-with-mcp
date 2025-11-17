"""Update up to 10 records in a table."""
from typing import Any, Dict, List
from airtable_mcp_client.airtable_client import call_mcp_tool


async def update_records(
    base_id: str,
    table_id: str,
    records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Update up to 10 records in a table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        records: List of record dictionaries with 'id' and 'fields'
            Example: [{"id": "recXXX", "fields": {"Name": "Updated"}}]
    
    Returns:
        List of updated record dictionaries
    
    Example:
        updated = await update_records(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            records=[
                {'id': 'recXXX1', 'fields': {'Status': 'Active'}},
                {'id': 'recXXX2', 'fields': {'Status': 'Inactive'}}
            ]
        )
    """
    if len(records) > 10:
        raise ValueError("Cannot update more than 10 records at once")
    
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "records": records
    }
    
    return await call_mcp_tool("update_records", arguments)