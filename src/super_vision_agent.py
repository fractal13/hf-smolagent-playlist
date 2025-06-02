#!/usr/bin/env python3

import sys
from smolagents import LiteLLMModel
from smolagents import CodeAgent
from smolagents import LogLevel
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
import dotenv
import os



def build_model():
    model = LiteLLMModel(
        # model_id="ollama_chat/qwen2:7b",
        # model_id="ollama_chat/qwen3:8b",
        model_id="ollama_chat/granite3.3:latest",
        api_base="http://127.0.0.1:11434",
        num_ctx=8192,
    )
    return model

def build_vision_model():
    model = LiteLLMModel(
        model_id="ollama_chat/granite3.2-vision:latest",
        api_base="http://127.0.0.1:11434",
        num_ctx=8192,
        flatten_messages_as_text=False,
    )
    return model

def build_openai_model():
    from smolagents import CodeAgent, OpenAIServerModel
    # model = OpenAIServerModel(model_id="gpt-4o",
    #                           api_base="https://api.openai.com/v1",
    #                           api_key=os.getenv("OPENAI_API_KEY"),
    #                           )
    model = OpenAIServerModel(
        #model_id="granite3.2-vision:latest",
        model_id="llava:7b",
        api_base="http://127.0.0.1:11434/v1",
        api_key="ollama"
    )
    return model



######
from PIL import Image
import requests
from io import BytesIO

def get_images():
    image_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg", # Joker image
    ]
    # "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg" # Joker image
    
    images = []
    for url in image_urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" 
        }
        response = requests.get(url,headers=headers)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        images.append(image)
    return images
######

def build_agent(model):
    agent = CodeAgent(
        tools=[], 
        model=model,
        max_steps=3,
        verbosity_level = LogLevel.DEBUG)
    return agent

def main(argv):
    dotenv.load_dotenv()
    prompt = """
    Describe this image.
    """
    #     These images are photos of a pop-culture character. Describe the costume and makeup worn by the user, and return the description.
    
    # Describe the costume and makeup that the comic character in these photos is wearing and return the description.
    # Tell me if the guest is The Joker or Wonder Woman.
    images = get_images()
    # model = build_vision_model()
    model = build_openai_model()
    agent = build_agent(model)
    result = agent.run(prompt, images=images)
    print()
    print("Return from agent.run():")
    print(result)
    print()
    return

if __name__ == "__main__":
    main(sys.argv)
