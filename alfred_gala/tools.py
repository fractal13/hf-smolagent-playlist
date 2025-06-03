#!/usr/bin/env python3
"""Currently useless
"""

from smolagents import DuckDuckGoSearchTool

if __name__ == "__main__":
    # Initialize the DuckDuckGo search tool
    search_tool = DuckDuckGoSearchTool()

    # Example usage
    results = search_tool("Who's the current President of France?")
    print(results)
