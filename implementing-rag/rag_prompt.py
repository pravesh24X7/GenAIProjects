from langchain_core.prompts import PromptTemplate

template = """
    Answer the below given question based on the given context.\n
    {content}.
    \n\n
    {question}
"""

prompt_template = PromptTemplate(template=template,
                                 validate_template=True,
                                 input_variables=["content", "question"])
prompt_template.save("./rag_prompt.json")