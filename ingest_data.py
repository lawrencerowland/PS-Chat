


from utils.pdf_loader import ingest_pdf
from utils.graph_loader import ingest_graph
from dotenv import load_dotenv
import os

load_dotenv()

neo4j_url = os.getenv('NEO4J_URL')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')

openai_key = os.getenv('OPENAI_KEY')
os.environ['OPENAI_API_KEY'] = openai_key

pinecone_api_key = os.getenv('PINECONE_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV')
pinecone_index_name = os.getenv('PINECONE_INDEX')
pdf_namespace = os.getenv('PINECONE_PDF_NAMESPACE')
graph_namespace = os.getenv('PINECONE_GRAPH_NAMESPACE')
source_name = os.getenv('SOURCE_NAME')
doc_dir = os.getenv('PDF_DOC_DIR')

chunk_size = int(os.getenv('CHUNK_SIZE'))
chunk_overlap = int(os.getenv('CHUNK_OVERLAP'))

if __name__ == "__main__":

    pdf_ingest = ingest_pdf(None, pinecone_api_key, pinecone_env_name, pinecone_index_name, doc_dir)
    # pdf_ingest.delete_namespaces ("Praxis")
    pdf_ingest.check_pinecone_index()
    pdf_ingest.upload_pdf_to_pinecone(chunk_size, chunk_overlap)
    pdf_ingest.check_pinecone_index()
    # graph_ingest = ingest_graph(graph_namespace, neo4j_url, neo4j_user, neo4j_password,
    #                             pinecone_api_key, pinecone_env_name, pinecone_index_name)
    # graph_ingest.upload_graph_to_pinecone(source_name)