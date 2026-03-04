# Interpretation der Ergebnisse

## Welche Teilprozesse haben den größten Einfluss auf die Gesamtdauer?
- Korrelation Übergabedauer zu Gesamtdauer : 0.82 -> starker linearer Zusammenhang
- Korrelation Lieferdauer zu Gesamtdauer : 0.27 -> schwacher linearer Zusammenhang
- Korrelation Genehmigungsdauer zu Gesamtdauer : 0.25 -> schwacher linearer Zusammenhang


Die Übergabedauer hat den größten Einfluss auf die Gesamtdauer. Wenn die Übergabedauer steigt dann steigt auch die Gesamtdauer.
Die Liefer- und Genehmigungsdauer haben ebenfalls mit den größten Einfluss, auch wenn dieser jeweils nur schwach ausgeprägt ist.

In den Scatterplots sieht man ausschließlich bei der Übergabedauer einen klaren linearen Zusammenhang zur Gesamtdauer.

## Gibt es Prozessschritte, deren Dauer kaum Einfluss auf die Gesamtdauer hat?
- Korrelation Bestelldauer zu Gesamtdauer : 0.19 -> schwacher linearer Zusammenhang
- Korrelation Anzahl Rückfragen zu Gesamtdauer : -0.08 -> schwacher linearer Zusammenhang


Mit steigender Bestelldauer steigt die Gesamtdauer schwach an.
Wenn es mehr Rückfragen gibt, dann sinkt die Gesamtdauer schwach.

## Gibt es Abhängigkeiten bei Abteilung und Priorität

### Priorität
- Korrelation Niedrige Priorität zu Gesamtdauer : 0.08 -> schwacher linearer Zusammenhang
- Korrelation Mittlere Priorität zu Gesamtdauer : 0.00 -> kein linearer Zusammenhang
- Korrelation Hohe Priorität zu Gesamtdauer : -0.11 -> schwacher linearer Zusammenhang


Bei einer niedrigen Priorität steigt die Gesamtdauer sehr schwach an.
Eine Mittlere Priorität hat gar keinen Einfluss auf die Gesamtdauer.
Eine hohe Priorität führt zu einer schwach sinkenden Gesamtdauer.

### Abteilung
- Korrelation Abteilung IT zu Gesamtdauer : 0.24 -> schwacher linearer Zusammenhang
- Korrelation Abteilung HR zu Gesamtdauer : 0.12 -> schwacher linearer Zusammenhang
- Korrelation Abteilung Marketing zu Gesamtdauer : 0.07 -> schwacher bis kein linearer Zusammenhang
- Korrelation Abteilung Vertrieb zu Gesamtdauer : -0.21 -> schwacher linearer Zusammenhang
- Korrelation Abteilung Buchhaltung zu Gesamtdauer : -0.16 -> schwacher linearer Zusammenhang
- Korrelation Abteilung Forschung zu Gesamtdauer : -0.04 -> schwacher bis kein linearer Zusammenhang


Die Abteilungen IT, HR und Marketing sind am langsamsten. Wobei die Abteilung IT die langsamste ist.
Die Abteilungen Vertrieb, Buchhaltung und Forschung arbeiten schneller. Die Abteilung Vertrieb ist die schnellste. 

Für die Abteilungen und die Priorität sieht man in den Scatterplots keinen linearen Zusammenhang.

## Optimierung

Der Prozess zur Übergabe muss optimiert werden um die Gesamtdauer zu reduzieren.

## Verwendete Modelle

- Spalten mit Datum wurden mit to_datetime in das richtige Format gebracht
- NaN Werte wurden entfernt
- Überprüfung der Shape von Feature und Target Daten
- Aufteilung der Daten in Train und Test Datensätze

- Lineare Regression 

    1. 
    - 13 Features: 
    Dauer_genehmigung, Dauer_bestellung, Dauer_lieferung, Dauer_uebergabe --> wurden aus vorhanden Spalten im Dataframe berechnet und zu float umgewandelt
    Abt_Buchhaltung, Abt_Forschung, Abt_HR, Abt_IT, Abt_Marketing, Abt_Vertrieb, Prio_hoch, Prio_mittel, Prio_niedrig --> wurden per One-Hot-Endocing aus den Spalten Abteilung und Prioritaet erstellt
    - 1 Target
    Dauer_gesamt --> wurde aus vorhandenen Spalten im Dataframe berechnet und zu float umgewandelt
    - Visualisierung der daten in einer Korralationsmatrix, Scatterplot, Boxplot
    - Visualisierung der in einem Pairplot
    - Ausgabe der Genauigkeit für Trainings- und Testdaten
    - Ausgabe R2 für Trainings- und Testdaten
    - Erstellung der Fnktionsgleichung für die Lineare Funktion

    2. 
    - 12 Features: 
    Dauer_genehmigung, Dauer_lieferung, Dauer_uebergabe --> wurden aus vorhanden Spalten im Dataframe berechnet und zu float umgewandelt
    Abt_Buchhaltung, Abt_Forschung, Abt_HR, Abt_IT, Abt_Marketing, Abt_Vertrieb, Prio_hoch, Prio_mittel, Prio_niedrig --> wurden per One-Hot-Endocing aus den Spalten Abteilung und Prioritaet erstellt
    - 1 Target
    Dauer_gesamt --> wurde aus vorhandenen Spalten im Dataframe berechnet und zu float umgewandelt
    - Ausgabe der Genauigkeit für Trainings- und Testdaten
    - Ausgabe R2 für Trainings- und Testdaten

- KNN

    - 2 Features:
    Abteilung_num, Prioritaet_num
    - 1 Target:
    Dauer_gesamt
    - Label_encoder um aus Abteilung und Priorität numerische Werte zu machen
    - NaN Werte durch 0 ersetzen
    - KNN mit 8 Nachbarn und Manhattan Distanz
    - Ausgabe R2 für Trainings- und Testdaten

- Neuronales Netz

    - 13 Features: 
    Dauer_genehmigung, Dauer_bestellung, Dauer_lieferung, Dauer_uebergabe
    Abt_Buchhaltung, Abt_Forschung, Abt_HR, Abt_IT, Abt_Marketing, Abt_Vertrieb, Prio_hoch, Prio_mittel, Prio_niedrig
    - 1 Target
    Dauer_gesamt
    - Sequenzielles Neuronales Netz --> 1 Input Neuron --> Hidden Schicht mit 128 Neuronen, Aktivierungsfunktion "relu" --> 1 Ausgabe Neuron, Aktivierungsfunktion "linear"
    - Optimizer --> Adaptive Moment Estimation
    - Loss --> Mean Squared Error
    - batch_size --> Anzahl Datenpunkte pro Gewichts-Update --> 32 (gut für kleine Datenmengen)
    - epochs --> 100 Trainingsdurchläufe
    - validation_data --> Testdaten während Training
    - verbose --> 1 --> Fortschrittsbalken für Epochen
    - Ausgabe MAE, MSE, RMSE, R2
    - Visualisierung der Modellqualität mittels Scatterplot --> Tatsächliche Dauer_gesamt und Vorhergesagte Dauer_gesamt