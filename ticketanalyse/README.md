# Ticketanalyse Projekt mit Python #

## Verwendete Tools ##

- Python
- MySQL
- Grafana

## Startanleitung ##

- Es muss eine MySQL Datenbank mit dem namen **"ticketanalyse"** existieren, andernfalls muss das Attribut **database** für die Verindung angepasst werden
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

## Analyse in Python

1. CSV eingelesen (ticketdaten_block2_mit_uhrzeit.csv)
2. Daten bereinigt (leere Zeilen + Duplikate entfernt)
3. 12+ KPIs berechnet (Volumen, Zeit, Trends, Verhältnisse)
4. Problematische Tickets/Bearbeiter identifiziert
5. KPI-Dashboard erstellt (dfKPI)
6. MySQL-Tabelle 'kpi' gefüllt

## Visualisierung in Grafana ##

[Link zum Snapshot vom Grafana Dashboard](http://localhost:3000/dashboard/snapshot/4TK3D5XWWjBqoIm2cwUNQqYlJ3opNOB6) in dem die KPIs visualisiert wurden

## Früherkennung kritischer Tickets

Tickets mit einer hohen Priorität und überdurchschnittlicher Bearbeitungszeit werden als kritisch betrachtet.

**Ticket-Früherkennung mit Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green.svg)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit-learn-1.2%2B-orange.svg)](https://scikit-learn.org/)

**Automatisierte Erkennung kritischer Helpdesk-Tickets durch KNN-Klassifikation**

---

**Funktion**
Identifiziert **kritische Tickets** (hohe Priorität + lange Bearbeitungszeit) mit **K-Nearest-Neighbors** und **Label Encoding**.

**Input:** CSV mit Ticketdaten  
**Output:** **Vorhersagen + Modellgenauigkeit**

---

**Schnellstart**

```bash
pip install pandas scikit-learn numpy matplotlib seaborn
python ticket_frueherkennung.py

