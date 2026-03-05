"""
Checks that all deployment config files reference the correct ASGI entry point.
Prevents stale start commands from reaching the host.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXPECTED_ENTRY = "app.main:app"


def test_procfile_start_command():
    procfile = (ROOT / "Procfile").read_text()
    assert EXPECTED_ENTRY in procfile, (
        f"Procfile must reference '{EXPECTED_ENTRY}'. Got:\n{procfile}"
    )


def test_railway_json_start_command():
    railway = json.loads((ROOT / "railway.json").read_text())
    start_command = railway.get("deploy", {}).get("startCommand", "")
    assert EXPECTED_ENTRY in start_command, (
        f"railway.json startCommand must reference '{EXPECTED_ENTRY}'. Got: {start_command!r}"
    )


def test_render_yaml_start_command():
    render = (ROOT / "render.yaml").read_text()
    assert EXPECTED_ENTRY in render, (
        f"render.yaml must reference '{EXPECTED_ENTRY}'. Got:\n{render}"
    )
