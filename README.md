# About this repository

This tool is a command-line utility, which leverages the power of OpenAI's embeddings and language models (like GPT-4) to enable users to perform complex queries on their local data. This tool utilizes `llama_index` package functionalities to build a searchable index from user documents and provides an easy-to-use interface for querying this information.

## Features

- **Command Line Queries**: Enter queries directly through the command line interface.
- **Local Data Indexing**: Load and index documents stored in your local directory.
- **OpenAI Embeddings**: Uses OpenAI's text embeddings for accurate document retrieval.
- **GPT-4 Powered Search**: Leverage GPT-4 for understanding and responding to natural language queries.
- **Persistent Storage**: Save and load indexes from disk for efficient data reuse.
- **Verbose Output**: Get detailed responses back from the query engine.

## Installation

Before using this script, ensure you have Python installed and the necessary dependencies available.

1. Clone the repository:

```sh
git clone https://github.com/markconde/experiment-llama-index-vector-store-react.git
cd experiment-llama-index-vector-store-react
```

2. Install requirements (preferably in a virtual environment):

```sh
python -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

3. Add your data to the `./data` directory that the system will read from.

## Usage

To use the Llama Index Query Tool, provide a question as a command line argument:

```sh
python script.py "<question>"
```

Example:

```sh
python main.py "What did I spend most in the last month?"
```

Make sure to include your question within quotes.

## How It Works

Upon executing the script with a question, the following steps take place:

1. The system checks if there's already a persistent index available.
2. If not, it creates a new index by reading files from the specified `./data` directory.
3. The query is then passed through the indexing engine powered by the configured embeddings and language model.
4. The system responds with the best-matched answer or an error message if something went wrong.

## Troubleshooting

If you encounter errors, ensure that:

- Your documents are in the correct `./data` directory.
- The `.persist-storage` folder has appropriate read/write permissions.
- You have internet access if required by the embedding model.

## Disclaimer

The codebase provided here is intended **strictly for experimentation and educational purposes only.** It is not meant for use in production environments or in any high-stakes situations.

As the author and maintainer of this code, I assume no responsibility for any unintended use or misuse outside the experimental scope that it was designed for. Users should be aware that they are responsible for complying with relevant laws and regulations, and they should utilize this tool in accordance with ethical guidelines and privacy considerations.

Any use of this tool for purposes other than experimentation must be done at the user's own risk, and the user assumes full liability for any consequences that may arise from such use.

Please exercise caution and good judgment when working with this or any index querying tool.

---

Happy querying!