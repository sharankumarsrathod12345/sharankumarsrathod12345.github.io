# Portfolio refinement and audit

Reviewed: 13 November 2026. This is a bounded website and evidence review, not a claim of full WCAG conformance, a Lighthouse score, or native execution of every analytical deliverable.

## Published improvements

- Replaced two large announcement panels with one compact collection row.
- Added a direct live Tableau demo link near the hero actions.
- Added readable evidence summaries to all nine project cards, outside the cover images.
- Added dedicated E-commerce and Global Data Jobs case studies. All nine projects now have case-study pages.
- Added a consistent decision / inspectable work / next-step brief to each case study.
- Added a source and validation index that distinguishes checked results, historical validation records, and outstanding work.
- Preserved the existing cover originals and analytical source files.

## Performance checks

The hero dashboard PNG was 145,403 bytes. Its WebP display version is 56,970 bytes, approximately 60.8% smaller. The original remains available. Nine responsive mobile cover variants total 305,754 bytes (about 34 KB each on average). Source images retain their complete compositions; no redesign or crop was introduced.

HTML image dimensions are declared, the hero is prioritized, and below-the-fold card images are lazy-loaded. The shared enhancement JavaScript is about 9 KB and has no external animation dependency. `docs/site-checks.json` records current uncompressed asset sizes and enforced budgets. These are transfer-size improvements, not measured real-user speed or Core Web Vitals results.

## Accessibility and structural checks

`python scripts/audit_site.py` passed for 11 pages: the homepage, nine case studies, and the evidence index. It checks local links and HTML fragments, one H1 per page, unique IDs, image descriptions, document language and viewport metadata, inline JavaScript syntax, selected text contrast pairs, and asset budgets. Shared JavaScript syntax passed `node --check assets/experience.js`.

Selected body/muted/link color pairs in both themes exceeded 4.5:1; the lowest tested ratio was 6.19:1. This is not an audit of every pixel, image text, or possible state. Visible focus indicators and reduced-motion styling are retained.

Browser checks passed for desktop and a 390px phone-width iframe (375px content area with the browser scrollbar): all-project and Excel filters, search, dedicated case-study navigation, image preview opening with Enter, Escape closing, source/evidence navigation, and light/dark themes. No horizontal overflow was observed on the mobile homepage or Global Data Jobs case study. This is responsive browser QA, not physical-device testing.

## Analytical evidence

`docs/data-checks.json` records SHA-256 hashes and the exact repository snapshots used. `scripts/check_snapshots.py` reproduces the checks with a supplied HR CSV and Gold-export folder.

- HR: 8,950 unique employee IDs; 7,984 active plus 966 terminated reconciles to all records.
- SQL exports: 60,398 sales rows, 27,659 distinct orders, sales amount 29,356,250, and 60,423 units. Product/customer dimension keys are unique; each fact row matches exactly one dimension row, preserving row count and sales.
- Bikes: 96.46% of sales value; accessories: 59.77% of units. Nineteen missing order dates account for 4,992 in sales value. Currency is unspecified.
- Python: existing repository validation records dated 25 October 2026 were inspected and linked. They report 9 executed cells / 9 reconciled CSVs for customer analysis and 7 cells / 5 CSVs for movie analysis. These notebooks were not rerun in this pass.

## Open items requiring additional evidence

- Native SQL Server execution and reconciliation of report views. Original SQL is preserved at the author's request.
- Excel and sales Tableau source-to-dashboard reconciliation, including filter and refresh behavior.
- HR completed-birthday age calculation and explicit as-of-date policy. The label is fixed; the current workbook's year-boundary limitation is disclosed.
- Exact original lesson/dataset URLs and reuse terms where existing source notes explicitly say they are unconfirmed. No provider or license has been inferred from filenames.
- Full Lighthouse/Core Web Vitals testing, comprehensive assistive-technology testing, and additional physical devices/browsers.

## Ongoing checks

`.github/workflows/site-quality.yml` runs the structural audit and shared JavaScript syntax check on relevant pushes and pull requests. The local checks passed before publication; a cloud workflow run should be inspected separately rather than assumed successful from the presence of the workflow file.
