from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = "./information.txt"

file_loader = TextLoader(file_path=FILE_PATH, encoding="UTF-8")
content = file_loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0,
                        separators=["\n", "."])
documents = splitter.split_documents(content)

embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

vector_store = FAISS.from_documents(
    embedding=embeddings,
    documents=documents
)

vector_store.save_local("./vector-store/")