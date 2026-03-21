from langchain_core.prompts import PromptTemplate

template="""
    Write a professional job application email for the position of AI Engineer.
    Company Name: {company_name}

    Candidate Background:
    I am a developer with strong experience in Artificial Intelligence, Machine Learning, and NLP systems.

    Technical Skills:

    Languages:
    Python, SQL, Java, C/C++

    Machine Learning & Deep Learning:
    Supervised Learning, Unsupervised Learning, Feature Engineering, CNN, Natural Language Processing, Transformers, Retrieval Augmented Generation (RAG), Model Fine-tuning

    Libraries & Frameworks:
    PyTorch, TensorFlow, HuggingFace Transformers, Scikit-learn, NumPy, Pandas, Seaborn

    Data Science & Mathematics:
    Statistics, Probability, Linear Algebra

    Tools:
    Git, PyCharm, JupyterLab, Google Colab, VS Code

    Research Work:
    I have authored a research paper titled:
    "Forensic Text Completion using Transformer-based Models: Fine-tuning and Retrieval Augmented Approach."

    The paper has been accepted at:
    International Conference on Advances in Distributed Computing and Machine Learning (ICADCML 2026)

    The proceedings will be published in Springer LNNS.

    Instructions:
    - Write a concise and professional job application email.
    - Use simple, natural student-level English.
    - Avoid fancy vocabulary, overly formal language, or marketing-style phrases.
    - The email should sound genuine and human-written.
    - Express interest in the AI Engineer role at the company.
    - Briefly highlight relevant skills in AI, NLP, Transformers, and RAG systems.
    - Mention the research paper briefly.
    - Mention that my resume is attached for review.
    - Mention that I am available for an interview during the upcoming weekend, such as Friday or Saturday, at a time convenient for them.
    - Keep the email around 80-100 words.
    - Use Applicant name as `Pravesh Srivastava` and HR manager name as `{hr_name}`.

    Greeting Rules:
    - Start the email with: Dear {hr_name},
    - Do NOT add titles like Mr., Ms., Mrs., Dr.
    - Use only the exact name provided.

    Signature:
    - End with:
    Best regards,
    Pravesh Srivastava

    IMPORTANT OUTPUT RULES:
    - Return ONLY valid JSON with exactly these keys: "subject" and "body".
    - Do NOT include any extra text, markdown, or explanations.
    - Use double quotes for all keys and string values.
"""

# for each contact in the contacts file generate an object.
final_template = PromptTemplate(
    template=template,
    validate_template=True,
    input_variables=["company_name", "hr_name"]
)

final_template.save("job_template2.json")


"""
rules removed:
    Greeting Rules:
    - Start the email with: Dear {hr_name},
    - Do NOT add titles like Mr., Ms., Mrs., Dr.
    - Use only the exact name provided.
    - Start writing body after next line, do not append text in same line.

    Signature:
    End with:
    Best regards,
    Pravesh Srivastava

    IMPORTANT OUTPUT RULES:
    - Return ONLY valid JSON.
    - Do NOT include markdown.
    - Do NOT include explanations.
    - Do NOT include text before or after the JSON.
    - Use double quotes for all JSON keys and values.

    Expected JSON format:

    {
    "subject": "string",
    "body": "string"
    }
"""
