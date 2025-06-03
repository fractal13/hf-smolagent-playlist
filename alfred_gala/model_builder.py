#!/usr/bin/env python3
"""Functions for building accessible LLM models

reasoning models are for textual reasoning
vision models are for image to text or text to image

ollama are for local LLM
openai are for api access to openai

Following are currently available
- ollama_build_reasoning_model
- openai_build_reasoning_model
"""

from smolagents import LiteLLMModel
def ollama_build_reasoning_model():
    model = LiteLLMModel(
        # model_id="ollama_chat/qwen2:7b",
        model_id="ollama_chat/qwen3:8b",
        # model_id="ollama_chat/granite3.3:latest",
        api_base="http://127.0.0.1:11434"
    )
    return model

from smolagents import OpenAIServerModel
def openai_build_reasoning_model():
    import dotenv
    import os
    dotenv.load_dotenv()
    model = OpenAIServerModel(model_id="gpt-4o",
                              api_base="https://api.openai.com/v1",
                              api_key=os.getenv("OPENAI_API_KEY"),
                              )
    return model
