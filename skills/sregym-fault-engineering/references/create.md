# Create a fault

## Design

1. Check the registry and existing problems for overlap before writing code.
2. Define the operational incident in concrete terms:
   - affected application and component;
   - injected Kubernetes or data-plane state;
   - externally observable symptom;
   - why normal health signals may be misleading;
   - accepted safe outcomes and explicitly unsafe shortcuts.
3. Prefer a real controller or platform mechanism over a conductor-side simulation.
4. Choose neutral resource names that resemble normal platform or application resources.

Read the source incident and the applicable sections of `fault-models.md`. Define what the agent can observe and change through its normal tools. Avoid hidden Conductor-only controls and inert evidence props.

Define the data contract before implementing the oracle. State which original records, write permissions, constraints, security properties, and workflow roles must survive. Do not require the author's exact recovery procedure.

For an application port, compare effective runtime behavior with the original application. Verify image contents, data paths, credentials, defaults, and workload semantics. Do not copy field names without checking their meaning.

## Implement

Create or update the complete lifecycle:

- `Problem` class and structured root cause;
- injection and reliable symptom wait;
- diagnosis oracle wiring;
- purpose-built mitigation oracle when generic readiness is insufficient;
- recovery for persistent, node, cluster, and cross-namespace state;
- registry entry;
- focused tests;
- fault documentation or testing note when requested.

Keep the problem definition declarative. Put reusable Kubernetes operations in established helpers when repetition is real, but avoid premature framework-wide refactors.

Use the current application-scoped layout and registry conventions. Keep shared abstractions limited to real reuse. Do not add provider credentials, prompt changes, workflows, or maintenance commands without a requirement.

Keep runtime dependencies available through the supported setup. Verify images and consumer pins before assuming a rebuild reaches normal runs. Publishing images or changing shared infrastructure requires user authorization.

## Validate

Prove at least these cases where applicable:

1. Healthy baseline works.
2. Injection creates the exact documented state.
3. The claimed symptom occurs and remains stable long enough to hand to an agent.
4. No mitigation fails.
5. The intended mitigation passes.
6. A safe equivalent mitigation passes.
7. The most plausible incomplete or destructive solutions fail.
8. A fresh restart, rollout, request, or record still works.
9. Official recovery removes consequential residual state.
10. Re-injection remains reliable.
11. Values that control manifestation or scoring have useful boundary and sensitivity evidence.
12. Missing-resource, partial-injection, and Kubernetes API error paths fail safely where applicable.

Do not call the fault ready based only on mocked tests.

For metastable faults, use a workload that does not disappear when the target stalls. Keep its lifecycle under benchmark control. Prove a healthy vulnerable baseline, then degradation after the temporary trigger ends. Replay the trigger after mitigation to verify removal of the sustaining loop.

Validate the workload and oracle against a healthy application first. Require request progress and semantic correctness, not only low error rate. A probe that exhausts the healthy application invalidates the experiment.
