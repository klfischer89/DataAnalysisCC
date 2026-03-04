import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score   


# Datei einlesen
df = pd.read_csv("analyse_prozesslaufzeit\\csv\\hardwarebestellung_prozesse.csv")

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


# Umwandlung zu float
df["Dauer_genehmigung"] = df["Dauer_genehmigung"].dt.total_seconds() / (24 * 3600)
df["Dauer_bestellung"] = df["Dauer_bestellung"].dt.total_seconds() / (24 * 3600)
df["Dauer_lieferung"] = df["Dauer_lieferung"].dt.total_seconds() / (24 * 3600)
df["Dauer_uebergabe"] = df["Dauer_uebergabe"].dt.total_seconds() / (24 * 3600)
df["Dauer_gesamt"] =  df["Dauer_gesamt"].dt.total_seconds() / (24 * 3600)

# NaN Werte entfernen
df_clean = df.dropna()

# Daten in Train und Test aufteilen
X = df_clean[["Dauer_genehmigung", "Dauer_bestellung", "Dauer_lieferung", "Dauer_uebergabe"]]
y = df_clean["Dauer_gesamt"]

# Shape und length anzeigen
print("X.shape:", X.shape)  
print("y.shape:", y.shape) 
print("len(X):", len(X), "len(y):", len(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75, random_state = 42)

# Modell erstellen
model = LinearRegression()

# Modell trainieren
model.fit(X_train, y_train)

# Genauigkeiten des Modells für Trainings- und Testdaten
print("Genauigkeit für Trainingsdaten:", model.score(X_train, y_train))
print("Genauigkeitfür Testdaten:", model.score(X_test, y_test))

print("y_train.shape:", y_train.shape)  # z.B. (70, Anz_Features)
print("y_test.shape:", y_test.shape)  # Sollte (70,) sein
print("len(X):", len(y_train), "len(y):", len(y_train))

# Predictions für TRAIN erstellen
y_train_pred = model.predict(X_train)

# Predictions für TEST erstellen  
y_test_pred = model.predict(X_test)

# Bestimmtheitsmaß
print("R2 Train:", r2_score(y_train, y_train_pred)) 
print("R2 Test: ", r2_score(y_test, y_test_pred))   

# plot Data
fig = plt.figure(figsize=(20, 5))

# Korrelation
plt.subplot(1, 3, 1)
corr_matrix = df.select_dtypes(include=['number']).corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar_kws={'shrink': 0.8})
plt.title('Korrelationsmatrix')

# Scatter (erstes Feature vs Target)
plt.subplot(1, 3, 2)
plt.scatter(X.iloc[:,0], y, alpha=0.7)
plt.xlabel(X.columns[0])
plt.ylabel('Target')
plt.title('Scatterplot')

# Boxplot
plt.subplot(1, 3, 3)
plt.boxplot([y_train, y_test], labels=['Train', 'Test'])
plt.title('Train/Test Verteilung')

plt.tight_layout()
plt.show()
