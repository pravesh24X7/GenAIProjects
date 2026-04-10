try:
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except Exception as e:
    print("[+] Program Terminated\n\n{e}".format(e))
    raise SystemExit

import json
from datetime import date
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.load import loads
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from rag.retriever import get_retriever
from utils.format import format_docs
from tools.capture import mock_lead_capture
from langchain_classic import hub
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

lead_state = {
    "name": None,
    "email": None,
    "platform": None
}

chat_history = [SystemMessage(content="You are an AI agent of a fictional SaaS company named as `AutoStream`, which provides automated video editing tools for content creators. " \
        "Only provide answers to the questions which user asked. Do not provide any other information regarding anything.")]

chain = base_prompt | llm_model | parser
enquiry_chain = ({
    "context": lambda x: format_docs(retriever.invoke(x["query"])),
    "query": lambda x: x["query"],
    "chat_history": lambda x: x["chat_history"],
} | enquiry_template | llm_model | text_parser)
greet_chain = greet_template | llm_model | text_parser
high_intent_chain = high_intent_template | llm_model | text_parser

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
        greetings_reponse = greet_chain.invoke({
            "query": user_msg,
            "chat_history": chat_history
        })
        chat_history.append(AIMessage(content=greetings_reponse))
        print(greetings_reponse)
    elif response.intent == 'enquiry':
        enquiry_response = enquiry_chain.invoke({
            "query": user_msg,
            "chat_history": chat_history,
        })
        chat_history.append(AIMessage(content=enquiry_response))
        print(enquiry_response)
    elif response.intent == 'high_intent':
        msg_lower = user_msg.lower()

        # --- extract info ---
        if "@" in user_msg:
            lead_state["email"] = user_msg
        elif any(p in msg_lower for p in ["youtube", "instagram", "tiktok"]):
            lead_state["platform"] = user_msg
        elif lead_state["name"] is None and len(user_msg.split()) <= 3:
            lead_state["name"] = user_msg

        if all(lead_state.values()):
            mock_lead_capture(
                lead_state["name"],
                lead_state["email"],
                lead_state["platform"]
            )
            response_text = "Thanks! Our team will contact you soon."
        else:
            response_text = high_intent_chain.invoke({
                "query": user_msg,
                "chat_history": chat_history
            })

        print(response_text)
        chat_history.append(AIMessage(content=response_text))


history = [
    {
        "role": "human" if isinstance(msg, HumanMessage) else "ai",
        "content": msg.content
    }
    for msg in chat_history
]

with open(f"history-{date.today()}.json", "a") as f:
    json.dump(history, f, indent=2)