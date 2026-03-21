from langchain_groq import ChatGroq
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from retriever import get_retriever
from dotenv import load_dotenv

load_dotenv()

# create llm model
llm_model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
                     temperature=0.5,
                     model_kwargs={})

# get the prompt
prompt = load_prompt("./yt_chat.json")

# setup parser
parser = StrOutputParser()

# setup retriever
retriever = get_retriever("./test_trascript_store/")

# create execution chain
chain = ({
    "context": retriever,
    "question": RunnablePassthrough(),
}) | prompt | llm_model | parser

# set query
query = "How do examples improve clarity in teaching complex mathematical ideas?"

# execute chain
result = chain.invoke(query)
print(result)