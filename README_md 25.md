# 🧾 AI-Powered Accounts Payable (AP) Invoice Processing Automation

> An end-to-end AI pipeline that reads invoices, validates them, matches them to purchase orders, and routes only genuine exceptions to a human — built and stress-tested against a deliberately messy synthetic dataset.

![status](https://img.shields.io/badge/status-complete-brightgreen) ![extraction](https://img.shields.io/badge/extraction-Claude%20Vision-1F6F78) ![touchless](https://img.shields.io/badge/touchless%20rate-62%25-4F7A56) ![accuracy](https://img.shields.io/badge/extraction%20accuracy-100%25-4F7A56)

## Results — actual test run (13 invoices)

| Metric | Result |
|---|---|
| Touchless (auto-approved & posted) | **62%** (8 / 13) |
| Extraction accuracy vs. ground truth | **100%** |
| Exceptions correctly flagged | **4 / 4 planted scenarios** |
| Total value posted | **$8,413.97** |
| Projected cost reduction at scale | **~72%** vs. manual baseline |
| Projected time reduction at scale | **~82%** vs. manual baseline |

<img src="chart_outcome_breakdown.png" width="420">

Full methodology, benchmarks, and ROI math: [`AP_Invoice_Automation_Capstone_Report.pdf`](./AP_Invoice_Automation_Capstone_Report.pdf)

## What this is

Manual AP invoice processing is slow and expensive — industry benchmarks cite $10–15+ per invoice and multi-day cycle times for manual workflows. This project builds a working prototype that:

1. Renders synthetic invoices as **images** (3 visual layouts + simulated scan noise) — not clean structured data
2. Reads them directly with **Claude's vision model** — no per-vendor OCR templates
3. Validates, matches against purchase orders (3% tolerance), and routes exceptions
4. Auto-approves clean matches; posts to a mock ledger
5. Reports live KPIs: touchless rate, extraction accuracy, exception breakdown

The test dataset is deliberately adversarial — duplicate invoices, PO amount mismatches, an unapproved vendor, non-PO invoices — to verify the pipeline correctly *rejects* bad invoices, not just processes the easy ones.

## Architecture

```
Invoice (image)
   ↓
AI Extraction        Claude (vision): vendor, invoice #, date, line items, tax, total
   ↓
Validation           vendor master lookup · duplicate check · required-field check
   ↓
PO Matching          2-/3-way match, 3% amount tolerance
   ↓
Exception Routing    mismatches flagged with reason codes
   ↓
Approval Simulation  auto-approve under threshold + clean match, else → human
   ↓
ERP Posting (mock)   write to ledger with GL code
   ↓
Analytics Dashboard  STP rate · accuracy · exception trends · cycle time
```

## ⚠️ Running the live demo

`dashboard.html` calls Claude's API to read each invoice image. **That call only works when the file is opened as an artifact inside Claude.ai** — the platform proxies the request without an exposed API key.

Opening the file directly in a browser (or hosting it on GitHub Pages as-is) will fail at the extraction step — there's no key and no backend to call Anthropic's API securely.

- **To run it:** open it in Claude.ai (upload `dashboard.html` to a chat)
- **To watch it work without running it:** see the demo video — [link]
- **To make it a real public live demo:** put an API key behind a small serverless proxy (Vercel/Cloudflare Worker) — not included here, noted as a roadmap item

## Project structure

```
ap-invoice-automation/
├── README.md
├── AP_Invoice_Automation_Capstone_Report.pdf   final report: charter, benchmarks, architecture, results, ROI
├── dashboard.html                              interactive working prototype
├── core-logic.js                               unit-tested business logic, standalone for code review
├── generate_charts.py                          regenerates the chart images
├── build_report.py                             regenerates the PDF report
├── chart_outcome_breakdown.png
├── chart_cost_projection.png
├── chart_time_projection.png
├── 01-project-charter.md
├── 02-current-state-analysis.md
└── 03-architecture-and-tech-stack.md
```

## Business rules

| Rule | Value | Rationale |
|---|---|---|
| Amount tolerance | 3% | Allowable variance between invoice total and matched PO |
| Non-PO auto-approval limit | $750 | Low-value, no-PO invoices route to auto-approval |
| Auto-approve limit | $5,000 | Matched invoices below this post automatically |
| Duplicate detection | Vendor + invoice # | Flags repeat submissions within a batch |
| Vendor approval check | Vendor master flag | Unapproved vendors flagged regardless of match quality |

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Extraction | Claude (vision) | Handles varied/messy layouts, no per-template OCR tuning |
| Business logic | Vanilla JavaScript | Portable, no build step, unit-testable in isolation |
| Visualization | Chart.js | Lightweight, sufficient for KPI/exception charts |
| Data | Synthetic generator (in-app) | Reproducible; includes deliberate exception scenarios |
| Report | Python (reportlab + matplotlib) | Scripted, reproducible PDF generation |

## Limitations

- 100% extraction accuracy measured on 13 invoices — not yet validated at production scale
- ERP posting is mocked (no real ledger/payment integration)
- Single currency, single entity; no fraud-detection layer
- Live demo depends on Claude.ai's request proxy (see above)

## Roadmap

- [ ] Real ERP integration (NetSuite / SAP / QuickBooks)
- [ ] Production-scale accuracy testing (100s–1000s of invoices, multiple languages)
- [ ] Fraud-detection controls (bank-detail-change alerts, anomaly detection)
- [ ] Multi-currency / multi-entity support
- [ ] Backend-hosted public live demo
- [ ] Configurable multi-level approval workflows

## License

No license file included yet — add one (MIT is a common choice for portfolio projects) if you want others to freely reuse this code.

---

Built as a self-directed capstone project exploring AI-powered finance process automation.
