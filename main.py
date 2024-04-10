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
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Ensure that a question is provided as a command line argument
if len(sys.argv) < 2:
    print("Usage: python script.py \"<question>\"")
    sys.exit(1)

question = sys.argv[1]

# Initialize variables for flow control
index_loaded = False

def initialize_index():
    global index_loaded
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./.persist-storage")
        return load_index_from_storage(storage_context), True
    except Exception as e:
        print(f"Error loading index: {e}")
        return None, False

def create_new_index():
    embed_model = OpenAIEmbedding(embed_batch_size=10)

    # Set embedding model and language model settings
    Settings.embed_model = embed_model
    Settings.llm = OpenAI(temperature=0.2, model="gpt-4")

    # Load documents from a directory into a new VectorStoreIndex
    documents = SimpleDirectoryReader("./data").load_data()
    vector_index = VectorStoreIndex.from_documents(documents)
    vector_index.storage_context.persist(persist_dir=".persist-storage")
    return vector_index

def query_index(query, vector_index):
    try:
        query_engine = vector_index.as_query_engine()

        tool_metadata = ToolMetadata(
            name="My_documents",
            description="Contains documents about personal finance information from the user",
        )

        query_tool = QueryEngineTool(query_engine=query_engine, metadata=tool_metadata)

        base_agent = ReActAgent.from_tools([query_tool], verbose=True)

        return base_agent.chat(query), None
    
    except Exception as e:
        return None, f"Error during completion: {e}"

# Main execution path
vector_index, index_loaded = initialize_index()

if not index_loaded:
    vector_index = create_new_index()

response, error = query_index(question, vector_index)

if response is not None:
    print(str(response))
else:
    print(error)