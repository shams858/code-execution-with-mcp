"""Create a comment on a record."""
from typing import Any, Dict, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def create_comment(
    base_id: str,
    table_id: str,
    record_id: str,
    text: str,
    parent_comment_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a comment on a record.
    
    Args:
        base_id: The ID of the base
        table_id: The ID or name of the table
        record_id: The ID of the record
        text: The comment text
        parent_comment_id: Optional parent comment ID for threaded replies
    
    Returns:
        Created comment dictionary
    
    Example:
        comment = await create_comment(
            base_id='appXXXXXXXXXXXXXX',
            table_id='Contacts',
            record_id='recXXXXXXXXXXXXXX',
            text='This is a comment'
        )
    """
    arguments = {
        "baseId": base_id,
        "tableId": table_id,
        "recordId": record_id,
        "text": text
    }
    
    if parent_comment_id is not None:
        arguments["parentCommentId"] = parent_comment_id
    
    return await call_mcp_tool("create_comment", arguments)