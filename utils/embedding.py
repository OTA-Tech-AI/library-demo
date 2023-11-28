import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import DataFrameLoader

def change_status(path):
	df = pd.read_csv(path, index_col=0)
	df['status'] = 1
	df.to_csv(path)

def generate_index_csv():
	embeddings = HuggingFaceEmbeddings()
	loader = CSVLoader(file_path="data/knowledge.csv")
	documents = loader.load()
	print(len(documents))
	db = FAISS.from_documents(documents, embeddings)
	query = "quiz"
	docs = db.similarity_search(query)
	print(docs[0].page_content)
	db.save_local("faiss_index")

### Reference: https://python.langchain.com/docs/integrations/document_loaders/pandas_dataframe
def generate_index_dataframe():
	embeddings = HuggingFaceEmbeddings()

	### FAQ Section ###
	faq_csv_path = "data/qa.csv"
	faq_df = pd.read_csv(faq_csv_path, index_col=0)
	faq_df['combined'] = faq_df['question'] + ": \n" + faq_df['answer']
	faq_df.drop(columns=['status', 'question', 'answer'], inplace=True)
	print("FAQ Section DataFrame: ", faq_df)

	### General Knowledge / Information ###
	knowledge_csv_path = "data/knowledge.csv"
	knowledge_df = pd.read_csv(knowledge_csv_path, index_col=0)
	knowledge_df['combined'] = knowledge_df['title'] + ": \n" + knowledge_df['knowledge']
	knowledge_df.drop(columns=['status', 'title', 'knowledge'], inplace=True)
	print("General Knowledge Section DataFrame: ", knowledge_df)

	combined_df = pd.concat([faq_df, knowledge_df], ignore_index=True)
	print("Combined DataFrame: ", combined_df)

	loader = DataFrameLoader(combined_df, page_content_column="combined")
	documents = loader.load()
	print("Entries in the document: ", len(documents))

	db = FAISS.from_documents(documents, embeddings)
	query = "quiz"
	docs = db.similarity_search(query)

	print(docs[0].page_content)
	print(docs[1].page_content)
	db.save_local("faiss_index")

	change_status(faq_csv_path)
	change_status(knowledge_csv_path)

if __name__ == '__main__':
	generate_index_dataframe()