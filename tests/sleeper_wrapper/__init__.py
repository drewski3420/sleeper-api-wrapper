from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parents[2]
_real_package_init = _repo_root / "sleeper_wrapper" / "__init__.py"

_spec = importlib.util.spec_from_file_location(
  __name__,
  _real_package_init,
  submodule_search_locations=[str(_repo_root / "sleeper_wrapper")],
)

if _spec is None or _spec.loader is None:
  raise ImportError(f"Unable to load package from {_real_package_init}")

_module = importlib.util.module_from_spec(_spec)
sys.modules[__name__] = _module
_spec.loader.exec_module(_module)
