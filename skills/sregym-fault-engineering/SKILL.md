---
name: sregym-fault-engineering
description: Use when creating, reviewing, testing, hardening, or releasing SREGym faults, including injectors, diagnosis, mitigation oracles, recovery, fault PRs, and live-cluster qualification.
---

# SREGym Fault Engineering

Use the SREGym checkout selected by the user. If no checkout is selected, identify it before work on repository files.
Resolve SREGym source paths relative to that checkout. Resolve skill references and scripts relative to this skill directory.
Verify the selected cluster and active work before mutation. Saved VM names and Kubernetes contexts do not prove current ownership or availability.

Use these Markdown instructions with any agent. Adapt the instruction format and tools to the available environment.
Preserve the task scope, safety boundaries, and evidence requirements during adaptation.
If a required capability is unavailable, report the gap. Do not claim that an unexecuted check passed.

## Select the mode

- For a new fault, read [references/create.md](references/create.md).
- For a PR or diff review, read [references/review.md](references/review.md).
- For an existing-fault audit or hardening pass, read [references/audit.md](references/audit.md).
- For publication or release readiness, read [references/release.md](references/release.md).
- Before any live mutation, read [references/live-testing.md](references/live-testing.md).
- For mechanism-specific checks, read the applicable sections of [references/fault-models.md](references/fault-models.md).

Use `scripts/collect_fault_context.py` to locate a registry entry, problem, injector, oracle, tests, and prior notes when the fault identifier is known.
The helper finds a SREGym checkout from the working directory or its parents. Use `--repo` to select another checkout.

For a live PR review, read both `review.md` and `live-testing.md`. A static review cannot establish runtime correctness.

Match the evidence to the claim. A focused fix needs its reproduction, valid controls, and affected integration paths. Full fault qualification needs the complete applicable matrix. Do not require a full benchmark campaign after every change.

For static-only or read-only requests, inspect permitted artifacts and report in the conversation. Do not perform live tests or write notes. List missing evidence instead of executing the completion contract. For other requests, keep tests and artifacts within the authorized scope.

## Apply the common workflow

1. Read repository instructions and relevant code, tests, application metadata, and permitted prior notes. Respect exclusions from an independent review.
2. Establish the causal chain: source incident → injected state → operational effect → agent-visible evidence → safe repaired state. Define required data and functions before judging alternative repairs.
3. Inspect runtime provenance: source revisions, image digests, mounted code, effective configuration, workload, and post-Conductor topology. For authorized live tests, capture a functional baseline before injection.
4. For authorized tests, reproduce the effect over a meaningful observation window. Separate fault, application, workload, measurement, oracle, harness, and infrastructure defects.
5. Before implementing a non-obvious change, explain it to the user in this order:
   - **Failure scenario:** what happens in concrete terms.
   - **Unsafe action:** what incomplete or harmful solution currently passes, if any.
   - **Proposed fix:** what will change and why it closes that path.
6. Implement the smallest coherent change. Reuse established helpers and application structure. Avoid unrelated refactors, agent-prompt changes, and environment workarounds.
7. Add focused regression tests. Repeat the affected scenarios, valid alternatives, recovery, and relevant error paths. Audit successful outcomes as well as failures.
8. For full qualification, complete the standard-runner gate in `live-testing.md` on the final relevant source. Direct oracle calls remain exploration evidence.
9. Record **Action → Expected result → Actual result → Raw oracle output → Verdict** in `notes.mo/fault_testing/<fault-id>.md`. Keep commands and relevant output in the note or linked artifacts. Record PR reviews in `notes.mo/fault_pr_reviews/`.
10. Report evidence, limitations, and readiness. State which cases remain untested. Commit or publish only when asked.

Create the required `notes.mo/` directories only when the task permits file writes.
If the user selects another record location, use that location instead.
Do not include credentials or private access configuration in records.

## Required completion contract

A full fault test or live PR review is incomplete until it includes:

- healthy baseline and functional probe;
- exact injected state and steady-state symptom;
- unmitigated oracle failure;
- official recovery pass and residual-state check;
- intended fix pass;
- at least one valid alternative fix where one exists;
- plausible insufficient and destructive mitigations;
- parameter sensitivity for values that control manifestation or scoring;
- restart, re-injection, partial-failure, or API-error paths when relevant;
- a scenario table with expected and actual outcomes;
- final-source standard-runner submissions for known-valid and known-invalid states, with raw evaluator logs and matching stored results;
- final live cleanup verification and the required notes.

Do not claim that all scenarios were tested when any applicable item is missing. Separate static risks from live-reproduced results.

Do not infer agent failure from `mitigation_success=False`. Read the evaluator reason and trace first. Repeated failure signatures across valid repairs or unrelated faults require a shared-layer investigation before model attribution.

## Enforce fault-quality invariants

- Make injection produce the documented root cause and symptom reliably.
- Preserve the failure mechanism during adaptation. A slowdown replaced by OOM, or version skew replaced by a broken binary, is a different fault.
- Evaluate behavior and safety, not merely the presence or absence of one Kubernetes field.
- Accept materially equivalent safe fixes. Reject symptom hiding and destructive shortcuts.
- Do not accept deletion, scale-to-zero, stale healthy pods, unrelated replacement workloads, fabricated endpoints, or metadata-only changes when they remove required functionality.
- Distinguish desired, current, updated, Ready, Available, and serving state. Tie pods and endpoints to the intended controller generation where relevant.
- Exercise durability with a fresh pod, rollout, request, connection, admission, controller event, or data record when restart resistance matters.
- Do not reject restart-only repairs by default. Restart can correctly remove a runtime fault. Persistent or metastable causes need stronger durability checks.
- Preserve required data identities, contents, constraints, and authorized access. Row counts, sentinel rows, HTTP 200, and SLOs alone do not prove correctness.
- Verify the workload and measurement path. Missing samples, absent traffic, stale results, and failed probes are not healthy application evidence.
- Keep the oracle from creating the failure it claims to measure. Use a healthy control for invasive probes.
- Check collateral health where the mitigation can damage other required components.
- Prioritize consequential unsafe states. Do not block a fault on harmless template drift that namespace teardown eliminates.
- Restore cluster-scoped, node-scoped, persistent, or cross-namespace changes explicitly. Namespace deletion cannot clean them.
- Keep planted resources operationally plausible. Remove answer-bearing labels, expected repairs, sentinel messages, and benchmark-only control files from agent-visible evidence. Ordinary project or image branding alone does not prove answer leakage.

## Use past evidence carefully

Read prior review and testing notes as evidence, not as current truth. Separate the initial finding, later correction, final source, and deferred work. An old review can also contain an overly strict requirement.

During an independent review, inspect raw artifacts before prior conclusions. Historical examples in this skill suggest checks. They do not establish current defects or replace reproduction.

For a port or shared change, compare the original application with the new application. Verify effective defaults and runtime paths independently. For regression attribution, use a controlled base/head comparison. Failure on AMD64 does not prove that a defect predates an ARM branch.

Do not promise that empirical tests exclude every possible bypass. Identify the tested contract, consequential remaining risks, and evidence limits.

## Communicate clearly

Explain Kubernetes terms the first time they matter. Prefer one coherent scenario over fragmented analysis. Cite the exact code when reviewing or explaining an issue. Separate confirmed live observations from inferences.

For fault decisions, use the compact structure **Scenario → Unsafe action → Fix → Evidence** unless the user asks for another format.
