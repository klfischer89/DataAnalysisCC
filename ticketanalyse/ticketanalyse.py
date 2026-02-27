import pandas as pd

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
# 🔍 3. DUPLIKATE PRÜFEN → Nur UNIQUE ticket_id einfügen
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
# 🔍 3. PRÜFEN OB STATUS NICHT ABGESCHLOSSEN
# ============================================================================
# Boolesche Liste: True wo Status == "Abgeschlossen"
status_nicht_abgeschlossen = [status != "Abgeschlossen" for status in dfTicktetsClean["Status"]]

# Anzahl abgeschlossener Tickets
anzahl__nicht_abgeschlossen = sum(status_nicht_abgeschlossen)
print(f"⚠️ Anzahl nicht abgeschlossener Tickets: {anzahl__nicht_abgeschlossen}")

# Als Maske für DataFrame-Filter verwenden
df_nicht_abgeschlossen = dfTicktetsClean[status_nicht_abgeschlossen]
# print(f"{df_nicht_abgeschlossen["Ticket_ID"]}")

# ============================================================================
# 🔍 3. PRÜFEN AUF LANGE BEARBEITUNGSZEITEN
# ============================================================================
lange_bearbeitungszeiten = [bearbeitungszeit > dfTicktetsClean["Bearbeitungszeit_h"].mean() for bearbeitungszeit in dfTicktetsClean["Bearbeitungszeit_h"]]
anzahl_lange_bearbeitungszeiten = sum(lange_bearbeitungszeiten)
print(f"⚠️ Anzahl Tickets mit langen Bearbeigunszeiten: {anzahl_lange_bearbeitungszeiten}")
df_lange_bearbeitungszeiten = dfTicktetsClean[lange_bearbeitungszeiten]
# print(f"{df_lange_bearbeitungszeiten["Ticket_ID"]}")

# ============================================================================
# 🔍 3. PRÜFEN AUF BEARBEITER MIT AUFFÄLLIGEN WERTEN
# ============================================================================

# 1. GRUPPIEREN nach Bearbeiter
bearbeiter_stats = dfTicktetsClean.groupby('Bearbeiter').agg({
    'Bearbeitungszeit_h': 'mean',      # Durchschnittliche Bearbeitungszeit pro Bearbeiter
    'Status': lambda x: sum(x != 'Abgeschlossen'),  # Anzahl NICHT abgeschlossener Tickets
    'Ticket_ID': 'count'             # Gesamtanzahl Tickets (optional)
}).round(2)

bearbeiter_stats.columns = ['Durchschnitts_Bearbeitungszeit', 
                           'Offene_Tickets', 
                           'Gesamt_Tickets']

# 2. Globale Durchschnittswerte berechnen
durchschnitt_zeit = bearbeiter_stats['Durchschnitts_Bearbeitungszeit'].mean()
durchschnitt_offene = bearbeiter_stats['Offene_Tickets'].mean()

# 3. Bearbeiter filtern: BEIDE Bedingungen erfüllen
problematische_bearbeiter = bearbeiter_stats[
    (bearbeiter_stats['Durchschnitts_Bearbeitungszeit'] > durchschnitt_zeit) &
    (bearbeiter_stats['Offene_Tickets'] > durchschnitt_offene)
]

print("Durchschnitt Bearbeitungszeit:", round(durchschnitt_zeit, 2))
print("Durchschnitt offene Tickets:", round(durchschnitt_offene, 2))
print("\n⚠️ Problematische Bearbeiter:")
print(problematische_bearbeiter.sort_values('Offene_Tickets', ascending=False))
