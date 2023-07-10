from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from utils.generic_cypher import Neo4jGPTQuery
import neo4j
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from neo4j import GraphDatabase
from langchain.chains import GraphQAChain
from langchain.indexes.graph import NetworkxEntityGraph

class QueryDocs():
    def __init__(self, openai_key=None,
                pinecone_api_key=None,
                pinecone_env_name=None,
                pinecone_index_name=None,):
        
        self.openai_key=openai_key
        self.pinecone_api_key=pinecone_api_key
        self.pinecone_env_name=pinecone_env_name
        self.pinecone_index_name=pinecone_index_name
        self.embeddings = OpenAIEmbeddings()

        pinecone.init(api_key=self.pinecone_api_key,environment=self.pinecone_env_name)
        self.index = pinecone.Index(self.pinecone_index_name)
    
    def qa_pdf (self, question, my_namespace="unilever", text_key="text", topK=5):
        vectorstore = Pinecone(self.index , self.embeddings.embed_query, text_key, namespace=my_namespace)
        docs = vectorstore.similarity_search(question, k=topK)
        chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff")
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        return response["output_text"]

    def qa_knowledge_triples(self, question, graph_pth="ps-graph.gml"):
        loaded_graph = NetworkxEntityGraph.from_gml(graph_pth)
        chain = GraphQAChain.from_llm(OpenAI(temperature=0), graph=loaded_graph, verbose=True)
        response = chain.run(question)
        return response
    