import pandas as pd
import numpy as np
import json

df = pd.DataFrame({
    'name': ['Anna', 'Ben'],
    'info': [
        {"alter":25,"stadt":"Berlin"},
        {"alter":30,"stadt":"Hamburg"}
    ]
})

# Alter und Stadt extrahieren und als eigene Spalten speichern
df["alter"] = df['info'].apply(lambda x: x['alter'])
df["stadt"] = df['info'].apply(lambda x: x['stadt'])

# print(df)

df2 = pd.DataFrame({
    "user": ["u1", "u2"],
    "details": [
        {"adresse": {"stadt": "Berlin", "plz": "10115"}},
        {"adresse": {"stadt": "München", "plz": "80331"}}
    ]
})

# Stadt und PLZ aus Adresse extrahieren und als eigene Spalten speichern
df2["stadt"] = df2['details'].apply(lambda x: x['adresse']['stadt'])
df2["plz"] = df2['details'].apply(lambda x: x['adresse']['plz'])

# print(df2)

df3 = pd.DataFrame({
    "kunde": ["A", "B"],
    "tickets": [
        [{"id": 1, "status": "offen"}, {"id": 2, "status": "geschlossen"}],
        [{"id": 3, "status": "offen"}]
    ]
})

# Anzahl offener Tickets zählen
df3["offene_tickets"] = df3["tickets"].apply(
    lambda tickets: sum(1 for ticket in tickets if ticket["status"] == "offen")
)

# print(df3)

df4 = pd.read_json("jsonAufgaben\\test.json")

# 2. Durchschnitt der werte berechnen
df4['durchschnitt'] = df4['werte'].apply(lambda x: np.mean(x))

# 3. Filtern: aktiv == True UND durchschnitt > 4
ergebnis = df4[(df4['aktiv'] == True) & (df4['durchschnitt'] > 4)]

# print("Vollständiger DataFrame:")
# print(df4)
# print("\nGefiltertes Ergebnis:")
# print(ergebnis)

with open('jsonAufgaben\\test2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df5 = pd.json_normalize(
    data['standorte'], 
    'mitarbeiter',      
    ['stadt']           
)

# print(df5)
