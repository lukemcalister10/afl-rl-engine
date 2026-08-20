# SELF-REVIEW of PLAN_v1 (supervisor, before the independent review) — 9 findings, all folded into v2

S1 [1a, MATERIAL]. CI cross-host float hazard. Board builds are md5-pinned; the env pin is byte-exact
numpy+OpenBLAS, but BLAS kernels dispatch by CPU — GitHub-hosted runners are a different host class,
and the existing CI estate already contains an "independent-host negative-control battery," i.e. the
project has prior knowledge that host matters. v1's "gates run on every push" overpromises. FIX: scope
CI gates to host-insensitive checks (committed-artifact hashes, manifest coherence, contract check,
laws/register lint, runner in identity mode). Full board REBUILDS in CI only if first proven
reproducible on that runner class — as its own measured act, never assumed.

S2 [4b, MATERIAL]. The fire drill criterion inherits S1. A years-later rebuild-from-tag can fail md5
because floats drifted, not because rollback is broken. The v783 ruling already says artifact tags are
BYTES, not rebuild recipes — the plan should align: PRIMARY rollback = restore the tagged artifact
bytes + boot guards accept them; the drill proves THAT. Rebuild-from-source parity is a secondary,
best-effort check, its failure a finding about reproducibility, not about rollback.

S3 [3b]. Before changing the register's form, ENUMERATE ITS READERS (pens grep marker strings; anything
else parsing the file must be found first). Pre-act added: reader inventory, then design the new form
to keep every found reader working or migrate it in the same act.

S4 [Sequencing]. Timeline honesty: historical evidence is that everything here takes longer than
estimated. Estimates stated as ±2x guesses; calendar time for P2 soak is dominated by ROUNDS, not
sessions. No promise made on elapsed weeks.

S5 [4d]. Pruning cadence should be denominated in ROUNDS, not weeks — sessions are episodic and rounds
are the project's real clock. (Owner still picks the number, G3.iii.)

S6 [1c]. The claims CHECKER needs its own negative control: a claims file carrying one deliberately
false claim must fail the checker in CI/self-test. Without it, a silently broken checker green-lights
everything (the exact failure mode of the pre-M1a "suite").

S7 [2a/2b, MATERIAL]. Two commands must not become two divergent scripts — the repo's own history shows
hand-mirrored pairs drift (the two mirrored loaders; the emitter forks). FIX: ONE landing-transaction
library; `land lever` and `land round` are thin entry points over shared writers-of-record calls.

S8 [1a]. Red CI must be LOUD or it rots — the estate's one permanent-red workflow is the proof that
silent red becomes furniture. FIX: red on main notifies the owner (GitHub notification at minimum) and
any active session treats it as a standing halt on landings until attributed.

S9 [G1]. Falsifier precision: process changes legitimately move identity/administrative artifacts
(contract sha, manifest fields). G1 restated: the BOARD and every value-bearing artifact byte-unmoved;
identity-file churn allowed but enumerated per change; anything outside the enumerated set = halt.

Judgement withheld for the independent reviewer: whether the package boundaries are right; whether
anything in the plan repeats a mistake recorded in the register that I've stopped seeing; whether the
plan's own process (this review chain) is proportionate.
