from flask import Flask, render_template, request, jsonify, Response
from utils.graph_qurey import QueryGraph
import time
import json

### Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
neo4j_url = os.getenv('NEO4J_URL')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')
openai_key = os.getenv('OPENAI_KEY')
pinecone_api_key = os.getenv('PINECONE_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV')
pinecone_index_name = os.getenv('PINECONE_INDEX')
os.environ['OPENAI_API_KEY'] = openai_key

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response(): 
    question = request.form.get('msg')

    QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, 
                    openai_key, pinecone_api_key, pinecone_env_name, pinecone_index_name)
    
    response = {}

    try:
        # Exp 2: Generic Cypher
        response["Generic_Cypher"] = QG.generic_cypther(question)
        print ("........Finished Generic Cypher........")
    except Exception as e:
        response["Generic_Cypher"] = str(e)
        print(f"An error occurred in Generic Cypher: {str(e)}")

    try:
        # Exp 3: Graph Cypher QA
        response["Graph_Cypher_QA"] = QG.graph_cypher_qa(question)
        print ("........Finished Graph_Cypher_QA........")
    except Exception as e:
        response["Graph_Cypher_QA"] = str(e)
        print(f"An error occurred in Graph Cypher QA: {str(e)}")

    try:
        # Exp 4: Graph Cypher QA with Sources (Pinecone)
        response["Graph_Cypher_QA_with_Graph_in_Pinecone"] = QG.graph_cypher_qa_pinecone(question, text_key="context", my_namespace="graph_02")
        print ("........Finished Graph_Cypher_QA_with_Graph_in_Pinecone........")
    except Exception as e:
        response["Graph_Cypher_QA_with_Graph_in_Pinecone"] = str(e)
        print(f"An error occurred in Graph Cypher QA with Graph in Pinecone: {str(e)}")

    try:
        response["Graph_Cypher_QA_with_PDF_in_Pinecone"] = QG.graph_cypher_qa_pinecone(question, text_key="text", my_namespace="unilever")
        print ("........Finished Graph_Cypher_QA_with_PDF_in_Pinecone........")
    except Exception as e:
        response["Graph_Cypher_QA_with_PDF_in_Pinecone"] = str(e)
        print(f"An error occurred in Graph Cypher QA with PDF in Pinecone: {str(e)}")

    try:
        # Exp 5: Graph Cypher QA with Triples
        response["Graph_Cypher_QA_with_Knowledge_Triples"] = QG.graph_cypher_qa_knowledge_triples(question)
        print ("........Finished Graph_Cypher_QA_with_Knowledge_Triples........")
    except Exception as e:
        response["Graph_Cypher_QA_with_Knowledge_Triples"] = str(e)
        print(f"An error occurred in Graph Cypher QA with Knowledge Triples: {str(e)}")


    return jsonify(response) 




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
