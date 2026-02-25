import pandas as pd # import pandas as pd

df = pd.read_csv("data\\support_tickets.csv") # read csv file and safe as dataframe

print(df.head())

anzahlDatensaetze = len(df)  # Anzahl Zeilen/Datensätze
durchschnittlicheBearbeitungszeit = df["Bearbeitungszeit_Minuten"].mean() # Durschnitt für die Bearbeitungszeit in Minuten

print("Anzahl Datensätze:", anzahlDatensaetze)
print("Durchschnittliche Bearbeitungszeit:", durchschnittlicheBearbeitungszeit)

