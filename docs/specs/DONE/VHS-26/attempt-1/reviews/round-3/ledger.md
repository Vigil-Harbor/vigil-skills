closure_manifest (round 3 → next):
  - correctness/F-1 (P0) "Terminal addenda cannot always be ‘checked’" — fixed: edited § Decision 4 — prepare the ledger without consuming a failed round; § Test plan; § Done when (sites: 3)
  - edge-cases/F-1 (P0) "Duplicate-heading deletion still has no valid tombstone" — fixed: edited § Decision 3 — one immutable ground-truth ledger per dispatched round; § Decision 6 — the checker owns mechanical structure, not semantic truth; § Decision 10 — only correctness receives and samples the ground-truth ledger; § Test plan; § Done when (sites: 5)
