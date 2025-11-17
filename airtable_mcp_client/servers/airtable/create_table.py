"""Create a new table in a base."""
from typing import Any, Dict, List, Optional
from airtable_mcp_client.airtable_client import call_mcp_tool


async def create_table(
    base_id: str,
    name: str,
    fields: List[Dict[str, Any]],
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new table in a base.
    
    Args:
        base_id: The ID of the base
        name: The name of the table
        fields: List of field definitions
            Example: [{"name": "Name", "type": "singleLineText"}]
        description: Optional description for the table
    
    Returns:
        Created table dictionary
    
    Example:
        table = await create_table(
            base_id='appXXXXXXXXXXXXXX',
            name='New Contacts',
            fields=[
                {'name': 'Name', 'type': 'singleLineText'},
                {'name': 'Email', 'type': 'email'},
                {'name': 'Status', 'type': 'singleSelect', 'options': {
                    'choices': [
                        {'name': 'Active'},
                        {'name': 'Inactive'}
                    ]
                }}
            ],
            description='Contact management table'
        )
    """
    arguments = {
        "baseId": base_id,
        "name": name,
        "fields": fields
    }
    
    if description is not None:
        arguments["description"] = description
    
    return await call_mcp_tool("create_table", arguments)