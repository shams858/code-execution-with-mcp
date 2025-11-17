"""Search for records containing specific text."""
from typing import Any, Dict, List, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def search_records(
    base_id: str,
    table_id: str,
    search_term: str,
    field_ids: Optional[List[str]] = None,
    max_records: Optional[int] = None,
    view: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for records containing specific text.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        search_term: The text to search for
        field_ids: Optional array of field IDs to search in
        max_records: Maximum number of records to return (optional)
        view: The name or ID of a view (optional)
    
    Returns:
        List of matching records
    
    Example:
        results = await search_records(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            search_term='john@example.com'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "searchTerm": search_term
    }
    
    if field_ids is not None:
        arguments["fieldIds"] = field_ids
    if max_records is not None:
        arguments["maxRecords"] = max_records
    if view is not None:
        arguments["view"] = view
    
    return await call_mcp_tool("search_records", arguments)