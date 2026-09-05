# Source-preserving relocation

This is PR #323 at source commit
`c5cc48058a554461f9e07b1302ea2db96853ebe6`, relocated from the colliding
`foundation_v1` path. Original source files and `RECEIPT.json` retain their exact
bytes. Historical command paths in those documents identify the original study.

The current checker is `foundation.py` in this directory; the root test
`tests/unit/test_me_foundation_revision_v1.py` uses the new package path. Its
original bytes are archived and its adaptation is separately bound by
`../foundation_integration_v1/MANIFEST.json`. Run the integration checker to
verify both original receipt bindings and successor source identities.
