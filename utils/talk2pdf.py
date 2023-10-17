
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import GraphQAChain
from langchain.indexes.graph import NetworkxEntityGraph
import re
from langchain.callbacks import get_openai_callback
from utils.count_tokens import log_token_details_to_file
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT



def get_citations(response):
    citations = []
    idx = 1
    for d in response["input_documents"]:
        cited_text = "<b>" + f"[{idx}] File Name of Source: " + d.metadata["source"] + "</b>" + "<br>" + d.page_content
        citations.append (cited_text)
        idx+=1
    return citations

def get_citations_v2(response):
    citations = []
    idx = 1
    for d in response["source_documents"]:
        cited_text = "<b>" + f"[{idx}] File Name of Source: " + d.metadata["source"] + "</b>" + "<br>" + d.page_content
        citations.append (cited_text)
        idx+=1
    return citations

class QueryDocs():
    def __init__(self,
                pinecone_api_key=None,
                pinecone_env_name=None,
                pinecone_index_name=None,
                model_version="gpt-3.5-turbo-16k"):
        
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
    
    def qa_pdf_with_citations_from_multiple_srcs (self, question, namespaces_list=["unilever"], text_key="text", topK=5):

        all_docs = []
        for namespace in namespaces_list:
            vectorstore = Pinecone(self.index, self.embeddings.embed_query, text_key, namespace=namespace)
            docs = vectorstore.similarity_search(question, k=topK)
            for doc in docs:
                if len(doc.page_content) > 200: # filter out short documents
                    all_docs.append(doc)

        chain = load_qa_with_sources_chain(ChatOpenAI(model=self.model_version ,temperature=0), chain_type="stuff")
        print ("model version: ", self.model_version)
        with get_openai_callback() as cb:
            question = question + "Try to summarise your answer in a list. Make sure each item in a list is in as many details as possible, but does not have overlap content."
            response = chain({"input_documents": all_docs, "question": question}, return_only_outputs=False)
            response["citations"] = get_citations(response)
            response["output_text"] = re.sub(r'^SOURCES:.*$', '', response["output_text"], flags=re.MULTILINE)
            
            # log token details
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            log_token_details_to_file(cb.prompt_tokens, cb.completion_tokens, self.model_version)

        return response

    def qa_pdf_with_conversational_chain (self, question, chat_history, my_namespace="unilever", text_key="text", topK=10):

        vectorstore = Pinecone(self.index , self.embeddings.embed_query, text_key, namespace=my_namespace)
        llm = ChatOpenAI(model=self.model_version ,temperature=0)
        doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        question = question + "Summarize your answer in a list. Ensure that each item is detailed but without overlapping content."

        chain = ConversationalRetrievalChain(
                    retriever=vectorstore.as_retriever(),
                    question_generator=question_generator,
                    combine_docs_chain=doc_chain,
                    return_source_documents=True
                )

        with get_openai_callback() as cb:
            print ("input chat_history: ", chat_history)
            response = chain({"question": question, "chat_history": chat_history})
            response["output_text"] = response["answer"]
            response["citations"] = get_citations_v2(response)
            
            # log token details
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            log_token_details_to_file(cb.prompt_tokens, cb.completion_tokens, self.model_version)
        return response