import pandas as pd

# load contacts.csv file
contacts = pd.read_csv("./contacts.csv")

# create a new column of boolean datatype with default value False
contacts["applied"] = False
contacts.to_csv("./contacts_upd.csv")