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
# 🔍 4. PRÜFEN AUF LANGE BEARBEITUNGSZEITEN
# ============================================================================
lange_bearbeitungszeiten = [bearbeitungszeit > dfTicktetsClean["Bearbeitungszeit_h"].mean() for bearbeitungszeit in dfTicktetsClean["Bearbeitungszeit_h"]]
anzahl_lange_bearbeitungszeiten = sum(lange_bearbeitungszeiten)
print(f"⚠️ Anzahl Tickets mit langen Bearbeigunszeiten: {anzahl_lange_bearbeitungszeiten}")
df_lange_bearbeitungszeiten = dfTicktetsClean[lange_bearbeitungszeiten]
# print(f"{df_lange_bearbeitungszeiten["Ticket_ID"]}")

# ============================================================================
# 🔍 5. PRÜFEN AUF BEARBEITER MIT AUFFÄLLIGEN WERTEN
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

# ============================================================================
# 🔍 6. KPIS ERMITTELN
# ============================================================================
anzahl_alle_Tickets = len(dfTicktetsClean)
print("✅ Anzahl aller Tickets:", anzahl_alle_Tickets)

anzahl_tickets_pro_kategorie = dfTicktetsClean.groupby("Kategorie").size()
print("✅ Anzahl Tickets pro Kategorie:")
print(anzahl_tickets_pro_kategorie)

anzahl_tickets_pro_bearbeiter = dfTicktetsClean.groupby("Bearbeiter").size()
print("✅ Anzahl Tickets pro Bearbeiter:")
print(anzahl_tickets_pro_bearbeiter)

anzahl_tickets_pro_Woche = dfTicktetsClean.groupby("Woche").size()
print("✅ Anzahl Tickets pro Woche:")
print(anzahl_tickets_pro_Woche)

durchschnitt_bearbeitungszeit_je_prio = dfTicktetsClean.groupby("Priorität").agg({
    'Bearbeitungszeit_h': 'mean'
}).round(2)
print("✅ Durchschnittliche Bearbeitungszeit je Priorität:")
print(durchschnitt_bearbeitungszeit_je_prio)

mailaufwand_pro_ticket = pd.DataFrame({
    "Ticket_ID": [],
    "Anzahl_Mails" : []
})
mailaufwand_pro_ticket["Ticket_ID"] = dfTicktetsClean["Ticket_ID"]
mailaufwand_pro_ticket["Anzahl_Mails"] = dfTicktetsClean["Anzahl_Mails"]
print("✅ Mailaufwand pro Ticket:")
print(mailaufwand_pro_ticket)

bearbeitungszeit_je_Mittarbeiter = dfTicktetsClean.groupby("Bearbeiter").agg({
    'Bearbeitungszeit_h': 'sum'
}).round(2)
print("✅ Bearbeitungszeit je Mitarbeiter:")
print(bearbeitungszeit_je_Mittarbeiter)

verhaltnis_prio_dauer = dfTicktetsClean.groupby("Priorität").agg({
    'Bearbeitungszeit_h': 'sum'
}).round(2)

komplette_bearbeitungszeit = dfTicktetsClean["Bearbeitungszeit_h"].sum()
print("✅ Gesamte Bearbeitungszeit:")
print(komplette_bearbeitungszeit)

durchschnitt_bearbeitungszeit = dfTicktetsClean["Bearbeitungszeit_h"].mean()
print("✅ Durchscnittliche Bearbeitungszeit:")
print(komplette_bearbeitungszeit)

verhaeltnis = verhaltnis_prio_dauer / komplette_bearbeitungszeit

print("✅ Verhältnis Priorität ↔ Bearbeitungsdauer:")
print(verhaeltnis)

# 3-Wochen gleitender Durchschnitt
trend_gleitend = anzahl_tickets_pro_Woche.rolling(window=3, center=True).mean()

print("✅ Trend (3-Wochen-Durchschnitt):")
print(pd.DataFrame({
    'Woche': anzahl_tickets_pro_Woche.index,
    'Tickets': anzahl_tickets_pro_Woche.values,
    'Trend': trend_gleitend.values
}))

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(anzahl_tickets_pro_Woche.index, anzahl_tickets_pro_Woche.values, 'o-', label='Tickets')
plt.plot(anzahl_tickets_pro_Woche.index, trend_gleitend.values, 'r--', linewidth=2, label='Trend (3W-MA)')
plt.title('Ticket-Trend pro Woche')
plt.ylabel('Anzahl Tickets')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================================
# 💾 7. DATEN IN EINEM DATA FRAME (KPI DASHBOARD)
# ============================================================================

# 1. Alle Daten normalisieren (Index → Kategorie-Spalte)
tickets_pro_woche = anzahl_tickets_pro_Woche.reset_index().rename(columns={0: 'Wert'})
tickets_pro_woche.columns = ['Kategorie', 'Wert']

tickets_pro_kat = anzahl_tickets_pro_kategorie.reset_index().rename(columns={0: 'Wert'})

bearbeitungszeit_mitarbeiter = bearbeitungszeit_je_Mittarbeiter.reset_index().rename(columns={'Bearbeiter': 'Kategorie', 'Bearbeitungszeit_h': 'Wert'})

bearzeitungszeit_prioritaet = verhaeltnis.reset_index().rename(columns={'Priorität': 'Kategorie', 'Bearbeitungszeit_h': 'Wert'})

tickets_pro_bearbeiter_df = anzahl_tickets_pro_bearbeiter.reset_index().rename(columns={'Bearbeiter': 'Kategorie', 0: 'Wert'})

# 2. Einzelwerte als 1-Zeilen-DataFrames
durchschnitt_df = pd.DataFrame({'Kategorie': ['Durchschnitt'], 'Wert': [durchschnitt_bearbeitungszeit]})
mail_durchschnitt_df = pd.DataFrame({'Kategorie': ['Mailaufwand_Durchschnitt'], 'Wert': [mailaufwand_pro_ticket['Anzahl_Mails'].mean()]})

# 3. ALLE zusammenfügen
dfKPI = pd.concat([
    tickets_pro_woche.assign(KPI_Typ='Tickets_pro_Woche'),
    tickets_pro_kat.assign(KPI_Typ='Tickets_pro_Kategorie'),
    bearbeitungszeit_mitarbeiter.assign(KPI_Typ='Bearbeitungszeit_Mitarbeiter'),
    bearzeitungszeit_prioritaet.assign(KPI_Typ='Bearbeitungszeit_Priorität'),
    tickets_pro_bearbeiter_df.assign(KPI_Typ='Tickets_pro_Bearbeiter'),
    durchschnitt_df.assign(KPI_Typ='Durchschnitt_Zeit'),
    mail_durchschnitt_df.assign(KPI_Typ='Mailaufwand_Durchschnitt')
], ignore_index=True)

print("✅ Vollständiges KPI-Dashboard:")
print(dfKPI)

# 4. Zusammenfassung pro KPI-Typ
print("\n📊 KPI-Zusammenfassung:")
pivot_kpi = dfKPI.pivot_table(values='Wert', index='KPI_Typ', aggfunc=['count', 'mean', 'sum']).round(1)
print(pivot_kpi)

# ============================================================================
# 💾 8. DATEN NACH MYSQL EXPORTIEREN
# ============================================================================
from sqlalchemy import create_engine

# Verbindung konfigurieren
user = "root"
password = "Kallefisch,-123!"
host = "127.0.0.1"
port = 3306
database = 'ticketanalyse'

# Engine erstellen
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

print("\n📤 Speichere in MySQL...")

# Tabelle: 'tickets' (ersetzt wenn vorhanden)
dfKPI.to_sql(
    name='kpi',              # Tabellenname
    con=engine,              # Datenbankverbindung
    if_exists='replace',     # Ersetzt Tabelle (oder 'append' zum Anhängen)
    index=False,             # Pandas Index NICHT speichern
    chunksize=1000,          # In Batches von 1000 Zeilen (schneller)
    method='multi'           # Schnelleres INSERT (MySQL)
)

print("✅ ERFOLGREICH in MySQL-Tabelle 'tickets' gespeichert!")
print(f"📋 Finale Daten: {len(dfKPI)} Zeilen, {len(dfKPI.columns)} Spalten")