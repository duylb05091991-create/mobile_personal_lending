"""Export the served OpenAPI to the committed openapi.yaml.

Run: PYTHONPATH=src python scripts/export_openapi.py
Because the spec is generated from the running app, the committed file cannot
drift from the runtime (G4 / OpenAPI standard).
"""
from __future__ import annotations

import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from nopbai.app import create_app  # noqa: E402


def main() -> None:
    app = create_app()
    spec = app.openapi()
    out = pathlib.Path(__file__).resolve().parents[1] / "openapi.yaml"
    out.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True))
    ops = sum(len(v) for v in spec["paths"].values())
    print(f"Wrote {out} ({len(spec['paths'])} paths, {ops} operations)")


if __name__ == "__main__":
    main()
