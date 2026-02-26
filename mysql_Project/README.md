# MySQL Projekt mit Python #

## 1. Startanleitung ##

- Es muss eine MySQL Datenbank mit dem namen **"datenanlayse"** existieren, andernfalls muss das Attribut **database** für die Verindung angepasst werden
- Die Attribute für den SQL Connector müssen angepasst werden, **password** eintragen und ggf. **host** auf "localhost" setzen
```
user = "root"
password = ""
host = "127.0.0.1"
port = 3306
database = 'datenanalyse'
```
- Das Programm kann wie gewohnt über eine IDE wie VS Code ausgeführt werden
- Der Pfad für die CSV Datei entspricht dem Projektordner

## 2. Tabellenbeschreibung ##

### Tabelle tickets ###

- Attribute: 
``` 
Kundennummer
Startzeit
Endzeit
Bearbeiter
```

- Enthält eindeutige Kundennummern (Keine Duplikate)
- Leere Zeilen wurden entfernt

### Tabelle ###

- Attribute: 
``` 
Kundennummer
Startzeit
Endzeit
Bearbeiter
dauer_timedelta
dauer_minuten
dauer_stunden
dauer_hhmmss
```

- Enthält zusätzlich zu der Tabelle tickets, Informationen über die Dauer
- dauer_timedelta ist die Differenz zwischen der Startzeit und der Endzeit (beide sind im dateformat)
- dauer_minuten stellt die Dauer in Minuten dar
- dauer_stunden stellt die Dauer in Stunden dar
- dauer_hhmmss stellt die Dauer im folgenden Format dar d days hh:mm:ss

## 3. Umgang mit Duplikaten/Fehlern ##

1.  **_FEHLENDE WERTE PRÜFEN → FEHLERLISTE_**

* Alle Spalten mit fehlenden Werten werden in einen Dataframe der als Maske fungiert gespeichert (enthält Boolean Werte, TRUE wenn ein Feld leer ist)
* Mit Hilfe der Maske wird aus dem ursprünglichen Dataframe eine Kopie erstellt (enthält nur Zeilen mit leeren Feldern)
* Es wird geprüft ob Fehler exestieren, wenn Fehler exestieren, dann werden diese in eine CSV Datei gespeichert
* Es wird eine Kopie eines validen Dataframes gespeichert, der keine Fehlerhaften Zeilen enthält, mit der weiter gearbeitet werden kann

2. **_DUPLIKATE PRÜFEN → Nur UNIQUE ticket_id einfügen_**

* Es wird auf doppelte Werte nur in der Spalte 'Kundennnummer' geprüft
* Alle doppelten Zeilen werten extrahiert (mit allen Spalten)
* Prüfung ob Duplikate exestieren
* Duplikate löschen, immer die zweite Zeile, die erste Zeile eines Duplikats bleibt erhalten