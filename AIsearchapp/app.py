import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import numpy as np
import random
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from puzzle_8 import (generate_random_puzzle, solve_8puzzle, state_to_grid,
                       GOAL_STATE, manhattan_distance)
from word_ladder import generate_random_word_pair, solve_word_ladder, WORD_SET, WORD_PAIRS
from maze import generate_maze, solve_maze
from sudoku import generate_sudoku, solve_sudoku

#Page Config 
st.set_page_config(
    page_title="AI Search Visualizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Developed Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .main-header h1 {
        color: #e2e8f0;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin: 0.5rem 0 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    .metric-card .label { color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-card .value { color: #f1f5f9; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; }
    .metric-card .sub   { color: #64748b; font-size: 0.75rem; margin-top: 2px; }

    .algo-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    .winner-box {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #d1fae5;
        font-weight: 600;
    }
    .puzzle-cell {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px; height: 52px;
        font-size: 1.4rem;
        font-weight: 700;
        border-radius: 8px;
        margin: 2px;
    }
    .section-header {
        color: #e2e8f0;
        font-size: 1.3rem;
        font-weight: 700;
        border-left: 4px solid #3b82f6;
        padding-left: 12px;
        margin: 1.5rem 0 1rem;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown { color: #cbd5e1; }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

#Helpers
ALGO_COLORS = {
    "DFS":              "#ef4444",
    "BFS":              "#3b82f6",
    "Greedy Best-First":"#f59e0b",
    "A*":               "#10b981",
}
ALGO_NAMES = ["DFS", "BFS", "Greedy Best-First", "A*"]


def metric_card(label, value, sub=""):
    return f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="sub">{sub}</div>
    </div>"""


def render_comparison_chart(results: dict, title="Algorithm Comparison"):
    algos = [a for a, r in results.items() if r and r.success]
    if not algos:
        st.warning("No algorithm found a solution.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.patch.set_facecolor('#0f172a')
    for ax in axes:
        ax.set_facecolor('#1e293b')
        ax.spines['bottom'].set_color('#334155')
        ax.spines['top'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['right'].set_color('#334155')
        ax.tick_params(colors='#94a3b8', labelsize=9)
        ax.yaxis.label.set_color('#94a3b8')

    colors = [ALGO_COLORS[a] for a in algos]

    # Time
    times = [results[a].time_taken * 1000 for a in algos]
    bars = axes[0].bar(algos, times, color=colors, edgecolor='#0f172a', linewidth=1.5, width=0.6)
    axes[0].set_title("Time (ms)", color='#e2e8f0', fontweight='bold', pad=10)
    for bar, val in zip(bars, times):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(times)*0.02,
                     f'{val:.1f}', ha='center', va='bottom', color='#f1f5f9', fontsize=8, fontweight='600')

    # Nodes
    nodes = [results[a].nodes_explored for a in algos]
    bars = axes[1].bar(algos, nodes, color=colors, edgecolor='#0f172a', linewidth=1.5, width=0.6)
    axes[1].set_title("Nodes Explored", color='#e2e8f0', fontweight='bold', pad=10)
    for bar, val in zip(bars, nodes):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(nodes)*0.02,
                     f'{val:,}', ha='center', va='bottom', color='#f1f5f9', fontsize=8, fontweight='600')

    # Depth
    depths = [results[a].solution_depth for a in algos]
    bars = axes[2].bar(algos, depths, color=colors, edgecolor='#0f172a', linewidth=1.5, width=0.6)
    axes[2].set_title("Solution Depth", color='#e2e8f0', fontweight='bold', pad=10)
    for bar, val in zip(bars, depths):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(depths, default=1)*0.02,
                     f'{val}', ha='center', va='bottom', color='#f1f5f9', fontsize=8, fontweight='600')

    for ax in axes:
        ax.set_xticklabels(algos, rotation=15, ha='right', fontsize=8.5)
    fig.suptitle(title, color='#e2e8f0', fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def find_winner(results):
    best_algo = None
    best_score = float('inf')
    for algo, r in results.items():
        if r and r.success:
            # Score: normalize time + nodes + depth
            score = r.time_taken * 1000 + r.nodes_explored * 0.01 + r.solution_depth * 0.1
            if score < best_score:
                best_score = score
                best_algo = algo
    return best_algo


def show_winner(results):
    winner = find_winner(results)
    if winner:
        r = results[winner]
        color = ALGO_COLORS[winner]
        st.markdown(f"""
        <div class="winner-box">
            🏆 Most Effective: <span style="color:{color}; font-size:1.1em">{winner}</span>
            — {r.time_taken*1000:.2f} ms &nbsp;|&nbsp; {r.nodes_explored:,} nodes 
            &nbsp;|&nbsp; depth {r.solution_depth}
        </div>""", unsafe_allow_html=True)


# 8-PUZZLE
def render_8puzzle_grid(state, title="", highlight_path=None):
    goal = GOAL_STATE
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    ax.set_xlim(-0.1, 3.1); ax.set_ylim(-0.1, 3.1)
    ax.set_aspect('equal'); ax.axis('off')
    if title:
        ax.set_title(title, color='#e2e8f0', fontsize=11, fontweight='bold', pad=8)

    for i, val in enumerate(state):
        r, c = divmod(i, 3)
        y = 2 - r
        if val == 0:
            color = '#1e293b'
            ec = '#334155'
            tc = '#334155'
        elif val == goal[i]:
            color = '#064e3b'
            ec = '#10b981'
            tc = '#d1fae5'
        else:
            color = '#1e3a5f'
            ec = '#3b82f6'
            tc = '#bfdbfe'

        rect = mpatches.FancyBboxPatch((c + 0.08, y + 0.08), 0.84, 0.84,
                                        boxstyle="round,pad=0.05",
                                        facecolor=color, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        if val != 0:
            ax.text(c + 0.5, y + 0.5, str(val), ha='center', va='center',
                    color=tc, fontsize=20, fontweight='bold')
    plt.tight_layout(pad=0.3)
    return fig


def page_8puzzle():
    st.markdown('<div class="section-header">🎯 8-Puzzle Problem</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94a3b8; margin-bottom:1.5rem;">
    Slide tiles on a 3×3 grid to reach the goal state <b style="color:#10b981">[1,2,3,4,5,6,7,8,_]</b>.
    Each algorithm explores states differently — watch how their efficiency compares.
    </p>""", unsafe_allow_html=True)

    col_ctrl, col_main = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown("#### ⚙️ Configuration")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="p8_diff")
        selected_algos = st.multiselect("Algorithms", ALGO_NAMES,
                                         default=["BFS", "A*", "Greedy Best-First"],
                                         key="p8_algos")
        if st.button("🎲 Generate Puzzle", key="p8_gen"):
            st.session_state.p8_state = generate_random_puzzle(difficulty)
            st.session_state.p8_results = {}

        if "p8_state" not in st.session_state:
            st.session_state.p8_state = generate_random_puzzle("Medium")
            st.session_state.p8_results = {}

        if st.button("▶️ Solve All", key="p8_solve"):
            if not selected_algos:
                st.error("Select at least one algorithm.")
            else:
                results = {}
                prog = st.progress(0)
                for i, algo in enumerate(selected_algos):
                    with st.spinner(f"Running {algo}…"):
                        results[algo] = solve_8puzzle(st.session_state.p8_state, algo)
                    prog.progress((i + 1) / len(selected_algos))
                st.session_state.p8_results = results
                prog.empty()

    with col_main:
        state = st.session_state.get("p8_state", GOAL_STATE)
        results = st.session_state.get("p8_results", {})

        # Show initial and goal state
        c1, c2 = st.columns(2)
        with c1:
            fig = render_8puzzle_grid(state, "Initial State")
            st.pyplot(fig, use_container_width=False)
            plt.close()
        with c2:
            fig = render_8puzzle_grid(GOAL_STATE, "Goal State")
            st.pyplot(fig, use_container_width=False)
            plt.close()

        if results:
            st.markdown("---")
            # Metrics row
            cols = st.columns(len(results))
            for i, (algo, r) in enumerate(results.items()):
                with cols[i]:
                    color = ALGO_COLORS.get(algo, "#64748b")
                    status = "✅" if r and r.success else "❌"
                    t = f"{r.time_taken*1000:.1f}" if r else "—"
                    n = f"{r.nodes_explored:,}" if r else "—"
                    d = f"{r.solution_depth}" if r and r.success else "—"
                    st.markdown(f"""
                    <div class="metric-card" style="border-color:{color}40">
                        <div class="label" style="color:{color}">{algo} {status}</div>
                        <div class="value">{t}<span style="font-size:0.7em;color:#64748b">ms</span></div>
                        <div class="sub">{n} nodes · depth {d}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            render_comparison_chart(results, "8-Puzzle: Algorithm Comparison")
            show_winner(results)

            # Show solution path for best algorithm
            winner = find_winner(results)
            if winner and results[winner].success:
                with st.expander(f"📍 Solution Path ({winner}) — {results[winner].solution_depth} moves"):
                    path = results[winner].path
                    cols_path = st.columns(min(len(path), 8))
                    for i, (state_step, col) in enumerate(zip(path[:8], cols_path)):
                        with col:
                            fig = render_8puzzle_grid(state_step, f"Step {i}")
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                    if len(path) > 8:
                        st.info(f"… {len(path)-8} more steps (showing first 8)")


# WORD LADDER

def page_word_ladder():
    st.markdown('<div class="section-header">🔤 Word Ladder Problem</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94a3b8; margin-bottom:1.5rem;">
    Transform one word into another by changing one letter at a time.
    Each intermediate word must be a valid English word.
    </p>""", unsafe_allow_html=True)

    col_ctrl, col_main = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown("#### ⚙️ Configuration")
        if st.button("🎲 Random Pair", key="wl_gen"):
            start, end = generate_random_word_pair()
            st.session_state.wl_start = start
            st.session_state.wl_end = end
            st.session_state.wl_results = {}

        if "wl_start" not in st.session_state:
            st.session_state.wl_start = "cold"
            st.session_state.wl_end = "warm"
            st.session_state.wl_results = {}

        start_word = st.text_input("Start Word", value=st.session_state.wl_start, key="wl_s_in")
        end_word   = st.text_input("End Word",   value=st.session_state.wl_end,   key="wl_e_in")

        # Validate
        s_ok = start_word.lower() in WORD_SET
        e_ok = end_word.lower() in WORD_SET
        if not s_ok: st.error(f"'{start_word}' not in word list")
        if not e_ok: st.error(f"'{end_word}' not in word list")

        selected_algos = st.multiselect("Algorithms", ALGO_NAMES,
                                         default=["BFS", "A*", "Greedy Best-First"],
                                         key="wl_algos")

        if st.button("▶️ Solve All", key="wl_solve"):
            if not selected_algos:
                st.error("Select at least one algorithm.")
            elif s_ok and e_ok:
                results = {}
                prog = st.progress(0)
                for i, algo in enumerate(selected_algos):
                    with st.spinner(f"Running {algo}…"):
                        results[algo] = solve_word_ladder(
                            start_word.lower(), end_word.lower(), algo)
                    prog.progress((i + 1) / len(selected_algos))
                st.session_state.wl_results = results
                prog.empty()

    with col_main:
        results = st.session_state.get("wl_results", {})
        start_w = st.session_state.get("wl_start", "cold")
        end_w   = st.session_state.get("wl_end",   "warm")

        # Show word pair
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:1.5rem;">
            <div style="background:#1e293b;border:2px solid #3b82f6;border-radius:12px;
                        padding:16px 24px;font-size:2rem;font-weight:800;color:#bfdbfe;
                        font-family:'JetBrains Mono'">{start_w.upper()}</div>
            <div style="color:#64748b;font-size:1.5rem">→</div>
            <div style="background:#1e293b;border:2px solid #10b981;border-radius:12px;
                        padding:16px 24px;font-size:2rem;font-weight:800;color:#d1fae5;
                        font-family:'JetBrains Mono'">{end_w.upper()}</div>
        </div>""", unsafe_allow_html=True)

        if results:
            # Metrics
            cols = st.columns(len(results))
            for i, (algo, r) in enumerate(results.items()):
                with cols[i]:
                    color = ALGO_COLORS.get(algo, "#64748b")
                    status = "✅" if r and r.success else "❌"
                    t = f"{r.time_taken*1000:.1f}" if r else "—"
                    n = f"{r.nodes_explored:,}" if r else "—"
                    d = f"{r.solution_depth}" if r and r.success else "—"
                    st.markdown(f"""
                    <div class="metric-card" style="border-color:{color}40">
                        <div class="label" style="color:{color}">{algo} {status}</div>
                        <div class="value">{t}<span style="font-size:0.7em;color:#64748b">ms</span></div>
                        <div class="sub">{n} nodes · {d} steps</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            render_comparison_chart(results, "Word Ladder: Algorithm Comparison")
            show_winner(results)

            # Show solution path
            winner = find_winner(results)
            if winner and results[winner].success:
                path = results[winner].path
                st.markdown(f"#### 🪜 Ladder ({winner}) — {len(path)} words")
                # Visual ladder
                html = '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:1rem 0;">'
                for j, word in enumerate(path):
                    if j == 0:
                        bg, border, tc = "#1e3a5f", "#3b82f6", "#bfdbfe"
                    elif j == len(path) - 1:
                        bg, border, tc = "#064e3b", "#10b981", "#d1fae5"
                    else:
                        # Highlight changed letter
                        bg, border, tc = "#1e293b", "#475569", "#e2e8f0"

                    # Diff with previous
                    if j > 0:
                        prev = path[j-1]
                        letters = ""
                        for k, (a, b) in enumerate(zip(prev, word)):
                            if a != b:
                                letters += f'<span style="color:#f59e0b;font-weight:900">{b.upper()}</span>'
                            else:
                                letters += f'<span>{b.upper()}</span>'
                    else:
                        letters = word.upper()

                    html += f'''<div style="background:{bg};border:2px solid {border};
                                border-radius:10px;padding:10px 16px;font-size:1.2rem;
                                font-weight:700;color:{tc};font-family:'JetBrains Mono';
                                letter-spacing:2px">{letters}</div>'''
                    if j < len(path) - 1:
                        html += '<div style="color:#475569;font-size:1.2rem">→</div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)


# MAZE
def render_maze_fig(maze, path=None, algo_name="", explored_cells=None):
    rows, cols = len(maze), len(maze[0])
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    # Draw maze
    img = np.zeros((rows, cols, 3))
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                img[r, c] = [0.07, 0.10, 0.18]  # wall: dark blue
            else:
                img[r, c] = [0.12, 0.18, 0.30]  # path: lighter blue

    # Mark explored
    if explored_cells:
        for (er, ec) in explored_cells:
            if maze[er][ec] == 0:
                img[er, ec] = [0.18, 0.28, 0.50]

    # Mark solution path
    if path:
        for (pr, pc) in path[1:-1]:
            img[pr, pc] = [0.06, 0.40, 0.26]

    ax.imshow(img, interpolation='nearest')

    # Start / end markers
    start = (1, 1)
    end   = (rows-2, cols-2)
    ax.plot(start[1], start[0], 'o', color='#3b82f6', markersize=10, zorder=5)
    ax.plot(end[1],   end[0],   '*', color='#f59e0b', markersize=14, zorder=5)

    if path:
        py = [p[0] for p in path]
        px = [p[1] for p in path]
        color = ALGO_COLORS.get(algo_name, "#10b981")
        ax.plot(px, py, '-', color=color, linewidth=2.5, alpha=0.9, zorder=4)

    title = f"Maze — {algo_name}" if algo_name else "Maze"
    if path:
        title += f" ✅ ({len(path)-1} steps)"
    ax.set_title(title, color='#e2e8f0', fontsize=11, fontweight='bold', pad=8)
    ax.axis('off')

    # Legend
    legend_items = [
        mpatches.Patch(color='#3b82f6', label='Start'),
        mpatches.Patch(color='#f59e0b', label='End'),
    ]
    if path:
        legend_items.append(mpatches.Patch(color=ALGO_COLORS.get(algo_name, "#10b981"), label='Path'))
    ax.legend(handles=legend_items, loc='lower right', fontsize=8,
              facecolor='#1e293b', edgecolor='#334155', labelcolor='#e2e8f0')

    plt.tight_layout(pad=0.2)
    return fig


def page_maze():
    st.markdown('<div class="section-header">🗺️ Maze Searching Problem</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94a3b8; margin-bottom:1.5rem;">
    Find a path from <span style="color:#3b82f6">●Start</span> (top-left) to 
    <span style="color:#f59e0b">★End</span> (bottom-right) through the maze.
    </p>""", unsafe_allow_html=True)

    col_ctrl, col_main = st.columns([1, 3])

    with col_ctrl:
        st.markdown("#### ⚙️ Configuration")
        size = st.selectbox("Maze Size", ["Small (11×11)", "Medium (15×15)", "Large (21×21)"], index=1)
        size_map = {"Small (11×11)": 11, "Medium (15×15)": 15, "Large (21×21)": 21}
        n = size_map[size]

        if st.button("🎲 Generate Maze", key="mz_gen"):
            seed = random.randint(0, 9999)
            st.session_state.maze_data   = generate_maze(n, n, seed)
            st.session_state.maze_seed   = seed
            st.session_state.maze_size   = n
            st.session_state.maze_results = {}

        if "maze_data" not in st.session_state:
            st.session_state.maze_data   = generate_maze(n, n, 42)
            st.session_state.maze_size   = n
            st.session_state.maze_results = {}

        selected_algos = st.multiselect("Algorithms", ALGO_NAMES,
                                         default=["DFS", "BFS", "A*", "Greedy Best-First"],
                                         key="mz_algos")

        if st.button("▶️ Solve All", key="mz_solve"):
            if not selected_algos:
                st.error("Select at least one algorithm.")
            else:
                maze = st.session_state.maze_data
                sz = len(maze)
                start = (1, 1)
                end   = (sz-2, sz-2)
                results = {}
                prog = st.progress(0)
                for i, algo in enumerate(selected_algos):
                    with st.spinner(f"Running {algo}…"):
                        results[algo] = solve_maze(maze, start, end, algo)
                    prog.progress((i + 1) / len(selected_algos))
                st.session_state.maze_results = results
                prog.empty()

    with col_main:
        maze     = st.session_state.get("maze_data", generate_maze(15, 15, 42))
        results  = st.session_state.get("maze_results", {})

        if not results:
            # Show bare maze
            fig = render_maze_fig(maze, algo_name="")
            st.pyplot(fig, use_container_width=False)
            plt.close()
        else:
            # Show one maze per algorithm
            solved_algos = [a for a, r in results.items() if r and r.success]
            n_algos = len(solved_algos)
            if n_algos > 0:
                cols = st.columns(min(n_algos, 2))
                for i, algo in enumerate(solved_algos):
                    with cols[i % 2]:
                        r = results[algo]
                        fig = render_maze_fig(maze, r.path, algo)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()

            # Metrics
            if results:
                st.markdown("---")
                m_cols = st.columns(len(results))
                for i, (algo, r) in enumerate(results.items()):
                    with m_cols[i]:
                        color = ALGO_COLORS.get(algo, "#64748b")
                        status = "✅" if r and r.success else "❌"
                        t = f"{r.time_taken*1000:.2f}" if r else "—"
                        n = f"{r.nodes_explored:,}" if r else "—"
                        d = f"{r.solution_depth}" if r and r.success else "—"
                        st.markdown(f"""
                        <div class="metric-card" style="border-color:{color}40">
                            <div class="label" style="color:{color}">{algo} {status}</div>
                            <div class="value">{t}<span style="font-size:0.7em;color:#64748b">ms</span></div>
                            <div class="sub">{n} nodes · {d} steps</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                render_comparison_chart(results, "Maze: Algorithm Comparison")
                show_winner(results)



# SUDOKU
def render_sudoku(board, original=None, title=""):
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 9); ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, color='#e2e8f0', fontsize=10, fontweight='bold', pad=8)

    # Draw cells
    for r in range(9):
        for c in range(9):
            val = board[r][c] if board else 0
            orig_val = original[r][c] if original else 0

            if val == 0:
                bg = '#1e293b'
                tc = '#334155'
            elif original and orig_val != 0:
                bg = '#1e3a5f'  # given
                tc = '#93c5fd'
            else:
                bg = '#064e3b'  # solved
                tc = '#6ee7b7'

            rect = plt.Rectangle((c, 8-r), 1, 1, facecolor=bg,
                                   edgecolor='#334155', linewidth=0.5)
            ax.add_patch(rect)
            if val != 0:
                ax.text(c + 0.5, 8-r + 0.5, str(val),
                        ha='center', va='center', color=tc,
                        fontsize=13, fontweight='bold' if (original and orig_val!=0) else 'normal')

    # 3×3 box borders
    for i in range(0, 10, 3):
        lw = 3 if i % 3 == 0 else 0.5
        ax.axhline(i, color='#60a5fa', linewidth=lw, zorder=3)
        ax.axvline(i, color='#60a5fa', linewidth=lw, zorder=3)

    plt.tight_layout(pad=0.2)
    return fig


def page_sudoku():
    st.markdown('<div class="section-header">🔢 Sudoku Puzzle</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94a3b8; margin-bottom:1.5rem;">
    Fill the 9×9 grid so every row, column, and 3×3 box contains digits 1-9.
    <span style="color:#93c5fd">Blue = given</span> · <span style="color:#6ee7b7">Green = solved</span>
    </p>""", unsafe_allow_html=True)

    col_ctrl, col_main = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown("#### ⚙️ Configuration")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="sdk_diff")
        if st.button("🎲 Generate Puzzle", key="sdk_gen"):
            board, solved = generate_sudoku(difficulty)
            st.session_state.sdk_board  = board
            st.session_state.sdk_solved = solved
            st.session_state.sdk_results = {}

        if "sdk_board" not in st.session_state:
            board, solved = generate_sudoku("Medium")
            st.session_state.sdk_board  = board
            st.session_state.sdk_solved = solved
            st.session_state.sdk_results = {}

        selected_algos = st.multiselect("Algorithms", ALGO_NAMES,
                                         default=["DFS", "Greedy Best-First", "A*"],
                                         key="sdk_algos")
        st.info("⚠️ BFS is memory-intensive for Sudoku and may timeout on Hard puzzles.")

        if st.button("▶️ Solve All", key="sdk_solve"):
            if not selected_algos:
                st.error("Select at least one algorithm.")
            else:
                board   = st.session_state.sdk_board
                results = {}
                prog    = st.progress(0)
                for i, algo in enumerate(selected_algos):
                    with st.spinner(f"Running {algo}…"):
                        results[algo] = solve_sudoku(board, algo)
                    prog.progress((i + 1) / len(selected_algos))
                st.session_state.sdk_results = results
                prog.empty()

    with col_main:
        board   = st.session_state.get("sdk_board")
        results = st.session_state.get("sdk_results", {})

        c1, c2 = st.columns(2)
        with c1:
            if board:
                fig = render_sudoku(board, title="Puzzle")
                st.pyplot(fig, use_container_width=False)
                plt.close()
        with c2:
            # Show best solved board
            winner = find_winner(results) if results else None
            if winner and results[winner].success:
                fig = render_sudoku(results[winner].solution, board,
                                     title=f"Solved ({winner})")
                st.pyplot(fig, use_container_width=False)
                plt.close()
            elif board:
                solved = st.session_state.get("sdk_solved")
                if solved:
                    fig = render_sudoku(solved, board, title="Solution")
                    st.pyplot(fig, use_container_width=False)
                    plt.close()

        if results:
            st.markdown("---")
            m_cols = st.columns(len(results))
            for i, (algo, r) in enumerate(results.items()):
                with m_cols[i]:
                    color = ALGO_COLORS.get(algo, "#64748b")
                    status = "✅" if r and r.success else "❌ (timeout)"
                    t = f"{r.time_taken*1000:.1f}" if r else "—"
                    n = f"{r.nodes_explored:,}" if r else "—"
                    d = f"{r.solution_depth}" if r and r.success else "—"
                    st.markdown(f"""
                    <div class="metric-card" style="border-color:{color}40">
                        <div class="label" style="color:{color}">{algo}</div>
                        <div class="value">{t}<span style="font-size:0.7em;color:#64748b">ms</span></div>
                        <div class="sub">{status} · {n} nodes · depth {d}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            render_comparison_chart(results, "Sudoku: Algorithm Comparison")
            show_winner(results)


# SIDEBAR & MAIN
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0;">
            <div style="font-size:3rem">🧠</div>
            <div style="color:#e2e8f0;font-size:1.2rem;font-weight:700">AI Search Lab</div>
            <div style="color:#64748b;font-size:0.8rem">Search Strategy Visualizer</div>
        </div>
        <hr style="border-color:#334155">
        """, unsafe_allow_html=True)

        st.markdown("#### 🔍 Algorithm Legend")
        for algo, color in ALGO_COLORS.items():
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:6px 0;">
                <div style="width:12px;height:12px;border-radius:50%;background:{color}"></div>
                <span style="color:#cbd5e1;font-size:0.9rem">{algo}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#334155'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#64748b;font-size:0.8rem;padding:0.5rem 0">
        <b style="color:#94a3b8">DFS</b> — Explores deep before wide. Fast but not optimal.<br><br>
        <b style="color:#94a3b8">BFS</b> — Explores level by level. Guarantees shortest path.<br><br>
        <b style="color:#94a3b8">Greedy</b> — Always moves toward goal. Fast but may not find optimal path.<br><br>
        <b style="color:#94a3b8">A*</b> — Combines cost + heuristic. Optimal and efficient.
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#334155'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#475569;font-size:0.75rem;text-align:center">
        Built with Streamlit + Python<br>
        4 Puzzles · 4 Algorithms · Real-time metrics
        </div>""", unsafe_allow_html=True)


def main():
    sidebar()

    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI Search Strategy Visualizer</h1>
        <p>Compare DFS · BFS · Greedy Best-First · A* across four classic AI problems</p>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯  8-Puzzle",
        "🔤  Word Ladder",
        "🗺️   Maze",
        "🔢  Sudoku",
    ])

    with tab1:
        page_8puzzle()
    with tab2:
        page_word_ladder()
    with tab3:
        page_maze()
    with tab4:
        page_sudoku()


if __name__ == "__main__":
    main()
