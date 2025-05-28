#!/usr/bin/env python3

import sys
from smolagents import LiteLLMModel
from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool

def build_model():
    model = LiteLLMModel(
        # model_id="ollama_chat/qwen2:7b",
        model_id="ollama_chat/qwen3:8b",
        # model_id="ollama_chat/granite3.3:latest",
        api_base="http://127.0.0.1:11434",
        num_ctx=8192,
    )
    return model

from smolagents import LogLevel

def build_agent(model):
    search_tool = DuckDuckGoSearchTool()
    visit_webpage_tool = VisitWebpageTool()
    authorized_imports = ["requests"]
    agent = CodeAgent(
        #tools=[search_tool, visit_webpage_tool], 
        tools=[visit_webpage_tool], 
        model=model,
        additional_authorized_imports=authorized_imports,
        verbosity_level = LogLevel.DEBUG)
    return agent

def main(argv):
    prompt = """
    Build a list of the 10 best music recommendations for a party at the Wayne's mansion. The music should be appropriate given that batman movies have spanned the 80s, 90s, 2000s, and 2010s.

    https://www.allmusic.com/ is a great resource for popular music.
    You can use the "visit webpage tool" to get the contents of any webpage you want to visit.
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
