# Custody correction: source identity and complete inventory

The initial integration checker verified file bytes and the ten PR numbers, but
accepted a syntactically valid forged head and a shortened per-PR file list.
An internal reviewer reproduced both false-green cases. This did not alter the
actual imported source bytes: a separate direct Git tree comparison had matched
all 130 files. It did invalidate the checker's stronger claim that arbitrary
manifest input could establish exact source identity and completeness.

Before repair, four new controls failed as expected: all-zero forged head,
substitution of another genuine PR head, one omitted source file, and a
substituted source path. Their actual pytest output is preserved in
`history/initial-custody-check/custody-red.txt`. The original checker, test and
replay receipt are retained there. `ARTIFACT_INDEX.json` maps all eight original
receipt-bound integration artifacts to preserved original bytes.

The repaired checker uses `SOURCE_INVENTORY.json`, independently acquired from
the original connected-GitHub PR-head/changed-file responses and each exact
head's Git tree. Its SHA-256 is pinned as a checker constant outside
`MANIFEST.json`. Verification requires exact equality of every PR head and
complete original path/blob inventory before checking source and integrated
bytes. An additional hostile changes both editable inputs; the separate pinned
inventory digest rejects that change.

The internal reviewer subsequently replayed the clean 130-file integration,
confirmed both original attacks now raise the intended errors, and independently
compared all ten inventory heads and complete changed-path sets with their own
connected-GitHub fetches: ten agreements and no disagreement. This is an internal
engineering review, not independent external scientific assumption review.

The current `REPLAY_RECEIPT.json` is a successor receipt over the repaired
checker, all integration artifacts and fresh finite replay. It links the
preserved initial receipt. No original study receipt, prior negative result,
scientific terminal, or external admission state was rewritten.
