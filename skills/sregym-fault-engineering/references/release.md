# Check release readiness

Treat publication readiness as an evidence check, not a documentation exercise.

## Require

- The registry entry constructs the intended problem and application.
- Injection produces the documented state and stable symptom on the live cluster.
- The unmitigated oracle fails.
- Intended and materially equivalent safe mitigations pass.
- Plausible destructive or incomplete mitigations fail.
- Durability is tested when the incident can recur after restart, rollout, admission, bootstrap, or controller reconciliation.
- Consequential cluster-scoped, node-scoped, persistent, and cross-namespace state is recoverable.
- Agent-visible evidence does not disclose planted answers or the expected repair.
- Required data, authorized operations, and response semantics remain correct. Readiness and SLOs alone do not prove these properties.
- The workload and measurement path distinguish rejected, accepted, pending, and completed work.
- Oracle probes do not cause the observed incident or alter the repair outcome.
- Focused tests and the relevant broader suite pass.
- On the final relevant source, a known-valid mitigation passes through the normal Conductor lifecycle with setup and observers active. A known-invalid state fails for the intended reason.
- Raw evaluator output is archived for those submissions. A submission acknowledgement, trajectory-only view, or result boolean is insufficient.
- Oracle unit fixtures match the live post-setup topology for every Service, Endpoint, controller, and cross-namespace resource the oracle assumes.
- Fault documentation and live-testing notes describe the current behavior rather than an obsolete implementation.
- Published images and consumer pins match the tested source. Required manifests are accessible without maintainer credentials.
- Every promised architecture exists in the published index. Native runtime qualification and deferred execution tests remain explicit.

Keep a compact evidence map: claim, scenario, source revision or hash, image, environment, raw artifact, and limitation. Existing artifacts remain useful only when relevant dependencies are unchanged.

For a shared change, include representative existing consumers and the original application when port behavior differs. A full model campaign is not required by default.

## Report

State one of:

- **Ready:** no known issue can materially invalidate diagnosis, mitigation scoring, repeatability, or shared-cluster safety.
- **Ready with limitation:** a bounded, documented edge case does not undermine the intended benchmark lifecycle.
- **Not ready:** identify the concrete blocker, unsafe scenario, and required correction.

Do not block publication for harmless state that guaranteed namespace teardown removes. Do block for false-positive scoring, unreliable injection, information leakage, or residual state outside that teardown boundary.

Also block publication for rejection of a known-valid repair or repeated unexplained evaluator exceptions. Repeat the standard-runner gate after the last relevant change.

Separate merge readiness from experiment conclusions. Model pass rates do not prove task validity, oracle correctness, or unchanged difficulty. State what empirical testing supports without claiming universal coverage.
