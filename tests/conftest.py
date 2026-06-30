import importlib.util
import sys
from pathlib import Path
import pytest


def _load_module(name, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def app_module():
    """Load the starter/app.py module from the repository without requiring a package import.
    Returns the loaded module object so tests can access module-level state (CURRENT).
    """
    repo_root = Path(__file__).resolve().parents[1]
    app_path = repo_root / "starter" / "app.py"
    if not app_path.exists():
        raise RuntimeError(f"Could not find app.py at {app_path}")
    module = _load_module("starter_app", app_path)
    return module


@pytest.fixture(scope="session")
def sudoku_logic_module():
    """Load the starter/sudoku_logic.py module for unit tests of logic functions."""
    repo_root = Path(__file__).resolve().parents[1]
    mod_path = repo_root / "starter" / "sudoku_logic.py"
    if not mod_path.exists():
        raise RuntimeError(f"Could not find sudoku_logic.py at {mod_path}")
    module = _load_module("starter_sudoku_logic", mod_path)
    return module


@pytest.fixture(scope="session")
def app(app_module):
    """Return the Flask app object from the loaded module and enable TESTING."""
    if not hasattr(app_module, "app"):
        raise RuntimeError("Loaded module does not expose 'app'")
    flask_app = getattr(app_module, "app")
    flask_app.config.setdefault("TESTING", True)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
