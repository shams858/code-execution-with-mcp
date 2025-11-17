"""Delete records from a table."""
from typing import Any, Dict, List
from airtable_mcp_client.airtable_client import call_mcp_tool


async def delete_records(
    base_id: str,
    table_id: str,
    record_ids: List[str]
) -> Dict[str, Any]:
    """
    Delete records from a table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        record_ids: List of record IDs to delete
    
    Returns:
        Result dictionary
    
    Example:
        result = await delete_records(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            record_ids=['recXXX1', 'recXXX2']
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "recordIds": record_ids
    }
    
    return await call_mcp_tool("delete_records", arguments)