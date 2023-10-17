from flask import Flask, render_template, request, jsonify, session
# from utils.graph_qurey import QueryGraph
from utils.talk2graphs import QueryGraph
from utils.talk2pdf import QueryDocs
# from utils.talk2pdf_llm import QueryDocs
import json
### Load environment variables
from dotenv import load_dotenv
import os
import ast
from utils.get_doc_info import get_files, get_namespaces, get_questions
from utils.combine_chat_history import save_tuples_to_json, load_tuples_from_json
import random
import string

load_dotenv()
neo4j_url = os.getenv('NEO4J_URL')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')

openai_key = os.getenv('OPENAI_KEY')
os.environ['OPENAI_API_KEY'] = openai_key

pinecone_api_key = os.getenv('PINECONE_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV')
pinecone_index_name = os.getenv('PINECONE_INDEX')

graph_namespace = os.getenv('PINECONE_GRAPH_NAMESPACE')

pdf_doc_dir = os.getenv('PDF_DOC_DIR')

CHAT_HISTORY_FILE = "chat_history.json"


def get_response_from_pdf(question, pdf_namespaces, chat_history=[]):
	QD = QueryDocs(pinecone_api_key, pinecone_env_name, pinecone_index_name)
	response_answer = QD.qa_pdf_with_conversational_chain(question, chat_history, pdf_namespaces[0])
	response_answer["text"] = response_answer["output_text"].replace("\n", "<br>")
	response_answer["source"] = response_answer["citations"]
	
	return response_answer

def get_response_from_graph(question):
	try:
		print(f"Start querying graph... with {graph_namespace}")
		QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, openai_key)
		response_answer = QG.optimised_cypher(question, pinecone_api_key, pinecone_env_name, pinecone_index_name, graph_namespace)
		return response_answer.replace("\n", "<br>")
	except Exception as e:
		return "There is no associated information from graph."

app = Flask(__name__)
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(characters) for i in range(8))
app.secret_key = password
@app.route('/')
def home():
	files = {}
	namespaces = []
	questions = {}

	# initialise chat history
	with open(CHAT_HISTORY_FILE, 'w') as file:
		json.dump([], file)

	## If there are is a docs folder, use files within to to populate Source Selection, Document Display and Example Questions
	if os.path.isdir('./docs'):
		files = get_files(pdf_doc_dir)
		namespaces = get_namespaces(pdf_doc_dir)
		questions = get_questions(pdf_doc_dir)

	# Else if there is a client_doc_structure.json file use that
	elif os.path.isfile('./data/client_doc_structure.json'):
		with open('./data/client_doc_structure.json') as json_file:
			file_contents = json_file.read()

		data = json.loads(file_contents)
		files = data['files']
		namespaces = data['namespaces']
		questions = data['questions']

	# Else return placeholders
	else:
		files = {'No documents found': {'No data': None}}
		namespaces = []
		questions = {'No documents found': ['No data']}
		  
	session.clear() 
	return render_template('bot.html', files=files, namespaces=namespaces, questions=json.dumps(questions))

@app.route('/get', methods=['POST'])
def get_bot_response():
	question = request.form.get('msg')
	try:
		chat_history = load_tuples_from_json(CHAT_HISTORY_FILE)
	except FileNotFoundError:
		# create a new file
		with open(CHAT_HISTORY_FILE, 'w') as file:
			json.dump([], file)

	print ('history length', len(chat_history))

	# get all parameters
	pdf_namespaces = ast.literal_eval(request.form.get('namespace'))
	chat_mode = ast.literal_eval(request.form.get('chat_mode'))
	print (pdf_namespaces)
	print (chat_mode)

	# invalid chat mode
	if len(pdf_namespaces) == 0 and chat_mode!="Graph":
		return jsonify({"Answer": {"text": "Please select at least one source for PDF mode."}})
	
	# valid chat mode
	response = {"Answer": {}}
	if chat_mode=="PDF":
		response_pdf = get_response_from_pdf(question, pdf_namespaces, chat_history)
		response['Answer']["text"] = response_pdf["output_text"].replace("\n", "<br>")
		response["Answer"]["source"] = response_pdf["citations"]


	elif chat_mode=="Graph":
		response['Answer']['text'] = get_response_from_graph(question)

	else:
		response_graph = get_response_from_graph(question)
		response_pdf = get_response_from_pdf(question, pdf_namespaces, chat_history)
		response_all = f"<b>\n Response from graph: </b> \n {response_graph} <br> <b>Response from pdf: </b> {response_pdf['text']}"
		
		response["Answer"]["text"] = response_all
		response["Answer"]["source"] = response_pdf["source"]
	
	chat_history_per_round = (question, response["Answer"]["text"].replace("<br>", " "))
	chat_history.append(chat_history_per_round)

	save_tuples_to_json(chat_history, CHAT_HISTORY_FILE)

	return jsonify(response)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
