from langchain_core.load import dumps
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "Provide a sweet and simple response to user greetings."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

with open("./greet_template.json", "w") as f:
    f.write(dumps(prompt))