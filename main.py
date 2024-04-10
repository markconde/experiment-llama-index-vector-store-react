import sys
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from llama_index.core.agent import ReActAgent

import guidance
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.schema import QueryBundle
from llama_index.question_gen.guidance import GuidanceQuestionGenerator

def initialize_vector_index():
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./.persist-storage")
        return load_index_from_storage(storage_context), True
    except Exception as e:
        print(f"Error loading index: {e}")
        return None, False

def create_new_vector_index():
    embed_model = OpenAIEmbedding(embed_batch_size=10)

    # Set embedding model and language model settings
    Settings.embed_model = embed_model
    Settings.llm = OpenAI(temperature=0.2, model="gpt-4")

    # Load documents from a directory into a new VectorStoreIndex
    documents = SimpleDirectoryReader("./data").load_data()
    vector_index = VectorStoreIndex.from_documents(documents)
    vector_index.storage_context.persist(persist_dir="./.persist-storage")
    return vector_index

def query_index(query, vector_index):
    try:
        query_tool = QueryEngineTool(
            query_engine=vector_index.as_query_engine(),
            metadata=ToolMetadata(
                name="My_documents",
                description="Contains documents about personal finance information from the user",
            )
        )
        
        GuidanceOpenAI = guidance.models.OpenAI(
            model="gpt-4"
        )

        question_gen = GuidanceQuestionGenerator.from_defaults(
            guidance_llm=GuidanceOpenAI
        )

        print(question_gen.generate(
            tools=[
                ToolMetadata(
                    name="My_documents",
                    description="Contains documents about personal finance information from the user",
                )
            ],
            query=QueryBundle(query)
        ))

        base_agent = ReActAgent.from_tools([query_tool], verbose=True)

        return base_agent.chat(query), None
    
    except Exception as e:
        return None, f"Error during completion: {e}"

if __name__ == "__main__":

    
    # Initialize variables for flow control
    index_loaded = False

    # Main execution path
    vector_index, index_loaded = initialize_vector_index()

    # Ensure that a question is provided as a command line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<question>\"")
        sys.exit(1)

    question = sys.argv[1]

    if not index_loaded:
        vector_index = create_new_vector_index()

    response, error = query_index(question, vector_index)

    if response is not None:
        print(str(response))
    else:
        print(error)