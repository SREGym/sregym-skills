# Review a fault change

Keep review work read-only unless the user authorizes fixes or live mutation. Draft GitHub feedback only. Publish it only with explicit user authorization.

## Establish scope and context

1. Confirm the base branch or merge-base commit and check out the exact PR head locally when requested.
2. Inspect the full diff and identify problem, injector, oracle, recovery, registry, tests, docs, and notes.
3. Read `problems/base.py`, relevant oracle bases, the closest existing fault, application metadata and manifests, and established injector helpers.
4. Search for an existing equivalent fault or injector before accepting new inline machinery.
5. Within the authorized scope, run focused lint, type diagnostics, compilation, and tests. Respect no-write and static-only limits. Report failures even outside CI.
6. Check registration style, ordering, decorators, diagnosis and mitigation wiring, workload setup, and differentiation from existing problems.
7. When permitted, read relevant past notes and later corrections. Verify current source before reusing an old finding.

Map the full dependency path: registry → problem → application → image or mounted code → workload → observer → oracle → recovery. Inspect sibling repositories and consumer pins when the diff depends on them.

For scope, identify unrelated prompt changes, credential selection, workflows, documentation, and harness behavior. Remove unrelated additions only when fixes are authorized. Do not expand an application PR into a general framework rewrite.

Repository conventions:

- register a no-argument problem with the class directly and use a lambda only when constructor arguments are required;
- verify lifecycle decorators and baseline timing against the current base classes and nearest working problem;
- mitigation-oracle importance normally inherits or equals `1.0`;
- prefer the established injector when an exact operation already exists;
- do not flag `kubectl.exec_command()` merely for shelling out when it matches repository convention;
- treat `tasklist.yml.example` as stale and do not flag a missing entry there;
- verify workload and baseline capture ordering through the actual Conductor path;
- keep shared startup repair scoped to state that application teardown cannot restore. Avoid unbounded per-resource work that namespace deletion already performs.

For live reviews, use `live-testing.md`. Complete its applicable matrix before claiming full fault qualification. Label focused checks as focused checks.

## Review the oracle first

Determine the invariant the oracle actually proves. Check:

- **No-fix behavior:** the injected fault reaches steady state and the oracle fails.
- **Outcome versus prescribed shape:** safe equivalent repairs pass even when labels, names, selectors, commands, or manifests differ from the author's expected fix.
- **Destructive shortcuts:** deletion, scale-to-zero, stale pods, unrelated replacements, fake endpoints, and symptom hiding fail.
- **Required functionality:** desired replicas, current generation, Ready/Available state, endpoints, and fault-specific serving behavior are verified where applicable.
- **Data contract:** original records, correct responses, authorized writes, required constraints, and legitimate new records remain correct.
- **Durability:** a fresh pod, rollout, request, connection, admission, controller event, or data record still works when restart resistance matters.
- **Measurement:** current traffic and fresh evidence support the result. Zero, missing, stale, and invalid measurements remain distinct.
- **Probe side effects:** the oracle does not cause overload, release required locks, repair the fault, or erase evidence.
- **Error handling:** preserve the evaluator error contract and causal classification. Missing required resources differ from API outages or broken probe execution.
- **Client consistency:** new API clients share the configured client when the codebase expects that.
- **Return contract:** every path returns `{"success": bool}` plus optional evidence.

Read the current generic `MitigationOracle` implementation. Verify which resources its baseline captures, when capture occurs, and which rollout states it checks. Do not assume that inheritance alone covers serving behavior, data safety, or later resources.

Check diagnosis metadata against the implemented cause, not only the affected service. For example, a CoreDNS mutation can break an application's DNS without making that application the root-cause component. Accept equivalent accurate explanations through the supported grading contract.

Do not classify errors by exception type alone. An unchecked shell command can return `NOAUTH` as text. A connection refusal can occur outside Kubernetes `ApiException`. Preserve stdout, stderr, exit status, and the operation that failed.

Ask whether a custom oracle proves more than the generic oracle. When the generic oracle enforces the complete invariant, reuse it. Retain custom checks for serving behavior, data, durability, or other unmet requirements.

## Review the problem and injector

Check:

- root-cause component, namespace, ports, labels, and described mechanism against actual manifests and live evidence;
- reliable injection ordering and a bounded wait until the documented symptom exists;
- atomicity when a later injection step fails;
- idempotent or safely rejected repeated injection;
- realistic values on the target cluster;
- actual workload startup and whether `create_workload()` or lazy startup is correct for this app;
- durable injected state when the incident model requires survival across pod restart;
- full recovery of consequential state, including partial injection. When the contract requires forward-rotated state, recover to that state rather than an incompatible old snapshot;
- correct cleanup scope: namespace teardown handles namespaced state, not cluster, node, persistent, cross-namespace, or external state;
- agent-visible resources, logs, commands, and files for planted answer disclosure;
- diagnosis shortcuts that expose the original correct value or planted mechanism without operational reasoning.

Compare the fault with the closest existing problem. State the distinct mechanism, symptom, diagnosis path, and mitigation. Ask the author when meaningful differentiation is unclear.

Read the source incident when the fault cites one. Verify that adaptations preserve its causal mechanism. A decorative ConfigMap or a simulated delay cannot establish the claimed controller or SQL defect.

Review recovery as a separate operation. Verify exact restoration, partial-injection cleanup, repeatability, and bounded completion. Removing a LimitRange does not remove defaults already copied into Deployments. Merging an old object does not remove newly added fields.

## Classify findings

**Must-fix:**

- oracle false positive or false negative for a valid outcome;
- oracle crash or missing required-resource check;
- incorrect manifest assumption or root cause;
- planted answer disclosure that materially compromises diagnosis;
- recovery failure that leaves consequential state;
- a persistent or metastable incident that disappears before the intended handoff or grading window;
- dangerous shared-infrastructure mitigation accepted as success.

**Should-fix:**

- partial injection is not rolled back or recoverable;
- injection returns before the symptom exists;
- runtime dependency or timing makes the intended failure unreliable;
- unrealistic values or misleading diagnostic claims;
- duplicate fault without clear differentiation;
- cleanup that blocks the Conductor or falsely reports completion. Check for redundant per-resource work where namespace deletion handles cleanup;
- missing focused coverage for a reproduced edge case.

**Nit:** style, import order, minor comments, and harmless drift removed by guaranteed teardown.

Avoid speculative findings. State why each scenario violates required behavior. Do not call every different manifest shape, harmless marker, or valid restart an unsafe mitigation.

Distinguish a reproduced defect from a static risk, ambiguous requirement, environment defect, or code-quality preference. Use a controlled base/head comparison before calling a failure pre-existing or newly introduced.

## Required output

For each actionable finding provide:

1. severity and exact code location;
2. scenario;
3. expected outcome;
4. observed outcome and evidence, or the code-supported risk with missing runtime evidence stated;
5. smallest practical correction.

Include one scenario table with **Action → Expected → Actual → Verdict**. Separate live results from static risks and explicitly list untested cases.

Keep the top-level review short, friendly, and natural. Summarize the blocking behavior without repeating every inline comment. Match the user's requested tone.

For a full live review, record `notes.mo/fault_pr_reviews/<fault-id>_pr<number>.md` and link the live testing note. For static-only requests, report in the conversation without file writes. Say directly when there are no actionable findings. Green CI and mocks do not establish live correctness.

Do not require an autonomous model campaign for every merge. Controlled submissions through the normal runner can satisfy integration checks. Use existing trajectories when they add relevant evidence.

Inline comments belong on the shortest changed-line range that contains the issue. Include actual commands and output when the finding was reproduced. Keep code-level detail out of the top-level review body.
