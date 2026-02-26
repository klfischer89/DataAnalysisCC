from sqlalchemy import create_engine
import pandas as pd

# Verbindung konfigurieren
user = "root"
password = ""
host = "127.0.0.1"
port = 3306
database = 'datenanalyse'

# Engine erstellen
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

df = pd.read_csv("mysql_Project\\ticketdaten.csv")

# ============================================================================
# 🛡️ 1. LEERE ZEILEN ÜBERSPRINGEN
# ============================================================================
print("\n🔍 Prüfe leere Zeilen...")
df_clean = df.dropna(how='all')  # Nur Zeilen entfernen WO ALLES leer ist
print(f"✅ Leere Zeilen entfernt: {len(df) - len(df_clean)}")


# ============================================================================
# ❌ 2. FEHLENDE WERTE PRÜFEN → FEHLERLISTE
# ============================================================================
kritische_spalten = ['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter']

# Prüfe fehlende Werte in kritischen Spalten
fehler_maske = df_clean[['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter']].isna().any(axis=1)
fehler_df = df_clean[fehler_maske].copy()

if not fehler_df.empty:
    print(f"\n❌ {len(fehler_df)} Zeilen mit fehlenden kritischen Werten:")
    print(fehler_df[['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter']].head())
    
    # Fehlerliste als CSV speichern
    fehler_df.to_csv("csv\\fehler_tickets.csv", index=False)
    print("💾 Fehlerliste gespeichert: csv\\fehler_tickets.csv")
else:
    print("\n✅ Keine fehlenden kritischen Werte gefunden!")

# Gültige Daten (ohne Fehlerzeilen)
df_valid = df_clean[~fehler_maske].copy()
print(f"✅ Gültige Daten: {len(df_valid)} Zeilen")

# ============================================================================
# 🔍 3. DUPLIKATE PRÜFEN → Nur UNIQUE ticket_id einfügen
# ============================================================================
print("\n🔍 Prüfe Duplikate...")
duplikate_maske = df_valid.duplicated(subset=['Kundennummer'], keep=False)
duplikate = df_valid[duplikate_maske]

if not duplikate.empty:
    print(f"⚠️  {len(duplikate)} doppelte ticket_id gefunden")
    print("Beispiele:")
    print(duplikate[['Kundennummer']].head())
    
    # BEHALT nur ERSTE ticket_id (rest löschen)
    df_valid = df_valid.drop_duplicates(subset=['Kundennummer'], keep='first')
    print(f"✅ Duplikate entfernt: {len(df_valid)} unique Tickets")
else:
    print("✅ Keine Duplikate gefunden!")

# ============================================================================
# 💾 4. DATENBANK-SPEICHERN (MySQL)
# ============================================================================
print("\n📤 Speichere in MySQL...")

# Tabelle: 'tickets' (ersetzt wenn vorhanden)
df_valid.to_sql(
    name='tickets',           # Tabellenname
    con=engine,              # Datenbankverbindung
    if_exists='replace',     # Ersetzt Tabelle (oder 'append' zum Anhängen)
    index=False,             # Pandas Index NICHT speichern
    chunksize=1000,          # In Batches von 1000 Zeilen (schneller)
    method='multi'           # Schnelleres INSERT (MySQL)
)

print("✅ ERFOLGREICH in MySQL-Tabelle 'tickets' gespeichert!")
print(f"📋 Finale Daten: {len(df_valid)} Zeilen, {len(df_valid.columns)} Spalten")

# ============================================================================
# 🔎 5. VERIFIZIERUNG: Prüfe MySQL-Inhalt
# ============================================================================
print("\n🔍 Verifiziere MySQL-Daten...")
df_mysql = pd.read_sql("SELECT COUNT(*) as anzahl FROM tickets", engine)
print(f"✅ MySQL enthält: {df_mysql['anzahl'].iloc[0]} Zeilen")

# Zeige Struktur
print("\n📋 MySQL-Tabelle Struktur:")
df_struktur = pd.read_sql("DESCRIBE tickets", engine)
print(df_struktur[['Field', 'Type', 'Null']].to_string(index=False))

print("📥 Lade Tickets aus MySQL...")
# 1. ALLE Tickets aus Tabelle 'tickets' lesen
df_tickets = pd.read_sql("SELECT * FROM tickets", engine)
print(f"✅ {len(df_tickets)} Tickets geladen")

# Erste 3 Zeilen anzeigen
print("\n📋 Erste Tickets:")
print(df_tickets[['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter']].head(3))

# ============================================================================
# 🕐 2. DAUER BERECHNEN: ende - start
# ============================================================================

# Sicherstellen dass start/ende datetime sind
df_tickets['Startzeit'] = pd.to_datetime(df_tickets['Startzeit'])
df_tickets['Endezeit'] = pd.to_datetime(df_tickets['Endezeit'])

# Dauer berechnen (als timedelta)
df_tickets['dauer_timedelta'] = df_tickets['Endezeit'] - df_tickets['Startzeit']

print("\n🔍 Erste Dauer-Berechnungen:")
print(df_tickets[['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter', 'dauer_timedelta']].head())

# ============================================================================
# ⏱️ 3. UMLAGEN IN MINUTEN, STUNDEN, HH:MM:SS
# ============================================================================

# Minuten (total_seconds() / 60)
df_tickets['dauer_minuten'] = df_tickets['dauer_timedelta'].dt.total_seconds() / 60

# Stunden
df_tickets['dauer_stunden'] = df_tickets['dauer_minuten'] / 60

# HH:MM:SS Format
df_tickets['dauer_hhmmss'] = df_tickets['dauer_timedelta'].apply(
    lambda td: str(td).split('.')[0]  # Mikrosekunden abschneiden
)

print("\n⏱️  Dauer in allen Formaten:")
print(df_tickets[['Kundennummer', 'dauer_minuten', 'dauer_stunden', 'dauer_hhmmss']].head())

# ============================================================================
# 💾 4. ZURÜCK IN MYSQL SPEICHERN (erweiterte Tabelle)
# ============================================================================
print("\n💾 Speichere mit Dauer-Spalten zurück...")

df_tickets.to_sql(
    name='tickets_mit_dauer',  # Neue Tabelle
    con=engine,
    if_exists='replace',       # Ersetzt alte Version
    index=False,
    chunksize=1000
)

print("✅ Tickets mit Dauer in 'tickets_mit_dauer' gespeichert!")

# ============================================================================
# 📊 5. STATISTIKEN ANZEIGEN
# ============================================================================
print("\n📈 Dauer-Statistiken:")
stats = df_tickets['dauer_minuten'].describe()
print(stats)

print("\n🏆 Top 5 längste Tickets:")
top5 = df_tickets.nlargest(5, 'dauer_minuten')[['Kundennummer', 'dauer_minuten', 'dauer_hhmmss']]
print(top5)

# ============================================================================
# 🔍 6. VERIFIZIERUNG
# ============================================================================
print("\n🔍 MySQL-Verifizierung:")
check = pd.read_sql("SELECT COUNT(*) as anzahl, "
                   "AVG(dauer_minuten) as durchschnitt_minuten "
                   "FROM tickets_mit_dauer", engine)
print(check)

print("📥 Lade Tickets aus MySQL...")
# 1. Tickets aus erweiterter Tabelle laden (mit Dauer)
df_tickets = pd.read_sql("SELECT * FROM tickets_mit_dauer", engine)
print(f"✅ {len(df_tickets)} Tickets geladen")

# ============================================================================
# 📊 2. Excel-Datei erstellen: Ticket-Auswertung.xlsx
# ============================================================================

# Nur geforderte Spalten auswählen
excel_spalten = ['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter', 'dauer_minuten']
df_excel = df_tickets[excel_spalten].copy()

# Datetime-Format für Excel optimieren (schön anzeigen)
df_excel['Startzeit'] = pd.to_datetime(df_excel['Startzeit']).dt.strftime('%d.%m.%Y %H:%M')
df_excel['Endezeit'] = pd.to_datetime(df_excel['Endezeit']).dt.strftime('%d.%m.%Y %H:%M')

# Dauer-Minuten auf 2 Dezimalstellen runden
df_excel['dauer_minuten'] = df_excel['dauer_minuten'].round(2)

print("\n📋 Vorschau Excel-Daten:")
print(df_excel.head())

# ============================================================================
# 💾 3. EXCEL EXPORT: Tabellenblatt "Auswertung"
# ============================================================================

# Excel-Datei erstellen
excel_datei = "Ticket-Auswertung.xlsx"

with pd.ExcelWriter(excel_datei, engine='openpyxl') as writer:
    # Tabellenblatt "Auswertung" schreiben
    df_excel.to_excel(writer, sheet_name='Auswertung', index=False)
    
    # 📈 BONUS: Zusätzliche Übersicht als zweites Sheet
    zusammenfassung = pd.DataFrame({
        'Gesamtanzahl': [len(df_excel)],
        'Durchschnittliche Dauer [min]': [df_excel['dauer_minuten'].mean().round(2)],
        'Längstes Ticket [min]': [df_excel['dauer_minuten'].max().round(2)],
        'Kürzestes Ticket [min]': [df_excel['dauer_minuten'].min().round(2)]
    })
    
    zusammenfassung.to_excel(writer, sheet_name='Zusammenfassung', index=False)

print(f"\n✅ Excel-Datei erstellt: {excel_datei}")
print("📄 Tabellenblätter:")
print("   • Auswertung (Hauptdaten)")
print("   • Zusammenfassung (Statistiken)")


# ============================================================================
# 🔄 1. SORTIEREN: Nach längster Dauer ABSTEIGEND
# ============================================================================
df_sortiert = df_tickets.sort_values('dauer_minuten', ascending=False).copy()

print("\n📊 Vorschau: Top 5 längste Tickets")
print(df_sortiert[['Kundennummer', 'dauer_minuten']].head())

# Excel-Spalten vorbereiten
excel_spalten = ['Kundennummer', 'Startzeit', 'Endezeit', 'Bearbeiter', 'dauer_minuten']
df_excel = df_sortiert[excel_spalten].copy()

# Datetime-Format für Excel (deutsch)
df_excel['Startzeit'] = pd.to_datetime(df_excel['Startzeit']).dt.strftime('%d.%m.%Y %H:%M')
df_excel['Endezeit'] = pd.to_datetime(df_excel['Endezeit']).dt.strftime('%d.%m.%Y %H:%M')

# Dauer runden
df_excel['dauer_minuten'] = df_excel['dauer_minuten'].round(2)

# ============================================================================
# 📊 2. STATISTIK-Tabelle erstellen
# ============================================================================
statistik_data = {
    'Metrik': [
        'Gesamtanzahl Tickets',
        'Durchschnittliche Dauer (Minuten)',
        'Kürzeste Dauer (Minuten)', 
        'Längste Dauer (Minuten)',
        'Median Dauer (Minuten)',
        'Gesamtdauer (Stunden)'
    ],
    'Wert': [
        len(df_excel),
        f"{df_sortiert['dauer_minuten'].mean():.2f}",
        f"{df_sortiert['dauer_minuten'].min():.2f}",
        f"{df_sortiert['dauer_minuten'].max():.2f}",
        f"{df_sortiert['dauer_minuten'].median():.2f}",
        f"{df_sortiert['dauer_minuten'].sum() / 60:.2f}"
    ]
}
df_statistik = pd.DataFrame(statistik_data)

print("\n📈 Statistik-Vorschau:")
print(df_statistik)

# ============================================================================
# 💾 3. EXCEL mit 2 Tabellenblättern erstellen
# ============================================================================
excel_datei = "Ticket-Auswertung.xlsx"

with pd.ExcelWriter(excel_datei, engine='openpyxl') as writer:
    # Tab1: AUSWERTUNG (sortiert nach Dauer absteigend)
    df_excel.to_excel(writer, sheet_name='Auswertung', index=False)
    
    # Tab2: STATISTIK
    df_statistik.to_excel(writer, sheet_name='Statistik', index=False)

print(f"\n✅ Excel erstellt: {excel_datei}")
print("📄 Tabellenblätter:")
print("   • Auswertung (sortiert nach längster Dauer)")
print("   • Statistik (5 wichtige Kennzahlen)")
