from langchain_core.load import dumps
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

high_intent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant of AutoStream. "
     "Your goal is to handle high intent users and collect their details properly."
    ),
    
    MessagesPlaceholder(variable_name="chat_history"),
    
    ("human",
     """
     Ask to the user for the below given details:
        1. Name
        2. Email
        3. Creator Platform.

     Also provide the answer to the user query.

     {query}
     """
    )
])

with open("./high_intent_prompt.json", "w") as f:
    f.write(dumps(high_intent_prompt))