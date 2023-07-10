# PS-Chat
The code for delivering the ChatBot project for PS

# Install the Requirements in your terminal

```
pip install -r requirements.txt

```


# Upload your own documents
Put your documents into ``` ./docs ```  or another path to match your .env setting


# Sett your environment file as .env in the main folder
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

# Upload parameters change as you like
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 0

PINECONE_PDF_NAMESPACE = "my-pdf" 
PINECONE_GRAPH_NAMESPACE = "my-graph" 

```


# Ingest your data
This could take a while if you have multiple documents. This function will upload the embeddings of your PDF documents and graph database to the cloud vector database.
You can uncomment the graph ingesting if you only want to upload a new pdf.

```
python ingest_data.py
```


# Launch your app
After ingesting your data, simply run main.py for local deployment and debugging.

```
python main.py
```

# Deploy your app using Gunicorn

```
gunicorn -w 2 -b :8000 main:app --timeout=120
```

# For port forwarding using Ngrok
Please refer https://ngrok.com/docs/getting-started/
