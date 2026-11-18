# Live-cluster testing

Live tests mutate shared infrastructure. Run them only when authorized. Use the selected target and its configured access path. Read recovery before injection. Keep cleanup available throughout the run.

Use the Python environment documented by the selected SREGym checkout for Conductor and problem code.
If the checkout provides `.venv/bin/python`, use that interpreter.
Verify the current checkout's KIND, CNI, and network-mode requirements.
Do not recreate or upgrade a shared cluster merely to make a test pass.

## Preflight

From the selected SREGym checkout and target environment:

```bash
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
kubectl get namespace <app-namespace> --ignore-not-found
helm list -A
git status --short --branch
```

Verify the intended context, access identity, active processes, and target ownership. Inspect namespaces and relevant shared dependencies. Preserve unrelated resources and user changes.

For Calico-dependent faults, verify IPPool, IPAM, and policy support before mutation. Remote tests can use the user's selected SSH host directly. Do not assume that a saved alias still points to a valid or idle VM.

Record the source commit, dirty changes, sibling-repository revisions, image pins, and relevant environment configuration. Verify actual pod image IDs after deployment. Mounted files or local builds can override the apparent source version.

Serialize tests that share application names, namespaces, ports, observers, or cluster-scoped state. Separate namespaces are insufficient isolation for node, CNI, admission, or storage mutations.

If authentication or access fails, diagnose the credentials and target configuration first. Do not remove recovery code, disable TLS, or weaken expected commands to hide the access defect.

## Establish the healthy baseline

Deploy through the normal Conductor lifecycle. Preserve its construction and baseline-capture ordering. Wait for required workloads, initialization, and real application operations before measuring.

Do not substitute a manual Helm deployment for the normal benchmark topology. Run Conductor stages that transform the application: observers, admission hooks, workload creation, controllers, and cross-namespace resources. Capture the baseline after those stages finish. Record transformed Services, EndpointSlices, controllers, and cross-namespace dependencies that the oracle reads.

Capture before injection:

- Deployment desired, updated, Ready, and Available replicas;
- pod phase, readiness, restart count, and controller ownership;
- Service selectors, endpoints or EndpointSlices, and a fault-specific functional probe;
- relevant limits, requests, configuration, and `kubectl top` metrics;
- baseline oracle result when meaningful;
- required data identities and content, write permissions, and relevant constraints;
- workload request rate, accepted work, completion rate, and measurement freshness.

If injection already happened, recover first and re-establish the baseline. Without baseline evidence, do not claim that an observed metric was caused by the fault.

Run the proposed measurement or invasive oracle probe against the healthy application. Record probe-generated CPU, memory, load, writes, restarts, and cleanup. A baseline that fails under the probe needs investigation before fault attribution.

## Inject and verify the claimed symptom

1. Inject through the repository's real `Problem` or injector path.
2. Measure how long injection takes and whether it returns before the fault is observable.
3. Verify exact Kubernetes state independently of injector logs.
4. Observe long enough to cover the relevant retry, reconciliation, cache, workload, scrape, and export cycles. State the chosen window.
5. Capture pod states, warning events, termination reasons, logs, metrics, and a functional/data-plane probe.
6. Cross-check every diagnostic claim in the PR or documentation. If the claimed signal differs from the observed one, record a finding.

For resource faults, compare usage against both baseline and configured limits. For network faults, distinguish DNS resolution, TCP connection, protocol response, and correct response content. For data-plane faults, verify durable progress or correctness rather than logs alone.

For sustained resource or latency faults, a single response or snapshot is insufficient. Use at least a minute as an initial observation window unless a measured mechanism supports another duration. Extend the window for slow controllers or delayed failures.

Verify that injection actually changed the state. Check command exit status and effects, not only a log message. A failed `exec`, API request, or probe is not proof of application failure.

Audit the workload itself. Correlate inputs with outputs, delivery with acknowledgment, and pending work with completion. Distinguish zero from missing samples. Use explicit time zones and fresh measurement windows.

Fault-specific signal checks include:

- CPU throttling: read cgroup `cpu.stat`, compare `nr_throttled` with `nr_periods`, and inspect process thread count;
- memory: record limit, working set, termination reason, and restart timing;
- latency or networking: compare baseline and injected response time, DNS, TCP, and application response separately;
- scheduling: record the exact request, node allocatable capacity, scheduler event, and whether the value is believable for production;
- persistent or data faults: identify the PVC, external store, or durable log and prove whether a restart preserves the incident.

## Run the required scenario matrix

Start each independent scenario from a known clean state. Record **Action → Expected oracle result → Actual oracle result → Verdict**.

| ID | Scenario | Required outcome |
|----|----------|------------------|
| A | No mitigation after the fault reaches steady state | Oracle fails |
| B | Official `recover_fault()` | Oracle passes and consequential injected state is gone |
| C | Intended manual mitigation | Oracle passes |
| D | Every materially different safe alternative identified during review | Oracle passes |
| E | Plausible partial or insufficient mitigations | Oracle fails |
| U | Destructive or symptom-hiding actions such as deletion, scale-to-zero, stale pods, fake endpoints, or unrelated replacements | Oracle fails |
| X | Relevant API-error, partial-injection, repeated-injection, restart, rollout, or bootstrap paths | Safe failure or correct durable behavior |

Do not stop after A and B. A green official lifecycle does not prove oracle correctness.

Select alternatives and unsafe cases from the fault contract. Removing a broken policy can be valid if required behavior survives. Restart can be valid if it removes the cause. Mark inapplicable cases with a reason rather than creating artificial blockers.

For every oracle submission, preserve the evaluator's raw stdout/stderr and failure reason. The HTTP submission acknowledgement, agent trajectory, and final boolean are not evaluator evidence. If evaluation runs asynchronously, read the conductor or worker log before classifying the result.

Wait for evaluation to finish before another repair or cleanup changes the tested state. Preserve the scenario's state and timestamps. Overlapping probes or repairs invalidate causal attribution.

Record `success`, reason, failure class, attempt completeness, and cleanup outcome separately. A known missing required workload differs from API unavailability or a broken test command. Do not turn unknown evidence into health or agent blame.

### Run the final standard-runner gate

On the final relevant source:

1. Record the exact commit and source hashes for any uncommitted implementation. Verify the worktree and cluster context.
2. Start the problem through the ordinary `uv run main.py ... --problem <fault-id>` path with its normal observability stack and setup hooks. Use the actual supported agent/model flags for the checkout.
3. Verify the post-setup topology that the oracle inspects. Do not assume that it matches the application chart.
4. In that same run, apply a known-valid mitigation and submit it through the normal conductor API.
5. Require both the stored success value and raw evaluator log to show a pass. Record the specific check that passed.
6. Run at least one unmitigated or known-invalid submission through the same path and require a logged failure for the intended reason.

Repeat affected gates after changes to the oracle, setup hooks, observers, deployment, workload, serving topology, or runtime image. A docs-only edit does not invalidate runtime evidence. Direct oracle calls cannot replace this gate.

For a focused fix, repeat its reproduction, valid control, recovery, and affected runner path. For shared changes, add representative existing consumers. Report remaining qualification gaps instead of implying a complete campaign.

### Select adversarial cases from the fault model

Test applicable cases, including:

- delete or scale the target or dependency to zero;
- leave an old healthy pod while the current rollout is broken;
- make a pod Running but not Ready;
- point a Service at the wrong Ready workload;
- return DNS without a working connection;
- change a checked template while admission mutates new objects;
- repair current state while leaving restart/bootstrap state broken;
- disable the harmful behavior through a valid alternative that preserves a different manifest shape;
- invoke injection twice or force a later injection step to fail;
- delete a resource that the oracle reads and verify the expected failed result and reason;
- lose original data while preserving its count or one sentinel;
- make a root probe succeed while application-principal requests fail;
- accept new legitimate records or use a renamed equivalent database object;
- stop traffic, return incorrect content, or leave a recurring publisher active;
- force a probe transport or telemetry failure without changing application health.

## Test parameter sensitivity

For values that control manifestation or scoring:

1. Choose meaningful nearby and boundary values. Three to five values are useful for a new tunable mechanism, not a universal quota.
2. Re-establish a clean baseline for each value.
3. Observe each value for the mechanism-specific window.
4. Record symptom, time-to-failure, metrics, and whether the value looks operationally realistic.

Flag values that are too mild, unnecessarily aggressive, or implausible on the target cluster.

Inspect values through the agent's normal tools. Flag implausible severity or planted answer text. Ordinary operational configuration is legitimate diagnostic evidence, even when a capable agent can identify it quickly.

## Verify recovery and cleanup

After official recovery:

- verify all consequential injected state is gone;
- wait for required Deployments and pods to become Ready;
- repeat the functional probe;
- run the oracle and require success;
- check cluster-scoped, node-scoped, persistent, cross-namespace, external-process, and helper-pod leftovers.

Exercise recovery before injection, after partial injection, after repeated invocation, and after an interrupted step where those paths exist. Preserve the original snapshot until restoration succeeds.

Stop fault publishers and their child processes before restoring state. Use graceful shutdown where forced termination leaves locks or sessions. Bound waits and verify that a timeout does not falsely report cleanup success.

Restore effective state, not only source configuration. Explicitly remove fields that were originally absent. Check node cordon, firewall rules, credentials, storage identity, durable data, and generated workloads where the fault touches them.

When the task lifecycle permits removal, remove the application release and namespace after the run. Verify that both are absent. Use a `finally`-style path so failures do not skip cleanup.

If normal recovery fails, use the narrowest authorized cleanup for the tested scope. Namespace deletion can remove namespaced resources. Restore cluster, node, persistent, and external state separately. Stop further tests if safe restoration cannot be verified.

For Calico IPAM faults, restore the captured IPPool and IPAM values. Do not overwrite a legitimate custom baseline with assumed defaults. Remove only verified injected pools.

For admission faults, verify the exact name and ownership before removing an injected `ValidatingWebhookConfiguration` or `MutatingWebhookConfiguration`.

## Recognize common failure signatures

- An oracle that passes with no mitigation is a false positive even when all surviving pods are Ready.
- An oracle that rejects a materially equivalent safe fix is too strict.
- Recovery after namespace removal can hang in repeated finalization. Reproduce and report the blocking call.
- Cleanup time that scales with the number of injected resources can block the conductor even when namespace deletion would remove those resources in bulk.
- A technically successful injection can still be too aggressive, too mild, or operationally implausible.
- A claimed persistent incident that self-heals before grading lacks the required durability. A runtime fault correctly repaired by restart is not automatically defective.
- Planted messages that name the fault, expected repair, or protected sentinel can disclose the answer. Ordinary manifests remain valid evidence.
- Repeated evaluator exceptions from valid-looking repairs need an integration investigation. Do not classify them as model failures without cause evidence.
- A unit fixture that invents a Service, Endpoint, controller, or pod relationship must be checked against the post-conductor live topology. Add the real alternative shape, such as `ExternalName` with no Endpoints, to regression coverage.
- A submission API returning success only proves receipt. Never treat `200 Submission received` as an oracle pass.
- A successful agent trajectory can contain repeated TLS, authentication, stream, or expected-command errors. Audit these independently of its score.
- A fully broken baseline, no traffic, empty histogram, stale metric batch, or unexecuted probe cannot establish recovered behavior.
- Official recovery can pass a weak oracle while the application remains broken. Repeat real requests and inspect required data after recovery.

## Required notes

Always write `notes.mo/fault_testing/<fault-id>.md` for a full fault test or live PR review. Include:

1. environment, access path, exact source revisions or hashes, and actual runtime images;
2. deployment timing and readiness;
3. baseline metrics and functional probes;
4. exact injected state and steady-state symptom;
5. warning events, errors, and claimed-signal comparison;
6. scenario table with expected result, actual result, and raw oracle output;
7. parameter-sensitivity table when applicable;
8. timing, workload correctness, probe side effects, partial failures, and durability observations;
9. agent-visible names, labels, annotations, logs, and possible diagnosis shortcuts;
10. recovery, residual-state, final cleanup, and verdict;
11. explicit list of cases not tested live;
12. final standard-runner command, exact commit, post-setup topology, and evaluator-log location.

Preserve commands and relevant observed output, directly or in linked artifacts. Keep later corrections separate from earlier results. The note is the source of truth for the actual tests.

Never place credentials, private keys, kubeconfigs, or secrets in notes. Do not add planted answer text to agent-visible resources.
