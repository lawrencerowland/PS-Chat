# PS-Chat
The code for delivering the ChatBot project for PS

# Step 0. Install the Requirements in your terminal

```
pip install -r requirements.txt

```


# Step 1. Prepare your own documents for chatbot talk to PDF documents

Put your documents into ``` ./docs/[category_name]/ ``` . Each [category_name] of subfolder will appear as tickboxes so that you can choose one or multiple categories of sources of PDF document for reference. Please create a subfolder inside the ``` ./docs ``` with careful naming [category_name], because it will be used for storing your document in cloud vector database


# Step 2. Set your environment file as .env in the main folder
```
# Graph Database for Chatbot talk to documents
NEO4J_URL="xxxxx"
NEO4J_USER="xxxxx"
NEO4J_PASSWORD="xxxxx"

# Your openai key 
OPENAI_KEY="xxxxx"

# Setting of Vector database
PINECONE_KEY = "xxxxx"
PINECONE_ENV = "xxxxx"
PINECONE_INDEX = "xxxxx"

# Name of directory for storing PDF documents
PDF_DOC_DIR = "./docs" 

# Upload parameters of PDF doucment into vector database
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 0

# Namespace for vector database
PINECONE_PDF_NAMESPACE = "my-pdf" 
PINECONE_GRAPH_NAMESPACE = "my-graph" 

```

# Step 3. Ingest your data
Use ``` ingest_data.py ``` upload the embeddings of your PDF documents and graph database to the cloud vector database. You can comment or uncomment partial of the code. 
```
python ingest_data.py
```


# Step 4. Launch your app
After ingesting your data, simply run main.py for local deployment and debugging.

```
python main.py
```

# Option 1. Deploy your app using Gunicorn

```
gunicorn -w 2 -b :8000 main:app --timeout=120
```

# Option 2. For port forwarding using Ngrok
Please refer https://ngrok.com/docs/getting-started/
