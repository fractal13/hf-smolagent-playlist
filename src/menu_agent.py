#!/usr/bin/env python3

import sys
from smolagents import LiteLLMModel
from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import tool

# Tool to suggest a menu based on the occasion
@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."


def build_model():
    model = LiteLLMModel(
        model_id="ollama_chat/qwen3:8b",
        api_base="http://127.0.0.1:11434",
        num_ctx=8192,
    )
    return model

def build_agent(model):
    search_tool = DuckDuckGoSearchTool()
    visit_webpage_tool = VisitWebpageTool()
    tools=[search_tool, visit_webpage_tool, suggest_menu]
    agent = CodeAgent(
        tools=tools, 
        model=model)
    return agent

def main(argv):
    prompt =  """
    Prepare a menu for Bruce Wayne's formal party. 
    Include the individual items in the menu.
    """
    model = build_model()
    agent = build_agent(model)
    result = agent.run(prompt)
    print()
    print("Return from agent.run():")
    print(result)
    print()
    return

if __name__ == "__main__":
    main(sys.argv)
