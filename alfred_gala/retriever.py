#!/usr/bin/env python3
"""Tool to retrieve guest information.
"""

import datasets
from langchain.docstore.document import Document

def load_guest_dataset_docs():
    # Load the dataset
    guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

    # Convert dataset entries into Document objects
    docs = [
        Document(
            page_content="\n".join([
                f"Name: {guest['name']}",
                f"Relation: {guest['relation']}",
                f"Description: {guest['description']}",
                f"Email: {guest['email']}"
            ]),
            metadata={"name": guest["name"]}
        )
        for guest in guest_dataset
    ]
    return docs

from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
class GuestInfoRetrieverTool(Tool):
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about."
        }
    }
    output_type = "string"

    def __init__(self, docs):
        self.is_initialized = False
        self.retriever = BM25Retriever.from_documents(docs)

    def forward(self, query: str):
        results = self.retriever.get_relevant_documents(query)
        if results:
            return "\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."

# Initialize the tool
def make_guest_info_retriever_tool():
    docs = load_guest_dataset_docs()
    guest_info_tool = GuestInfoRetrieverTool(docs)
    return guest_info_tool


def main():
    from model_builder import ollama_build_reasoning_model, openai_build_reasoning_model

    if False:
        model = ollama_build_reasoning_model()
    else:
        model = openai_build_reasoning_model()

    guest_info_tool = make_guest_info_retriever_tool()

    from smolagents import CodeAgent
    # Create Alfred, our gala agent, with the guest info tool
    alfred = CodeAgent(tools=[guest_info_tool], model=model)

    # Example query Alfred might receive during the gala
    response = alfred.run("Tell me about our guest named 'Lady Ada Lovelace'.")

    print("🎩 Alfred's Response:")
    print(response)

if __name__ == "__main__":
    main()

