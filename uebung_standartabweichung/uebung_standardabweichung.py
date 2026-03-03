import pandas as pd
import numpy as np

# Datei einlesen
df = pd.read_csv("uebung_standartabweichung\\csv\\hardwarebestellung_prozesse.csv")

# Spalten in datetime Format transformieren
df["Anfragedatum"] = pd.to_datetime(df["Anfragedatum"])
df["Genehmigungsdatum"] = pd.to_datetime(df["Genehmigungsdatum"])
df["Bestelldatum"] = pd.to_datetime(df["Bestelldatum"])
df["Lieferdatum"] = pd.to_datetime(df["Lieferdatum"])
df["Uebergabedatum"] = pd.to_datetime(df["Uebergabedatum"])

# neue Spalten berechenen
df["Dauer_genehmigung"] = df["Genehmigungsdatum"] - df["Anfragedatum"]
df["Dauer_bestellung"] = df["Bestelldatum"] - df["Genehmigungsdatum"]
df["Dauer_lieferung"] = df["Lieferdatum"] - df["Bestelldatum"]
df["Dauer_uebergabe"] = df["Uebergabedatum"] - df["Lieferdatum"]
df["Dauer_gesamt"] = df["Uebergabedatum"] - df["Anfragedatum"]

# Statistiken ermitteln
dauer_gesamt_mittelwert = df["Dauer_gesamt"].mean()
dauer_gesamt_std = df["Dauer_gesamt"].std()
dauer_gesamt_min = df["Dauer_gesamt"].min()
dauer_gesamt_max = df["Dauer_gesamt"].max()

print(df["Dauer_gesamt"].describe())

# Prognosefehler berechnen
df["Fehler"] = df["Dauer_gesamt"] - pd.Timedelta(days=10)

# Timedelta in Tage umwandeln (normalisiert auf 1 Tag)
df["Fehler_Tage"] = df["Fehler"].dt.total_seconds() / (24 * 3600)
df["Dauer_gesamt"] =  df["Dauer_gesamt"].dt.total_seconds() / (24 * 3600)

# MAE und RMSE berechnen
mae = np.mean(np.abs(df["Fehler_Tage"]))
rmse = np.sqrt(np.mean(df["Fehler_Tage"] ** 2))

print(f"MAE: {mae:.2f} Tage")
print(f"RMSE: {rmse:.2f} Tage")

# fertigen Dataframe als csv speichern
df.to_csv("uebung_standartabweichung\\csv\\fehler_prognose.csv")