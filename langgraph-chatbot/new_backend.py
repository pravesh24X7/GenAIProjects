import sqlite3

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from dotenv import load_dotenv


load_dotenv()


prompt = PromptTemplate(template="You're a helpful assistant. Provide answers to user query.\n\nQuery:{query}",
                        input_variables=['query'],
                        validate_template=True)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm_model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
                     model_kwargs={},
                     temperature=0.7)


def query_response(state: ChatState):

    response = llm_model.invoke(state['messages']).content
    return {'messages': [response]}


def retrieve_all_threads(thread_id=None):
    all_threads = set()
    for checkpoint in checkpointer.list(thread_id):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    return list(all_threads)


graph = StateGraph(ChatState)

graph.add_node('chat', query_response)

graph.add_edge(START, 'chat')
graph.add_edge('chat', END)


conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

workflow = graph.compile(checkpointer=checkpointer)
