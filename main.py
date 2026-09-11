from pathlib import Path
from random import randint
from typing import Literal

from fastmcp import FastMCP


mcp = FastMCP("Simple Tools Server")


@mcp.tool()
def calculator(
	operation: Literal["add", "subtract", "multiply", "divide"],
	first_number: float,
	second_number: float,
) -> float:
	"""Perform a basic calculation on two numbers."""
	if operation == "add":
		return first_number + second_number
	if operation == "subtract":
		return first_number - second_number
	if operation == "multiply":
		return first_number * second_number
	if second_number == 0:
		raise ValueError("Cannot divide by zero")
	return first_number / second_number


@mcp.tool()
def random_number(minimum: int, maximum: int) -> int:
	"""Generate a random integer between minimum and maximum, inclusive."""
	if minimum > maximum:
		raise ValueError("minimum must be less than or equal to maximum")
	return randint(minimum, maximum)


@mcp.tool()
def resource_finder(
	directory: str = ".",
	pattern: str = "*",
	recursive: bool = True,
	max_results: int = 50,
) -> list[str]:
	"""Find files in a directory matching a glob pattern."""
	if max_results < 1:
		raise ValueError("max_results must be greater than zero")

	search_directory = Path(directory).expanduser().resolve()
	if not search_directory.is_dir():
		raise ValueError(f"Directory does not exist: {directory}")

	matches = (
		search_directory.rglob(pattern)
		if recursive
		else search_directory.glob(pattern)
	)
	return [str(path) for path in matches if path.is_file()][:max_results]


def main() -> None:
	"""Start the MCP server."""
	mcp.run()


if __name__ == "__main__":
	mcp.run(transport="http",host="0.0.0.0",port=8000)