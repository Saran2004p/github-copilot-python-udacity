def test_app_imports_and_testing_mode(app):
    # Basic smoke test that app exists and TESTING is enabled
    assert app is not None
    assert app.testing is True


def test_index_route(client):
    # index should render successfully
    resp = client.get("/")
    assert resp.status_code == 200


def test_new_game_route_returns_puzzle(client, app_module):
    # Generate a new game and ensure puzzle is present and shaped 9x9
    resp = client.get("/new?clues=35")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert "puzzle" in data
    puzzle = data["puzzle"]
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)


def test_check_endpoint_with_solution(client, app_module):
    # Create a new game so CURRENT['solution'] is set, then submit the correct board
    resp = client.get("/new?clues=35")
    assert resp.status_code == 200
    # Access the module-level CURRENT store and its solution
    solution = app_module.CURRENT.get("solution")
    assert solution is not None
    # Post the solution — expect no incorrect cells
    resp2 = client.post("/check", json={"board": solution})
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert "incorrect" in data
    assert data["incorrect"] == []
