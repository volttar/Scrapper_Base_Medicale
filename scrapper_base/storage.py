from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


class JsonlStorage:
    def __init__(self, output_path: str) -> None:
        self._path = Path(output_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, items: Iterable[dict[str, Any]]) -> None:
        with self._path.open("a", encoding="utf-8") as handle:
            for item in items:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")

