import uuid

import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage
from new_backend import workflow, retrieve_all_threads

# st.session_state => dict, values persist until and unless you refresh the page manually, therefore it solves the problem of persistence.


# utility functions
def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    new_thread_id = generate_thread_id()
    st.session_state['thread_id'] = new_thread_id
    add_thread(new_thread_id)
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    if not workflow.get_state(config={
                                'configurable': {
                                    'thread_id': thread_id
                                }
                            }).values:
        return []
    return workflow.get_state(config={
                                'configurable': {
                                    'thread_id': thread_id
                                }
                            }).values['messages']


# session setup
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# sidebar
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Previous Conversation')

for tid in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(tid)):
        st.session_state['thread_id'] = tid
        messages = load_conversation(tid)
        
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'human'
            else:
                role = 'ai'
            temp_messages.append({
                'role': role,
                'content': message.content
            })
        
        st.session_state['message_history'] = temp_messages


# loading conversation history
for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])


user_query = st.chat_input('Type your message here ...')
if user_query:
    st.session_state['message_history'].append({
        'role': 'human',
        'content': user_query
    })

    with st.chat_message('human'):
        st.text(user_query)

    initial_state = {
        'messages': [HumanMessage(content=user_query)]
    }

    # streaming code
    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(initial_state,
                            config={
                                'configurable': {
                                    'thread_id': st.session_state['thread_id']
                                }
                            },
                            stream_mode="messages")
        )

    st.session_state['message_history'].append({
        'role': 'ai',
        'content': AIMessage(content=ai_message)
    })
