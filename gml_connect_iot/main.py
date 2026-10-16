import csv
import json
from pathlib import Path

from src.zfe_module import run_zfe_module
from src.safety_module import run_safety_module

####################################################################
    ## TESTS GESTION ERREUR AVEC FICHIERS CORROMPUS :
    # Pour run zfe module :
        # Remplacer la variable "truck_gps" :
            # par "corrupted_truck_gps" pour tester des éléments manquants"

    # Pour run safety module :
        ## Remplacer la variable "csv_accelerometer" :
            # par "corrupted_accelerometer_csv" pour tester des lignes mal formatées.
            # par "empty_csv" pour tester un fichier vide.


if __name__ == "__main__":
    lyon_polygon = Path("data/lyon_polygon.json")

    truck_gps = Path("data/truck_gps.json")
    # corrupted_truck_gps = Path("data/corrupted_truck_gps.json")

    csv_accelerometer = "data/accelerometer_data.csv"
    # corrupted_accelerometer_csv = "data/corrupted_accelerometer_data.csv"
    # empty_csv = "data/empty_csv.csv"

#####################################################################
    # RUN ZFE MODULE :
    try:
        with open(lyon_polygon, "r", encoding="utf-8") as f:
            file_lyon_polygon = json.load(f)
        ## remplacer la variable truck_gps ici
        with open(truck_gps,"r", encoding="utf-8") as f:
            file_truck_gps = json.load(f)
        run_zfe_module(file_lyon_polygon, file_truck_gps)

    except FileNotFoundError as e:
        print(f"[ERREUR] Fichier introuvable : {e.filename}\n")
    except json.JSONDecodeError as e:
        print(f"[ERREUR] JSON invalide : {e}\n")

#####################################################################
    # RUN SAFETY MODULE :
    try:
        ## remplacer la variable csv_accelerometer ici
        with open(csv_accelerometer, encoding='utf-8', errors="ignore") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            run_safety_module(reader)

    except FileNotFoundError as e:
        print(f"[ERREUR] Fichier introuvable : {e.filename}\n")
    except json.JSONDecodeError as e:
        print(f"[ERREUR] JSON invalide : {e}\n")
