# Excel Resource Request Tracker — Project Packet (v0)

*Last updated: Aug 19, 2025*

---

## 1) Executive Project Summary

**Goal:** Provide a centralized, no‑server spreadsheet to capture resource requests with strict validation and a low‑friction entry flow for non‑technical staff.

**Why Excel (no VBA):**

* Ubiquitous across the team; no install or permissions hurdles.
* Built‑in Data Form + Data Validation offers guardrails without macros.
* Works on network drives/SharePoint; survives spotty connectivity.

**What this delivers:**

* One workbook with four sheets: **Form**, **Data**, **Lists**, **README**.
* Validations for **Descriptor**, **For FY**, **Vote**, **Cost**, **Date**, and **Requestor (email)**.
* “Idiot‑proof” entry via **Form** sheet (blue cells) or Excel’s **Data > Form** dialog.
* Protected schema on **Data**/**Lists** to reduce accidental breakage.

**Out of scope (v0):**

* Automation (no VBA/macros), reporting dashboards, workflows/notifications.
* Multi‑user concurrency control beyond what Excel/SharePoint natively provides.

---

## 2) Current Schema (v0)

| Column              | Type / Validation                                   | Required | Notes                                         |
| ------------------- | --------------------------------------------------- | -------: | --------------------------------------------- |
| Date                | Date (>= 1900‑01‑01)                                |        ◯ | Optional; user‑entered or via Data Form       |
| Resource            | Text                                                |        ◯ | Free text title/name                          |
| Descriptor          | Dropdown {DB, Diagnostic Tool, CE, Journal, E‑Book} |        ◯ | Controlled vocabulary (editable in **Lists**) |
| Requestor           | Email‑like pattern                                  |        ◯ | Must contain `@` and a `.`; no spaces         |
| Demo and Trial Info | Text ≤ 500                                          |        ◯ | Long free text allowed                        |
| For FY              | Dropdown {FY25, FY26, FY27}                         |        ◯ | Update list as needed in **Lists**            |
| Cost                | Number ≥ 0                                          |        ◯ | Currency entry allowed                        |
| Vote                | Dropdown {Yes, No, Maybe}                           |        ◯ | Captures committee preference                 |
| Comments            | Text ≤ 500                                          |        ◯ | General notes                                 |

> Admins can modify vocabularies on **Lists**; structure is protected on **Data**.

---

## 3) Gap Report

**A. Functional Gaps**

1. **No workflow / approvals** — status changes and votes are captured, but no routing or notifications.
2. **Limited concurrency** — simultaneous edits may cause conflicts in Excel; SharePoint co‑authoring helps but is imperfect.
3. **Audit trail** — no immutable history/log per record.
4. **Reporting** — no pivot/dashboard packaged (could add a read‑only Pivot sheet in v0.1).
5. **Email validation** — uses a strict “looks like” rule (no regex), may accept edge cases or block rare valid addresses.

**B. Data Quality Risks**

1. **Free text spread** in Resource/Comments/Demo fields → inconsistent phrasing.
2. **Descriptor drift** — if lists are edited casually; mitigate by restricting **Lists** sheet access.
3. **Date / Cost formatting** — regional settings differences.
4. **Duplicate entries** — no deduping key beyond human vigilance.

**C. Security/Access Risks**

1. **Over‑permissive editing** on SharePoint could allow schema changes if sheet protection is removed.
2. **PHI/PII** — ensure no sensitive data is entered in free text.

**D. Suggested Mitigations (v0.1–v0.3)**

* Add a **Pivot & Filters** sheet (read‑only) for basic reporting.
* Add **conditional formatting** on Data to flag missing Date/Descriptor/Vote, and potential duplicates (same Resource + Requestor within 30 days).
* Lock **Lists** sheet with a known admin password; distribute a “Change Request” process.
* Introduce a **Request ID** (UUID formula approximation) to support dedupe.

---

## 4) Playbook (v0)

**Actors:** Requestors (staff), Admin (you), Reviewers (committee).

**Daily Use**

1. Open workbook → **Form** sheet → fill blue cells.
2. Option A: Copy the line to next empty row in **Data**.
3. Option B: Use **Data > Form** on the **Data** sheet to add/scroll/edit records safely.
4. Save to the shared location.

**Governance**

* Only Admin edits the **Lists** vocabulary.
* Changes to schema require Admin approval; track changes in a CHANGELOG tab (optional).

**Quality Checks (weekly)**

* Sort **Data** by Date descending.
* Filter for blanks in Descriptor/Vote.
* Scan duplicates (Resource + Requestor).

**Release Cadence**

* **v0.1:** Add Pivot & Filters + conditional formats.
* **v0.2:** Introduce Request ID & simple dedupe filter view.
* **v0.3:** Export CSV macro‑free instructions (documented steps); optional Power Query report (no macros).

---

## 5) Admin Notes

* To change controlled lists, go to **Lists** and add items within the existing ranges.
* If you expand lists, update the named ranges (Formulas → Name Manager) accordingly.
* Avoid unprotecting sheets unless absolutely necessary; re‑protect after edits.

---

## 6) Next Steps

1. Confirm lists for **Descriptor**, **For FY**, **Vote**.
2. Decide on Request ID approach (sequential vs. timestamp key) for v0.2.
3. Approve v0.1 enhancements (Pivot & Filters, conditional formats, duplicate flags).
