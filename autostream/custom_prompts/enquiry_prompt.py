from langchain_core.load import dumps
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

enquiry_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant of AutoStream.\n"
     "Answer user queries strictly based on the provided context.\n"
     "If the answer is not present in the context, say you don't know.\n"
     "Keep the response simple and relevant."
    ),
    
    MessagesPlaceholder(variable_name="chat_history"),
    
    ("human",
     """
     Context:
     {context}

     User Query:
     {query}
     """
    )
])

with open("./enquiry_prompt.json", "w") as f:
    f.write(dumps(enquiry_prompt))