"""
Complete usage examples for your existing Airtable MCP Server.
Demonstrates the code execution pattern from Anthropic's blog.
"""

import asyncio
from datetime import datetime
from airtable_client import airtable_client


# ============================================================================
# Example 1: Basic Operations
# ============================================================================
async def example_basic_operations():
    """Test basic CRUD operations."""
    print("=== Example 1: Basic Operations ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        # List all bases
        print("Listing bases...")
        bases = await airtable.list_bases()
        print(f"Found {len(bases)} bases:")
        for base in bases:
            print(f"  - {base.get('name', 'Unknown')}: {base.get('id')}")
        
        if not bases:
            print("No bases found!")
            return
        
        base_id = bases[0]['id']
        print(f"\nUsing base: {base_id}")
        
        # List tables
        print("\nListing tables...")
        tables = await airtable.list_tables(base_id)
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table.get('name', 'Unknown')}: {table.get('id')}")
        
        if not tables:
            print("No tables found!")
            return
        
        table_id = tables[0]['id']
        table_name = tables[0].get('name', 'Unknown')
        print(f"\nUsing table: {table_name} ({table_id})")
        
        # Get table details
        print(f"\nDescribing table '{table_name}'...")
        table_info = await airtable.describe_table(base_id, table_id)
        print(f"Table has {len(table_info.get('fields', []))} fields:")
        for field in table_info.get('fields', [])[:5]:  # Show first 5
            print(f"  - {field.get('name')}: {field.get('type')}")
        
        # List records
        print(f"\nListing records from '{table_name}'...")
        records = await airtable.list_records(
            base_id=base_id,
            table_id=table_id,
            max_records=5
        )
        print(f"Retrieved {len(records)} records")
        
        if records:
            print("\nFirst record:")
            print(f"  ID: {records[0].get('id')}")
            print(f"  Fields: {list(records[0].get('fields', {}).keys())}")


# ============================================================================
# Example 2: Context-Efficient Data Processing
# ============================================================================
async def example_efficient_filtering():
    """
    Process large datasets efficiently.
    Key benefit: Only summary reaches the model context!
    """
    print("\n=== Example 2: Context-Efficient Data Processing ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        # Get your base and table IDs
        bases = await airtable.list_bases()
        if not bases:
            print("No bases found!")
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        if not tables:
            print("No tables found!")
            return
        
        table_id = tables[0]['id']
        
        # Get ALL records - could be thousands!
        print(f"Fetching all records...")
        all_records = await airtable.list_records(
            base_id=base_id,
            table_id=table_id
        )
        
        print(f"Retrieved {len(all_records)} total records")
        
        # Process in code - NOT in context!
        # This is where the magic happens
        fields_summary = {}
        for record in all_records:
            for field_name in record.get('fields', {}).keys():
                fields_summary[field_name] = fields_summary.get(field_name, 0) + 1
        
        # Only the summary reaches the model context!
        print(f"\nSummary (only this goes to context):")
        print(f"  - Total records: {len(all_records)}")
        print(f"  - Unique fields: {len(fields_summary)}")
        print(f"\nField usage:")
        for field, count in sorted(fields_summary.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {field}: {count} records")


# ============================================================================
# Example 3: Search and Filter
# ============================================================================
async def example_search_and_filter():
    """Search for records and apply filters."""
    print("\n=== Example 3: Search and Filter ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        bases = await airtable.list_bases()
        if not bases:
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        if not tables:
            return
        
        table_id = tables[0]['id']
        
        # Search for records
        print("Searching for records...")
        search_results = await airtable.search_records(
            base_id=base_id,
            table_id=table_id,
            search_term="test",  # Replace with actual search term
            max_records=10
        )
        print(f"Found {len(search_results)} matching records")
        
        # Filter with formula
        print("\nFiltering records with formula...")
        filtered = await airtable.list_records(
            base_id=base_id,
            table_id=table_id,
            filter_by_formula='{Status} = "Active"',  # Adjust field name
            max_records=10
        )
        print(f"Found {len(filtered)} filtered records")
        
        # Sort records
        print("\nSorting records...")
        sorted_records = await airtable.list_records(
            base_id=base_id,
            table_id=table_id,
            sort=[{"field": "Created", "direction": "desc"}],  # Adjust field name
            max_records=10
        )
        print(f"Retrieved {len(sorted_records)} sorted records")


# ============================================================================
# Example 4: Batch Updates
# ============================================================================
async def example_batch_operations():
    """Demonstrate batch create, update, and delete."""
    print("\n=== Example 4: Batch Operations ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        bases = await airtable.list_bases()
        if not bases:
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        if not tables:
            return
        
        table_id = tables[0]['id']
        table_info = await airtable.describe_table(base_id, table_id)
        
        # Get the first text field for testing
        text_fields = [f for f in table_info.get('fields', []) 
                      if f.get('type') in ['singleLineText', 'multilineText']]
        
        if not text_fields:
            print("No text fields found for testing")
            return
        
        field_name = text_fields[0]['name']
        
        # Create a test record
        print(f"Creating test record with field '{field_name}'...")
        new_record = await airtable.create_record(
            base_id=base_id,
            table_id=table_id,
            fields={field_name: f"Test record {datetime.now().isoformat()}"}
        )
        record_id = new_record.get('id')
        print(f"Created record: {record_id}")
        
        # Update the record (batch update with 1 record)
        print("\nUpdating record...")
        updated = await airtable.update_records(
            base_id=base_id,
            table_id=table_id,
            records=[{
                'id': record_id,
                'fields': {field_name: f"Updated at {datetime.now().isoformat()}"}
            }]
        )
        print(f"Updated {len(updated)} record(s)")
        
        # Get the updated record
        print("\nFetching updated record...")
        fetched = await airtable.get_record(
            base_id=base_id,
            table_id=table_id,
            record_id=record_id
        )
        print(f"Record field value: {fetched.get('fields', {}).get(field_name)}")
        
        # Delete the test record
        print("\nDeleting test record...")
        await airtable.delete_records(
            base_id=base_id,
            table_id=table_id,
            record_ids=[record_id]
        )
        print("Record deleted")


# ============================================================================
# Example 5: Working with Comments
# ============================================================================
async def example_comments():
    """Add and list comments on records."""
    print("\n=== Example 5: Working with Comments ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        bases = await airtable.list_bases()
        if not bases:
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        if not tables:
            return
        
        table_id = tables[0]['id']
        
        # Get first record
        records = await airtable.list_records(
            base_id=base_id,
            table_id=table_id,
            max_records=1
        )
        
        if not records:
            print("No records found to comment on")
            return
        
        record_id = records[0]['id']
        
        # Create a comment
        print(f"Creating comment on record {record_id}...")
        comment = await airtable.create_comment(
            base_id=base_id,
            table_id=table_id,
            record_id=record_id,
            text=f"Test comment created at {datetime.now().isoformat()}"
        )
        print(f"Comment created: {comment.get('id')}")
        
        # List comments
        print("\nListing comments...")
        comments_result = await airtable.list_comments(
            base_id=base_id,
            table_id=table_id,
            record_id=record_id
        )
        comments = comments_result.get('comments', [])
        print(f"Found {len(comments)} comments on this record")
        
        for i, c in enumerate(comments[:3], 1):  # Show first 3
            print(f"  {i}. {c.get('text', '')[:50]}...")


# ============================================================================
# Example 6: Large Dataset Processing (Context-Efficient)
# ============================================================================
async def example_large_dataset_processing():
    """
    Process large datasets efficiently.
    Demonstrates 98.7% token reduction from the Anthropic blog!
    """
    print("\n=== Example 6: Large Dataset Processing ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        bases = await airtable.list_bases()
        if not bases:
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        if not tables:
            return
        
        table_id = tables[0]['id']
        
        # Get large dataset
        print("Fetching dataset...")
        all_records = await airtable.list_records(
            base_id=base_id,
            table_id=table_id
        )
        
        print(f"Processing {len(all_records)} records in code...")
        
        # Complex analysis happens in code, not in context!
        from collections import defaultdict
        
        stats = {
            'total': len(all_records),
            'with_data': 0,
            'empty': 0,
            'field_counts': defaultdict(int)
        }
        
        for record in all_records:
            fields = record.get('fields', {})
            if fields:
                stats['with_data'] += 1
                for field_name in fields.keys():
                    stats['field_counts'][field_name] += 1
            else:
                stats['empty'] += 1
        
        # Only summary reaches context!
        print("\n📊 Dataset Summary (context-efficient):")
        print(f"  Total records: {stats['total']}")
        print(f"  Records with data: {stats['with_data']}")
        print(f"  Empty records: {stats['empty']}")
        print(f"\n  Top 5 most used fields:")
        for field, count in sorted(stats['field_counts'].items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)[:5]:
            pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"    - {field}: {count} ({pct:.1f}%)")


# ============================================================================
# Example 7: Data Migration Pattern
# ============================================================================
async def example_data_migration():
    """
    Example of migrating/syncing data between tables.
    All transformation happens in code, not context!
    """
    print("\n=== Example 7: Data Migration Pattern ===\n")
    
    async with airtable_client() as client:
        from servers import airtable
        
        bases = await airtable.list_bases()
        if not bases:
            return
        
        base_id = bases[0]['id']
        tables = await airtable.list_tables(base_id)
        
        if len(tables) < 2:
            print("Need at least 2 tables for migration example")
            return
        
        source_table = tables[0]['id']
        dest_table = tables[1]['id']
        
        print(f"Source: {tables[0].get('name')}")
        print(f"Destination: {tables[1].get('name')}")
        
        # Get source records
        print("\nFetching source records...")
        source_records = await airtable.list_records(
            base_id=base_id,
            table_id=source_table,
            max_records=5  # Limit for demo
        )
        
        print(f"Found {len(source_records)} source records")
        
        # Transform in code (not in context!)
        print("\nTransforming data...")
        # This is where you'd do complex transformations
        # For demo, we'll just show the pattern
        
        print("\nMigration pattern:")
        print("  1. Fetch source data")
        print("  2. Transform in code (context-efficient!)")
        print("  3. Batch insert to destination")
        print("  4. Update source with migration status")
        print("\nAll data transformation happens in code, not in context!")


# ============================================================================
# Run all examples
# ============================================================================
async def main():
    """Run all examples."""
    print("="*70)
    print("Airtable MCP Client - Complete Usage Examples")
    print("Connecting to: http://localhost:8000/mcp")
    print("="*70 + "\n")
    
    try:
        await example_basic_operations()
        await example_efficient_filtering()
        await example_search_and_filter()
        await example_batch_operations()
        await example_comments()
        await example_large_dataset_processing()
        await example_data_migration()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
