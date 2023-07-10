from flask import Flask, render_template, request, jsonify, Response
# from utils.graph_qurey import QueryGraph
from utils.talk2graphs import QueryGraph
from utils.talk2pdf import QueryDocs
import time
import json
from threading import Thread

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

pdf_namespace = os.getenv('PINECONE_PDF_NAMESPACE')
graph_namespace = os.getenv('PINECONE_GRAPH_NAMESPACE')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('bot.html')


@app.route('/get', methods=['POST'])
def get_bot_response():
    question = request.form.get('msg')

    QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key)
    QD = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name)

    QG3 = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key, model_version="gpt-3.5-turbo-16k")
    QD3 = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name, model_version="gpt-3.5-turbo-16k")
    
    response = {}
    def run_exp(exp_name, func, *args, **kwargs):
        try:
            response[exp_name] = func(*args, **kwargs)
            print (f"........Finished {exp_name}........")
        except Exception as e:
            response[exp_name] = str(e)
            print(f"An error occurred in {exp_name}: {str(e)}")

    experiments = [
        ("Method of Generic_Cypher: - GPT4", QG.generic_cypher, question),
        ("Method of Langchain Graph Cypher QA - GPT4", QG.graph_cypher_qa, question),
        ("Method of Optimised Cypher QA - GPT4", QG.optimised_cyher, question, pinecone_api_key,  
                                            pinecone_env_name,pinecone_index_name, graph_namespace),
        ("Method of Talk to PDF - GPT4 ", QD.qa_pdf, question, pdf_namespace),
        ("Method of Talk to Knowledge Triples - GPT4", QD.qa_knowledge_triples, question),


        ("Method of Generic_Cypher: - GPT3.5", QG3.generic_cypher, question),
        ("Method of Langchain Graph Cypher QA - GPT3.5", QG3.graph_cypher_qa, question),
        ("Method of Optimised Cypher QA - GPT3.5", QG3.optimised_cyher, question, pinecone_api_key,  
                                            pinecone_env_name,pinecone_index_name, graph_namespace),
        ("Method of Talk to PDF - GPT3.5 ", QD3.qa_pdf, question, pdf_namespace),
        ("Method of Talk to Knowledge Triples - GPT3.5", QD3.qa_knowledge_triples, question)
    ]

    threads = [Thread(target=run_exp, args=exp) for exp in experiments]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
