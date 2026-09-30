# -*- coding: utf-8 -*-
# Name: Rahi Sadat Ruhan Roll: 2207088  Course: CSE 3209 
# agent_sim.py - Enhanced rule-based grid agent simulation
# Standard-library only: Python 3 + Tkinter

import os
import sys

if sys.version_info[0] < 3:
    import subprocess
    py3_candidates = [
        r"C:\Python313\python.exe",
        r"D:\python here\python.exe",
        "py",
        "python3",
    ]
    py3_exe = None
    for cand in py3_candidates:
        try:
            p = subprocess.Popen(
                [cand, "-c", "import sys; sys.exit(0 if sys.version_info[0] >= 3 else 1)"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p.communicate()
            if p.returncode == 0:
                py3_exe = cand
                break
        except Exception:
            continue

    if py3_exe:
        cmd = [py3_exe] + sys.argv
        sys.exit(subprocess.call(cmd))
    else:
        sys.stderr.write("Error: Python 3 is required to run agent_sim.py.\n")
        sys.exit(1)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# -----------------------------------------------------------------------------
# Core rules (kept compatible with the original simulator)
# -----------------------------------------------------------------------------
RULE1_IS_DEFAULT = True
KEEP_FIRST_LABEL = True
DEFAULT_CELL_SIZE = 34
MIN_CELL_SIZE = 22
MAX_CELL_SIZE = 50

OFFSETS = {
    "NW": (-1, -1), "N": (-1, 0), "NE": (-1, 1),
    "W":  (0, -1),                "E":  (0, 1),
    "SW": (1, -1),  "S": (1, 0), "SE": (1, 1),
}

MOVE_DELTAS = {
    "North": (-1, 0),
    "East": (0, 1),
    "South": (1, 0),
    "West": (0, -1),
}

# Rules are evaluated in this exact order. First match wins.
RULES = {
    2: {"A": ["N", "NE"], "B": ["E", "SE"], "move": "East"},
    3: {"A": ["E", "SE"], "B": ["S", "SW"], "move": "South"},
    4: {"A": ["S", "SW"], "B": ["W", "NW"], "move": "West"},
    5: {"A": ["W", "NW"], "B": ["N", "NE"], "move": "North"},
    1: {"A": [], "B": [], "move": "North"},
}
RULE_ORDER = [2, 3, 4, 5, 1]

# -----------------------------------------------------------------------------
# Theme
# -----------------------------------------------------------------------------
COLORS = {
    "bg": "#07111F",
    "surface": "#0C1A2E",
    "surface_2": "#10233D",
    "surface_3": "#142B49",
    "border": "#24405F",
    "text": "#F4F8FC",
    "muted": "#93A9BF",
    "accent": "#4DD0E1",
    "accent_2": "#66FF8A",
    "warning": "#FFCA58",
    "danger": "#FF6B6B",
    "red": "#FF4D5E",
    "cyan": "#32D8FF",
    "grid": "#21415E",
    "floor": "#0A1728",
    "obstacle": "#7CFF55",
    "void": "#07111F",
    "complete": "#5CE68A",
}

# -----------------------------------------------------------------------------
# Levels
# Symbols: . = free, # = obstacle, ~ = void/blocked, R/C = agent starts
# -----------------------------------------------------------------------------
LEVEL1_MAP = """...........~~~
...........~~~
...........~~~
...........~~~
..######......
..##..##......
..##..##......
...........~~~
....R....C.~~~
......~~...~~~
......~~...~~~"""

LEVEL2_MAP = """............
...######...
...######...
...######...
.....R......
............"""

LEVEL3_MAP = """..............
..###....###..
..###....###..
..............
....R....C....
.............."""

LEVEL4_MAP = """..............
..##########..
..#........#..
..#..####..#..
.....R..C.....
.............."""

LEVEL5_MAP = """..............
..##########..
........#.....
..###...#..#..
....R...C.....
.............."""

LEVEL6_MAP = """................
..#####....#####
..#...#....#...#
..#...#....#...#
..#...######...#
..R..........C..
................"""

LEVEL7_MAP = """..................
...###......###...
...#..........#...
...#..######..#...
......#....#......
..R...#....#...C..
......######......
.................."""

LEVEL8_MAP = """....................
..######....######..
..#....#....#....#..
..#....######....#..
..#..............#..
..####..####..####..
....R...####...C....
...................."""


def challenge(title, objective, target_steps, min_unique, required_rules, max_steps):
    return {
        "title": title,
        "objective": objective,
        "target_steps": target_steps,
        "min_unique": min_unique,
        "required_rules": set(required_rules),
        "max_steps": max_steps,
    }


LEVELS = [
    {
        "name": "Level 1 - Rule Tour",
        "short": "Original slide map",
        "difficulty": "Starter",
        "map": LEVEL1_MAP,
        "challenge": challenge(
            "Trigger every rule",
            "Keep the agents moving long enough to activate Rules 1-5 and explore at least 30 cells.",
            20, 30, {1, 2, 3, 4, 5}, 65,
        ),
    },
    {
        "name": "Level 2 - Single Block",
        "short": "Learn obstacle following",
        "difficulty": "Easy",
        "map": LEVEL2_MAP,
        "challenge": challenge(
            "Circle the block",
            "Use the directional obstacle rules to keep Red moving around the central block.",
            15, 16, {2, 3, 4, 5}, 45,
        ),
    },
    {
        "name": "Level 3 - Twin Blocks",
        "short": "Two agents, two obstacles",
        "difficulty": "Easy",
        "map": LEVEL3_MAP,
        "challenge": challenge(
            "Coordinate exploration",
            "Let both agents explore while demonstrating the default rule plus all four turn rules.",
            20, 40, {1, 2, 3, 4, 5}, 55,
        ),
    },
    {
        "name": "Level 4 - U Shape",
        "short": "Interior turns",
        "difficulty": "Medium",
        "map": LEVEL4_MAP,
        "challenge": challenge(
            "Handle the U-shape",
            "Navigate the enclosure and demonstrate every directional turn rule before the limit.",
            22, 44, {2, 3, 4, 5}, 58,
        ),
    },
    {
        "name": "Level 5 - Narrow Gate",
        "short": "Wall and gap reasoning",
        "difficulty": "Medium",
        "map": LEVEL5_MAP,
        "challenge": challenge(
            "Survive the gate",
            "Keep both agents exploring around the wall-and-gap layout without halting too early.",
            24, 48, {2, 3, 4, 5}, 60,
        ),
    },
    {
        "name": "Level 6 - Long Corridor",
        "short": "Long-form rule sequence",
        "difficulty": "Medium",
        "map": LEVEL6_MAP,
        "challenge": challenge(
            "Complete the rule cycle",
            "Explore the corridor long enough to demonstrate the complete Rule 1-5 cycle.",
            26, 52, {1, 2, 3, 4, 5}, 65,
        ),
    },
    {
        "name": "Level 7 - Crossroads",
        "short": "Dense multi-turn layout",
        "difficulty": "Hard",
        "map": LEVEL7_MAP,
        "challenge": challenge(
            "Master the crossroads",
            "Trigger every rule and explore at least 40 cells before the 35-step cap.",
            20, 40, {1, 2, 3, 4, 5}, 35,
        ),
    },
    {
        "name": "Level 8 - Maze Master",
        "short": "Advanced obstacle pattern",
        "difficulty": "Hard",
        "map": LEVEL8_MAP,
        "challenge": challenge(
            "Maze endurance",
            "Demonstrate all directional turn rules and explore 44 cells before the step cap.",
            22, 44, {2, 3, 4, 5}, 38,
        ),
    },
]

# Original Level 1 expected sequence retained for regression testing.
EXPECTED_RED_L1 = [
    ((7, 4), 1), ((6, 4), 5), ((5, 4), 5), ((5, 5), 2), ((6, 5), 3),
    ((7, 5), 3), ((7, 6), 2), ((7, 7), 2), ((7, 8), 2), ((6, 8), 5),
    ((5, 8), 5), ((4, 8), 5), ((3, 8), 5), ((3, 7), 4), ((3, 6), 4),
    ((3, 5), 4), ((3, 4), 4), ((3, 3), 4), ((3, 2), 4), ((3, 1), 4),
    ((4, 1), 3), ((5, 1), 3), ((6, 1), 3), ((7, 1), 3), ((7, 2), 2),
]
EXPECTED_CYAN_L1 = [
    ((7, 9), 1), ((6, 9), 1), ((5, 9), 1), ((4, 9), 1), ((3, 9), 1),
    ((2, 9), 1), ((1, 9), 1), ((0, 9), 1), ((0, 10), 2), ((1, 10), 3),
    ((2, 10), 3), ((3, 10), 3), ((4, 10), 3), ((4, 11), 2), ((4, 12), 2),
    ((4, 13), 2), ((5, 13), 3), ((6, 13), 3), ((6, 12), 4), ((6, 11), 4),
    ((6, 10), 4), ((7, 10), 3), ((8, 10), 3), ((9, 10), 3), ((10, 10), 3),
    ((10, 9), 4), ((10, 8), 4), ((9, 8), 5), ((8, 8), 5), ((8, 7), 4),
    ((8, 6), 4),
]

# -----------------------------------------------------------------------------
# Core simulation functions
# -----------------------------------------------------------------------------
def parse_map(ascii_map):
    lines = [line.rstrip("\n") for line in ascii_map.strip("\n").splitlines() if line.strip()]
    if not lines:
        raise ValueError("The map is empty.")

    width = len(lines[0])
    if width == 0 or any(len(line) != width for line in lines):
        raise ValueError("Every map row must have the same number of columns.")

    valid = set(".#~RC")
    bad = sorted({ch for line in lines for ch in line if ch not in valid})
    if bad:
        raise ValueError("Unsupported map symbol(s): " + ", ".join(repr(x) for x in bad))

    grid = [list(line) for line in lines]
    r_start = None
    c_start = None

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "R":
                if r_start is not None:
                    raise ValueError("Only one Red start (R) is allowed.")
                r_start = (r, c)
                grid[r][c] = "."
            elif grid[r][c] == "C":
                if c_start is not None:
                    raise ValueError("Only one Cyan start (C) is allowed.")
                c_start = (r, c)
                grid[r][c] = "."

    if r_start is None and c_start is None:
        raise ValueError("The map needs at least one agent start: R or C.")

    return grid, r_start, c_start


def is_occupied(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return True
    return grid[r][c] in ("#", "~")


def get_next_move(grid, r, c):
    matched = []
    for rule_num in [2, 3, 4, 5]:
        rule = RULES[rule_num]
        a_occ = any(
            is_occupied(grid, r + OFFSETS[d][0], c + OFFSETS[d][1])
            for d in rule["A"]
        )
        b_occ = any(
            is_occupied(grid, r + OFFSETS[d][0], c + OFFSETS[d][1])
            for d in rule["B"]
        )
        if a_occ and not b_occ:
            matched.append(rule_num)

    if matched:
        if len(matched) > 1:
            print("Warning: multiple rules matched at {}: {}".format((r, c), matched))
        rule_num = matched[0]
        dr, dc = MOVE_DELTAS[RULES[rule_num]["move"]]
        return rule_num, r + dr, c + dc

    if RULE1_IS_DEFAULT:
        dr, dc = MOVE_DELTAS[RULES[1]["move"]]
        nr, nc = r + dr, c + dc
        return (None, None, None) if is_occupied(grid, nr, nc) else (1, nr, nc)

    all_free = not any(
        is_occupied(grid, r + OFFSETS[d][0], c + OFFSETS[d][1]) for d in OFFSETS
    )
    if all_free:
        dr, dc = MOVE_DELTAS[RULES[1]["move"]]
        nr, nc = r + dr, c + dc
        return (None, None, None) if is_occupied(grid, nr, nc) else (1, nr, nc)
    return None, None, None


def run_test():
    """Regression test: confirms the original Level 1 movement still matches."""
    grid, r_start, c_start = parse_map(LEVEL1_MAP)
    print("Running original Level 1 regression test...")
    for name, start, expected in [
        ("Red", r_start, EXPECTED_RED_L1),
        ("Cyan", c_start, EXPECTED_CYAN_L1),
    ]:
        curr = start
        for step_i, (exp_pos, exp_rule) in enumerate(expected):
            r_num, nr, nc = get_next_move(grid, curr[0], curr[1])
            if r_num is None:
                print("FAIL: {} blocked at step {} from {}".format(name, step_i + 1, curr))
                return False
            if (nr, nc) != exp_pos or r_num != exp_rule:
                print("FAIL: {} mismatch at step {}".format(name, step_i + 1))
                print("  Expected: cell={} rule={}".format(exp_pos, exp_rule))
                print("  Got:      cell={} rule={}".format((nr, nc), r_num))
                return False
            curr = (nr, nc)
    print("PASS: original Level 1 path is unchanged.")
    return True


def simulate_level(level, step_cap=200):
    """Headless smoke simulation used by --test-all."""
    grid, r_start, c_start = parse_map(level["map"])
    agents = {}
    for name, start in (("Red", r_start), ("Cyan", c_start)):
        if start:
            agents[name] = {"pos": start, "visited": {start}, "active": True}

    rules_seen = set()
    step_count = 0
    challenge_data = level["challenge"]
    completed = False

    while any(a["active"] for a in agents.values()) and step_count < step_cap:
        moved = False
        for agent in agents.values():
            if not agent["active"]:
                continue
            rule_num, nr, nc = get_next_move(grid, *agent["pos"])
            if rule_num is None:
                agent["active"] = False
                continue
            moved = True
            rules_seen.add(rule_num)
            if (nr, nc) in agent["visited"]:
                agent["active"] = False
            else:
                agent["visited"].add((nr, nc))
            agent["pos"] = (nr, nc)
        if moved:
            step_count += 1

        unique_total = sum(len(a["visited"]) for a in agents.values())
        completed = (
            step_count >= challenge_data["target_steps"]
            and unique_total >= challenge_data["min_unique"]
            and challenge_data["required_rules"].issubset(rules_seen)
            and step_count <= challenge_data["max_steps"]
        )
        if completed:
            break

    return completed, step_count, sum(len(a["visited"]) for a in agents.values()), rules_seen


def run_test_all():
    ok = run_test()
    print("\nRunning level/challenge smoke tests...")
    for level in LEVELS:
        try:
            completed, steps, unique, rules_seen = simulate_level(level)
            status = "PASS" if completed else "FAIL"
            print(
                "{}: {} | steps={} | "
                "explored={} | rules={}".format(
                    status, level['name'], steps, unique, sorted(rules_seen)
                )
            )
            ok = ok and completed
        except Exception as exc:
            print("FAIL: {} | {}".format(level['name'], exc))
            ok = False
    return ok


# -----------------------------------------------------------------------------
# Tkinter GUI
# -----------------------------------------------------------------------------
DIR_TO_BOX = {
    "NW": (0, 0), "N": (0, 1), "NE": (0, 2),
    "W":  (1, 0),               "E":  (1, 2),
    "SW": (2, 0), "S": (2, 1), "SE": (2, 2),
}


class AgentSimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RuleLab - Grid Agent Simulator")
        self.root.geometry("1180x740")
        self.root.minsize(980, 650)
        self.root.configure(bg=COLORS["bg"])

        self.level_idx = 0
        self.is_custom_map = False
        self.is_running = False
        self.timer_id = None
        self.last_rule_fired = None
        self.rule_history = set()
        self.cell_size = DEFAULT_CELL_SIZE
        self.show_labels = tk.BooleanVar(value=True)
        self.show_trails = tk.BooleanVar(value=True)
        self.challenge_state = "READY"
        self.challenge_announced = False
        self.current_level = None
        self.current_ascii_map = ""
        self.current_title = ""

        self._setup_ttk_styles()
        self._build_ui()
        self._bind_shortcuts()
        self.load_level(0)

    # ---------------------------- UI setup ---------------------------------
    def _setup_ttk_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Level.TCombobox",
            fieldbackground=COLORS["surface_2"],
            background=COLORS["surface_2"],
            foreground=COLORS["text"],
            arrowcolor=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["surface_2"],
            darkcolor=COLORS["surface_2"],
            padding=6,
        )
        style.map(
            "Level.TCombobox",
            fieldbackground=[("readonly", COLORS["surface_2"])],
            foreground=[("readonly", COLORS["text"])],
            selectbackground=[("readonly", COLORS["surface_2"])],
            selectforeground=[("readonly", COLORS["text"])],
        )
        style.configure(
            "Challenge.Horizontal.TProgressbar",
            troughcolor=COLORS["surface_3"],
            background=COLORS["accent"],
            bordercolor=COLORS["surface_3"],
            lightcolor=COLORS["accent"],
            darkcolor=COLORS["accent"],
            thickness=10,
        )

    def _build_ui(self):
        self._build_header()
        self._build_toolbar()

        content = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            bg=COLORS["bg"],
            sashwidth=5,
            sashrelief=tk.FLAT,
            bd=0,
            showhandle=False,
        )
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))

        # Left: rule visualizer
        left = tk.Frame(content, bg=COLORS["surface"], width=250)
        left.pack_propagate(False)
        content.add(left, minsize=230, width=250)

        tk.Label(
            left, text="RULE ENGINE", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"), anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(14, 2))
        tk.Label(
            left,
            text="First matching rule wins",
            bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9), anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(0, 8))

        self.rules_canvas = tk.Canvas(
            left, width=244, bg=COLORS["surface"], highlightthickness=0,
        )
        self.rules_canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 8))

        legend = tk.Frame(left, bg=COLORS["surface_2"], padx=10, pady=9)
        legend.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(
            legend,
            text="Cyan cells = obstacle sensed\nTop cyan bar = those cells must be free",
            justify=tk.LEFT, anchor="w", bg=COLORS["surface_2"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(fill=tk.X)

        # Center: simulation area
        center = tk.Frame(content, bg=COLORS["surface"])
        content.add(center, minsize=430, stretch="always")

        grid_header = tk.Frame(center, bg=COLORS["surface"], padx=14, pady=10)
        grid_header.pack(fill=tk.X)
        self.grid_title_label = tk.Label(
            grid_header, text="Simulation", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"), anchor="w",
        )
        self.grid_title_label.pack(side=tk.LEFT)

        self.agent_chip = tk.Label(
            grid_header, text="", bg=COLORS["surface_2"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"), padx=9, pady=3,
        )
        self.agent_chip.pack(side=tk.RIGHT)

        grid_box = tk.Frame(center, bg=COLORS["floor"])
        grid_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.grid_canvas = tk.Canvas(
            grid_box,
            bg=COLORS["floor"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            xscrollincrement=10,
            yscrollincrement=10,
        )
        hs = tk.Scrollbar(grid_box, orient=tk.HORIZONTAL, command=self.grid_canvas.xview)
        vs = tk.Scrollbar(grid_box, orient=tk.VERTICAL, command=self.grid_canvas.yview)
        self.grid_canvas.configure(xscrollcommand=hs.set, yscrollcommand=vs.set)
        vs.pack(side=tk.RIGHT, fill=tk.Y)
        hs.pack(side=tk.BOTTOM, fill=tk.X)
        self.grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: challenge panel
        right = tk.Frame(content, bg=COLORS["surface"], width=295)
        right.pack_propagate(False)
        content.add(right, minsize=270, width=295)
        self._build_challenge_panel(right)

        # Bottom status bar
        status = tk.Frame(self.root, bg="#050C16", padx=12, pady=7)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_dot = tk.Label(status, text="●", bg="#050C16", fg=COLORS["accent"], font=("Segoe UI", 9))
        self.status_dot.pack(side=tk.LEFT, padx=(0, 7))
        self.status_bar = tk.Label(
            status, text="Ready", bg="#050C16", fg=COLORS["muted"],
            anchor="w", font=("Segoe UI", 9),
        )
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.hotkey_hint = tk.Label(
            status, text="Space: step   Enter: run/pause   R: reset   N: next",
            bg="#050C16", fg="#637C94", font=("Segoe UI", 8),
        )
        self.hotkey_hint.pack(side=tk.RIGHT)

    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg"], padx=16, pady=12)
        header.pack(fill=tk.X)

        title_box = tk.Frame(header, bg=COLORS["bg"])
        title_box.pack(side=tk.LEFT)
        tk.Label(
            title_box, text="RuleLab", bg=COLORS["bg"], fg=COLORS["text"],
            font=("Segoe UI", 20, "bold"), anchor="w",
        ).pack(anchor="w")
        tk.Label(
            title_box, text="Rule-based grid agent simulator", bg=COLORS["bg"],
            fg=COLORS["muted"], font=("Segoe UI", 9), anchor="w",
        ).pack(anchor="w")

        self.header_badge = tk.Label(
            header, text="CHALLENGE READY", bg=COLORS["surface_2"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"), padx=11, pady=6,
        )
        self.header_badge.pack(side=tk.RIGHT, pady=3)

    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg=COLORS["surface"], padx=12, pady=9)
        bar.pack(fill=tk.X, padx=12, pady=(0, 10))

        tk.Label(
            bar, text="Level", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.level_var = tk.StringVar(value=LEVELS[0]["name"])
        self.level_combo = ttk.Combobox(
            bar,
            textvariable=self.level_var,
            values=[level["name"] for level in LEVELS],
            state="readonly",
            style="Level.TCombobox",
            width=25,
        )
        self.level_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.level_combo.bind("<<ComboboxSelected>>", self.on_level_change)

        self.btn_step = self._make_button(bar, "Step", self.step, COLORS["accent"], "#082029")
        self.btn_run = self._make_button(bar, "Run", self.toggle_run, COLORS["complete"], "#082217")
        self.btn_reset = self._make_button(bar, "Reset", self.reset_sim, COLORS["warning"], "#2B2104")
        self.btn_next = self._make_button(bar, "Next Level", self.next_level, COLORS["surface_3"], COLORS["text"])
        self.btn_load = self._make_button(bar, "Load Map", self.load_map_file, COLORS["surface_3"], COLORS["text"])

        tk.Frame(bar, width=1, bg=COLORS["border"]).pack(side=tk.LEFT, fill=tk.Y, padx=8)

        tk.Label(
            bar, text="Speed", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(
            bar, from_=700, to=60, orient=tk.HORIZONTAL, showvalue=False,
            bg=COLORS["surface"], troughcolor=COLORS["surface_3"],
            activebackground=COLORS["accent"], highlightthickness=0, length=95,
        )
        self.speed_scale.set(220)
        self.speed_scale.pack(side=tk.LEFT, padx=(4, 8))

        self._make_small_button(bar, "-", self.zoom_out).pack(side=tk.LEFT, padx=(2, 1))
        tk.Label(
            bar, text="Zoom", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).pack(side=tk.LEFT, padx=3)
        self._make_small_button(bar, "+", self.zoom_in).pack(side=tk.LEFT, padx=(1, 6))

        tk.Checkbutton(
            bar, text="Labels", variable=self.show_labels, command=self.redraw_grid,
            bg=COLORS["surface"], fg=COLORS["muted"], selectcolor=COLORS["surface_2"],
            activebackground=COLORS["surface"], activeforeground=COLORS["text"],
            font=("Segoe UI", 8), bd=0,
        ).pack(side=tk.RIGHT, padx=4)
        tk.Checkbutton(
            bar, text="Trails", variable=self.show_trails, command=self.redraw_grid,
            bg=COLORS["surface"], fg=COLORS["muted"], selectcolor=COLORS["surface_2"],
            activebackground=COLORS["surface"], activeforeground=COLORS["text"],
            font=("Segoe UI", 8), bd=0,
        ).pack(side=tk.RIGHT, padx=4)

    def _build_challenge_panel(self, parent):
        tk.Label(
            parent, text="LEVEL CHALLENGE", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"), anchor="w",
        ).pack(fill=tk.X, padx=14, pady=(14, 2))
        self.level_meta_label = tk.Label(
            parent, text="", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 9), anchor="w",
        )
        self.level_meta_label.pack(fill=tk.X, padx=14, pady=(0, 10))

        mission = tk.Frame(parent, bg=COLORS["surface_2"], padx=12, pady=12)
        mission.pack(fill=tk.X, padx=12, pady=(0, 10))
        self.challenge_title_label = tk.Label(
            mission, text="", bg=COLORS["surface_2"], fg=COLORS["accent"],
            font=("Segoe UI", 11, "bold"), anchor="w",
        )
        self.challenge_title_label.pack(fill=tk.X)
        self.challenge_objective_label = tk.Label(
            mission, text="", wraplength=245, justify=tk.LEFT,
            bg=COLORS["surface_2"], fg=COLORS["text"],
            font=("Segoe UI", 9), anchor="w",
        )
        self.challenge_objective_label.pack(fill=tk.X, pady=(6, 0))

        self.challenge_status_label = tk.Label(
            parent, text="READY", bg=COLORS["surface_3"], fg=COLORS["accent"],
            font=("Segoe UI", 9, "bold"), padx=9, pady=5,
        )
        self.challenge_status_label.pack(anchor="w", padx=12, pady=(0, 12))

        progress = tk.Frame(parent, bg=COLORS["surface"])
        progress.pack(fill=tk.X, padx=12)

        self.steps_text = self._metric_row(progress, "Steps")
        self.steps_bar = ttk.Progressbar(
            progress, style="Challenge.Horizontal.TProgressbar", mode="determinate", maximum=100,
        )
        self.steps_bar.pack(fill=tk.X, pady=(1, 10))

        self.explore_text = self._metric_row(progress, "Explored cells")
        self.explore_bar = ttk.Progressbar(
            progress, style="Challenge.Horizontal.TProgressbar", mode="determinate", maximum=100,
        )
        self.explore_bar.pack(fill=tk.X, pady=(1, 10))

        tk.Label(
            progress, text="Required rules", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"), anchor="w",
        ).pack(fill=tk.X)
        self.rules_progress_label = tk.Label(
            progress, text="", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Consolas", 10, "bold"), anchor="w",
        )
        self.rules_progress_label.pack(fill=tk.X, pady=(3, 10))

        tk.Label(
            progress, text="Agent state", bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"), anchor="w",
        ).pack(fill=tk.X)
        self.agent_state_label = tk.Label(
            progress, text="", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 9), justify=tk.LEFT, anchor="w",
        )
        self.agent_state_label.pack(fill=tk.X, pady=(3, 12))

        tips = tk.Frame(parent, bg=COLORS["surface_2"], padx=10, pady=9)
        tips.pack(fill=tk.X, padx=12, pady=(8, 12), side=tk.BOTTOM)
        tk.Label(
            tips,
            text="Map format\n. free   # obstacle   ~ blocked\nR red start   C cyan start",
            justify=tk.LEFT, bg=COLORS["surface_2"], fg=COLORS["muted"],
            font=("Consolas", 8), anchor="w",
        ).pack(fill=tk.X)

    def _metric_row(self, parent, label_text):
        row = tk.Frame(parent, bg=COLORS["surface"])
        row.pack(fill=tk.X)
        tk.Label(
            row, text=label_text, bg=COLORS["surface"], fg=COLORS["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side=tk.LEFT)
        value = tk.Label(
            row, text="0 / 0", bg=COLORS["surface"], fg=COLORS["text"],
            font=("Segoe UI", 8, "bold"),
        )
        value.pack(side=tk.RIGHT)
        return value

    def _make_button(self, parent, text, command, bg, fg):
        btn = tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=bg, activeforeground=fg,
            font=("Segoe UI", 9, "bold"), padx=10, pady=5,
            relief=tk.FLAT, bd=0, cursor="hand2",
        )
        btn.pack(side=tk.LEFT, padx=3)
        return btn

    def _make_small_button(self, parent, text, command):
        return tk.Button(
            parent, text=text, command=command, bg=COLORS["surface_3"], fg=COLORS["text"],
            activebackground=COLORS["border"], activeforeground=COLORS["text"],
            font=("Segoe UI", 9, "bold"), width=2, relief=tk.FLAT, bd=0, cursor="hand2",
        )

    def _bind_shortcuts(self):
        self.root.bind("<space>", lambda _e: self.step())
        self.root.bind("<Return>", lambda _e: self.toggle_run())
        self.root.bind("<Key-r>", lambda _e: self.reset_sim())
        self.root.bind("<Key-R>", lambda _e: self.reset_sim())
        self.root.bind("<Key-n>", lambda _e: self.next_level())
        self.root.bind("<Key-N>", lambda _e: self.next_level())

    # --------------------------- level loading ------------------------------
    def load_level(self, idx):
        self._stop_timer()
        self.level_idx = idx % len(LEVELS)
        self.is_custom_map = False
        self.current_level = LEVELS[self.level_idx]
        self.current_ascii_map = self.current_level["map"]
        self.current_title = self.current_level["name"]
        self.level_var.set(self.current_title)
        self.init_map(self.current_ascii_map, self.current_title)

    def on_level_change(self, _event=None):
        selected = self.level_var.get()
        for i, level in enumerate(LEVELS):
            if level["name"] == selected:
                self.load_level(i)
                return

    def next_level(self):
        self.load_level((self.level_idx + 1) % len(LEVELS))

    def load_map_file(self):
        path = filedialog.askopenfilename(
            title="Load ASCII map",
            filetypes=[("Text maps", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                ascii_map = fh.read()
            # Validate before changing current state.
            parse_map(ascii_map)
            self._stop_timer()
            self.is_custom_map = True
            self.current_level = {
                "name": os.path.basename(path),
                "short": "Custom practice map",
                "difficulty": "Practice",
                "map": ascii_map,
                "challenge": None,
            }
            self.current_ascii_map = ascii_map
            self.current_title = os.path.basename(path)
            self.level_var.set(LEVELS[self.level_idx]["name"])
            self.init_map(ascii_map, self.current_title)
        except Exception as exc:
            messagebox.showerror("Invalid map", "Could not load the map:\n\n{}".format(exc))

    def init_map(self, ascii_map, title):
        self._stop_timer()
        self.grid, self.r_start, self.c_start = parse_map(ascii_map)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0]) if self.grid else 0

        self.agents = {}
        self.cell_labels = {}
        if self.r_start:
            self.agents["Red"] = self._new_agent(self.r_start, COLORS["red"])
        if self.c_start:
            self.agents["Cyan"] = self._new_agent(self.c_start, COLORS["cyan"])

        self.step_count = 0
        self.last_rule_fired = None
        self.rule_history = set()
        self.challenge_state = "PRACTICE" if self.current_level.get("challenge") is None else "READY"
        self.challenge_announced = False
        self.map_title = title

        self.grid_title_label.config(text=title)
        self._update_challenge_text()
        self.redraw_rules()
        self.redraw_grid()
        self.update_status("Ready")

    def _new_agent(self, start, color):
        return {
            "start": start,
            "pos": start,
            "color": color,
            "visited": {start},
            "labels": {},
            "path": [start],
            "active": True,
            "halt": None,
        }

    def reset_sim(self):
        self.init_map(self.current_ascii_map, self.current_title)

    # --------------------------- simulation ---------------------------------
    def step(self):
        if not self.agents:
            return

        if self.challenge_state == "READY":
            self.challenge_state = "RUNNING"

        any_moved = False
        for name, agent in self.agents.items():
            if not agent["active"]:
                continue

            rule_num, nr, nc = get_next_move(self.grid, *agent["pos"])
            if rule_num is None:
                agent["active"] = False
                agent["halt"] = "blocked"
                continue

            self.last_rule_fired = rule_num
            self.rule_history.add(rule_num)
            any_moved = True

            if (nr, nc) not in self.cell_labels:
                self.cell_labels[(nr, nc)] = {
                    "text": str(rule_num), "color": agent["color"], "agent": name,
                }
            else:
                prev_agent = self.cell_labels[(nr, nc)]["agent"]
                if prev_agent != name or not KEEP_FIRST_LABEL:
                    self.cell_labels[(nr, nc)] = {
                        "text": str(rule_num), "color": agent["color"], "agent": name,
                    }

            if (nr, nc) not in agent["labels"] or not KEEP_FIRST_LABEL:
                agent["labels"][(nr, nc)] = rule_num

            agent["pos"] = (nr, nc)
            agent["path"].append((nr, nc))
            if (nr, nc) in agent["visited"]:
                agent["active"] = False
                agent["halt"] = "loop detected"
            else:
                agent["visited"].add((nr, nc))

        if any_moved:
            self.step_count += 1

        self._check_challenge()
        self.redraw_rules()
        self.redraw_grid()
        self._update_challenge_text()

        if all(not a["active"] for a in self.agents.values()):
            self._stop_timer()
            halts = ", ".join("{}: {}".format(n, a['halt']) for n, a in self.agents.items())
            self.update_status("Halted - {}".format(halts))
        elif self.challenge_state == "COMPLETE":
            self.update_status("Challenge complete - press Run to keep exploring or Next Level")
        elif self.challenge_state == "FAILED":
            self.update_status("Challenge limit reached - reset to retry, or keep exploring")
        else:
            self.update_status("Stepping")

    def toggle_run(self):
        if self.is_running:
            self._stop_timer()
            self.update_status("Paused")
            return

        if not any(a["active"] for a in self.agents.values()):
            self.update_status("All agents are halted - reset to run again")
            return

        self.is_running = True
        self.btn_run.config(text="Pause", bg=COLORS["warning"], fg="#2B2104")
        self.update_status("Running")
        self._run_loop()

    def _run_loop(self):
        if not self.is_running:
            return
        if not any(a["active"] for a in self.agents.values()):
            self._stop_timer()
            return
        self.step()
        if self.is_running:
            self.timer_id = self.root.after(int(self.speed_scale.get()), self._run_loop)

    def _stop_timer(self):
        self.is_running = False
        self.btn_run.config(text="Run", bg=COLORS["complete"], fg="#082217")
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except tk.TclError:
                pass
            self.timer_id = None

    def _check_challenge(self):
        data = self.current_level.get("challenge")
        if not data or self.challenge_state in ("COMPLETE", "FAILED"):
            return

        unique_total = self._unique_total()
        achieved = (
            self.step_count >= data["target_steps"]
            and unique_total >= data["min_unique"]
            and data["required_rules"].issubset(self.rule_history)
        )

        if achieved and self.step_count <= data["max_steps"]:
            self.challenge_state = "COMPLETE"
            if not self.challenge_announced:
                self.challenge_announced = True
                self._stop_timer()
            return

        if self.step_count >= data["max_steps"]:
            self.challenge_state = "FAILED"
            self._stop_timer()
            return

        if all(not a["active"] for a in self.agents.values()) and not achieved:
            self.challenge_state = "FAILED"

    # --------------------------- rendering ----------------------------------
    def redraw_rules(self):
        self.rules_canvas.delete("all")
        width = max(self.rules_canvas.winfo_width(), 236)
        card_x1, card_x2 = 8, width - 8
        y = 8
        box_sz = 12

        for rule_num in RULE_ORDER:
            rule = RULES[rule_num]
            active = self.last_rule_fired == rule_num
            outline = COLORS["warning"] if active else COLORS["border"]
            fill = COLORS["surface_3"] if active else COLORS["surface_2"]
            self.rules_canvas.create_rectangle(
                card_x1, y, card_x2, y + 62,
                fill=fill, outline=outline, width=2 if active else 1,
            )
            self.rules_canvas.create_text(
                27, y + 18, text="R{}".format(rule_num), fill=COLORS["text"],
                font=("Segoe UI", 10, "bold"),
            )
            move_text = "DEFAULT -> North" if rule_num == 1 else "MOVE -> {}".format(rule['move'])
            self.rules_canvas.create_text(
                27, y + 44, text=move_text, fill=COLORS["muted"],
                font=("Segoe UI", 7), anchor="w",
            )

            bx1, by1 = 58, y + 13
            self.draw_mini_box(self.rules_canvas, bx1, by1, box_sz, rule["A"], False)
            if rule_num != 1:
                self.rules_canvas.create_text(
                    bx1 + 3 * box_sz + 10, by1 + 17, text="AND",
                    fill=COLORS["muted"], font=("Segoe UI", 6, "bold"),
                )
                bx2 = bx1 + 3 * box_sz + 32
                self.draw_mini_box(self.rules_canvas, bx2, by1, box_sz, rule["B"], True)
                self.draw_arrow(self.rules_canvas, bx2 + 3 * box_sz + 20, by1 + 18, rule["move"])
            else:
                self.rules_canvas.create_text(
                    141, by1 + 17, text="when no turn rule matches",
                    fill=COLORS["muted"], font=("Segoe UI", 7), anchor="w",
                )
            y += 70

        self.rules_canvas.config(scrollregion=(0, 0, width, y + 6))

    def draw_mini_box(self, canvas, sx, sy, sz, active_dirs, is_negated=False):
        if is_negated:
            canvas.create_line(
                sx, sy - 4, sx + 3 * sz, sy - 4,
                fill=COLORS["accent"], width=2,
            )
        for br in range(3):
            for bc in range(3):
                x1, y1 = sx + bc * sz, sy + br * sz
                cdir = next((d for d, coords in DIR_TO_BOX.items() if coords == (br, bc)), None)
                if (br, bc) == (1, 1):
                    canvas.create_rectangle(
                        x1, y1, x1 + sz, y1 + sz,
                        outline=COLORS["border"], fill=COLORS["surface"],
                    )
                    canvas.create_oval(
                        x1 + 3, y1 + 3, x1 + sz - 3, y1 + sz - 3,
                        fill=COLORS["red"], outline="",
                    )
                elif cdir in active_dirs:
                    canvas.create_rectangle(
                        x1, y1, x1 + sz, y1 + sz,
                        outline=COLORS["border"], fill=COLORS["accent"],
                    )
                else:
                    canvas.create_rectangle(
                        x1, y1, x1 + sz, y1 + sz,
                        outline=COLORS["border"], fill=COLORS["floor"],
                    )

    def draw_arrow(self, canvas, x, y, direction):
        ln = 15
        dr, dc = MOVE_DELTAS[direction]
        x1, y1 = x - dc * (ln // 2), y - dr * (ln // 2)
        x2, y2 = x + dc * (ln // 2), y + dr * (ln // 2)
        canvas.create_line(
            x1, y1, x2, y2, arrow=tk.LAST,
            fill=COLORS["accent_2"], width=2,
        )

    def redraw_grid(self):
        self.grid_canvas.delete("all")
        if not getattr(self, "grid", None):
            return

        cs = self.cell_size
        pad = 36
        map_w = self.num_cols * cs
        map_h = self.num_rows * cs
        total_w = max(map_w + pad * 2, self.grid_canvas.winfo_width())
        total_h = max(map_h + pad * 2, self.grid_canvas.winfo_height())
        self.grid_canvas.config(scrollregion=(0, 0, total_w, total_h))

        ox = max(pad, (self.grid_canvas.winfo_width() - map_w) // 2)
        oy = max(pad, (self.grid_canvas.winfo_height() - map_h) // 2)

        # Subtle panel behind the board.
        self.grid_canvas.create_rectangle(
            ox - 9, oy - 9, ox + map_w + 9, oy + map_h + 9,
            fill="#081423", outline=COLORS["border"], width=1,
        )

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                ctype = self.grid[r][c]
                x1 = ox + c * cs
                y1 = oy + r * cs
                x2 = x1 + cs
                y2 = y1 + cs
                if ctype == "~":
                    self.grid_canvas.create_rectangle(
                        x1, y1, x2, y2, fill=COLORS["void"], outline=COLORS["void"],
                    )
                elif ctype == "#":
                    self.grid_canvas.create_rectangle(
                        x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                        fill=COLORS["obstacle"], outline="#14311F",
                    )
                    self.grid_canvas.create_line(
                        x1 + 5, y1 + 5, x2 - 5, y1 + 5, fill="#B8FF9E", width=1,
                    )
                else:
                    self.grid_canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=COLORS["floor"], outline=COLORS["grid"], width=1,
                    )

        # Start markers.
        for name, agent in self.agents.items():
            r, c = agent["start"]
            cx = ox + c * cs + cs / 2
            cy = oy + r * cs + cs / 2
            radius = max(5, cs * 0.17)
            self.grid_canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                outline=agent["color"], width=1, dash=(2, 2),
            )

        # Trails.
        if self.show_trails.get():
            for agent in self.agents.values():
                if len(agent["path"]) > 1:
                    points = []
                    for r, c in agent["path"]:
                        points.extend((ox + c * cs + cs / 2, oy + r * cs + cs / 2))
                    line_opts = {
                        "fill": agent["color"],
                        "width": max(1, cs // 14),
                        "dash": (3, 3),
                        "smooth": False,
                    }
                    self.grid_canvas.create_line(*points, **line_opts)

        # Rule labels are drawn above trails.
        if self.show_labels.get():
            for (r, c), item in self.cell_labels.items():
                cx = ox + c * cs + cs / 2
                cy = oy + r * cs + cs / 2
                self.grid_canvas.create_text(
                    cx, cy, text=item["text"], fill=item["color"],
                    font=("Consolas", max(8, cs // 3), "bold"),
                )

        # Agents.
        for name, agent in self.agents.items():
            r, c = agent["pos"]
            cx = ox + c * cs + cs / 2
            cy = oy + r * cs + cs / 2
            radius = cs * 0.34
            self.grid_canvas.create_oval(
                cx - radius + 2, cy - radius + 3, cx + radius + 2, cy + radius + 3,
                fill="#02060B", outline="",
            )
            self.grid_canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                fill=agent["color"], outline=COLORS["text"], width=2,
            )
            self.grid_canvas.create_text(
                cx, cy, text=name[0], fill="#06121B",
                font=("Segoe UI", max(8, cs // 3), "bold"),
            )

    # --------------------------- challenge/status ---------------------------
    def _unique_total(self):
        return sum(len(agent["visited"]) for agent in self.agents.values())

    def _update_challenge_text(self):
        level = self.current_level
        data = level.get("challenge")
        self.level_meta_label.config(
            text="{}  |  {}".format(level.get('difficulty', 'Practice'), level.get('short', ''))
        )

        if not data:
            self.challenge_title_label.config(text="Practice mode")
            self.challenge_objective_label.config(
                text="Custom maps run with the same rule engine. Explore freely and inspect which rules fire."
            )
            self.steps_text.config(text=str(self.step_count))
            self.explore_text.config(text=str(self._unique_total()))
            self.steps_bar["value"] = 0
            self.explore_bar["value"] = 0
            self.rules_progress_label.config(
                text="  ".join("R{}:{}".format(r, 'ON' if r in self.rule_history else '--') for r in [1, 2, 3, 4, 5])
            )
            self._set_challenge_badge("PRACTICE")
        else:
            self.challenge_title_label.config(text=data["title"])
            self.challenge_objective_label.config(text=data["objective"])
            self.steps_text.config(text="{} / {}".format(self.step_count, data['target_steps']))
            self.explore_text.config(text="{} / {}".format(self._unique_total(), data['min_unique']))
            self.steps_bar["value"] = min(100, 100 * self.step_count / max(1, data["target_steps"]))
            self.explore_bar["value"] = min(100, 100 * self._unique_total() / max(1, data["min_unique"]))

            rule_bits = []
            for rule_num in [1, 2, 3, 4, 5]:
                if rule_num not in data["required_rules"]:
                    marker = "--"
                else:
                    marker = "OK" if rule_num in self.rule_history else ".."
                rule_bits.append("R{}:{}".format(rule_num, marker))
            self.rules_progress_label.config(text="  ".join(rule_bits))
            self._set_challenge_badge(self.challenge_state)

        state_lines = []
        for name, agent in self.agents.items():
            state = "active" if agent["active"] else (agent["halt"] or "halted")
            state_lines.append("{}: {}  |  pos {}".format(name, state, agent['pos']))
        self.agent_state_label.config(text="\n".join(state_lines))
        active_count = sum(1 for a in self.agents.values() if a["active"])
        self.agent_chip.config(text="{}/{} agents active".format(active_count, len(self.agents)))

    def _set_challenge_badge(self, state):
        palette = {
            "READY": ("READY", COLORS["surface_3"], COLORS["accent"]),
            "RUNNING": ("IN PROGRESS", COLORS["surface_3"], COLORS["warning"]),
            "COMPLETE": ("COMPLETE", "#143C2B", COLORS["complete"]),
            "FAILED": ("RETRY", "#422029", COLORS["danger"]),
            "PRACTICE": ("PRACTICE", COLORS["surface_3"], COLORS["muted"]),
        }
        text, bg, fg = palette.get(state, palette["READY"])
        self.challenge_status_label.config(text=text, bg=bg, fg=fg)
        self.header_badge.config(text="CHALLENGE {}".format(text), bg=bg, fg=fg)

    def update_status(self, action_state):
        rule_text = "R{}".format(self.last_rule_fired) if self.last_rule_fired else "None"
        self.status_bar.config(
            text=(
                "{}   |   Step {}   |   "
                "Last rule {}   |   {}".format(
                    self.map_title, self.step_count, rule_text, action_state
                )
            )
        )
        if self.challenge_state == "COMPLETE":
            self.status_dot.config(fg=COLORS["complete"])
        elif self.challenge_state == "FAILED":
            self.status_dot.config(fg=COLORS["danger"])
        elif self.is_running:
            self.status_dot.config(fg=COLORS["warning"])
        else:
            self.status_dot.config(fg=COLORS["accent"])

    # --------------------------- zoom ---------------------------------------
    def zoom_in(self):
        self.cell_size = min(MAX_CELL_SIZE, self.cell_size + 4)
        self.redraw_grid()

    def zoom_out(self):
        self.cell_size = max(MIN_CELL_SIZE, self.cell_size - 4)
        self.redraw_grid()


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            return 0 if run_test() else 1
        if sys.argv[1] == "--test-all":
            return 0 if run_test_all() else 1

    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print("Could not start Tkinter GUI: {}".format(exc))
        print("Run with --test-all for a headless verification.")
        return 1

    AgentSimApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
