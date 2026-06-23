# 01 — Project Charter

## Problem Statement
Manual AP invoice processing is slow, error-prone, and labor-intensive. Costs and cycle times scale poorly with invoice volume, and exception handling (mismatches, duplicates, missing POs) consumes disproportionate staff time.

## Objective
Design and prototype an AI-powered AP pipeline that:
1. Extracts invoice data via computer vision (no template-specific OCR tuning)
2. Validates extracted data against vendor and duplicate-invoice records
3. Matches invoices to purchase orders within a defined tolerance
4. Routes only genuine exceptions to a human, auto-approving clean matches
5. Measures accuracy and touchless-processing rate against industry benchmarks

## Scope
**In scope:** PO-backed and non-PO invoices, single currency (USD), 2-/3-way matching logic, vendor and duplicate validation, exception routing, mock ERP posting (ledger write), synthetic data generation for testing.

**Out of scope:** Real ERP integration, multi-currency/multi-tax-jurisdiction logic, live payment execution, dedicated fraud-detection controls (noted as a future-roadmap item).

## Success Metrics
- Straight-through processing (STP) / touchless rate
- Extraction field-accuracy vs. ground truth
- Exception rate, broken down by reason code
- Simulated cost and cycle-time savings vs. manual baseline (using cited industry benchmarks, see `02-current-state-analysis.md`)

## Stakeholders (simulated)
- AP clerks/processors (exception review, manual approval)
- AP manager (approval thresholds, policy)
- Controller/Finance lead (ROI, controls, audit trail)
