# Wind-Down Procedure — Step-by-Step (Exact; no inference)

> **Mode context:** This procedure is **mode-aware**. In **Model Mode**, UI checks like Offline-First and AAA are **N/A**; canonical headers are enforced via `docs/REQUEST_SCHEMA.md`. In **UI Mode**, the HTML table of 7 headers, Service Worker, IndexedDB, and AAA are required.

---

## A. Trigger & Immediate Announcement

1. **Trigger condition detected** (any one):

   * Performance degradation signal (lag, growing queues, rising memory), **or**
   * Explicit user command “Enter Wind-Down,” **or**
   * Session close intent.
2. **User alert (must display):**
   “**Wind-Down initiated — pausing new operations.**”

---

## B. Pause Intake (Stop New Work)

3. Disable all controls that start work (set `aria-disabled="true"` where applicable).
4. Halt scheduling of new bulk ops, lookups, enrichments, exports.

---

## C. Concurrency Freeze (Quiesce Safely)

5. Allow **critical** in-flight tasks to finish; cancel **non-critical** tasks.
6. Verify **no open** transactional state remains (e.g., no pending writes, timers, or background workers).
7. Record result `concurrency_ok=true` into `reports/MANIFEST_FLAGS.json`.
8. **User alert:** “**Concurrency audit complete — all tasks quiesced.**”

---

## D. Stabilize & Persist (State Safety)

9. Flush any queues/buffers to persistence.
10. Append a continuity entry (timestamp + metrics) to `docs/modeling/CONTINUITY.md`.
11. Set current **Mode** and important flags in `reports/MANIFEST_FLAGS.json`.
12. Freeze the UI to a single status view (if UI Mode).
13. **User alert:** “**Session stabilized — state persisted.**”

---

## E. Packaging (Generate Artifacts; **include *every* file**)

14. Generate:

    * File tree → `reports/FILE_TREE.txt`
    * SHA-256 checksums → `reports/CHECKSUM_MANIFEST.csv`
    * Placeholder scan → `reports/PLACEHOLDER_SCAN.csv`
    * Regression matrix → `REGRESSION_TEST_MATRIX.md`
    * Canon flags → `reports/MANIFEST_FLAGS.json` (set `"mode":"model"` or `"ui"`, `"phase":"wind_down"`)
    * Ensure canonical SOP present → `docs/security_ops_spinup_winddown.md`
    * Ensure 7-field schema (Model Mode) → `docs/REQUEST_SCHEMA.md`
15. Build **full-environment ZIP** (no exclusions):
    `dist/SilentStacks_SESSION_<timestamp>_FULL_ARCHIVE.zip` (contains **everything** under the working root, including `/docs`, `/reports`, `/dist`, and all other files).
16. **User alert:** “**Packaging in progress.**”

---

## F. Audit (Gate 0 — Mode Aware)

17. Run Gate-0 audit and write `reports/GATE0_README.md`:

    * **CT.gov policy** = **linkout-only** (required in all modes).
    * **No XLSX** (CSV/TSV only; no Excel/SheetJS/ExcelJS).
    * **Canonical headers**:

      * **Model Mode:** `docs/REQUEST_SCHEMA.md` must specify the 7 fields *in order* with `n/a` filler rule.
      * **UI Mode:** a 7-column **HTML** table (fixed order; blanks = “n/a”).
    * **Offline-First** (SW + IndexedDB) → **required** in **UI Mode**, **N/A** in **Model Mode**.
    * **Rate limit ≤2/sec** → required if network retrieval present; otherwise N/A.
    * **AAA accessibility** → **required** in **UI Mode**, **N/A** in **Model Mode**.
    * **procedural\_neglect** category present and updated if any step was missed.
18. **User alert:** “**Wind-Down audit complete — review results.**”

---

## G. P0 Brakes & Review (**Gate 0 / Phase 0 status**)

19. **Engage brakes:** Set `locked_at_gate: 0` (Phase 0). No modeling, no packaging forward, no Flush.
20. **Print (= display inline, full text) the 4 major docs** on screen — not just listed:

    * `docs/security_ops_spinup_winddown.md` (canonical SOP)
    * `Playbook` (authoritative **P0 Failure Log** present)
    * `docs/modeling/CONTINUITY.md` (this session’s entries)
    * `reports/GATE0_README.md` (audit summary)
21. **Audit bundle prepared (not printed by default, but zipped):**

    * `reports/FILE_TREE.txt`, `reports/CHECKSUM_MANIFEST.csv`, `reports/PLACEHOLDER_SCAN.csv`,
      `REGRESSION_TEST_MATRIX.md`, `reports/MANIFEST_FLAGS.json`, and the **full-environment ZIP**.
22. **Failure handling (automatic; no permission prompts):**

    * If any failure (including **procedural neglect** like not displaying docs):

      * **Immediately log** the P0 in **Playbook** (authoritative), **Continuity**, and **Gate 0 README**.
      * **Auto-repair** and **iterate** across all docs until concurrent and correct.
      * Remain locked at Gate 0; alert at start and completion of repairs.

---

## H. Flush System (**Final step; strictly gated**)

23. **Preconditions (all required):**

    * Steps **A–G** completed **successfully**.
    * **User approval** granted after reviewing the printed major docs.
    * **No procedural neglect occurred during this Wind-Down** (if any neglect occurred, **Flush is prohibited**; a **clean Spin-Up** is required next).
24. **Actions:**

    * Clear runtime queues/caches/temp state; terminate workers/timers; reset transient vars.
    * Verify only persisted artifacts remain: `/docs`, `/reports`, `/dist` (and the full-environment ZIP).
25. **User alert:** “**Wind-Down complete — system flushed and fully halted. Ready for next Spin-Up.**”

---

## Emergency Override (applies during any step)

* If hard-failure threshold is hit (e.g., **browser ≥\~800–830 MB**, hang, heartbeat loss):

  * **Immediately switch to Emergency Procedure** (Crash Log, P0 log entries, Gate-0 lock, auto-package with **Emergency** flag).
  * Emergency overrides normal Wind-Down flow.

---

## Non-Negotiable Logging Rules

* **All P0 failures** log **immediately** to: **Playbook** (authoritative), **Continuity**, **Gate 0 README** (`procedural_neglect`).
* **Repairs auto-run** with **alerts** (start/finish) — **never** prompt for permission.
* **Iteration** continues until **all docs are concurrent and correct**; only then can approval be requested.

---

### Output/Artifacts checklist (you should see these every Wind-Down)

* `reports/FILE_TREE.txt`
* `reports/CHECKSUM_MANIFEST.csv`
* `reports/PLACEHOLDER_SCAN.csv`
* `REGRESSION_TEST_MATRIX.md`
* `reports/MANIFEST_FLAGS.json`
* `reports/GATE0_README.md`
* `docs/security_ops_spinup_winddown.md` (printed)
* `Playbook` with **P0 Failure Log** (printed)
* `docs/modeling/CONTINUITY.md` (printed)
* **ZIP**: `dist/SilentStacks_SESSION_<timestamp>_FULL_ARCHIVE.zip` (**every single file included**)
