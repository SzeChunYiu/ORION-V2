#!/usr/bin/env python3
"""Shared, receipt-friendly runtime bindings for native BugsInPy commands."""

from __future__ import annotations

import os
from collections.abc import Mapping


def compile_environment(
    *,
    project_python_bin: str,
    compiler_compat_cflags: str,
    base_environment: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Bind the declared project Python and narrow compiler compatibility flags."""
    environment = dict(os.environ if base_environment is None else base_environment)
    if project_python_bin:
        environment["PATH"] = project_python_bin + os.pathsep + environment.get("PATH", "")
    if compiler_compat_cflags:
        environment["CFLAGS"] = " ".join(
            part for part in (environment.get("CFLAGS", "").strip(), compiler_compat_cflags) if part
        )
    return environment
