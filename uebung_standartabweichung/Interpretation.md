# Interpretation

## Streuung und Prozessstabilität

Eine Standardabweichung von 2,74 Tagen bei einem Median von 10 Tagen bedeutet, dass ca. 68% der Werte innerhalb ±2,74 Tagen um den Mittelwert streuen (≈7,26 bis 12,74 Tage bei Normalverteilung).

Prozessstabilität: Die Streuung ist moderat bis hoch. Der Prozess zeigt:

   - Gewöhnliche Ursachen: Natürliche Variabilität (std ≈27% des Medians)

   - Keine extremen Ausreißer: min/max-Ratio (17/5=3,4) ist akzeptabel

   - Potenzielle Instabilität: std > IQR/1,35 deutet auf über normale Variation hin


## Prozessanalyse: Dauer_gesamt

### Deskriptive Statistik

mean 10 days 07:08:56.170212766
std 2 days 17:49:42.162956135 (~2,74 Tage)
min 5 days 00:00:00
25% 8 days 00:00:00
50% 10 days 00:00:00
75% 12 days 00:00:00
max 17 days 00:00:00


## Prozesskennzahlen
| Metrik | Wert     | Einheit |
|--------|----------|---------|
| **MAE** | 2,23    | Tage    |
| **RMSE**| 2,74    | Tage    |
| **IQR** | 4,00    | Tage    |

### Analyse-Ergebnisse

#### 1. Prozessstabilität
**Moderater bis schwankender Prozess**
- std = 27% des Mittels (10,07 Tage)
- IQR (4 Tage) kompakter als Gesamtstreuung (12 Tage Spannweite)
- **Grenzwertig für Stabilität** → Regelkarten-Kontrolle empfohlen

#### 2. Ausreißer-Erkennung
**Keine statistischen Ausreißer**
IQR = 4 Tage
untere Grenze: 8 - 1,5×4 = 2 Tage (min: 5 Tage)
obere Grenze: 12 + 1,5×4 = 18 Tage (max: 17 Tage)

#### 3. MAE vs. RMSE
**Moderate Ausreißer-Effekt**

RMSE² - MAE² = 7,51 - 4,97 = 2,54
√2,54 ≈ 1,6 Tage zusätzliche Abweichung durch größere Fehler

### Prozessstatus
Ziel: 10,00 Tage
Tatsächl. Mittel: 10,12 Tage (+1,2%)
±1 std (68%): 7,38-12,86 Tage
±2 std (95%): 4,64-15,60 Tage

**Fazit: Akzeptabler Prozess mit Optimierungspotenzial bei Streuungsreduktion.**
