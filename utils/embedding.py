from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader

def generate_index():
	embeddings = HuggingFaceEmbeddings()
	loader = CSVLoader(file_path="history.csv")
	documents = loader.load()
	print(len(documents))
	db = FAISS.from_documents(documents, embeddings)
	query = "quiz"
	docs = db.similarity_search(query)
	print(docs[0].page_content)
	db.save_local("faiss_index")

if __name__ == '__main__':
	generate_index()