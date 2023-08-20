from bidict import bidict

actions = [
    ("h", 0),  # LEFT
    ("h", 1),  # RIGHT
    ("v", 0),  # DOWN
    ("v", 1),  # UP
    ("s", 0),  # DOWN
    ("s", 1),  # UP
]

moves = {
    "U": ("h", 0, 0),
    "U'": ("h", 1, 0),
    "D": ("h", 1, 2),
    "D'": ("h", 0, 2),
    "R": ("v", 1, 2),
    "R'": ("v", 0, 2),
    "L": ("v", 0, 0),
    "L'": ("v", 1, 0),
    "F": ("s", 1, 2),
    "F'": ("s", 0, 2),
    "B": ("s", 0, 0),
    "B'": ("s", 1, 0),
}

faces = {
    "U": "⬜",
    "⬜": "U",
    "L": "🟧",
    "🟧": "L",
    "F": "🟩",
    "🟩": "F",
    "R": "🟥",
    "🟥": "R",
    "B": "🟦",
    "🟦": "B",
    "D": "🟨",
    "🟨": "D"
}



def annotation_to_move(annotation):
    m = []
    if "2" in annotation:
        m.append(moves[annotation[0]])
        m.append(moves[annotation[0]])
    else:
        m.append(moves[annotation])
    return m
