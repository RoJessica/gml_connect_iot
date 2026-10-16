# GML-Connect IoT POC - Procédure de Test Local

Ce dépôt contient le code source du POC pour le traitement télématique embarqué.

### Prérequis
- Python 3.10 (ou supérieur) installé sur la machine de test.
- Aucune dépendance externe (bibliothèque standard uniquement)

Le moteur ne contacte aucun service distant pour la détection de la zone.

### Exécution du Test
1. Clonez ce dépôt (gml_connect_iot) ou copiez le dossier complet.
2. Ouvrez un terminal à la racine du dépôt (le dossier contenant le fichier main.py).
3. Exécutez la commande suivante :
   ```bash
   python main.py
   ```

### Résultats attendus
1. Module ZFE : pour chaque point GPS, la console affiche le statut attendu et le statut calculé.
- Points 1 et 2 : OUT (Filtre Box), rejetés par la Bounding Box sans lancer le Ray Casting.
- Point 3 : OUT. Le fichier l'annonce "IN (Bordure)", mais ce point est dans le rectangle englobant et hors du polygone : à sa latitude (45.785), la ZFE ne commence qu'à environ 4.83 de longitude. La Bounding Box seule aurait déclenché une fausse alerte. Le Ray Casting la corrige.
- Points 4 et 5 : IN, avec le log [ALERT ZFE].
2. Un log [ALERT SAFETY] doit s'afficher avec l'évènement du freinage violent du point avec l'id 6 du fichier "accelerometer_data.csv" (valeur -3.45 m/s²).
3. Un fichier "daily_score.json" doit être généré dans le dossier "output/" sans aucun plantage du script.

### Format de sortie
Le fichier 'daily_score.json' contient les évènements enregistrés par le module Safety.

```
{
    "truck_day_summary": {
        "date": date de la journée de conduite évaluée,
        "truck_id": id du camion,
        "safety_score": 100 - 10 x nombre d'évènements avec minimum à 0 ou null si aucune donnée exploitable
        "total_harsh_braking_events": nombre de freinages violents total,
        "safety_status": EXCELLENT (aucun évènement), WARNING (au moins un) ou NO_DATA (fichier vide),
        "detected_events": [ => détails des évènements détectés
            {
                "timestamp": horodatage de l'évènement,
                "event_type": type d'évènement,
                "value_ms2": accélération en m/s²,
                "severity": sévérité de l'évènement
            }
        ]
    }
}
```

Exemple de contenu du fichier avec l'enregistrement d'un freinage violent :
```
{
    "truck_day_summary": {
        "date": "2023-03-15",
        "truck_id": "GML-001",
        "safety_score": 90,
        "total_harsh_braking_events": 1,
        "safety_status": "WARNING",
        "detected_events": [
            {
                "timestamp": 1678880005,
                "event_type": "Harsh Braking",
                "value_ms2": -3.45,
                "severity": "CRITICAL"
            }
        ]
    }
}
```

### Test de robustesse
Pour tester un fichier corrompu, remplacez dans 'main.py' le chemin du fichier par celui indiqué ci-dessous (les chemins sont rappelés en commentaire dans 'main.py') :

- Module Safety :

Pour vérifier que le script ne plante pas, vous pouvez tester avec le fichier "corrupted_accelerometer_data.csv" qui contient une ligne additionnelle avec des valeurs corrompues (1678880010,0.12,abc,9.81)

Le script affiche un message d'erreur de parsing pour cette ligne et poursuit l'analyse.

Pour tester que le script ne plante pas avec un fichier CSV vide, vous pouvez utiliser le fichier "empty_csv.csv".

Le résultat pour un fichier CSV vide affiche un message d'erreur en console et le safety_score du fichier daily_score.json est généré à null, le safety_status est généré à NO_DATA.

- Module ZFE :

Pour tester que le script ne plante pas avec un fichier JSON avec des données invalides, vous pouvez utiliser le fichier "corrupted_truck_gps.json" qui contient une ligne avec la longitude manquante (le point avec l'id 2) ainsi qu'une ligne additionnelle avec des valeurs corrompues ("lat" manquant au point avec l'id 6).

Un fichier de données absent ou un JSON mal formé est également signalé sans arrêt brutal du script.