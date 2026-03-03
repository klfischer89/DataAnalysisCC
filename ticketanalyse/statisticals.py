import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Datensatz erstellen
# -----------------------------
data = {
    "Kategorie": ["IT", "Personal", "IT"],
    "Priorität": ["Hoch", "Mittel", "Niedrig"],
    "Mails": [4, 2, 1],
    "Bearbeitungszeit": [12, 8, 3]
}

df = pd.DataFrame(data)

print("Datensatz:")
print(df)
print("\n-----------------------------")

# -----------------------------
# Grundlegende Statistik
# -----------------------------
min_wert = df["Bearbeitungszeit"].min()
max_wert = df["Bearbeitungszeit"].max()
mittelwert = df["Bearbeitungszeit"].mean()
std_abw = df["Bearbeitungszeit"].std()

print("Statistische Kennzahlen:")
print(f"Minimum: {min_wert}")
print(f"Maximum: {max_wert}")
print(f"Mittelwert: {mittelwert:.2f}")
print(f"Standardabweichung (Streuung): {std_abw:.2f}")

print("\n-----------------------------")

# -----------------------------
# describe() Übersicht
# -----------------------------
print("describe() Ausgabe:")
print(df["Bearbeitungszeit"].describe())

print("\n-----------------------------")

df.groupby("Priorität")["Bearbeitungszeit"].mean().plot(kind="bar")
plt.show()

df.plot.scatter(x="Mails", y="Bearbeitungszeit")
plt.show()