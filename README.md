# PS-Chat
The code of delivering ChatBot project for PS

# Install the Requirements in your terminal

```
pip install -r requirements.txt

```


# Upload your own documents
Put your documents into ``` ./docs ```  or other path to match your .env setting


# .env
```
NEO4J_URL="xxxxx"
NEO4J_USER="xxxxx"
NEO4J_PASSWORD="xxxxx"

OPENAI_KEY="xxxxx"

PINECONE_KEY = "xxxxx"
PINECONE_ENV = "xxxxx"
PINECONE_INDEX = "xxxxx"

# pdf doc directory
PDF_DOC_DIR = "./docs" # change as you like

# upload parameters
CHUNK_SIZE = 1000 # change as you like
CHUNK_OVERLAP = 0 # change as you like

PINECONE_PDF_NAMESPACE = "my-pdf" # change as you like
PINECONE_GRAPH_NAMESPACE = "my-graph" # change as you like

```


# Ingest your data
This could be take a while if you have multiple documents. This function will ingest PDF documents in your folder and also your graph database.
You can uncommnent the graph ingesting if you only want to upload a new pdf.

```
python ingest_data.py
```


# Launch your app
After ingesting your data, simply run main.py for local deployment and debugging.

```
python main.py
```

# Deploy your app using gunicorn

```
gunicorn -w 2 -b :8000 main:app --timeout=120
```

# For port forwarding using Ngrok
Please refer https://ngrok.com/docs/getting-started/