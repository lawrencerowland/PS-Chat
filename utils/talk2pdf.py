
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import GraphQAChain
from langchain.indexes.graph import NetworkxEntityGraph


def get_citations(response):
    citations = []
    idx = 1
    for d in response["input_documents"]:
        cited_text = "<b>" + f"[{idx}] File Name of Source: " + d.metadata["source"] + "</b>" + "<br>" + d.page_content
        citations.append (cited_text)
        idx+=1
    return citations


class QueryDocs():
    def __init__(self,
                pinecone_api_key=None,
                pinecone_env_name=None,
                pinecone_index_name=None,
                model_version="gpt-4"):
        
        self.pinecone_api_key=pinecone_api_key
        self.pinecone_env_name=pinecone_env_name
        self.pinecone_index_name=pinecone_index_name
        self.embeddings = OpenAIEmbeddings()
        self.model_version = model_version
        pinecone.init(api_key=self.pinecone_api_key,environment=self.pinecone_env_name)
        self.index = pinecone.Index(self.pinecone_index_name)
    
    def qa_pdf (self, question, my_namespace="unilever", text_key="text", topK=5):
        vectorstore = Pinecone(self.index , self.embeddings.embed_query, text_key, namespace=my_namespace)
        docs = vectorstore.similarity_search(question, k=topK)
        chain = load_qa_with_sources_chain(ChatOpenAI(model=self.model_version ,temperature=0), chain_type="stuff")
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        return response["output_text"]

    def qa_knowledge_triples(self, question, graph_pth="ps-graph.gml"):
        loaded_graph = NetworkxEntityGraph.from_gml(graph_pth)
        chain = GraphQAChain.from_llm(ChatOpenAI(model=self.model_version , temperature=0), graph=loaded_graph, verbose=True)
        response = chain.run(question)
        return response
    
    def qa_pdf_with_citations (self, question, my_namespace="unilever", text_key="text", topK=5):
        vectorstore = Pinecone(self.index , self.embeddings.embed_query, text_key, namespace=my_namespace)
        docs = vectorstore.similarity_search(question, k=topK)
        chain = load_qa_with_sources_chain(ChatOpenAI(model=self.model_version ,temperature=0), chain_type="stuff")
        question = question + "Try to summarise your answer in a list. Make sure each item in a list is detailed, but does not have overlap content."
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=False)
        response["citations"] = get_citations(response)
        print (response)
        return response