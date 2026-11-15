# Computational supplement for Global twistor sources

Version **1.0.0**, accompanying manuscript **v1.0.1** by Lior Isthmus, in the
same repository and release. [Read the paper](../paper/manuscript.pdf),
[canonical Markdown](../paper/manuscript.md) and
[check-to-manuscript table](CHECKS.md).

The source SHA-256 is `4dfa6c2966485a8eff8c689ab26697e02963508925b6b8ad7320287802307a5b`.
Printed equation numbers and pages are read from the accompanying v1.0.1 PDF and
bound to its source/TeX/PDF hashes in [MANUSCRIPT-LOCATORS.json](MANUSCRIPT-LOCATORS.json).

The 68 saved checks are inherited from the audited rc.2 package. No mathematical
job was rerun for this v1.0 packaging step. Historical references to retained
rc.1 runs and fresh rc.2 runs below identify their actual execution provenance.

## Contents and scope

- [CHECKS.md](CHECKS.md): every stable check ID, manuscript locator,
  implementation, input, expected result, actual result and scope.
- [checks.json](checks.json), [inputs.json](inputs.json) and [INPUTS.md](INPUTS.md):
  machine-readable index and explicit embedded symbolic inputs.
- [CONVENTIONS.md](CONVENTIONS.md): curvature, signature, index and normalization conventions.
- [RUNS.md](RUNS.md), [results/](results/): fresh execution summaries, actual JSON-lines
  output, environment/resource evidence and exit status.
- [provenance.json](provenance.json): source hashes, adaptation and original targets.
- [environment.lock.json](environment.lock.json): pinned runtime and limits.
- [SHA256SUMS.txt](SHA256SUMS.txt): hashes of the distributed files.
- [CITATION.cff](CITATION.cff), [LICENSES.md](LICENSES.md): draft citation and licensing status.

The package contains 68 checks: 57 retained from rc.1 plus eleven universal-jet
checks executed for rc.2. [JET-SCOPE.md](JET-SCOPE.md) supplies the general
Gaussian coordinate/jet reduction and shared-code dependencies. The checks concern exact symbolic identities and explicit metric cases:
Nariai curvature and explicit null/conic/endpoint formulas; rank-six tractor and
rank-four infinity-pair normalizations; and Gaussian curvature and contracted
Bianchi identities. The analytic, topological and categorical arguments in the
paper, including non-Hausdorffness, descent and terminality, remain mathematical
proofs rather than CAS outputs. Local-paper Q1–Q3, coefficient-bound and potential
checks are not included in this global supplement.

Two originally separate routes are retained. A was prepared with SymPy in a
Codex audit; B was prepared with SageMath manifolds/SR in a separate Claude audit.
The frozen record for B states that A was not reused. Packaging and reporting
were prepared together. This provenance is not a claim of independent formal
certification. Original review discussions and private logs are not distributed.

| Topic | A: SymPy route | B: SageMath route |
| --- | --- | --- |
| Real Nariai | Coordinate Ricci and one mixed Weyl component | Manifold Ricci, scalar and Weyl |
| Tractor | Arbitrary Lambda, algebra in a parallel frame | Nariai coordinate connection, curvature and normality |
| Quadric/conic | Several exact identities and a nonvanishing reduction | Extended set, including a polynomial-ideal radical test |
| Nonclosed sequence | Initial energy and limiting endpoint | Return-time, velocity and limiting-direction formulas |
| Infinity pair | Not implemented | Product, Pfaffian; ranks at c=1 and c=0 |
| Bianchi | Arbitrary symmetric K at a spatial-normal point, E_ij=0 | Full residual identities in two explicit polynomial metrics |

The original executions targeted v0.9/v0.9.1, whose relevant formulas remain
unchanged in the relevant formulas of manuscript v1.0. The 57 distributed rc.1 outputs and their executed runtime,
code and input files are retained byte-for-byte; they are not relabeled as new
rc.2 runs. The eleven universal-jet outputs are fresh rc.2 executions. The direct
3jet module imports the 2jet helper; this is one complementary shared-code route,
not two independent implementations. The retained Sage polynomial examples are
a separate curvature route. All six symmetric metric entries and all four
coordinate directions are covered by the universal-jet inputs.

## Reproduce one small job

Use an already installed Docker image matching [environment.lock.json](environment.lock.json).
The runner never pulls or builds an image and requires cgroup v2 enforcement.
From this directory, run:

```sh
python3 code/run.py --job a-nariai --out reproduced/a-nariai
```

Other jobs, run **serially**, are `a-tractor`, `a-bianchi`,
`b-nariai-tractor`, `b-quadric-infinity`, `b-gaussian-d`, and `b-gaussian-o`.
Each output directory must be new. A failed run is not retried automatically.
The original list and expected IDs remain in [jobs.json](jobs.json). For the
new universal-jet route, run serially:

```sh
python3 jets/code/run.py --job general-jet --out reproduced/general-jet
python3 jets/code/run.py --job third-time --out reproduced/third-time
python3 jets/code/run.py --job third-space --out reproduced/third-space
```

[execution-index.json](execution-index.json) connects all ten jobs to their
drivers, inputs and evidence origins. [jets/jobs.json](jets/jobs.json) lists the
three new jobs. Each helper is pinned and checked before import.

The host controller uses only Python's standard library; all mathematical
imports, symbolic construction and simplification occur inside the container.
Its `mkdir` lock is `$HOME/.local/state/math-job.lock`. All executors on a machine
must use that same lock. The parent directory must already exist. An existing
lock blocks execution and is never removed by the runner. Only its own lock is
released, after container termination and removal are confirmed.

Existing containers block a run by default. An operator may identify known
non-mathematical services with repeated `--allow-service NAME` arguments. The
runner records their limits and usage before proceeding; it does not change
service or VM configuration. Run only when no other mathematical job is active.

Each container has memory plus swap at most **1,999,998,976 bytes** (swap zero),
1 CPU, PID limit 32, network `none`, read-only root, all capabilities dropped,
OOM killing enabled and restart disabled. Tmpfs totals 256 MiB; file size and
captured output are bounded to 1 MiB, with Docker logging bounded separately.
The command receives TERM after 117 seconds and KILL after a further 3 seconds;
PID1 has an outer 297-second deadline, and the host has a 300-second deadline.
The host kills and inspects the entire container on abnormal completion. Inside
cgroup and network checks run before mathematics. No host output directory is
writable from the container.

A mathematical failure, exception, missing/duplicate check ID, timeout, OOM or
unconfirmed cleanup gives a nonzero exit. The intentional test

```sh
python3 code/run.py --job failure-probe --out reproduced/failure-probe
```

must return nonzero and record `RUNNER-FAILURE-PROBE: FAIL`. It is a runner test,
not one of the 68 mathematical checks. Its recorded failure must not be counted
as a mathematical failure or changed into a PASS result. The new jet driver
has its own saved probe:

```sh
python3 jets/code/run.py --job failure-probe --out reproduced/jet-failure-probe
```

## Verify the saved package

```sh
python3 code/verify_package.py
```

This performs only file/hash, correspondence and saved-result checks on the
host. It does not rerun mathematics. Times and memory are measurements;
mathematical tests use exact arithmetic/symbolic expressions with no floating
point tolerance. See the input profiles for domains and exceptional cases.

## Citation and publication status

[CITATION.cff](CITATION.cff) identifies supplement 1.0.0 within the published
[shared v1.0 release](https://github.com/lioristhmus/global-twistor-sources/releases/tag/v1.0).
The paper and checks are distributed together. See [license scopes](LICENSES.md)
and the repository's [publication record](../docs/RELEASE.md).
The v1.0 tag and attached archives retain the reviewed release snapshot.
Publication notices on the default branch are maintained separately.
No separate supplement DOI has been assigned.

The v1.0.1 paper changes only bibliography markup. Its source/PDF hashes are
bound in the current correspondence files; all mapped formula numbers and
pages are unchanged. The mathematical code, inputs and recorded results are
identical to v1.0. No mathematical job was rerun for this update.
