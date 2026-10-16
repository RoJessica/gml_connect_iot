TRUCK_ID = "GML-001"

# =====================================================================
# MODULE 1 : ZFE (Geo) - Ray Casting & Bounding Box Optimization
# =====================================================================

def get_bounding_box(polygon):
    """Calcule la Bounding Box du polygone."""
    lats = [pt["lat"] for pt in polygon]
    lons = [pt["lon"] for pt in polygon]

    return {
        "min_lat": min(lats),
        "max_lat": max(lats),
        "min_lon": min(lons),
        "max_lon": max(lons),
    }

def is_point_in_bounding_box(lat, lon, bbox):
    """Vérification rapide si le point est dans la bounding box"""
    return bbox["min_lat"] <= lat <= bbox["max_lat"] and bbox["min_lon"] <= lon <= bbox["max_lon"]


def is_point_in_polygon(lat, lon, polygon):
    """Algorithme de Ray Casting (Point in Polygon)"""
    inside = False
    nb_polygon = len(polygon)
    p1x = polygon[0]["lon"]
    p1y = polygon[0]["lat"]

    # Boucle pour passer tous les côtés du polygone => chaque côté va du point p1 au point p2.
    # Le modulo (%) permet de revenir au premier point après le dernier,
    # pour fermer le polygone (dans le cas où le fichier JSON ne le fait pas).

    for i in range(nb_polygon + 1):
        p2x = polygon[i % nb_polygon]["lon"]
        p2y = polygon[i % nb_polygon]["lat"]
        # vérification si longitude comprise entre p1 et p2
            # => sinon rayon vertical, ne croisera jamais le segment
        # vérification si latitude est inférieure ou égale à p1 et p2 (point le plus haut du polygone)
            # => sinon rayon ne touchera jamais le segment
        # le côté vertical (px1 == px2) est écarté ici car l'intervalle de longitude est vide
        # donc lat_intersection n'est calculée que quand la division est possible
        if min(p1x, p2x) < lon <= max(p1x, p2x) and lat <= max(p1y, p2y):
            if p1x != p2x:
                # calcul intersection où le rayon vertical croise le segment
                lat_intersection = (lon - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
            # si latitude du point est inférieure à la latitude d'intersection => rayon croise le bord du polygone
            if p1y == p2y or lat <= lat_intersection:
                # inversion de l'état de inside => False ou True en fonction de l'état de base
                inside = not inside
        # passage au point suivant
        p1x, p1y = p2x, p2y
    # Renvoi de la valeur de inside pour la suite du code
    return inside

def run_zfe_module(polygon_data, truck_gps_data):
    print("--- DÉBUT ANALYSE MODULE 1 : ZFE (Geo) ---\n")
    bbox = get_bounding_box(polygon_data)

    for point in truck_gps_data:
        try:
            lat = point["lat"]
            lon = point["lon"]
            ts = point["timestamp"]
            point_id = point["id"]
        except (KeyError, TypeError, ValueError) as e:
            print(f"[ERREUR] Point GPS invalide ignoré : {point} ({e})\n")
            continue

        # Optimisation Bounding Box
        if not is_point_in_bounding_box(lat, lon, bbox):
            # Le point est loin en dehors
            status = "OUT (Filtre Box)"
        else:
            # Le point est proche ou dedans, on vérifie précisément via Ray Casting
            if is_point_in_polygon(lat, lon, polygon_data):
                status = "IN"
                print(f"[{ts}] [ALERT ZFE] Le camion {TRUCK_ID} est entré dans la zone réglementée ! (point {point_id}, {lat}, {lon})\n")
            else:
                status = "OUT"

        print(f"Point {point_id} ({ts}) -> Attendu: {point['expected']} | Calculé: {status} \n")

    print("--- FIN ANALYSE MODULE 1 ---\n")
