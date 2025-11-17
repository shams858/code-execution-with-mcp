"""List comments on a record."""
from typing import Any, Dict, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def list_comments(
    base_id: str,
    table_id: str,
    record_id: str,
    page_size: Optional[int] = None,
    offset: Optional[str] = None
) -> Dict[str, Any]:
    """
    List comments on a record.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        record_id: The ID of the record
        page_size: Number of comments to return (max 100, default 100)
        offset: Offset for pagination (optional)
    
    Returns:
        Dictionary with comments and pagination info
    
    Example:
        result = await list_comments(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            record_id='recXXXXXXXXXXXXXX'
        )
        comments = result['comments']
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "recordId": record_id
    }
    
    if page_size is not None:
        arguments["pageSize"] = page_size
    if offset is not None:
        arguments["offset"] = offset
    
    return await call_mcp_tool("list_comments", arguments)