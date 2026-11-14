# Global twistor sources for analytic Einstein spacetimes

**Lior Isthmus · manuscript v1.0 · computational supplement 1.0.0**

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

## Verify the downloaded files

```sh
python3 scripts/validate_release.py
```

This checks local file hashes, the paper-to-check mapping and the saved execution
records. It does not run the mathematical jobs. Reproduction commands and their
resource requirements are documented in `computations/README.md`.

## Citation

Use [CITATION.cff](CITATION.cff) for the paper and
[computations/CITATION.cff](computations/CITATION.cff) for the checks. The
version-specific target is [GitHub release v1.0](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0).

**Publication status:** [Release v1.0](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0) is public.
The paper PDF, three ZIP packages and SHA-256 list are attached to the release.
Public downloads were checked against the reviewed files; see the
[publication and download-verification record](docs/github-publication.json).
The v1.0 tag identifies the reviewed paper and computation snapshot. Publication
metadata on the default branch is maintained separately.

The same five files are archived on [Zenodo](https://zenodo.org/records/24186390).
Version-specific DOI: [10.5281/zenodo.24186390](https://doi.org/10.5281/zenodo.24186390).
All versions: [10.5281/zenodo.24186389](https://doi.org/10.5281/zenodo.24186389).
Zenodo public downloads match the GitHub release assets byte for byte; see the
[Zenodo publication and verification record](docs/zenodo-publication.json).

The paper is also published as [Hexagon 2611.00425v1](https://hexagonmath.org/2611.00425v1)
and listed on the author's [ORCID record](https://orcid.org/0009-0004-7908-9876).
Zenodo's related works link to this Hexagon version. Publication links were
checked on 14 November 2026; see [current status](docs/release-status.json).
The frozen v1.0 tag, paper files and release attachments are unchanged.
