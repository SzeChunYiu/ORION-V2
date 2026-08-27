"""ORION-V2 research package.

The candidate stable public boundary is :mod:`orion_v2.kernel`. Research,
compatibility and parent/reference modules remain available through explicit
module imports, but are intentionally not re-exported from the package root.
This prevents transparent reference implementations from becoming accidental
universal V2 primitives before protected parity and kernel freeze.
"""

from . import kernel
from .kernel import (
    GRANTS_ARCHITECTURE_AUTHORITY,
    GRANTS_NOVELTY,
    GRANTS_PUBLICATION_AUTHORITY,
    GRANTS_SCIENTIFIC_TRUTH,
    KERNEL_API_VERSION,
    KERNEL_FROZEN,
)

__all__ = (
    "kernel",
    "KERNEL_API_VERSION",
    "KERNEL_FROZEN",
    "GRANTS_ARCHITECTURE_AUTHORITY",
    "GRANTS_SCIENTIFIC_TRUTH",
    "GRANTS_NOVELTY",
    "GRANTS_PUBLICATION_AUTHORITY",
)
