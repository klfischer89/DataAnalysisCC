import pandas as pd # import pandas as pd

df = pd.read_csv("csv\\ticketdaten.csv") # read csv file and safe as dataframe

# print(df)

dfBearbeiter = df["Bearbeiter"]
dfValueCounts = dfBearbeiter.value_counts()

print(dfValueCounts)