import streamlit as st

from langchain_core.messages import HumanMessage
from chatbot_backend import workflow, config

# st.session_state => dict, values persist until and unless you refresh the page manually, therefore it solves the problem of persistence.

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


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

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(initial_state,
                            config=config,
                            stream_mode="messages")
        )

    st.session_state['message_history'].append({
        'role': 'ai',
        'content': ai_message
    })
