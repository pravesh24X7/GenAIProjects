import re
import json

results = []
with open("generated_emails.json") as f:
    results = json.load(f)

for raw_email in results:
    match = re.match(r"Subject: (.+?)\n+Email:\n+(.+)", raw_email, re.DOTALL)
    
    if match:
        subject = match.group(1).strip()
        email_body = match.group(2).strip()
    else:
        print("Could not parse email", raw_email)