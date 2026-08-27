"""Pytest support for dynamically loaded pre-freeze research modules."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType
from typing import Any


_original_module_from_spec = importlib.util.module_from_spec


def _registered_module_from_spec(spec: Any) -> ModuleType:
    module = _original_module_from_spec(spec)
    if getattr(spec, "name", None):
        sys.modules[spec.name] = module
    return module


# The V0 test module loads a file by path so the research subtree need not be an
# admitted Python package. Dataclasses with postponed annotations still consult
# sys.modules during class construction; register the temporary module first.
importlib.util.module_from_spec = _registered_module_from_spec
