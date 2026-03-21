import os, sys
import random, time, json
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import load_prompt
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from datetime import datetime

print("[+] Comment me before running")
print("[*] Remainder, Did you forget to update the contacts file")
sys.exit(0)


API_KEYS=[
    "KEY1",
    "KEY2",
    "KEY3",
]

MODEL_LIST = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

class Email(BaseModel):
    subject: str
    body: str

parser = JsonOutputParser(pydantic_object=Email)

contacts = pd.read_csv("./contacts-2026-03-13_15-24-05.csv")
selected_contacts = contacts[contacts["applied"] == False][:20]

sys_lvl_msg = SystemMessage(content="Return the response strictly in valid JSON format with keys `subject` and `body`.")

history = []

for idx in range(selected_contacts.shape[0]):

    print("[+] Begin processing :", idx)

    key = API_KEYS[(idx%len(API_KEYS))]
    model_name = MODEL_LIST[idx % len(MODEL_LIST)]
    os.environ["GROQ_API_KEY"]=key

    llm_model = ChatGroq(model=model_name,
                         temperature=0.45,
                         model_kwargs={})
    llm_model = llm_model.with_structured_output(Email)
    prompt_template = load_prompt("job_template2.json")

    hr_mail_id = selected_contacts.iloc[idx]["Email"]
    company_name = selected_contacts.iloc[idx]["Company"]
    hr_name = selected_contacts.iloc[idx]["Name"]

    final_template = prompt_template.invoke({
        "company_name": company_name,
        "hr_name": hr_name
    }).to_string()
    
    try:
        model_response = llm_model.invoke([sys_lvl_msg, HumanMessage(content=final_template)])
    except Exception as e:
        print("Error generating email:", e)
        continue
    else:
        history.append({
            "hr_name": hr_name,
            "hr_email": hr_mail_id,
            "company": company_name,
            "subject": model_response.subject,
            "body": model_response.body
        })

        # mark contact as applied
        contacts.loc[contacts["Email"] == hr_mail_id, "applied"] = True

        print(f"[+] Successfully processed {idx} -> {hr_mail_id}")
    finally:
        time.sleep(2)

with open("generated_emails.json", "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=4)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
contacts.to_csv(f"contacts-{timestamp}.csv", index=False)