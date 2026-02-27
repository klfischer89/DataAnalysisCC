from sqlalchemy import create_engine
import pandas as pd

# Verbindung konfigurieren
user = "root"
password = ""
host = "127.0.0.1"
port = 3306
database = 'datenanalyse'

# Engine erstellen
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# csv Dateien einlesen und als Dataframes speichern
dfKunde = pd.read_csv("kundenverteilung\\csv\\kunden.csv")
dfBundesland = pd.read_csv("kundenverteilung\\csv\\bundeslaender_hauptstaedte_koordinaten.csv")
dfPLZ = pd.read_csv("kundenverteilung\\csv\\eintraege_einmal_pro_plz.csv")

# Spalten umbenennen, damit ein Merge möglich ist
dfPLZ = dfPLZ.rename(columns={'plz': 'PLZ'})
dfPLZ = dfPLZ.rename(columns={'bundesland': 'Bundesland'})

# Merge der Postleitzahlen mit den Bundesländern
dfMerged1 = pd.merge(dfPLZ, dfBundesland, on = 'Bundesland', how='left', indicator=True)
# print(dfMerged1.head())

# Merge der Kundendaten mit dem vorherigen merge
dfMerged2 = pd.merge(dfKunde, dfMerged1, on = 'PLZ', how='left')
# print(dfMerged2.head())

# Nach Bundesland gruppieren und zählen, um Anzahl Kunden pro Bundesland zu ermitteln
dfBundeslandKunden = dfMerged2.groupby("Bundesland").size()

# Reset index um Spaltennamen anpassen zu könne, nötig für letzen Merge
dfBundeslandKunden = dfBundeslandKunden.reset_index()
dfBundeslandKunden.columns = ['Bundesland', 'Kunden_Anzahl']
# print(dfBundeslandKunden)

# Bundesländer mit Anzahl der Kunden mergen
dfData = pd.merge(
    left=dfBundeslandKunden,           # LINKS: Kunden-Daten
    right=dfBundesland,                # RECHTS: Koordinaten
    on='Bundesland',                   # VERKNÜPFEN nach Bundesland-Spalte
    how='left'                         # LEFT JOIN: Alle Bundesländer mit Kunden
)
# print(dfData.head())

# Finalen Dataframe in die Datenbank speichern
dfData.to_sql(
    name='kundenverteilung',          # Tabellenname
    con=engine,              # Datenbankverbindung
    if_exists='replace',     # Ersetzt Tabelle (oder 'append' zum Anhängen)
    index=False,             # Pandas Index NICHT speichern
    chunksize=1000,          # In Batches von 1000 Zeilen (schneller)
    method='multi'           # Schnelleres INSERT (MySQL)
)