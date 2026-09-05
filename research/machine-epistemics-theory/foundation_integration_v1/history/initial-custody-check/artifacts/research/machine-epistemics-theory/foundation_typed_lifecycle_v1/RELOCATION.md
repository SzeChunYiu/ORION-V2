# Source-preserving relocation

This is PR #328 at source commit
`2ade489db9b4dca382c68e7e049bcf2f68b96fe5`, relocated from the colliding
`foundation_v1` path. Original source files and `RECEIPT.json` retain their exact
bytes. Historical command paths in those documents identify the original study.

Run `python verify_bundle.py --hostile` from this directory. The dedicated
workflow now uses this directory; its original bytes are archived and the path
adaptation is separately bound by `../foundation_integration_v1/MANIFEST.json`.
The original receipt still verifies the unchanged package-relative source bytes.
