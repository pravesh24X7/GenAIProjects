from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough
from retriever import get_retriever
from dotenv import load_dotenv

load_dotenv()

# create llm model
llm_model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
                     temperature=0.5,
                     model_kwargs={})

prompt_template = load_prompt("./rag_prompt.json")

parser = StrOutputParser()

retriever = get_retriever("./vector_store002/")

query = "What is the best model's accuracy?"

chain = ({"content": retriever,
          "question": RunnablePassthrough()}) | prompt_template | llm_model | parser
result = chain.invoke(query)

print("Answer from LLM : \n", result)