import pandas as pd
import matplotlib.pyplot as plt
import json

# CSV Daten einlesen, PLZ als String
dfKunden = pd.read_csv("csv\\kunden.csv", dtype={"PLZ": str})
dfPLZ = pd.read_csv("csv\\zuordnung_plz_ort.csv", dtype={"plz": str})

# print(dfKunden.head())
# print(dfPLZ.head())

#### Aufgabe 1 ####

# alle Kunden zählen
print(len(dfKunden))

# alle Kunden aus Köln
dfKundenKoeln = dfKunden[dfKunden["Ort"] == "Köln"]
# print(dfKundenKoeln.head())

# Liste unterschiedlicher PLZ
unterschiedlichePLZ = dfKunden["PLZ"].unique()

#### Aufagbe 2 ####

# Spalte im zweiten Dataframe umbennen um mergen zu können
dfPLZ = dfPLZ.rename(columns={'plz': 'PLZ'})

# merge ausführen, der den ganzen ersten Dataframe nimmt und ein Indikator für den Merge liefert
dfMerged = pd.merge(dfKunden, dfPLZ, on = 'PLZ', how='left', indicator=True)
# print(dfMerged.head())

# für jeden Kunden das Bundesland ausgeben
for i in range(0, len(dfMerged)):
    print(dfMerged["Vorname"].iloc[i],  dfMerged["Nachname"].iloc[i], dfMerged["bundesland"].iloc[i])

# Kunden pro Bundesland zählen und als Excel ausgeben
dfBundeslandKunden = dfMerged.groupby("bundesland").size()
dfBundeslandKunden.to_excel("bundeslandKunden.xlsx")

#### Aufgabe 3 ####

# neue Spalte voller_name einfügen
dfMerged["voller_name"] = dfMerged["Vorname"] + " " + dfMerged["Nachname"]
# print(dfMerged.head())

# Sortieren nach Bundesland und Name
dfMerged = dfMerged.sort_values(by=["bundesland", "Nachname"])

# Unterschiedliche Orte pro Bundesland zählen
dfOrte = dfMerged.groupby('bundesland')['Ort'].nunique()
# print(dfOrte.head())

# Kunden deren PLZ nicht in der Zuordnung vorkommt
ungueltige_plz = dfKunden[~dfKunden['PLZ'].isin(dfMerged['PLZ'])]
print(ungueltige_plz.head())

#### Aufgabe 4 ####

# Report mit allen Metriken
report = dfMerged.groupby('bundesland').agg({
    'voller_name': 'count',              # Anzahl Kunden
    'Ort': 'nunique',              # Anzahl unterschiedliche Orte
    'PLZ': lambda x: x.mode()[0] if not x.mode().empty else None  # Häufigste PLZ
})
# Spalten für den Report bennen
report.columns = ['Anzahl_Kunden', 'Anzahl_Orte', 'Häufigste_PLZ']
# Report ausgeben
print(report)

# JSON Datei aufbauen für Kunden gruppiert nach Bundesland, mit voller_name, PLZ und Ort
kunden_json = {}
for bundesland, group in dfMerged.groupby('bundesland'):
    kunden_json[bundesland] = group[['voller_name', 'PLZ', 'Ort']].to_dict('records')

# JSON Datei erstellen
with open('kunden_nach_bundesland.json', 'w', encoding='utf-8') as f:
    json.dump(kunden_json, f, indent=2, ensure_ascii=False)


# 3 Kategorien für die Datenqulaität, Kunden mit wiedersprüchllicher PLZ/Ort Zuordnung:
print("=== DATENQUALITÄT ===")
print(f"✅ Gültige PLZ/Ort: {len(dfMerged[dfMerged['_merge'] == 'both'])}")
print(f"❌ Unbekannte PLZ/Ort: {len(dfMerged[dfMerged['_merge'] == 'left_only'])}")
print(f"Fehlprozentsatz: {(len(dfMerged[dfMerged['_merge'] == 'left_only'])/len(dfMerged)*100):.1f}%")

# Problem-Kunden anzeigen
problematisch = dfMerged[dfMerged['_merge'] == 'left_only'][['voller_name', 'PLZ', 'Ort']]
print("\nProblem-Kunden:\n", problematisch)

# Kunden nach Bundesland zählen
kunden_pro_bl = dfMerged['bundesland'].value_counts()

# Balkendiagramm erstellen uns ausgaben
plt.figure(figsize=(10, 6))
kunden_pro_bl.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Kundenverteilung nach Bundesland')
plt.xlabel('Bundesland')
plt.ylabel('Anzahl Kunden')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('kunden_bundesland.png', dpi=300)
plt.show()