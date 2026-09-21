# Reliable publishing and document conversion

Original ACO operational method · v0.6.0. Select for the relevant task; do not load every playbook.

## Establish the publication contract
Identify source of truth, editor/approver, format, audience, delivery channel, edition/version and rights. Distinguish a working manuscript from a final proof or scanned source. Use existing document tooling first; choose a new pipeline only if it solves a real production problem.

## Intake and extraction
Extract native text and structure before considering OCR. OCR is a last resort for image-only/scanned material and needs uncertainty/spot checking; do not run it repeatedly over already usable text. Keep source files unchanged. Docling is an optional structure-extraction tool, not a guarantee of correct table order, footnotes or captions. Work locally where privacy requires it; model downloads and cloud services need explicit review.

## Conversion choices
Pandoc suits structured format conversion; Quarto suits reproducible multi-output publications; Paged.js can support designed HTML-to-print pagination. These are alternatives or a deliberate pipeline, not three mandatory dependencies. Validate templates, installed versions and fonts. Do not run untrusted embedded code, macros or notebook cells merely to read a document.

## Editorial and production QA
Track captions, credits, citations, image licences and approval status. Check heading hierarchy, reading order, links, tables, index/cross-references and bibliography. Inspect rendered pages for missing glyphs, widows, crop/bleed issues, image resolution and page breaks. Validate EPUB navigation/accessibility with tools actually available. Print production and digital accessibility have different acceptance criteria.

A conversion that exits successfully is not a proofread publication. An identifier request is not an assigned ISBN. Do not promise printer acceptance without the printer's actual specifications.

## Output and memory
Deliver the requested document formats and editable source as appropriate, with version and known limitations. Store one canonical publication reference in ACO.md. Do not create permanent extracted-text, summary and review-note files for every source by default. Actual masters, permissions and final proofs are meaningful artifacts, not memory waste.

## References and use boundary
The linked sources inform scope and factual tool selection. Their courses, software, skill bundles and protected text are not included or relicensed by ACO. Recheck current terms before external reuse.

- [Docling](https://github.com/docling-project/docling)
- [Pandoc](https://github.com/jgm/pandoc)
- [Quarto](https://github.com/quarto-dev/quarto-cli)
- [Paged.js](https://github.com/pagedjs/pagedjs)
