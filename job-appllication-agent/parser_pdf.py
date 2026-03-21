import pdfplumber
import pandas as pd

data = []

with pdfplumber.open("./contacts.pdf") as pdf:
    for page in pdf.pages:
        table = page.extract_table()

        if table:
            for row in table:
                data.append(row)

df = pd.DataFrame(
    data[1:], columns=data[0]
)
df.to_csv("./contact.csv", index=False)