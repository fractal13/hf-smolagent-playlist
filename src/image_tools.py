#!/usr/bin/env python3
import base64
from pathlib import Path
from smolagents import tool
from smolagents import LiteLLMModel
from smolagents import OpenAIServerModel
from smolagents import CodeAgent
from smolagents import LogLevel
import litellm

# --- Your LiteLLMModel initialization (as you have it) ---
vision_model = OpenAIServerModel(
    model_id="granite3.2-vision:latest",
    #model_id="ollama_chat/llava:7b",
    api_base="http://127.0.0.1:11434/v1",
)
model = LiteLLMModel(
    #model_id="ollama_chat/granite3.3:latest",
    model_id="ollama_chat/llava:7b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)

# --- Define the Image Analysis Tool ---

@tool
def analyze_image_for_character_description(image_path: str) -> str:
    """
    Analyzes an image to determine a description of the character.
    Returns the description as a string.

    Args:
        image_path: The path to the image file (e.g., "my_image.jpg").
    """
    image_file = Path(image_path)
    if not image_file.exists():
        return f"Error: Image file not found at {image_path}"

    try:
        with open(image_file, "rb") as f:
            base64_image_data = base64.b64encode(f.read()).decode('utf-8')

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the character seen in this image."},
                    {"type": "image_url", "image_url": {"url": f"The_Joker_at_Wax_Museum_Plus.jpg"}}
                ]
            }
        ]

        print(f"Calling LiteLLMModel to analyze image: {image_path}")
        response = vision_model.generate(messages=messages)
        print(response.content)
        return response.content

    except Exception as e:
        print(f"An error occurred during image analysis: {e}")
        return f"An error occurred during image analysis: {e}"

# --- Add the tool to your CodeAgent ---
agent = CodeAgent(
    tools=[analyze_image_for_character_description], # <--- Pass your tool here
    model=model,
    max_steps=5,
    verbosity_level=LogLevel.DEBUG
)

# --- How to prompt your CodeAgent to use the tool ---
# You'll need to give the agent a task that implies using the tool.
# For example, if you have a list of image paths:

image_files_to_check = ["Joker_(DC_Comics_character).jpg", "The_Joker_at_Wax_Museum_Plus.jpg"] 

user_prompt = f"""
You are an expert at identifying superheroes and supervillains from images.
Your task is to analyze the following images and determine if they show a superhero or a supervillain.
For each image, use the `analyze_image_for_character_description` tool and then state your conclusion clearly.

Here are the image paths to analyze:
{', '.join(image_files_to_check)}

Present your findings for each image in a clear, concise manner.
"""

print(f"\n--- Running CodeAgent with prompt ---\n")
# litellm.set_verbose = True
final_response = agent.run(user_prompt)
# litellm.set_verbose = False
print(f"\n--- Agent's Final Response ---\n{final_response}")
