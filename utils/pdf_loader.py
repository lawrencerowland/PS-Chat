

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings


class ingest_pdf:
    def __init__(self, namespace, pinecone_api_key, pinecone_env_name, pinecone_index_name, 
                doc_dir):
        
        self.namespace=namespace
        self.pinecone_api_key=pinecone_api_key
        self.pinecone_env_name=pinecone_env_name
        self.pinecone_index_name=pinecone_index_name
        self.doc_dir=doc_dir

        # initialize pinecone
        self.pinecone = pinecone.init(
                        api_key=pinecone_api_key,  # find at app.pinecone.io
                        environment=pinecone_env_name  # next to api key in console
                    )




    def upload_pdf_to_pinecone(self, chunk_size=1000, chunk_overlap=0):

        print ("Start uploading PDFs to Pinecone...")

        
        index = pinecone.Index(self.pinecone_index_name)
        index.delete(deleteAll='true', namespace=self.namespace)
        print ("clearing pinecone index if namespace exists...")


        my_loader = DirectoryLoader(self.doc_dir, glob='**/*.pdf')
        documents = my_loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
        docs = text_splitter.split_documents(documents)
        
        
        Pinecone.from_documents(docs, OpenAIEmbeddings(), 
                                            index_name=self.pinecone_index_name, 
                                            namespace=self.namespace)
        print ("Finished uploading PDFs to Pinecone...")




    