closure_manifest (round 2 → next):
  - correctness/F-1 (P0) "Terminal red revisions bypass the immutable ground-truth ledger" — fixed: edited § Decision 4 — prepare the ledger without consuming a failed round; § Decision 9 — apply findings as a composed, re-grounded change set; § Revision and synthesis integration; § Test plan; § Done when (sites: 5)
  - correctness/F-2 (P0) "The no-Python flow skips the ledger it promises to preserve" — fixed: edited § Pre-dispatch flow; § Test plan (sites: 2)
  - edge-cases/F-1 (P0) "Deleted headings have no valid coverage representation" — fixed: edited § Decision 3 — one immutable ground-truth ledger per dispatched round; § Decision 6 — the checker owns mechanical structure, not semantic truth; § Decision 10 — only correctness receives and samples the ground-truth ledger; § Test plan; § Done when (sites: 5)
  - edge-cases/F-2 (P0) "Unavailable-Python flow skips the ledger it must dispatch" — fixed: edited § Pre-dispatch flow; § Test plan (sites: 2)
  - edge-cases/F-3 (P1) "Checker-driven spec edits leave expected coverage stale" — fixed: edited § Decision 7 — one fix attempt per repeated checker diagnostic; § Test plan (sites: 2)
  - conventions/F-1 (P0) "No-Python path skips the required ledger preparation" — fixed: edited § Pre-dispatch flow; § Test plan (sites: 2)
