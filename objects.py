"""Placement des objets sur le terrain (pièces et obstacles).

Entrée : la liste `heights` produite par generator.generate_heights()
         (une hauteur par colonne, 0 = trou).
Sortie : une liste d'objets, chaque objet étant un dictionnaire
         {"type": "coin" | "enemy" | "spike", "x": colonne, "y": ligne}
         où y est compté depuis le bas (y = 0 est la ligne du bas).
         Un objet posé sur une colonne de hauteur h est donc en y = h.
"""

import random

# --- Types d'objets ---
COIN = "coin"      # pièce à ramasser
ENEMY = "enemy"    # ennemi qui marche sur le sol
SPIKE = "spike"    # piques (obstacle fixe)

OBSTACLES = (ENEMY, SPIKE)

# --- Paramètres ---
LEVEL_ROWS = 8             # nombre de lignes du niveau (même valeur que display.py)
JUMP_HEIGHT = 3            # hauteur max qu'un joueur peut atteindre en sautant
SAFE_START = 3             # colonnes sans obstacle au début
SAFE_END = 3               # colonnes sans obstacle à la fin
MIN_OBSTACLE_SPACING = 4   # distance min entre deux obstacles
ENEMY_PROBABILITY = 0.12
SPIKE_PROBABILITY = 0.08
COIN_ROW_PROBABILITY = 0.15
COIN_OVER_GAP_PROBABILITY = 0.6


# ---------------------------------------------------------------------------
# Fonctions utiles
# ---------------------------------------------------------------------------

def is_flat(heights, x):
    """Vrai si la colonne x et ses deux voisines ont la même hauteur (> 0).
    Un obstacle n'est posé que sur du sol plat : jamais au bord d'un trou
    ni au pied d'une marche, sinon il serait impossible à éviter."""
    if x <= 0 or x >= len(heights) - 1:
        return False
    h = heights[x]
    return h > 0 and heights[x - 1] == h and heights[x + 1] == h


def far_from_obstacles(objects, x):
    """Vrai si aucun obstacle n'est à moins de MIN_OBSTACLE_SPACING colonnes."""
    return all(abs(o["x"] - x) >= MIN_OBSTACLE_SPACING
               for o in objects if o["type"] in OBSTACLES)


def is_free(objects, x, y):
    """Vrai si aucune autre objet n'occupe déjà la case (x, y)."""
    return all(not (o["x"] == x and o["y"] == y) for o in objects)


# ---------------------------------------------------------------------------
# Placement
# ---------------------------------------------------------------------------

def place_obstacles(heights, objects, rng):
    width = len(heights)
    for x in range(SAFE_START, width - SAFE_END):
        if not is_flat(heights, x) or not far_from_obstacles(objects, x):
            continue
        r = rng.random()
        if r < SPIKE_PROBABILITY:
            objects.append({"type": SPIKE, "x": x, "y": heights[x]})
        elif r < SPIKE_PROBABILITY + ENEMY_PROBABILITY:
            objects.append({"type": ENEMY, "x": x, "y": heights[x]})


def place_coins(heights, objects, rng):
    width = len(heights)
    x = 1
    while x < width - 1:
        # 1. pièces au-dessus d'un trou : elles récompensent le saut
        if heights[x] == 0 and heights[x - 1] > 0:
            if rng.random() < COIN_OVER_GAP_PROBABILITY:
                gap_end = x
                while gap_end < width and heights[gap_end] == 0:
                    gap_end += 1
                y = min(heights[x - 1] + 2, LEVEL_ROWS - 1)
                for cx in range(x, gap_end):
                    objects.append({"type": COIN, "x": cx, "y": y})
                x = gap_end
                continue

        # 2. petite rangée de pièces au-dessus du sol (accessible en sautant)
        if heights[x] > 0 and rng.random() < COIN_ROW_PROBABILITY:
            length = rng.randint(2, 4)
            offset = rng.randint(1, 2)  # 1 = on la ramasse en marchant, 2 = en sautant
            for cx in range(x, min(x + length, width - 1)):
                if heights[cx] == 0:
                    break
                y = heights[cx] + offset
                if y < LEVEL_ROWS and is_free(objects, cx, y):
                    objects.append({"type": COIN, "x": cx, "y": y})
            x += length + 2
            continue
        x += 1


def place_objects(heights, seed=None):
    """Renvoie la liste des objets placés sur le terrain."""
    rng = random.Random(seed)
    objects = []
    place_obstacles(heights, objects, rng)  # obstacles d'abord...
    place_coins(heights, objects, rng)      # ...puis pièces dans les cases libres
    return objects


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_objects(heights, objects):
    """Vérifie que les objets respectent les règles de placement.
    Renvoie (True, []) si tout est bon, sinon (False, liste des erreurs)."""
    errors = []
    width = len(heights)
    obstacles = sorted((o for o in objects if o["type"] in OBSTACLES), key=lambda o: o["x"])

    for o in objects:
        x, y = o["x"], o["y"]
        if not (0 <= x < width and 0 <= y < LEVEL_ROWS):
            errors.append(f"{o['type']} en dehors du niveau ({x}, {y})")
            continue
        if heights[x] > y:
            errors.append(f"{o['type']} dans le sol ({x}, {y})")

        if o["type"] in OBSTACLES:
            if heights[x] == 0 or y != heights[x]:
                errors.append(f"{o['type']} pas posé sur le sol ({x}, {y})")
            if x < SAFE_START or x >= width - SAFE_END:
                errors.append(f"{o['type']} dans la zone de départ/arrivée ({x})")
            if not is_flat(heights, x):
                errors.append(f"{o['type']} au bord d'un trou ou d'une marche ({x})")

        if o["type"] == COIN:
            # la pièce doit être atteignable depuis le sol le plus proche
            nearby = [h for h in heights[max(0, x - 2):x + 3] if h > 0]
            if not nearby or y - max(nearby) > JUMP_HEIGHT:
                errors.append(f"pièce inaccessible ({x}, {y})")

    for a, b in zip(obstacles, obstacles[1:]):
        if b["x"] - a["x"] < MIN_OBSTACLE_SPACING:
            errors.append(f"obstacles trop proches ({a['x']} et {b['x']})")

    positions = [(o["x"], o["y"]) for o in objects]
    if len(positions) != len(set(positions)):
        errors.append("deux objets sur la même case")

    return len(errors) == 0, errors
