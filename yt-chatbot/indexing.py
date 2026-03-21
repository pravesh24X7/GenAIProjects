from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# load transcript file
loader = TextLoader("./test_transcript.txt")
transcript = [ item for item in loader.lazy_load() ]

# create splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                          chunk_overlap=20,
                                          separators=["\n\n", "\n", "."])
documents = splitter.split_documents(transcript)

# create embedding model
embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

# create vector store
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embedding_model
)

# save vector store
vector_store.save_local("./test_trascript_store/")

# IF everything goes fine
print("[+] Indexing done.")