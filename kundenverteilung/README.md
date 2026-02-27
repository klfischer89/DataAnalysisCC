# Kundenverteilung Projekt mit Python #

## Verwendete Tools ##

- Python
- MySQL
- Grafana

## Startanleitung ##

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
- Der Pfad für die CSV Datei entspricht dem csv Verzeichnis Projektordner

## Visualisierung in Grafana ##

[Link zum Snapshot vom Grafana Dashboard](http://localhost:3000/dashboard/snapshot/mlQcqIueUAlIGn3OH3lFIs8MKlZZJ1nN) in dem die Daten visualisiert wurden
