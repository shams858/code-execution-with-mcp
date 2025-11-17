"""
CLI Interface for Airtable MCP Agent
Simple command-line interface for interacting with the agent.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
import sys
from airtable_agent import AirtableMCPAgent


class CLI:
    """Command-line interface for the Airtable MCP Agent."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.agent = None
    
    def print_banner(self):
        """Print welcome banner."""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║         Airtable MCP Agent - Code Execution Pattern          ║
╚═══════════════════════════════════════════════════════════════╝

This agent generates and executes Python code to interact with
Airtable using the MCP protocol. Data is processed in code,
not in context, achieving 98.7% token efficiency!

Commands:
  /help     - Show this help message
  /clear    - Clear conversation history
  /exit     - Exit the program
  
Type your request and press Enter to begin.
""")
    
    def print_help(self):
        """Print help message."""
        print("""
Available Operations:
  • List bases and tables
  • Get table schemas and records
  • Search records
  • Create, update, delete records
  • Batch operations
  • Data analysis and reporting

Example Requests:
  "List all my Airtable bases"
  "Show me tables in base appXXXXXXXXXXXXXX"
  "Get all active contacts from my CRM base"
  "Find records containing 'john@example.com'"
  "Create a new contact with name John and email john@example.com"
  "Analyze my sales data and show top performers"
  "Count records in each table of my base"

Tips:
  • Be specific with base IDs and table names
  • The agent will process large datasets efficiently
  • Complex operations may take 10-60 seconds
  • Check generated code before execution
""")
    
    async def initialize_agent(self):
        """Initialize the agent with API key."""
        # Check for API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            print("❌ ANTHROPIC_API_KEY environment variable not set!")
            print("\nPlease set it with:")
            print("  export ANTHROPIC_API_KEY='your-api-key'")
            print("\nGet your API key from: https://console.anthropic.com/")
            return False
        
        # Check MCP server
        mcp_url = os.getenv("AIRTABLE_MCP_URL", "http://localhost:8000/mcp")
        
        print(f"🔌 Connecting to MCP server at {mcp_url}...")
        
        # TODO: Add connection test here
        
        print("✅ Initializing agent with Claude Sonnet 4...")
        self.agent = AirtableMCPAgent(api_key, mcp_url)
        print("✅ Agent ready!\n")
        
        return True
    
    async def handle_command(self, command: str) -> bool:
        """
        Handle special commands.
        
        Returns:
            True to continue, False to exit
        """
        command = command.strip().lower()
        
        if command == "/help":
            self.print_help()
            return True
        
        elif command == "/clear":
            if self.agent:
                self.agent.clear_history()
            print("✅ Conversation history cleared.\n")
            return True
        
        elif command in ["/exit", "/quit", "/q"]:
            print("\n👋 Goodbye!\n")
            return False
        
        return True
    
    async def run(self):
        """Run the CLI loop."""
        self.print_banner()
        
        # Initialize agent
        if not await self.initialize_agent():
            return
        
        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.startswith("/"):
                    should_continue = await self.handle_command(user_input)
                    if not should_continue:
                        break
                    continue
                
                # Process request
                print("\n🤖 Agent: Thinking...\n")
                
                result = await self.agent.run(user_input)
                
                if result["success"]:
                    print("✅ Success!\n")
                    print("Output:")
                    print("-" * 60)
                    print(result["output"])
                    print("-" * 60)
                    print(f"\n(Completed in {result['attempts']} attempt(s))\n")
                else:
                    print("❌ Failed!\n")
                    print("Error:")
                    print("-" * 60)
                    print(result.get("error", "Unknown error"))
                    print("-" * 60)
                    print(f"\n(Failed after {result['attempts']} attempt(s))\n")
                    print("💡 Tip: Try rephrasing your request or being more specific.\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Type /exit to quit or continue...\n")
                continue
            
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                continue


def main():
    """Main entry point."""
    cli = CLI()
    
    try:
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
