from flask import Flask, render_template, request, jsonify, Response
# from utils.graph_qurey import QueryGraph
from utils.talk2graphs import QueryGraph
from utils.talk2pdf import QueryDocs
# from utils.talk2pdf_llm import QueryDocs
import time
import json
from threading import Thread
import glob
### Load environment variables
from dotenv import load_dotenv
import os
import ast

load_dotenv()
neo4j_url = os.getenv('NEO4J_URL')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')
openai_key = os.getenv('OPENAI_KEY')
pinecone_api_key = os.getenv('PINECONE_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV')
pinecone_index_name = os.getenv('PINECONE_INDEX')
os.environ['OPENAI_API_KEY'] = openai_key
graph_namespace = os.getenv('PINECONE_GRAPH_NAMESPACE')

app = Flask(__name__)

def get_files(directory_path):
    files = {}
    for item in os.listdir(directory_path):
        if not item.startswith('.'):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                files[item] = get_files(item_path) or {}
            else:
                files[item] = None
    return files

def get_namespaces(directory):
    namespaces = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            namespaces.append(dir)
    return namespaces

def get_questions(directory):
    Example_Questions = {}
    # Glob pattern to find 'question.txt' files in all subdirectories
    for filename in glob.glob(directory + '/**/questions.txt', recursive=True):
        with open(filename, 'r') as f:
            # Get the subfolder name
            subfolder_name = os.path.dirname(filename).split('/')[-1]
            # Read the file content and store it as a list of lines
            content = f.read().splitlines()
            dict_key = f"Example Questions of {subfolder_name}"
            Example_Questions[dict_key] = content
    return Example_Questions


@app.route('/')
def home():
    directory_path = './docs'
    files = get_files(directory_path)
    namespaces = get_namespaces(directory_path)
    Example_Questions = get_questions(directory_path)
    return render_template('bot.html', files=files, namespaces=namespaces, questions=json.dumps(Example_Questions))


@app.route('/get', methods=['POST'])
def get_bot_response():
    question = request.form.get('msg')
    
    # get all parameters
    pdf_namespaces = ast.literal_eval(request.form.get('namespace'))
    chat_mode = ast.literal_eval(request.form.get('chat_mode'))
    print (pdf_namespaces)
    print (chat_mode)

    # check document sources
    if len(pdf_namespaces) == 0 and chat_mode!="Graph":
        return jsonify({"Answer": {"text": "Please select at least one source for PDF mode."}})
    
    # check chat mode
    if chat_mode=="PDF":
        QD = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name)
        response = {"Answer": {}}
        response_answer = QD.qa_pdf_with_citations_from_multiple_srcs(question, pdf_namespaces)
        response["Answer"]["text"]= response_answer["output_text"].replace("\n", "<br>")
        response["Answer"]["source"]= response_answer["citations"]
        print (response['Answer']['text'])
        return jsonify(response)


    elif chat_mode=="Graph":
        response = {"Answer": {}}
        
        try:
            print (f"Start querying graph... with {graph_namespace}")
            QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key)
            response_answer_from_graph = QG.optimised_cypher(question,
                                                             pinecone_api_key,pinecone_env_name,pinecone_index_name,
                                                             graph_namespace)
        except Exception as e:
            response_answer_from_graph = "There is no asscoiated information from graph."
        
        response["Answer"]["text"]= response_answer_from_graph.replace("\n", "<br>")
        return jsonify(response)

    else:
        response = {"Answer": {}}
        try:
            QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key)
            response_answer_from_graph = QG.optimised_cypher(question, 
                                                             pinecone_api_key,pinecone_env_name,pinecone_index_name,
                                                             graph_namespace)
        except Exception as e:
            response_answer_from_graph = "There is no asscoiated information from graph."            
        

        QD = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name)
        response_answer_from_pdf = QD.qa_pdf_with_citations_from_multiple_srcs(question, pdf_namespaces)
        
        
        response_all = "<b>\n Response from graph: </b> \n" + response_answer_from_graph + "\n" + "<b>Response from pdf: </b>" + response_answer_from_pdf["output_text"]

        response["Answer"]["source"]= response_answer_from_pdf["citations"]
        response["Answer"]["text"]= response_all.replace("\n", "<br>")

        return jsonify(response)
    
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
