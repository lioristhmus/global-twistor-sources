# Building the paper

`manuscript.md` is the canonical source. The distributed `manuscript.tex` is
self-contained and can be compiled using pdfLaTeX and standard TeX packages:

```sh
mkdir -p build/tex
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=build/tex paper/manuscript.tex
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=build/tex paper/manuscript.tex
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=build/tex paper/manuscript.tex
```

To regenerate TeX and PDF from Markdown, run from the repository root:

```sh
python3 scripts/build_paper.py --output-dir build/paper
```

This uses the vendored standard-profile Pandoc export pipeline and pdfLaTeX.
Required programs: Python 3, Pandoc, pandoc-crossref and pdfLaTeX. All bibliography
entries are embedded in the Markdown. No network access or external bibliography
download is needed. The original build used Pandoc 3.9 and TeX Live 2026;
the exact tool versions are recorded in `docs/build-environment.json`.

The release-specific TeX preparation removes the redundant body title while
retaining its anchor, promotes the original section hierarchy, applies the
shared Abstract heading, handles the Pandoc keyword wrapper and lets long
bibliographic links wrap. These are export-only operations. The maintained
layout helper wraps long formulas without changing their token order.
See `docs/build-origins.json` and `scripts/prepare_release_tex.py`.

Builds in another TeX/Pandoc environment may paginate differently. The distributed
PDF hashes and the computational correspondence identify this exact release.
