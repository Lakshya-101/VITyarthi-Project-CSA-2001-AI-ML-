# 🧠 AI Search Strategy Visualizer

An interactive web application that demonstrates and compares four classic AI search algorithms across four different puzzle domains — built as a study aid to showcase how algorithm effectiveness varies with problem structure.

---

## 📖 Overview

This project provides a hands-on, visual way to understand the trade-offs between uninformed and informed search strategies. For each puzzle, you can run multiple algorithms simultaneously and compare their performance across three key metrics: **time taken**, **nodes explored**, and **solution depth**.

The core insight the app is designed to teach: *there is no universally best search algorithm* — the right choice depends on the problem's branching factor, solution depth, and whether a good heuristic is available.

---

## ✨ Features

- **4 Puzzle Domains** — each with configurable difficulty and random puzzle generation
- **4 Search Algorithms** — DFS, BFS, Greedy Best-First, and A*
- **Side-by-side comparison charts** — bar charts for time (ms), nodes explored, and solution depth
- **Winner detection** — automatically scores and highlights the best-performing algorithm
- **Real-time progress indicators** — watch algorithms solve puzzles live
- **Dark-themed UI** — built with custom CSS on top of Streamlit

---

## 🧩 Puzzle Domains

### 🎯 8-Puzzle
The classic sliding tile puzzle on a 3×3 grid. The goal is to reach the ordered state `[1,2,3,4,5,6,7,8,_]` from a scrambled configuration.

- **Heuristic:** Manhattan distance (sum of tile displacements from goal positions)
- **Difficulty levels:** Easy (10 moves), Medium (25 moves), Hard (50 moves)
- **Note:** DFS is depth-limited to 50 to prevent runaway exploration

### 🔤 Word Ladder
Transform one 4-letter word into another by changing a single letter at a time, where every intermediate word must be a valid dictionary word.

- **Heuristic:** Hamming distance (number of character positions that differ from the goal word)
- **Word pairs:** 20 curated pairs (e.g., `cold → warm`, `love → hate`, `lead → gold`)
- **Custom input:** Enter your own start and end words

### 🗺️ Maze
Navigate from the top-left to the bottom-right of a procedurally generated maze.

- **Maze generation:** Recursive backtracking (depth-first carving)
- **Heuristic:** Manhattan distance to the exit cell
- **Configurable size:** 11×11 up to 31×31
- **Visualization:** Color-coded path overlay on the solved maze

### 🔢 Sudoku
Fill a 9×9 grid so every row, column, and 3×3 box contains digits 1–9.

- **Heuristic:** MRV (Minimum Remaining Values) — prefers filling cells with the fewest valid candidates
- **Difficulty levels:** Easy (30 removed cells), Medium (45), Hard (55)
- **Note:** BFS is memory-capped at 50,000 nodes for Sudoku due to the enormous branching factor

---

## 🔍 Search Algorithms

| Algorithm | Type | Optimal? | Complete? | Best For |
|---|---|---|---|---|
| **DFS** | Uninformed | ❌ | ❌ (depth-limited) | Memory-constrained spaces |
| **BFS** | Uninformed | ✅ | ✅ | Shallow solutions, small state spaces |
| **Greedy Best-First** | Informed | ❌ | ❌ | Speed when a good heuristic exists |
| **A\*** | Informed | ✅ | ✅ | Optimal solutions with a good heuristic |

All four algorithms share a unified interface defined in `algorithms.py` via the `SearchResult` object, which standardizes how results are returned across all puzzle types.

---

## 🏗️ Project Structure

```
.
├── app.py              # Streamlit UI — pages, charts, layout, and session state
├── algorithms.py       # Core search implementations: DFS, BFS, Greedy BFS, A*
├── puzzle_8.py         # 8-puzzle logic: state generation, neighbors, heuristics
├── maze.py             # Maze generation (recursive backtracking) and solver
├── sudoku.py           # Sudoku generation, validation, and algorithm variants
├── word_ladder.py      # Word graph, word pairs, and ladder solver
└── requirements.txt    # Python dependencies
```

### Key Design Decisions

- **Unified algorithm interface:** Every puzzle calls algorithms with the same `(start, goal_test, get_neighbors, heuristic)` signature, making it easy to plug in new puzzles or algorithms.
- **`SearchResult` object:** A shared result container (`solution`, `path`, `nodes_explored`, `time_taken`, `solution_depth`, `success`) normalizes output across all solvers.
- **Puzzle-specific algorithm wrappers:** Sudoku's fundamentally different state space (9×9 boards) requires custom DFS/BFS/Greedy/A* implementations in `sudoku.py`, while the other three puzzles use the generic implementations from `algorithms.py` directly.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/Lakshya-101/VITyarthi-Project-CSA-2001-AI-ML-.git
cd aisearchapp

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📦 Dependencies

```
streamlit>=1.28.0
matplotlib>=3.7.0
numpy>=1.24.0
```

---

## 📊 Metrics & Winner Scoring

Each algorithm is scored after solving using a composite formula:

```
score = (time_ms) + (nodes_explored × 0.01) + (solution_depth × 0.1)
```

The algorithm with the lowest score is declared the winner. This balances raw speed, search efficiency, and solution quality.

---

## 🎓 Learning Outcomes

After using this tool, you should be able to observe:

- **DFS** tends to find solutions quickly in deep search spaces but sacrifices optimality
- **BFS** guarantees the shortest path but can explode in memory for problems with high branching factors (like Sudoku)
- **Greedy Best-First** is fast when the heuristic is well-aligned with the problem but can get stuck in local optima
- **A\*** consistently finds optimal solutions at the cost of more memory, outperforming Greedy when solution paths are complex

---

## 🛠️ Extending the Project

To add a new puzzle:
1. Create a module with `generate_<puzzle>()` and `solve_<puzzle>(state, algorithm)` functions
2. Define `get_neighbors`, `goal_test`, and optionally a `heuristic` function
3. Import and wire up a new tab in `app.py`
4. Reuse the existing `render_comparison_chart()` and `show_winner()` helpers

To add a new algorithm:
1. Implement it in `algorithms.py` with the signature `(start, goal_test, get_neighbors, heuristic) → SearchResult`
2. Add it to the `ALGORITHMS` dict and `ALGO_NAMES` list in `app.py`

---

## 📸 UI Highlights

- Dark theme with a navy/slate color palette
- Algorithm color coding: 🔴 DFS · 🔵 BFS · 🟡 Greedy · 🟢 A*
- Matplotlib charts styled to match the dark UI
- Sidebar with algorithm descriptions and legend
- Per-algorithm metric cards with color-coded borders

---

*Built with Python · Streamlit · Matplotlib*
