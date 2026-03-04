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