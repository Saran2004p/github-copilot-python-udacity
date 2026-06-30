from flask import Flask, render_template, jsonify, request
import sudoku_logic
from pathlib import Path
import json
import os
import time

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

# Leaderboard storage (persisted to starter/leaderboard.json)
LEADERBOARD_FILE = Path(__file__).parent / "leaderboard.json"
LEADERBOARD_LOCK = None

# Lazy import of threading.Lock to avoid issues during test loading
def _get_lock():
    global LEADERBOARD_LOCK
    if LEADERBOARD_LOCK is None:
        import threading
        LEADERBOARD_LOCK = threading.Lock()
    return LEADERBOARD_LOCK


def _load_leaderboard():
    try:
        if not LEADERBOARD_FILE.exists():
            return []
        with LEADERBOARD_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        # On error return empty leaderboard to avoid crashing the app
        return []


def _save_leaderboard(entries):
    # Write atomically
    try:
        tmp_path = LEADERBOARD_FILE.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as fh:
            json.dump(entries, fh, ensure_ascii=False, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, LEADERBOARD_FILE)
    except Exception:
        # Best-effort: ignore write errors for now
        pass


def _normalize_entry(raw):
    # Validate and normalize incoming leaderboard entry.
    # Expected fields: name (str), time (number, seconds), difficulty (str), hints (int)
    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    name = name.strip()[:50]

    t = raw.get("time")
    try:
        t = float(t)
        if t < 0:
            raise ValueError()
    except Exception:
        raise ValueError("time must be a non-negative number")

    difficulty = raw.get("difficulty")
    if difficulty is None:
        difficulty = "unknown"
    difficulty = str(difficulty).lower()

    hints = raw.get("hints")
    try:
        hints = int(hints)
        if hints < 0:
            raise ValueError()
    except Exception:
        raise ValueError("hints must be a non-negative integer")

    return {
        "name": name,
        "time": t,
        "difficulty": difficulty,
        "hints": hints,
        "ts": int(time.time())
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    entries = _load_leaderboard()
    # Return top 10 entries
    return jsonify({'leaderboard': entries[:10]})


@app.route('/leaderboard', methods=['POST'])
def post_leaderboard():
    data = request.json or {}
    try:
        entry = _normalize_entry(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    lock = _get_lock()
    with lock:
        entries = _load_leaderboard()
        # Append and sort by time asc, then hints asc, then ts asc
        entries.append(entry)
        entries.sort(key=lambda e: (e.get('time', 0), e.get('hints', 0), e.get('ts', 0)))
        # Keep top 10
        entries = entries[:10]
        _save_leaderboard(entries)

    return jsonify({'leaderboard': entries}), 201


if __name__ == '__main__':
    app.run(debug=True)
