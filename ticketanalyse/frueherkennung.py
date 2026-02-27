import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


dfTicktets = pd.read_csv("ticketanalyse\\csv\\ticketdaten_block2_mit_uhrzeit.csv")

# print(dfTicktets.head())
# print(dfTicktets.describe())

# ============================================================================
# 🛡️ 1. LEERE ZEILEN ÜBERSPRINGEN
# ============================================================================
print("\n🔍 Prüfe leere Zeilen...")
dfTicktetsClean = dfTicktets.dropna(how='all')  # Nur Zeilen entfernen WO ALLES leer ist
print(f"✅ Leere Zeilen entfernt: {len(dfTicktets) - len(dfTicktetsClean)}")

# ============================================================================
# 🔍 2. DUPLIKATE PRÜFEN → Nur UNIQUE ticket_id einfügen
# ============================================================================
print("\n🔍 Prüfe Duplikate...")
duplikate_maske = dfTicktetsClean.duplicated(subset=['Ticket_ID'], keep=False)
duplikate = dfTicktetsClean[duplikate_maske]

if not duplikate.empty:
    print(f"⚠️  {len(duplikate)} doppelte ticket_id gefunden")
    print("Beispiele:")
    print(duplikate[['Ticket_ID']].head())
    
    # BEHALT nur ERSTE ticket_id (rest löschen)
    dfTicktetsClean = dfTicktetsClean.drop_duplicates(subset=['Ticket_ID'], keep='first')
    print(f"✅ Duplikate entfernt: {len(dfTicktetsClean)} unique Tickets")
else:
    print("✅ Keine Duplikate gefunden!")

# ============================================================================
#  3. FRÜHERKENNUNG
# ============================================================================

hohePrio = [prio == "Hoch" for prio in dfTicktetsClean["Priorität"]]
dfHohePrio = dfTicktetsClean[hohePrio]
# # print(dfHohePrio.head())

bearbeitungszeit = dfHohePrio['Bearbeitungszeit_h'].fillna(0).sum()
durschnitt = bearbeitungszeit / len(dfHohePrio)

# Neue Spalte "kritisch" erstellen
dfTicktetsClean['kritisch'] = (
    (dfTicktetsClean['Priorität'] == 'Hoch') & 
    (dfTicktetsClean['Bearbeitungszeit_h'] > durschnitt)
)

# Priorität zu Zahlen kodieren
label_encoder = LabelEncoder()
dfTicktetsClean['Priorität_num'] = label_encoder.fit_transform(dfTicktetsClean['Priorität'])

# Numerische Features verwenden
X = dfTicktetsClean[["Priorität_num", "Bearbeitungszeit_h"]].fillna(0)  # NaN → 0
y = dfTicktetsClean["kritisch"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42)

# Modell trainieren
model = KNeighborsClassifier(n_neighbors=3, p=1)
model.fit(X_train, y_train)

# Vorhersagen (NUMERISCHE Priorität!)
prioritaet_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print("Priorität → Zahl:", prioritaet_mapping)  # z.B. {'Hoch': 1, 'Mittel': 0, 'Niedrig': 2}

X_pred = np.array([
    [prioritaet_mapping['Niedrig'], 160],    
    [prioritaet_mapping['Niedrig'], 80],
    [prioritaet_mapping['Mittel'], 160],
    [prioritaet_mapping['Mittel'], 80],
    [prioritaet_mapping['Hoch'], 160],
    [prioritaet_mapping['Hoch'], 80]
])

y_pred = model.predict(X_pred)
print("Vorhersagen:", y_pred)
print("Genauigkeit:", model.score(X_test, y_test))
print("Wahrscheinlichkeiten:", model.predict_proba(X_test))