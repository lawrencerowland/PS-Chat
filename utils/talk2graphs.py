from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from utils.generic_cypher import Neo4jGPTQuery
import neo4j
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from neo4j import GraphDatabase


def list_to_string(lst):
    result = ''
    for item in lst:
        if isinstance(item, list):
            result += list_to_string(item) + '\n'
        elif isinstance(item, neo4j.graph.Node):
            result += str(dict(item)) + ', '
        elif isinstance(item, neo4j.graph.Relationship):
            result += f"({dict(item.start_node)})-[:{item.type}]->({dict(item.end_node)})" + ', '
        else:
            result += str(item) + ', '
    return result


class QueryGraph():
    def __init__(self, neo4j_url=None, neo4j_user=None, neo4j_password=None, 
                openai_key=None, model_version="gpt-4"):
        
        self.neo4j_url=neo4j_url
        self.neo4j_user=neo4j_user
        self.neo4j_password=neo4j_password
        self.openai_key=openai_key
        self.embeddings = OpenAIEmbeddings()
        self.driver = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))
        self.model_version = model_version

    # Experiment 2: Generic Cypher
    def generic_cypher(self, query):
        self.db = Neo4jGPTQuery(
                                url=self.neo4j_url,
                                user=self.neo4j_user,
                                password=self.neo4j_password,
                                openai_api_key=self.openai_key,
                                model_version=self.model_version)
        
        response = self.db.run(query)
        print (response)
        response =list_to_string(response)
        
        return response
    
    # Experiment 3: Graph Cypher QA
    def graph_cypher_qa(self, question):
        graph = Neo4jGraph(
                            url=self.neo4j_url,
                            username=self.neo4j_user,
                            password=self.neo4j_password)
        
        chain = GraphCypherQAChain.from_llm(ChatOpenAI(model=self.model_version, temperature=0), graph=graph, verbose=True,)
        response = chain.run(question)
        print (response)
        return response
    
    # Optimissed version of Cyher Query
    def optimised_cyher(self, question, pinecone_api_key,pinecone_env_name,pinecone_index_name,
                        my_namespace="graph", text_key="name", topK=20):
        
        pinecone.init(api_key=pinecone_api_key,environment=pinecone_env_name)
        index = pinecone.Index(pinecone_index_name)
        vectorstore = Pinecone(index, self.embeddings.embed_query, text_key, namespace=my_namespace)

        docs = vectorstore.similarity_search(question, k=topK)

        # Get the related node names, node types and edges
        related_node_names = ""
        related_node_types = ""
        related_edges = ""
        for d in docs:
            if d.metadata["info_type"] == "node_names":
                related_node_names+=d.page_content + "; "
            
            if d.metadata["info_type"] == "node_types":
                related_node_types+=d.page_content + "; "
            
            if d.metadata["info_type"] == "edges":
                related_edges+=d.page_content + "; "

        # Build additional hint
        additional_hint = f"""I used KNN and Pinecone to find the most relevant nodes, node types and edges closed to the questions which might be helpful for you.
                            Hint: Relevant names of nodes: {related_node_names} in the database.
                                  Relevant labels of nodes: {related_node_types} in the database. 
                                  Relevant edges type: {related_edges} in the database."""
        print (additional_hint)
        # Enquiry the database as graph cypher QA
        graph = Neo4jGraph(
                            url=self.neo4j_url,
                            username=self.neo4j_user,
                            password=self.neo4j_password)
        
        chain = GraphCypherQAChain.from_llm(ChatOpenAI(model=self.model_version,temperature=0.5), graph=graph, verbose=True,)
        response = chain.run(question + additional_hint)

        return response