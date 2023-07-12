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
    directory_path = './docs'
    filenames = os.listdir(directory_path)
    return render_template('bot.html', filenames=filenames)


@app.route('/get', methods=['POST'])
def get_bot_response():
    question = request.form.get('msg')

    # QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key)
    QD = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name)
    
    # response = {}
    # def run_exp(exp_name, func, *args, **kwargs):
    #     try:
    #         response[exp_name] = func(*args, **kwargs)
    #         print (f"........Finished {exp_name}........")
    #     except Exception as e:
    #         response[exp_name] = str(e)
    #         print(f"An error occurred in {exp_name}: {str(e)}")

    # experiments = [
    #     ("Method of Talk to PDF", QD.qa_pdf, question, pdf_namespace),
    #     ("Method of Talk to PDF with Citation", QD.qa_pdf_with_citations, question, pdf_namespace),
    # ]

    # threads = [Thread(target=run_exp, args=exp) for exp in experiments]
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()

    response = {"Answer": {}}
    response_answer = QD.qa_pdf_with_citations(question, pdf_namespace)
    response["Answer"]["text"]= response_answer["output_text"]
    response["Answer"]["source"]= response_answer["citations"]
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
