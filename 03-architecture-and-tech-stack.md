# 02 — Current-State Analysis (Industry Benchmarks)

These figures are external industry reference points used to frame the simulation's results — not measurements of any real organization. Sources are cited inline.

| Metric | Manual | Automated | Source |
|---|---|---|---|
| Cost per invoice | ~$10–15 typical; up to $40 for heavily manual workflows | ~$1–5; best-in-class ~$2–4 | Ardent Partners, *AP Metrics That Matter* (2025) |
| Cycle time | ~14.6 days average | ~3–5 days | Ascend Software, *AP Benchmarks 2025* |
| Touchless / STP rate | >60% of invoices still need human handling, industry-wide | Top performers: 60–80% touchless | Ardent Partners (via Ascend Software, 2025) |
| Error rate | Low single digits (data entry, miskeying) | Sub-1% with ML-based extraction at scale | Multiple AP research aggregators |
| Throughput | Roughly one invoice at a time through entry → routing → filing | 30+ invoices/hour | Quadient (via Parseur, 2025/2026) |

## Pain Points Mapped to This Project
1. **Slow, serial data entry** → addressed by vision-based extraction (no manual keying)
2. **Inconsistent invoice formats** → addressed by using a vision model instead of template-bound OCR
3. **Manual 3-way matching** → addressed by rules-based PO matching engine with tolerance thresholds
4. **Duplicate payments / unapproved vendors slipping through** → addressed by validation layer (duplicate detection, vendor approval check)
5. **Exception backlog with no visibility** → addressed by status-based queue + analytics dashboard

## Baseline Assumption Used in the Prototype
The prototype's cycle-time comparison chart uses a manual benchmark of ~12 minutes/invoice (consistent with the ~10–20 minute range cited across these sources) against the automated pipeline's actual run time, to illustrate relative — not absolute — savings.
