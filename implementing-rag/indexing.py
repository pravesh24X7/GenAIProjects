from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# load document
loader = PyPDFLoader("./Paperid_637_manuscript.pdf")
pdf_pages = []

for doc in loader.lazy_load():
    pdf_pages.append(doc)

# create splitter object
splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                          chunk_overlap=0,
                                          separators=["\n\n", "\n", "."])
documents = splitter.split_documents(pdf_pages)

print("Total no. of document are : ", len(documents))

# create embedding model
embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

# create a vector store
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embedding_model
)

# save vector store locally,
vector_store.save_local("./vector_store002/")

# IF everything goes according to plan.
print("[*] Indexing done.")