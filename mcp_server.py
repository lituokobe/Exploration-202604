from mcp.server import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("LocalToolsServer")


@mcp.tool()
def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Args:
        expression: A string containing a math expression (e.g., "25 * 4 + 10")
    """
    try:
        # Security: Only allow numbers and basic math operators
        allowed_chars = set("0123456789+-*/.() ")
        if not set(expression).issubset(allowed_chars):
            return "Error: Invalid characters in expression. Only numbers and +, -, *, /, (, ) are allowed."

        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the contents of a local text file.
    Args:
        file_path: The path to the file to read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a local text file.
    Args:
        file_path: The path to the file to write to.
        content: The string content to write.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"


if __name__ == "__main__":
    # Run the server using stdio transport (standard for local CLI apps)
    mcp.run(transport='stdio')