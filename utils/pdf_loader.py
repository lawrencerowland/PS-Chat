
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from tqdm import tqdm

def get_subfolders(directory):
    subfolders = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subfolder = os.path.join(root, dir)
            subfolders.append(subfolder)
    return subfolders

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


    def check_pinecone_index(self):
        print ("Checking if pinecone index exists...")
        index = pinecone.Index(self.pinecone_index_name)
        print(index.describe_index_stats())


    def upload_pdf_to_pinecone(self, chunk_size=1000, chunk_overlap=0):

        print ("Start uploading PDFs to Pinecone...")

        
        index = pinecone.Index(self.pinecone_index_name)
        available_namesacpes = index.describe_index_stats()["namespaces"]

        subfolders = get_subfolders(self.doc_dir)
        if len(subfolders)>=1:
            my_namespace = self.namespace     
            for subfolder in tqdm(subfolders):
                if self.namespace == None:
                    my_namespace = subfolder.split(self.doc_dir)[1].replace("/","")

                if my_namespace in available_namesacpes:
                    print ("Namespace " + my_namespace + " already exists in pinecone index. Skipping...")
                    continue

                my_loader = DirectoryLoader(subfolder, glob='**/*.pdf')

                documents = my_loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
                docs = text_splitter.split_documents(documents)

                print ("finsihed splitting documents and bigin uploading...")
                
                Pinecone.from_documents(docs, OpenAIEmbeddings(), 
                                                    index_name=self.pinecone_index_name, 
                                                    namespace=my_namespace)
                print ("Finished uploading PDFs to Pinecone in folder " + subfolder + " with namespace " + my_namespace)
        
        else:
            print ("No subfolders found in " + self.doc_dir)
            # upload all documents in the directory
            my_namespace = self.namespace
            if my_namespace== None:
                my_namespace = "MyPDFs"
            my_loader = DirectoryLoader(self.doc_dir, glob='**/*.pdf')
            documents = my_loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
            docs = text_splitter.split_documents(documents)
            
            Pinecone.from_documents(docs, OpenAIEmbeddings(), 
                                                index_name=self.pinecone_index_name, 
                                                namespace=my_namespace)
            print ("Finished uploading PDFs to Pinecone in folder " + subfolder + " with namespace " + my_namespace)