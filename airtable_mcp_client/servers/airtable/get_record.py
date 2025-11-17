"""Get a specific record by ID."""
from typing import Any, Dict
from airtable_mcp_client.airtable_client import call_mcp_tool


async def get_record(
    base_id: str,
    table_id: str,
    record_id: str
) -> Dict[str, Any]:
    """
    Get a specific record by ID.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        record_id: The ID of the record
    
    Returns:
        Record dictionary
    
    Example:
        record = await get_record(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            record_id='recXXXXXXXXXXXXXX'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "recordId": record_id
    }
    
    return await call_mcp_tool("get_record", arguments)