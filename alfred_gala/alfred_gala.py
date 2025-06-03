#!/usr/bin/env python3
"""Agent to host a gala event.

The agent knows information about the party guests,
the weather, and hugging face model download stats.
"""

import random
from smolagents import CodeAgent

# import our tools and agent support
from hub_stats_tool import HubStatsTool
from weather_info_tool import WeatherInfoTool, GeocodeTool
from retriever import make_guest_info_retriever_tool
from smolagents import DuckDuckGoSearchTool
from model_builder import ollama_build_reasoning_model


def build_agent():
    """Build an agent for the Gala event."""
    
    geocode_tool = GeocodeTool()
    weather_info_tool = WeatherInfoTool()
    hub_stats_tool = HubStatsTool()
    search_tool = DuckDuckGoSearchTool()
    guest_info_tool = make_guest_info_retriever_tool()

    model = ollama_build_reasoning_model()

    agent = CodeAgent(
        tools = [guest_info_tool, geocode_tool, weather_info_tool, hub_stats_tool, search_tool],
        model=model,
        add_base_tools=True,
        planning_interval=3,
        max_steps=10
    )

    return agent

def main():
    agent = build_agent()
    while True:
        query = input("Enter a query (^C to quit): ")
        response = agent.run(query, reset=False)
        print("🎩 Alfred's Response:")
        print(response)
    return

if __name__ == "__main__":
    main()
