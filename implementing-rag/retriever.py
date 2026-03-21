from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_vector_store(directory=""):
    if not directory:
        print("[-] Vector stoage directory missing ...\nPlease Update!!!")
        raise SystemExit
    
    embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(directory, embeddings=embedding_model, allow_dangerous_deserialization=True)

    return vector_store

def get_retriever(store_path=None):
    vector_store = load_vector_store(store_path)
    retriever = vector_store.as_retriever(search_type="mmr",
                                          search_kwargs={
                                              "k": 5,
                                              "lambda_mult": 0.5,
                                          })
    
    return retriever