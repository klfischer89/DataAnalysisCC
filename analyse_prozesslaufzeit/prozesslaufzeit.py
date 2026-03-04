import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import keras 
from keras import layers


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

# One-Hot Encoding nur für diese 2 Spalten
one_hot_abt = pd.get_dummies(df['Abteilung'], prefix='Abt', dtype=int)
one_hot_prio = pd.get_dummies(df['Prioritaet'], prefix='Prio', dtype=int)

# NEUE Spalten zum Original-DataFrame hinzufügen
df = pd.concat([df, one_hot_abt, one_hot_prio], axis=1)

# NaN Werte entfernen
df_clean = df.dropna()

X_cols = ["Dauer_genehmigung", "Dauer_bestellung", "Dauer_lieferung", "Dauer_uebergabe"] + \
         [col for col in df.columns if 'Abt_' in col or 'Prio_' in col]

# Daten in Train und Test aufteilen
# X = df_clean[["Dauer_genehmigung", "Dauer_bestellung", "Dauer_lieferung", "Dauer_uebergabe"]]
X = df_clean[X_cols]
y = df_clean["Dauer_gesamt"]

# neuen Dateframe als csv speichern
df_clean.to_csv("analyse_prozesslaufzeit\\csv\\hardwarebestellung_prozesse_clean.csv")

# Shape und length anzeigen
print("X.shape:", X.shape)  
print("y.shape:", y.shape) 
print("len(X):", len(X), "len(y):", len(y))

# Train und Test Daten bereitstellen
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75)

# Modell erstellen
model = LinearRegression()

# Modell trainieren
model.fit(X_train, y_train)

# Genauigkeiten des Modells für Trainings- und Testdaten
print("Genauigkeit für Trainingsdaten:", model.score(X_train, y_train))
print("Genauigkeitfür Testdaten:", model.score(X_test, y_test))

# shape und length für targtes
print("y_train.shape:", y_train.shape)
print("y_test.shape:", y_test.shape)
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

# Daten für Dauer für Pairplot vorbereiten
plot_data = X[["Dauer_genehmigung", "Dauer_bestellung", "Dauer_lieferung", "Dauer_uebergabe"]]
plot_data['Dauer_gesamt'] = y

sns.pairplot(plot_data, diag_kind='kde', corner=True)
plt.suptitle('Pairplot: Alle Features + Target', y=1.02)
plt.show()

# Daten für Abteilungen und Prioritaeten für Pairplot vorbereiten
plot_data = X[[col for col in df.columns if 'Abt_' in col or 'Prio_' in col]]
plot_data['Dauer_gesamt'] = y

sns.pairplot(plot_data, diag_kind='kde', corner=True)
plt.suptitle('Pairplot: Alle Features + Target', y=1.02)
plt.show()

# Standardabweichungen für die Regressionsformel berechnen
dauer_genehmigung_std = df_clean["Dauer_genehmigung"].std()
dauer_bestellung_std = df_clean["Dauer_bestellung"].std()
dauer_lieferung_std = df_clean["Dauer_lieferung"].std()
dauer_uebergabe_std = df_clean["Dauer_uebergabe"].std()
dauer_gesamt_std = df_clean["Dauer_gesamt"].std()


# Korrelationen berechenen für die Regressionsformel
korrelation_genehmigung = df_clean['Dauer_genehmigung'].corr(df_clean['Dauer_gesamt'])
korrelation_bestellung = df_clean['Dauer_bestellung'].corr(df_clean['Dauer_gesamt'])
korrelation_lieferung = df_clean['Dauer_lieferung'].corr(df_clean['Dauer_gesamt'])
korrelation_uebergabe = df_clean['Dauer_uebergabe'].corr(df_clean['Dauer_gesamt'])

# Berchnung der Steigungen
steigung_genehmigung = korrelation_genehmigung * dauer_gesamt_std/dauer_genehmigung_std
steigung_bestellung = korrelation_bestellung * dauer_gesamt_std/dauer_bestellung_std
steigung_lieferung = korrelation_lieferung * dauer_gesamt_std/dauer_lieferung_std
steigung_uebergabe = korrelation_uebergabe * dauer_gesamt_std/dauer_uebergabe_std

# Lineare Funktion
print(f"Lineare Funktion: Dauer_gesamt = {steigung_genehmigung:.2f} * Dauer_genehmigung + {steigung_bestellung:.2f} * Dauer_bestellung + {steigung_lieferung:.2f} * Dauer_lieferung + {steigung_uebergabe:.2f} * Dauer_uebergabe + b")

# Lineare Regression ohne Bestelldauer
X_cols_neu = ["Dauer_genehmigung", "Dauer_lieferung", "Dauer_uebergabe"] + \
         [col for col in df.columns if 'Abt_' in col or 'Prio_' in col]

# Daten in Train und Test aufteilen
# X = df_clean[["Dauer_genehmigung", "Dauer_bestellung", "Dauer_lieferung", "Dauer_uebergabe"]]
X_neu = df_clean[X_cols_neu]
y_neu = df_clean["Dauer_gesamt"]

# Train und Test Daten bereitstellen
X_train_neu, X_test_neu, y_train_neu, y_test_neu = train_test_split(X_neu, y_neu, train_size = 0.75)

# Modell erstellen
model_neu = LinearRegression()

# Modell trainieren
model_neu.fit(X_train_neu, y_train_neu)

# Genauigkeiten des Modells für Trainings- und Testdaten
print("Genauigkeit für Trainingsdaten:", model_neu.score(X_train_neu, y_train_neu))
print("Genauigkeitfür Testdaten:", model_neu.score(X_test_neu, y_test_neu))

# Predictions für TRAIN erstellen
y_train_pred_neu = model_neu.predict(X_train_neu)

# Predictions für TEST erstellen  
y_test_pred_neu = model_neu.predict(X_test_neu)

# Bestimmtheitsmaß
print("R2 Train:", r2_score(y_train_neu, y_train_pred_neu)) 
print("R2 Test: ", r2_score(y_test_neu, y_test_pred_neu))   

# KNN für Abteilungen und Prioritäten als Kategorien

# Priorität zu Zahlen kodieren
label_encoder = LabelEncoder()
df_clean['Prioritaet_num'] = label_encoder.fit_transform(df_clean['Prioritaet'])
df_clean['Abteilung_num'] = label_encoder.fit_transform(df_clean['Abteilung'])

# Numerische Features verwenden
X = df_clean[["Prioritaet_num", "Abteilung_num"]].fillna(0)  # NaN → 0
y = df_clean["Dauer_gesamt"]

# Train/Test Split
X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(X, y, train_size=0.75, random_state=42)

# Modell trainieren
model_knn = KNeighborsClassifier(n_neighbors=8, p=1)
model_knn.fit(X_train_knn, y_train_knn)

# Genauigkeiten des Modells für Trainings- und Testdaten
print("Genauigkeit für Trainingsdaten:", model_knn.score(X_train_knn, y_train_knn))
print("Genauigkeit für Testdaten:", model_knn.score(X_test_knn, y_test_knn))

# Predictions für TRAIN erstellen
y_train_pred_knn = model_knn.predict(X_train_knn)

# Predictions für TEST erstellen  
y_test_pred_knn = model_knn.predict(X_test_knn)

# Bestimmtheitsmaß
print("R2 Train:", r2_score(y_train_knn, y_train_pred_knn)) 
print("R2 Test: ", r2_score(y_test_knn, y_test_pred_knn))   

# Deeplearning

# Daten bereitstellen
X_dl = df_clean[X_cols]
y_dl = df_clean["Dauer_gesamt"]

# Modell erstellen, Anzahl Neuronen und Aktivierungsfunktionen
model_dl = keras.Sequential([
    keras.Input(shape=(13,)),
    layers.Dense(128, activation="relu"),
    layers.Dense(1, activation="linear")  # ← Linear für Regression!
])

# Modell konfigurieren, Optimizer und Fehler
model_dl.compile(
    optimizer=keras.optimizers.Adam(0.001),  
    loss=keras.losses.MeanSquaredError(),   # MSE für Regression
    metrics=['mae']
)

X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_dl, y_dl, test_size=0.2)

history = model_dl.fit(X_train_dl, y_train_dl, 
                      batch_size=32,  # ← 32 besser für kleine Daten
                      epochs=100,
                      validation_data=(X_test_dl, y_test_dl),
                      verbose=1)

# Test-Performance
test_loss, test_mae = model_dl.evaluate(X_test, y_test, verbose=0)
print(f"Test MAE: {test_mae:.2f}")
print(f"Test MSE: {test_loss:.2f}")


# RMSE und R2 berechnen
y_pred_dl = model_dl.predict(X_test_dl).flatten()
rmse = np.sqrt(mean_squared_error(y_test_dl, y_pred_dl))
r2 = r2_score(y_test_dl, y_pred_dl)

print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.3f}")

# Visualisierung
plt.figure(figsize=(10, 6))
plt.scatter(y_test_dl, y_pred_dl, alpha=0.6)
plt.plot([y_test_dl.min(), y_test_dl.max()], [y_test_dl.min(), y_test_dl.max()], 'r--', lw=2)
plt.xlabel('Tatsächliche Dauer_gesamt')
plt.ylabel('Vorhergesagte Dauer_gesamt')
plt.title(f'Modell-Qualität (R²={r2:.3f})')
plt.show()