



### Load environment variables
from dotenv import load_dotenv
import os
from tqdm import tqdm
load_dotenv()
neo4j_url = os.getenv('NEO4J_URL')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')
openai_key = os.getenv('OPENAI_KEY')
pinecone_api_key = os.getenv('PINECONE_KEY')
pinecone_env_name = os.getenv('PINECONE_ENV')
pinecone_index_name = os.getenv('PINECONE_INDEX')
os.environ['OPENAI_API_KEY'] = openai_key

pinecone_namespace = os.getenv('PINECONE_NAMESPACE')


from utils.graph_qurey import QueryGraph


questions = [
    "What are the strategic dependencies of our ongoing technological implementation projects?",
    "Which mitigation strategies are linked to the risk of poor project execution?",
    "What is our supply chain strategy associated with digital transformation?",
    "Hello, how are you?",
    "How is the weather today?",
]


if __name__ == "__main__":
    QG = QueryGraph(neo4j_url, neo4j_user, neo4j_password, 
                    openai_key, pinecone_api_key, pinecone_env_name, pinecone_index_name)
    inqualified_ans = 0
    print ("Start testing")
    for q in tqdm(questions):
        response = QG.graph_qa_pdf_pinecone(q, pinecone_namespace, "text")

        print(f"Question: {q} \nAnswer: {response}")

        if "SOURCES: n/a" in response:
            inqualified_ans += 1
            print(f"Question: {q} do not have an answer from reference.")
    
    print (f"The passing rate is {round(1-inqualified_ans/len(questions),2)*100}%")