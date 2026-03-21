from langchain_core.prompts import PromptTemplate

template = """
    You're a helpful assistant. Answer user's question based on given context.\n
    {context}.
    \n\n
    {question}.
"""

prompt_template = PromptTemplate(template=template,
                                 validate_template=True,
                                 input_variables=["context", "question"])
prompt_template.save("./yt_chat.json")