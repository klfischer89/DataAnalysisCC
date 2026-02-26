import pandas as pd
import numpy as np

#### Aufagbe 1 ####
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])

print("Element mit Index c:" ,s["c"])
print("Elemente größer 25:")
print(s[s>25])
s["b"] = 99
print("Geänderter Wert an Index b:", s["b"])
sMittelwert = s.mean()
print("Mittelwert:", sMittelwert)

#### Aufagbe 2 ####
s1 = pd.Series(np.random.randint(1, 101, size=5))

print("Series mit 5 zufälligen Zahlen")
print(s1)
s1Multipliziert = s1 *2
print("Series mit 2 multipliziert")
print(s1Multipliziert)
s1Neu = s1[s1>50]
print("Neue Series mit Werten über 50")
print(s1Neu)
print("Anzahl Werte größer 70")
s1Zaehlen = s1[s1>70].value_counts()
print(s1Zaehlen)
print("Standardabweichung:", s1.std())

#### Aufagbe 3 ####

sFarben = pd.Series(["rot", "blau", "rot", "grün", "blau", "blau"])
sFarbenUnigque = sFarben.unique()
print(sFarbenUnigque)
sFarben.loc["neu"] = "lila"
print(sFarben["neu"])
sFarben[sFarben == "blau"] = "cyan"
print(sFarben)
sFarben = sFarben.sort_values()
print(sFarben)

#### Aufagbe 4 ####

preise = pd.Series([10, 15, 20], index=["Apfel", "Banane", "Kiwi"])
mengen = pd.Series([2, 3, 1], index=["Apfel", "Banane", "Kiwi"])

gesamtPreis = preise * mengen
print(gesamtPreis)

prozente = (gesamtPreis / gesamtPreis.sum()) * 100
print(prozente.map("{:.1f}%".format))

df = pd.DataFrame()
df = pd.concat([df, gesamtPreis.to_frame().T])
df = df.rename(index={0: 'Wert'})
print(df)

print("Zeitreihe:")
# 7 Tage ab heute (Start: 25.02.2026)
dates = pd.date_range(start='2026-02-25', periods=7, freq='D')
# Zufällige Werte (z.B. 0-100)
zufalls_werte = np.random.randint(0, 101, size=7)
# Zeitreihe erstellen
zeitreihe = pd.Series(zufalls_werte, index=dates)
print(zeitreihe)