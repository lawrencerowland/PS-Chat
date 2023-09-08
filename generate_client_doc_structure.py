import os
import glob
import json

from main import get_files, get_namespaces, get_questions

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