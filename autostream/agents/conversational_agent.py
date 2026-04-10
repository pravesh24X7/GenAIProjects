try:
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except Exception as e:
    print("[+] Program Terminated\n\n{e}".format(e))
    raise SystemExit

import json
from datetime import date
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.load import loads
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from rag.retriever import get_retriever
from utils.format import format_docs
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class Intent(BaseModel):
    intent: Literal["greeting", "enquiry", "high_intent"] = Field(description="describes the context of query.")


llm_model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
                     temperature=0.7,
                     model_kwargs={})

parser = PydanticOutputParser(pydantic_object=Intent)
text_parser = StrOutputParser()

base_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an AI agent of a fictional SaaS company named as `AutoStream`, which provides automated video editing tools for content creators. " \
        "Only provide answers to the questions which user asked. Do not provide any other information regarding anything."
    ),
    MessagesPlaceholder(
        variable_name="chat_history"
    ),
    HumanMessagePromptTemplate.from_template(
        """
        Classify the intent of given statement into below given three categories.
            1. Greeting.
            2. Product or price enquiry.
            3. High Intent.
        \n\n
        {format_instruction}.
        \n\n
        {statement}
        """
    )
])

with open("../custom_prompts/greet_template.json", "r") as f:
    greet_template = loads(f.read())
with open("../custom_prompts/enquiry_prompt.json", "r") as f:
    enquiry_template = loads(f.read())
with open("../custom_prompts/high_intent_prompt.json", "r") as f:
    high_intent_template = loads(f.read())

retriever = get_retriever(store_path="../rag/vector-store/")

chat_history = []

chain = base_prompt | llm_model | parser

while True:
    user_msg = input("HUMAN : ").strip()
    if user_msg.lower() == "exit":
        break

    response = chain.invoke({
        "statement": user_msg,
        "chat_history": chat_history,
        "format_instruction": parser.get_format_instructions()
    })

    chat_history.append(HumanMessage(content=user_msg))

    if response.intent == 'greeting':
        greet_chain = greet_template | llm_model | text_parser
        
        greetings_reponse = greet_chain.invoke({
            "query": user_msg,
            "chat_history": chat_history
        })
        chat_history.append(AIMessage(content=greetings_reponse))
        print(greetings_reponse)
    elif response.intent == 'enquiry':
        enquiry_chain = ({
            "context": lambda x: format_docs(retriever.invoke(x["query"])),
            "query": lambda x: x["query"],
            "chat_history": lambda x: x["chat_history"],
        } | enquiry_template | llm_model | text_parser)

        enquiry_response = enquiry_chain.invoke({
            "context": retriever,
            "query": user_msg,
            "chat_history": chat_history,
        })
        chat_history.append(AIMessage(content=enquiry_response))
        print(enquiry_response)
    elif response.intent == 'high_intent':
        high_intent_chain = high_intent_template | llm_model | text_parser

        high_intent_response = high_intent_chain.invoke({
            "query": user_msg,
            "chat_history": chat_history,
        })
        chat_history.append(AIMessage(content=high_intent_response))
        print(high_intent_response)


history = [
    {
        "role": "human" if isinstance(msg, HumanMessage) else "ai",
        "content": msg.content
    }
    for msg in chat_history
]

with open(f"history-{date.today()}.json", "a") as f:
    json.dump(history, f, indent=2)