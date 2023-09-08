import os
import glob
import json

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

if __name__ == "__main__":
	doc_dir = './docs'
	files = get_files(doc_dir)
	namespaces = get_namespaces(doc_dir)
	questions = get_questions(doc_dir)
	docs_dict = {'files': files, 'namespaces': namespaces, 'questions': questions}
	filepath = "./data/client_doc_structure.json"
	
	os.makedirs(os.path.dirname(filepath), exist_ok=True)

	f = open(filepath, "w")
	json.dump(docs_dict, f)
	f.close()