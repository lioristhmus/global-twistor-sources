# Recorded executions included in supplement 1.0.0

All records below are preserved from rc.2; no mathematical jobs were rerun for release packaging. "Fresh rc.2" refers to that earlier execution, not a new v1.0 run.

The original seven jobs and their 57 IDs are retained byte-for-byte from rc.1, with the same executed code, inputs and runtime files. They were not rerun. The three universal-jet jobs below are fresh rc.2 executions. The two concrete Sage Gaussian metrics and their fourteen checks remain included.

| Job / origin | Checks | Status | Worker seconds | Controller seconds | Cgroup memory peak (bytes) | PID peak |
| --- | --- | --- | --- | --- | --- | --- |
| a-nariai / rc.1 retained | 3 | [PASS](results/a-nariai/result.json) | 0.933 | 10.119 | 73084928 | 7 |
| a-tractor / rc.1 retained | 1 | [PASS](results/a-tractor/result.json) | 0.185 | 9.392 | 67858432 | 7 |
| a-bianchi / rc.1 retained | 1 | [PASS](results/a-bianchi/result.json) | 0.167 | 9.388 | 67448832 | 7 |
| b-nariai-tractor / rc.1 retained | 11 | [PASS](results/b-nariai-tractor/result.json) | 7.716 | 17.052 | 334032896 | 18 |
| b-quadric-infinity / rc.1 retained | 27 | [PASS](results/b-quadric-infinity/result.json) | 7.355 | 16.661 | 302067712 | 18 |
| b-gaussian-d / rc.1 retained | 7 | [PASS](results/b-gaussian-d/result.json) | 4.914 | 14.268 | 332599296 | 18 |
| b-gaussian-o / rc.1 retained | 7 | [PASS](results/b-gaussian-o/result.json) | 7.705 | 17.039 | 319774720 | 18 |
| general-jet / rc.2 fresh | 7 | [PASS](jets/results/general-jet/result.json) | 0.371 | 9.664 | 69914624 | 7 |
| third-time / rc.2 fresh | 1 | [PASS](jets/results/third-time/result.json) | 0.659 | 9.91 | 71430144 | 7 |
| third-space / rc.2 fresh | 3 | [PASS](jets/results/third-space/result.json) | 1.581 | 10.921 | 73785344 | 7 |

Both [original-driver](results/failure-probe/result.json) and [new jet-driver](jets/results/failure-probe/result.json) false-check probes retain actual FAIL results and exit 1. They are separate from the 68 mathematical checks.

All runs used the pinned SageMath 10.9 image, Python 3.12.3 and SymPy 1.14.0, with linux/amd64 emulation on macOS arm64. Their selected Docker/VM/service facts, inside-container limits, input hashes and actual output are in each environment/log/result triplet.

The common limits remain memory plus swap 1,999,998,976 bytes, swap zero, 1 CPU, PID 32, network none, read-only root, OOM killer enabled and restart disabled. Command TERM117/KILL+3 seconds, outer PID1 297 seconds, host300 seconds, bounded tmpfs/files/logs. Each final run confirms actual termination, removal and own-lock release. New jobs were serial; no VM/service setting or image was changed.

The original arbitrary-function Sage Gaussian attempt exceeded the cap; the rc.1 examples narrowed its input scope and remain labeled as examples. The rc.2 universal jets restore general differential-identity coverage by the reduction in JET-SCOPE.md, with lower measured resource use. The original preparation also had startup/helper failures; these remain in private preparation records and are not converted into PASS outputs.

The 2jet and 3jet modules share a helper. Every new job records the exact main/helper/domain-audit hashes, verifies them before import and reports the input symbol counts. The direct 3jet jobs compute the derivative of Ricci rather than assuming Bianchi. The general residual rearrangement and the direct zero identity are distinct checks.
