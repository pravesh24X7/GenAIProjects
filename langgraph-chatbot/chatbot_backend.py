from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
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


config = {
    'configurable': {
        'thread_id': '1'
    }
}

graph = StateGraph(ChatState)

graph.add_node('chat', query_response)

graph.add_edge(START, 'chat')
graph.add_edge('chat', END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

# for message_chunk, metadata in workflow.stream(
#     {'messages': [HumanMessage(content="Write a 500 words essay on `History of India`")]},     # initial state
#     config=config,
#     stream_mode="messages"  # for LLM token generation, messages are the default mode to fetch tokens.
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end="", flush=True)
