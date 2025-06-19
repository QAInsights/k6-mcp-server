import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp = FastMCP("k6")

async def run_k6_script(script_file: str, duration: str = "30s", vus: int = 10) -> str:
    """Run a k6 load test script.

    Args:
        script_file: Path to the k6 test script (.js)
        duration: Duration of the test (e.g., "30s", "1m", "5m")
        vus: Number of virtual users to simulate

    Returns:
        str: k6 execution output
    """
    try:
        # Convert to absolute path
        script_file_path = Path(script_file).resolve()
        
        # Validate file exists and is a .js file
        if not script_file_path.exists():
            return f"Error: Script file not found: {script_file}"
        if not script_file_path.suffix == '.js':
            return f"Error: Invalid file type. Expected .js file: {script_file}"

        # Get k6 binary path from environment
        k6_bin = os.getenv('K6_BIN', 'k6')
        
        # Print the k6 binary path for debugging
        print(f"k6 binary path: {k6_bin}")

        # Build command
        cmd = [str(Path(k6_bin).resolve())]
        cmd.extend(['run'])
        cmd.extend(['-d', duration])
        cmd.extend(['-u', str(vus)])
        cmd.extend([str(script_file_path)])

        # Print the full command for debugging
        print(f"Executing command: {' '.join(cmd)}")
        
        # Run the command asynchronously and capture output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout_bytes, stderr_bytes = await process.communicate()
        stdout = stdout_bytes.decode()
        stderr = stderr_bytes.decode()

        # Print output for debugging
        print(f"\nCommand output:")
        print(f"Return code: {process.returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")

        if process.returncode != 0:
            return f"Error executing k6 test:\n{stderr}"

        return stdout

    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def execute_k6_test(script_file: str, duration: str = "30s", vus: int = 10) -> str:
    """Execute a k6 load test.

    Args:
        script_file: Path to the k6 test script (.js)
        duration: Duration of the test (e.g., "30s", "1m", "5m")
        vus: Number of virtual users to simulate
    """
    return await run_k6_script(script_file, duration, vus)

@mcp.tool()
async def execute_k6_test_with_options(script_file: str, duration: str, vus: int) -> str:
    """Execute a k6 load test with custom duration and VUs.

    Args:
        script_file: Path to the k6 test script (.js)
        duration: Duration of the test (e.g., "30s", "1m", "5m")
        vus: Number of virtual users to simulate
    """
    return await run_k6_script(script_file, duration, vus)

if __name__ == "__main__":
    mcp.run(transport='stdio')
