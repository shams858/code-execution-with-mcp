"""List records from a table."""
from typing import Any, Dict, List, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def list_records(
    base_id: str,
    table_id: str,
    view: Optional[str] = None,
    max_records: Optional[int] = None,
    filter_by_formula: Optional[str] = None,
    sort: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, Any]]:
    """
    List records from a table.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        view: The name or ID of a view in the table (optional)
        max_records: The maximum total number of records to return (optional)
        filter_by_formula: A formula used to filter records (optional)
        sort: List of sort objects (optional)
            Example: [{"field": "Name", "direction": "asc"}]
    
    Returns:
        List of record dictionaries
    
    Example:
        records = await list_records(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            filter_by_formula='{Status} = "Active"',
            max_records=100
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id
    }
    
    if view is not None:
        arguments["view"] = view
    if max_records is not None:
        arguments["maxRecords"] = max_records
    if filter_by_formula is not None:
        arguments["filterByFormula"] = filter_by_formula
    if sort is not None:
        arguments["sort"] = sort
    
    return await call_mcp_tool("list_records", arguments)