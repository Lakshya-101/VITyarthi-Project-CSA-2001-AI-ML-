import random
from algorithms import dfs, bfs, greedy_bfs, astar


WORD_LIST_4 = [
    "cold", "cord", "core", "care", "bare", "dare", "date", "gate", "late", "lake",
    "like", "bike", "bite", "site", "sire", "fire", "fine", "line", "lane", "cane",
    "came", "game", "name", "same", "sale", "tale", "tale", "pale", "pile", "mile",
    "mild", "wind", "will", "fill", "fall", "ball", "bell", "belt", "melt", "felt",
    "feel", "feet", "feed", "seed", "weed", "weed", "need", "heed", "head", "heat",
    "heap", "reap", "read", "lead", "dead", "deal", "seal", "real", "reel", "heel",
    "peel", "peel", "feel", "fell", "tell", "tall", "talk", "walk", "wall", "hall",
    "call", "mall", "mail", "sail", "tail", "toil", "toll", "told", "bold", "gold",
    "sold", "sole", "role", "rose", "cake", "note", "vote", "vole", "hole", "pole",
    "pale", "male", "tale", "time", "lime", "life", "wife", "wise", "rise", "rice",
    "race", "lace", "face", "fact", "fast", "last", "list", "fist", "fish", "dish",
    "wish", "wash", "cash", "gash", "lash", "lust", "just", "gust", "gush", "bush",
    "rush", "ruse", "fuse", "muse", "mute", "lute", "cute", "cure", "pure", "sure",
    "sore", "bore", "bone", "tone", "tune", "dune", "done", "gone", "cone", "coke",
    "joke", "poke", "pole", "mole", "more", "mare", "made", "fade", "fame", "came",
    "warm", "farm", "harm", "hard", "card", "cart", "dart", "dark", "bark", "park",
    "part", "mart", "mark", "mars", "bars", "cars", "jars", "jabs", "cabs", "dabs",
    "dabs", "labs", "lads", "lark", "lady", "lazy", "hazy", "haze", "maze", "made",
    "wade", "wade", "wide", "hide", "hand", "hire", "here", "herd", "bird", "bind",
    "find", "kind", "king", "ring", "sing", "sink", "link", "lint", "hint", "mint",
    "mink", "wink", "wine", "vine", "dine", "pine", "mine", "nine", "nice", "dice",
    "mice", "lice", "vice", "vibe", "jibe", "jive", "give", "live", "love", "dove",
    "cove", "code", "mode", "node", "nose", "note", "tome", "home", "dome", "dose",
    "lose", "lore", "wore", "word", "ward", "warm", "worm", "form", "fork", "fore",
    "gore", "gorge", "lore", "band", "beat", "lord", "load", "road", "toad", "loan",
    "moan", "moon", "noon", "boon", "book", "cook", "cool", "fool", "pool", "poll",
    "pull", "bull", "full", "hull", "hill", "mill", "kill", "bill", "pill", "till",
    "tile", "file", "bile", "bite", "kite", "mite", "mate", "hate", "have", "gave",
    "cave", "rave", "rove", "rode", "rope", "ripe", "pipe", "wipe", "wise", "bite",
]

WORD_SET = set(WORD_LIST_4)

WORD_PAIRS = [
    ("cold", "warm"),
    ("head", "tail"),
    ("lead", "gold"),
    ("fire", "wind"),
    ("dark", "lark"),
    ("fast", "last"),
    ("love", "hate"),
    ("word", "ward"),
    ("hand", "band"),
    ("time", "lime"),
    ("bike", "like"),
    ("rose", "nose"),
    ("cake", "lake"),
    ("beat", "heat"),
    ("ball", "bell"),
    ("gate", "late"),
    ("mile", "mild"),
    ("seed", "weed"),
    ("call", "mall"),
    ("sole", "role"),
]


def get_neighbors_word(word):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                new_word = word[:i] + c + word[i+1:]
                if new_word in WORD_SET:
                    neighbors.append(new_word)
    return neighbors


def word_heuristic(word, goal):
    return sum(1 for a, b in zip(word, goal) if a != b)


def generate_random_word_pair():
    valid_pairs = []
    for start, end in WORD_PAIRS:
        if start in WORD_SET and end in WORD_SET:
            valid_pairs.append((start, end))
    if valid_pairs:
        return random.choice(valid_pairs)
    return ("cold", "warm")


def solve_word_ladder(start, goal, algorithm="A*"):
    goal_test = lambda w: w == goal
    get_neighbors = get_neighbors_word
    heuristic = lambda w: word_heuristic(w, goal)

    algo_map = {
        "DFS": lambda s, gt, gn, h: dfs(s, gt, gn, h, max_depth=30),
        "BFS": bfs,
        "Greedy Best-First": greedy_bfs,
        "A*": astar,
    }
    fn = algo_map[algorithm]
    return fn(start, goal_test, get_neighbors, heuristic)