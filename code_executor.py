"""
Code Executor for Airtable MCP Agent
Executes generated Python code in a sandboxed subprocess.
"""

import subprocess
import asyncio
import tempfile
import os
import sys
import ast
from pathlib import Path
from typing import Dict, Any, Optional


class CodeExecutor:
    """Executes Python code in a sandboxed subprocess."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize code executor.
        
        Args:
            timeout: Maximum execution time in seconds
        """
        self.timeout = timeout
        self.dangerous_imports = {
            'os', 'subprocess', 'sys', '__import__', 'eval', 'exec',
            'open', 'file', 'input', 'compile', 'reload'
        }
    
    def validate_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate code for dangerous operations.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        # Check for dangerous imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(danger in alias.name for danger in self.dangerous_imports):
                        return False, f"Forbidden import: {alias.name}"
            
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(danger in node.module for danger in self.dangerous_imports):
                    return False, f"Forbidden import: {node.module}"
        
        return True, None
    
    async def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute code in a subprocess.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary with stdout, stderr, and exit_code
        """
        # Validate code first
        is_valid, error = self.validate_code(code)
        if not is_valid:
            return {
                "success": False,
                "stdout": "",
                "stderr": error,
                "exit_code": 1
            }
        
        # Create temporary file with code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Add necessary imports at the top
            full_code = f"""
import asyncio
import sys
import json
from pathlib import Path

# Add project directory to path for imports
sys.path.insert(0, r"{os.getcwd()}")

async def main():
{self._indent_code(code, 1)}

if __name__ == "__main__":
    asyncio.run(main())
"""
            f.write(full_code)
            temp_file = f.name
        
        try:
            # Execute in subprocess using same Python interpreter
            process = await asyncio.create_subprocess_exec(
                sys.executable, temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            # Wait with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
                
                return {
                    "success": process.returncode == 0,
                    "stdout": stdout.decode('utf-8'),
                    "stderr": stderr.decode('utf-8'),
                    "exit_code": process.returncode
                }
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Execution timeout after {self.timeout} seconds",
                    "exit_code": -1
                }
        
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def _indent_code(self, code: str, levels: int) -> str:
        """Indent code by specified levels."""
        indent = "    " * levels
        return "\n".join(indent + line if line.strip() else line 
                        for line in code.split("\n"))


# Quick test
if __name__ == "__main__":
    async def test():
        executor = CodeExecutor()
        
        # Test valid code
        code = """
print("Hello from subprocess!")
result = {"status": "success", "value": 42}
print(f"Result: {result}")
"""
        
        print("Testing code execution...")
        result = await executor.execute(code)
        print(f"Success: {result['success']}")
        print(f"Output: {result['stdout']}")
        if result['stderr']:
            print(f"Errors: {result['stderr']}")
        
        # Test invalid code
        print("\nTesting validation...")
        code_bad = "import os\nos.system('ls')"
        result = await executor.execute(code_bad)
        print(f"Success: {result['success']}")
        print(f"Error: {result['stderr']}")
    
    asyncio.run(test())
