# Airtable MCP Agent - MVP

AI agent that generates and executes Python code to interact with Airtable using the MCP code execution pattern from [Anthropic's blog](https://www.anthropic.com/engineering/code-execution-with-mcp).

## Architecture

```
User Input → Claude Sonnet 4 → Python Code → Subprocess → Airtable MCP → Results
```

**Key benefit**: Process data in code, not in context = 98.7% token efficiency!

## Quick Start

### 1. Prerequisites

```bash
# Airtable MCP server running at http://localhost:8000/mcp
# Anthropic API key
```

### 2. Install

```bash
pip install langchain langchain-anthropic anthropic aiohttp
```

### 3. Set API Key

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 4. Run

```bash
python cli.py
```

## Files

```
agent/
├── code_executor.py      # Sandboxed code execution
├── airtable_agent.py     # LangChain agent
├── cli.py                # Command-line interface
└── requirements.txt      # Dependencies
```

## Usage

```
You: List all my Airtable bases

🤖 Agent: Thinking...

Generated Code (Attempt 1):
============================================================
from airtable_client import airtable_client

async with airtable_client("http://localhost:8000/mcp") as client:
    from servers import airtable
    
    bases = await airtable.list_bases()
    print(json.dumps({"bases": bases}))
============================================================

✅ Success!

Output:
------------------------------------------------------------
{"bases": [{"id": "appXXX", "name": "My Base"}]}
------------------------------------------------------------
```

## Example Queries

```
"List all my bases"
"Show tables in base appXXXXXXXXXXXXXX"
"Get all active contacts from Contacts table"
"Search for john@example.com"
"Create a contact: name=John, email=john@example.com"
"Analyze sales data and show top 5 performers"
```

## Commands

```
/help   - Show help
/clear  - Clear conversation history
/exit   - Exit
```

## How It Works

1. **User request** → "Get all active contacts"
2. **Claude generates code**:
   ```python
   records = await airtable.list_records(...)
   active = [r for r in records if r['fields']['Status'] == 'Active']
   print(len(active))  # Only summary to context!
   ```
3. **Execute in subprocess** (sandboxed, validated)
4. **Return results** to user

