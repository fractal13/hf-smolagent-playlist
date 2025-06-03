#!/usr/bin/env python3
"""Simple demo agent using the tools of this folder.

Makes all the tools of this folder available, then asks
the agent a question that should exercise all of the tools.
"""

from hub_stats_tool import HubStatsTool
from weather_info_tool import WeatherInfoTool, GeocodeTool
from smolagents import DuckDuckGoSearchTool

from model_builder import ollama_build_reasoning_model, openai_build_reasoning_model

from smolagents import CodeAgent

def build_agent():
    geocode_tool = GeocodeTool()
    weather_info_tool = WeatherInfoTool()
    hub_stats_tool = HubStatsTool()
    search_tool = DuckDuckGoSearchTool()
    model = ollama_build_reasoning_model()
    # model = openai_build_reasoning_model()
    agent = CodeAgent(
        tools = [geocode_tool, weather_info_tool, hub_stats_tool, search_tool],
        model=model
    )
    return agent

def main():
    agent = build_agent()
    response = agent.run("What is facebook? Also, what is their most popular model? What is the current weather at facebook's head quarters?")
    print("🎩 Alfred's Response:")
    print(response)

if __name__ == "__main__":
    main()
