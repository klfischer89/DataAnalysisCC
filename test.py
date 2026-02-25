import pandas as pd

s1 = pd.Series([100, 200, 300, 400], index=["a", "b", "c", "d"])
s2 = pd.Series([100, 200, 300, 400])

print(s1)
print(s2)

print("Mit selbs definierten Index:", s1["a"])
print("Mit autogenerierten Index:", s1.iloc[0])
print("Zugriff auf mehrere Elemente:", s1[["a", "c"]])

for i, value in s1.items():
    print(f"Index: {i}, Wert: {value}")

print([f"Index: {i}, Wert: {value}" for i, value in s1.items()])

s1Addiert = s1 + 10        # Alle Werte +10
s1Multipliziert = s1 * 2         # Alle Werte verdoppeln

print("Mittelwert:", s1.mean())      # Mittelwert der Werte
print("Median:", s1.median())

s1Summe = s1.sum()
s1Max = s1.max()
s1Min = s1.min()
s1ValueCount = s1.value_counts()
print("Häufigkeiten:", s1ValueCount)
s1Unique = s1.unique()
print("Einzigartige Werte:", s1Unique)
s1NUnique = s1.nunique()
print("Anzhal einzigartige:", s1NUnique)

print("Summe aller Elemente:", s1Summe)

print(s1[s1 > 300])    # Nur Werte > 300

print(s1Addiert)
print(s1Multipliziert)

print(s1>150)

data = {"Anna": 30, "Ben": 40, "Clara": 25}
s = pd.Series(data)

df = pd.DataFrame({
    "Name": ["Anna", "Ben", "Clara"],
    "Alter": [30, 40, 25]
})

s3 = df["Alter"]
s4 = df["Name"]