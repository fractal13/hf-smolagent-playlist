#!/usr/bin/env python3

import sys
from smolagents import LogLevel
import dotenv
import os

#####
from smolagents import LiteLLMModel
def build_reasoning_model():
    model = LiteLLMModel(
        # model_id="ollama_chat/qwen2:7b",
        model_id="ollama_chat/qwen3:8b",
        # model_id="ollama_chat/granite3.3:latest",
        api_base="http://127.0.0.1:11434",
        max_tokens=8192,
    )
    return model

#####
from smolagents import CodeAgent
import image_description_agent
def build_agent(model):
    id_agent = image_description_agent.full_build_agent()
    agent = CodeAgent(
        tools=[], 
        managed_agents=[id_agent],
        model=model,
        planning_interval=5,
        max_steps=10,
        verbosity_level = LogLevel.DEBUG,
    )
    return agent

#####
def main(argv):
    dotenv.load_dotenv()

    image_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg", # Joker image
        "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg" # Joker image
    ]
    image_paths = [
        "A.jpg",
        "M.jpg",
        "T.png",
        "W.png"
    ]

    prompt = f"""
    For this list of images, examine the contents of the image, and identify whether the images
    contains a super villain, a super hero, an average person, or no person at all. 
    Give your reasoning for your choice of the contents.

    Some images are located at these URLs: {image_urls}.
    Some images are located at these file paths: {image_paths}.
    """

    agent = build_agent(build_reasoning_model())
    result = agent.run(prompt)
    print()
    print("Return from agent.run():")
    print(result)
    print()
    return

if __name__ == "__main__":
    main(sys.argv)
