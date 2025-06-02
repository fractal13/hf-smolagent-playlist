#!/usr/bin/env python3

import sys
from smolagents import LogLevel

# for .env contents
import dotenv
import os
#

######
from smolagents import OpenAIServerModel
def build_vision_model():
    """
    Connect to OpenAI vision model

    Would like this to be able to connect to ollama
    """
    assert os.getenv("OPENAI_API_KEY") != "", "use dotenv to provide OPENAI_API_KEY"
    model = OpenAIServerModel(model_id="gpt-4o",
                              api_base="https://api.openai.com/v1",
                              api_key=os.getenv("OPENAI_API_KEY"),
                              )
    return model

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

######
import requests
from PIL import Image
from io import BytesIO

def image_url_to_bytes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" 
    }
    response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image

def get_images_from_urls(image_urls):
    images = []
    for url in image_urls:
        images.append(image_url_to_bytes(url))
    return images

from smolagents import tool
@tool
def download_image(image_url: str, file_name: str) -> str:
    """
    Downloads an image from a given URL.
    Returns a local file path to the downloaded image. If None is returned, the download failed.

    Args:
        image_url: a string with the url of an image
        file_name: the local file path to save the image
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" 
        }
        response = requests.get(image_url, headers=headers)
        image = Image.open(BytesIO(response.content))
        image.save(file_name)
        return file_name
    except:
        return None

######
from PIL import Image
from smolagents.utils import encode_image_base64, make_image_url

@tool
def describe_image(image_path: str) -> str:
    """
    Analyzes an image, and returns a short description of the image contents.
    Returns a text string with the image description.

    Args:
        image_path: The local file path to the image file.
    """
    multimodal_model = build_vision_model()
    assert os.path.exists(image_path), "{image_path} doesn't exist!"
    image = Image.open(image_path)
    prompt = "Here is an image. Describe it in 200 words or less."
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": make_image_url(encode_image_base64(image))},
                },
            ],
        }
    ]
    output = multimodal_model(messages).content
    return output

######
from smolagents import CodeAgent
def build_agent(model):
    agent = CodeAgent(
        tools=[describe_image, download_image],
        model=model,
        max_steps=10,
        name="image_describer_agent",
        description="Examines images and describes them. Provide either a file path or a URL for each of the images.",
    )
    # verbosity_level=0,
    # verbosity_level = LogLevel.DEBUG
    return agent
######
def full_build_agent():
    return build_agent(build_reasoning_model())

######

def main(argv):
    image_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg", # Joker image
        "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg" # Joker image
    ]

    prompt = f"""
    Obtain a description of each of the images found at these URLs: {image_urls}.
    """

    dotenv.load_dotenv()
    agent = full_build_agent()
    result = agent.run(prompt)
    print()
    print("Return from agent.run():")
    print(result)
    print()
    return

if __name__ == "__main__":
    main(sys.argv)
