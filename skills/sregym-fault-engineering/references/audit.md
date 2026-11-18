# Audit or harden an existing fault

## Build the model

Read the registry entry, `Problem`, injector, oracle, recovery, app metadata, tests, and permitted prior notes. Record:

- intended root cause;
- injected resource transition;
- expected symptom;
- currently accepted oracle state;
- official recovery boundary.

Also record the agent-visible evidence, available repair surface, required data, and relevant observation window. Use `fault-models.md` for checks specific to the mechanism.

For authorized tests, reproduce the current behavior before implementation. For static-only requests, report code-supported risks and missing runtime evidence. Distinguish a confirmed defect from an architectural preference.

## Explore adversarial solutions

Choose scenarios from the required behavior. During a full audit, complete the applicable matrix in `live-testing.md`:

- delete the broken or required resource;
- scale the target or dependency to zero;
- leave an old healthy pod while the current rollout is broken;
- make a pod Running but not Ready;
- point a Service at the wrong ready workload;
- return a DNS answer without a working connection;
- make one endpoint work while the required set remains unsafe;
- change the checked template while admission mutates new pods;
- repair current state but leave restart or bootstrap state broken;
- bypass the required controller with a one-time manual patch;
- fabricate logs, labels, annotations, output records, or similarly weak evidence.

For data faults, include lost original records, incorrect results, and application-principal write failures. Include valid repairs with different names, constraints, topology, or newly accepted records.

Probe actual behavior: HTTP/gRPC response content, TCP connection, admission of a fresh pod, endpoint ownership, controller reconciliation, consumer progress, credential acceptance, or the fault-specific invariant.

## Audit both passes and failures

Read the command, output, evaluator reason, stored result, and cleanup evidence together. Audit successful trajectories for generic errors and workarounds as well as false-positive scoring.

Look for TLS and authentication errors, stream EOFs, failed `exec` or `cp`, repeated retries, missing submissions, missing measurements, and incomplete cleanup. An agent that works around a broken expected command does not prove regression-free infrastructure.

Classify the cause separately: agent repair, fault, application, workload, measurement, oracle, harness, or environment. Mark mixed and interrupted attempts explicitly. Do not count an incomplete attempt as an ordinary mitigation failure.

Check shared failure signatures before blaming models. A repeated signature across unrelated faults often points to shared setup, credentials, networking, or observers.

## Attribute regressions

Compare base and head on the same environment with equivalent clean state and workload. Record actual runtime images and source overrides. Serialize mutations of shared application and cluster state.

Failure on both architectures does not establish a pre-existing defect. A successful later rerun does not explain an earlier intermittent failure. Mark attribution unknown until the comparison supports it.

## Decide whether to change

Recommend a change only when the current behavior produces a meaningful undesirable state. Explain **Scenario → Unsafe action → Proposed fix** before editing. If the user accepts the risk or the state is removed by guaranteed teardown, record that decision and move on.

After implementation, repeat the original failure, fixed cases, valid controls, recovery, and affected integration paths. Complete the full applicable matrix for a full qualification claim. Always update `notes.mo/fault_testing/<fault-id>.md` for a full live audit.

For full live qualification, finish with the standard-runner gate from `live-testing.md`. Compare live topology with oracle assumptions and unit fixtures. Read evaluator logs for valid and invalid submissions. Investigate repeated failure signatures before counting model failures.

Do not weaken an oracle to compensate for broken workload bookkeeping or an invasive probe. Fix the layer that violates its contract. Do not add strict checks without a consequential failure scenario.
