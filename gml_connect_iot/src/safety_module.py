import json
from datetime import datetime, timezone
from pathlib import Path

TRUCK_ID = "GML-001"
OUTPUT_DIR = Path("output")

# =====================================================================
# MODULE 2 : Safety (Physics) - Accelerometer Filtering & Threshold
# =====================================================================

def run_safety_module(csv_lines):
    print("--- DÉBUT ANALYSE MODULE 2 : Safety (Physics) ---\n")
    events = []
    samples_ok = 0 # sert à détecter un fichier vide
    line_number = 0

    # Lecture ligne par ligne pour simuler un traitement en streaming (Edge-native)
    for line in csv_lines:
        line_number += 1
        print(f"Lecture de la ligne : {line_number}\n")
        try:
            ts = line['timestamp']
            acc_y = line['acc_y']
            acc_y_val = float(acc_y)
            samples_ok += 1

            # Seuil de détection : décélération > 2.5 m/s² (valeur < -2.5)
            if acc_y_val < -2.5:
                event = {
                    "timestamp": int(ts),
                    "event_type": "Harsh Braking",
                    "value_ms2": acc_y_val,
                    "severity": "CRITICAL"
                }
                events.append(event)
                print(f"[{ts}] [ALERT SAFETY] Freinage Violent détecté sur l'axe Y : {acc_y_val} m/s² \n")
        except (ValueError, TypeError, KeyError) as e:
            print(f"Erreur de parsing sur la ligne : {line} ({e})\n")
            continue

    # Agrégation finale et export au format daily_score.json
    if samples_ok == 0:
        print("[ERREUR] Aucune donnée exploitable dans le fichier CSV : score non calculé.\n")
        safety_score = None
        safety_status = "NO_DATA"
    else:
        safety_score = max(0, 100 - 10 * len(events))
        safety_status = "WARNING" if len(events) > 0 else "EXCELLENT"
    first_ts = events[0]['timestamp'] if events else datetime.now(timezone.utc).timestamp()
    day = datetime.fromtimestamp(first_ts, tz=timezone.utc).strftime("%Y-%m-%d")

    daily_score = {
        "truck_day_summary": {
            "date": day,
            "truck_id": TRUCK_ID,
            "safety_score": safety_score,
            "total_harsh_braking_events": len(events),
            "safety_status": safety_status,
            "detected_events": events
        }
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "daily_score.json", "w") as f:
        json.dump(daily_score, f, indent=4)
    print("Fichier 'daily_score.json' généré avec succès.\n")
    print("--- FIN ANALYSE MODULE 2 ---\n")