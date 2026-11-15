# Global twistor sources for analytic Einstein spacetimes

**Lior Isthmus · manuscript v1.0.1 · computational supplement 1.0.0**

This repository contains the paper and its accompanying reproducible symbolic
checks. The paper globalizes the local analytic Einstein correspondence using
source atlases, null monodromy and parametrized incidence. It also proves Nariai
obstructions to Hausdorff whole-sky carriers and to the specified exact-support
module realization.

- [Read the paper (PDF)](paper/manuscript.pdf).
- [Canonical manuscript (Markdown)](paper/manuscript.md),
  [standalone TeX](paper/manuscript.tex) and [build instructions](paper/BUILD.md).
- [Computations and reproduction instructions](computations/README.md).
- [Check-to-proposition/equation correspondence](computations/CHECKS.md),
  [machine-readable index](computations/checks.json) and
  [recorded runs](computations/RUNS.md).
- [Release information](docs/RELEASE.md) and [licenses](LICENSES.md).

The 68 computational checks cover selected exact identities and explicit metric
cases. The general Gaussian jet checks and the two concrete Sage metric examples
are both included. The analytic, topological and categorical proofs remain in
the paper; these checks are not a formal verification of the whole manuscript.

The previous local paper is available at
[Hexagon 2611.00123v1](https://hexagonmath.org/2611.00123v1), with its own
[repository](https://github.com/lioristhmus/projective-twistor-einstein-germs).
That v1 record is the mathematical baseline cited by this paper. The local
paper's current v1.1 edition, adding computational references, is
[Hexagon 2611.00123v2](https://hexagonmath.org/2611.00123v2).
Its mathematical scope and release history remain separate. Any future Lean
formalization will use a separate repository tied to an exact paper version.

Version 1.0.1 marks the unchanged 25 reference entries as standard TeX
`\bibitem` entries for automatic extraction. Mathematical text and reference
content/order are unchanged. The computations retain their original code,
inputs and recorded results.

## Verify the downloaded files

```sh
python3 scripts/validate_release.py
```

This checks local file hashes, the paper-to-check mapping and the saved execution
records. It does not run the mathematical jobs. Reproduction commands and their
resource requirements are documented in `computations/README.md`.

## Citation and publication history

Use [CITATION.cff](CITATION.cff) for manuscript v1.0.1 and
[computations/CITATION.cff](computations/CITATION.cff) for supplement 1.0.0.
The current GitHub release is [v1.0.1](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0.1).
It includes the reviewed PDF, source package and SHA-256 checksums.
See the [current publication record](docs/github-publication.json).

The preserved [v1.0 release](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0)
and its attachments remain unchanged. That version is archived on
[Zenodo](https://doi.org/10.5281/zenodo.24186390), posted as
[Hexagon 2611.00425v1](https://hexagonmath.org/2611.00425v1), and listed on
[ORCID](https://orcid.org/0009-0004-7908-9876). These links identify v1.0;
v1.0.1 has not yet been submitted to those services and has no new DOI.
The [previous publication record](docs/github-publication-v1.0.json),
[Zenodo verification](docs/zenodo-publication.json) and
[version-specific status](docs/release-status-v1.0.json) remain available.

[Release notes](docs/RELEASE.md) describe the bibliography-only patch and
[current status](docs/release-status.json) tracks each service separately.
Actual Hexagon reference extraction remains to be checked after a later
submission; this GitHub release does not change the existing Hexagon record.
