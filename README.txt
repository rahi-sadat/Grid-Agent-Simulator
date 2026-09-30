RuleLab - Enhanced Rule-Based Grid Agent Simulator
===================================================

WHAT CHANGED
------------
- Redesigned dark UI with three clear areas: Rule Engine, Simulation, Challenge.
- 8 built-in levels with Starter / Easy / Medium / Hard progression.
- Challenge objectives with progress for steps, explored cells, and required rules.
- Next Level button and keyboard shortcuts.
- Agent trails and optional rule-number labels.
- Zoom controls and adjustable run speed.
- Better custom-map validation and Practice mode.
- Original Level 1 movement logic preserved and regression-tested.

HOW TO RUN (WINDOWS)
--------------------
1. Install Python 3 if needed: https://www.python.org/
2. Make sure "tcl/tk and IDLE" is included with Python (normally it is).
3. Double-click run_sim.bat

Or open Command Prompt in this folder and run:
    python agent_sim.py

HOW TO RUN (MAC/LINUX)
----------------------
    python3 agent_sim.py

If Tkinter is missing on Linux, install your distro's Python Tk package
(for example: python3-tk on Debian/Ubuntu).

TESTS
-----
Original movement regression test:
    python agent_sim.py --test

All built-in level/challenge smoke tests:
    python agent_sim.py --test-all

CONTROLS
--------
Space       Step once
Enter       Run / Pause
R           Reset current level
N           Next built-in level

CUSTOM MAP FORMAT
-----------------
Use a plain .txt file with equal-width rows.

Symbols:
    .   free cell
    #   obstacle
    ~   blocked/void cell
    R   Red agent start (optional if C exists)
    C   Cyan agent start (optional if R exists)

Example:
    ............
    ...######...
    ...#....#...
    ...#....#...
    ....R..C....
    ............

No third-party Python packages are required.
