import pandas as pd

dfTickets = pd.read_csv("ticketanalyse\\csv\\tickets_bearbeitungszeit.csv")

mittelwertRueckfragen = dfTickets["Rueckfragen"].mean()
mittelwertDauer = dfTickets["Bearbeitungsdauer_Tage"].mean()

print("Mittelwert:")
print(mittelwertRueckfragen)
print(mittelwertDauer)

stdRueckfragen = dfTickets["Rueckfragen"].std()
stdDauer = dfTickets["Bearbeitungsdauer_Tage"].std()

print("Standardabweichung:")
print(stdRueckfragen)
print(stdDauer)

kovarianz = dfTickets['Rueckfragen'].cov(dfTickets['Bearbeitungsdauer_Tage'])

print("Kovarianz:")
print(kovarianz)

varRueckfragen = dfTickets["Rueckfragen"].var()
varDauer = dfTickets["Bearbeitungsdauer_Tage"].var()

print("Varianz:")
print(varRueckfragen)
print(varDauer)

steigung = kovarianz/varRueckfragen

print("Steigung:")
print(steigung)

achsenabschnitt = mittelwertDauer - steigung * mittelwertRueckfragen

print("Achsenabschnitt:")
print(achsenabschnitt)

print("Dauer für ein Ticket mit 6 Rückfragen")
y = achsenabschnitt + steigung * 6
print(y)