# repositories/file_cache.py
"""Small JSON file cache helper."""

from __future__ import annotations

import json
from pathlib import Path
from time import time
from typing import Any


class FileCache:
  """Read and write JSON payloads to a local file."""

  def __init__(self, filename: str | Path):
    self.filename = Path(filename)
    self.max_age = 86400

  def recent(self) -> bool:
    """Return True if the cache file exists and is newer than the max_age"""
    try:
      return time() - self.filename.stat().st_mtime < self.max_age
    except FileNotFoundError:
      return False

  def read_json(self) -> Any:
    """Read and parse JSON from the cache file."""
    with self.filename.open("r", encoding="utf-8") as f:
      return json.load(f)

  def write_json(self, data: Any) -> None:
    """Write JSON data to the cache file."""
    self.filename.parent.mkdir(parents=True, exist_ok=True)
    with self.filename.open("w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)

  def read_or_none(self) -> Any | None:
    """Return parsed JSON if the file exists, otherwise None."""
    if not self.recent():
      return None
    return self.read_json()
