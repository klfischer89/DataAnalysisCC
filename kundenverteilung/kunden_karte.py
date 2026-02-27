import folium
import pandas as pd


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

# Reset index um Spaltennamen anpassen zu können, wird zum Dataframe, nötig für letzen Merge
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
print(dfData.head())

# Karte zentriert auf Deutschland
m = folium.Map(location=[51.1657, 10.4515], zoom_start=6, tiles="OpenStreetMap")

# Marker für jedes Bundesland hinzufügen
for idx, row in dfData.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<b>{row['Bundesland']}</b><br>Kunden: {row['Kunden_Anzahl']}<br>Hauptstadt: {row['Hauptstadt']}",
        tooltip=f"{row['Bundesland']} ({row['Kunden_Anzahl']} Kunden)",
        icon=folium.Icon(color='blue', icon='users')  # Anpassbar: 'red', 'green' etc.
    ).add_to(m)

# Karte speichern/anzeigen
m.save('kundenverteilung\\bundeslaender_kunden.html')