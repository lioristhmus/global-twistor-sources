# Release v1.0.1

Prepared on 2026-11-15 for publication on GitHub.
[Release](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0.1)
and [publication/download record](github-publication.json).

This patch changes reference-list markup for automatic extraction. All 25
reference entries, their order, and the mathematical text are unchanged from
v1.0. The standalone TeX now uses `thebibliography` with unique `\bibitem`
keys. Existing author-year text and original reference anchors remain.
The PDF remains 72 pages; the TeX preceding References is byte-identical to
v1.0 and PDF pages 1–69 have identical extracted text. The vendored Markdown
exporter applies the bibliography conversion reproducibly.

The 68 saved computational checks retain their original mathematical code,
inputs and results. Only the correspondence's paper version/hashes are
rebound to v1.0.1; all mapped formula numbers and pages remain unchanged.
No mathematical job was rerun.

The v1.0 tag, commit and Release attachments are preserved. This publication
step is limited to GitHub; Zenodo, Hexagon and ORCID remain at their recorded
v1.0 states. No DOI for v1.0.1 is claimed.

---

# Release v1.0

Published on GitHub: 2026-11-13T06:06:34Z.
[Release and downloads](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0).
Frozen release commit: `713e6feb37dad4e42ac5ca1acf237147cf42e1f5`.
[Public download verification](github-publication.json).

Archived on Zenodo on 2026-11-13 with the identical PDF, three ZIP files and
SHA-256 list. Version-specific DOI:
[10.5281/zenodo.24186390](https://doi.org/10.5281/zenodo.24186390).
[Zenodo public download verification](zenodo-publication.json).
The GitHub tag and attached release files are unchanged.

Published on Hexagon: [2611.00425v1](https://hexagonmath.org/2611.00425v1).
The paper is listed on [ORCID](https://orcid.org/0009-0004-7908-9876), linking
to that Hexagon record. Zenodo's related works now include the same Hexagon
version URL. Its DOI, version and archived files are unchanged.

Publication links checked on 2026-11-14. The default branch maintains current
publication metadata and its corresponding hashes. Paper and computational
files, frozen tags and attached PDF/ZIP/checksum assets are preserved. No
mathematical job was rerun for this metadata update.

The preparation record below describes the reviewed snapshot retained in the
published tag and attached archives.

Prepared locally on 2026-11-13. This preparation creates no public GitHub
repository, Release, DOI or submission.

- Paper: version **1.0**.
- Computational supplement: version **1.0.0**, included in this same release.
- Planned repository: https://github.com/lioristhmus/global-twistor-sources
- Planned release tag and citation URL: https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0

The paper starts from the preserved v0.9.8-draft Markdown, SHA-256
`559a830c073a079dac2ce8650c2c01779711cf58e3302805065e7ae35d5be0c7`. Changes are limited to release metadata, the computational-supplement
bibliography entry, and an AI-use disclosure with a computational-check summary. Mathematical text, assumptions,
equations, symbols, anchors and statement numbering are retained.

The supplement starts from the preserved 1.0.0-rc.2 ZIP, SHA-256
`151bea469f4fdca0539e95c7fb486104c0efc471bf85e89e5c577fedde9eeb96`.
Calculation code, actual executed inputs, environment evidence and output records
are retained. The check index and printed equation/page locators are updated to
the accompanying v1.0 PDF. No mathematical job is rerun or represented as new.
Historical rc.1/rc.2 labels in execution provenance describe the actual runs.

The local license proposal follows the previous local-paper package: CC BY 4.0
for the paper/data/docs and Apache-2.0 for executable/build code, with explicit
file scopes in LICENSES.md. The package includes the Apache-2.0 license text
and a CC BY 4.0 notice linking to the authoritative legal code.

The release asset directory prepared alongside this repository contains the PDF,
paper-source ZIP, computational ZIP, combined repository ZIP and their hashes.
GitHub's generated source archives need not have the same bytes as these
deterministic, locally checked ZIP files.

The published v1.0 tag and attached paper/ZIP assets retain this reviewed
snapshot. Later publication-metadata updates on the default branch do not replace
those release artifacts. No Zenodo, Hexagon or ORCID operation was performed as
part of the GitHub publication.
