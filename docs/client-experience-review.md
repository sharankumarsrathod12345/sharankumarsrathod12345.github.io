# Client experience review — 16 November 2026

## Delivered

Nine case-study summary blocks now come from `content/projects.json`. Each gives a decision, an evidence-backed takeaway and a next step. Figures are taken from existing published case-study evidence; this pass does not claim a new native SQL or Tableau execution.

The homepage business-need filter maps clients to relevant projects. Search can narrow the recommendation; choosing a tool filter clears the business need. Four featured projects remain the default.

Compact-screen improvements include 16px form text, 44px project-link targets, wrapping preview controls, readable hero metadata and consistent asset versions across case studies. Original SQL, datasets, notebooks and workbooks were not edited.

## Validation

- Local structural audit: 11 pages passed with no detected missing local links or image assets.
- JavaScript syntax and summary synchronization: passed.
- Regression experiments: a deliberately missing `srcset` image and a missing JavaScript preview asset both caused the audit to fail. Both fixtures were removed before publication.
- Browser: homepage at 360px and 390px frame widths; customer case study at 360px and 768px frame widths. Measured document scroll width did not exceed client width on the inspected pages. Frame scrollbars reduce the content viewport by 15px.
- Browser interactions: business needs returned two customer projects and one HR project; HR viewer opened and next-image navigation worked.
- Existing external links have an optional reachability checker; no claim is made that all remote destinations were checked in this pass.

## Boundaries

No physical iPhone/Android testing, throttled network benchmark, Core Web Vitals measurement, or full WCAG conformance assessment. The workflow checks explicit selected colors and byte budgets, not every computed color or total page transfer size. The existing GitHub Pages publishing workflow is unchanged and is not gated on the quality job. No new recording or client-impact claim was produced.
