from __future__ import annotations

import argparse
from pathlib import Path

from clinical_demo.web import serve


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local clinical nutrition automation demonstration."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("runtime") / "demo.sqlite3",
    )
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    serve(options.host, options.port, options.database)

