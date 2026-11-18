# Checks by failure mechanism

Read the sections that match the fault. These are review questions, not requirements to add every check to every oracle.

Historical examples explain why a check matters. They are not evidence about the source under review. Verify each current claim independently.

## Resource pressure and performance

- Verify that the victim uses the pressured resource. A stateless service does not necessarily suffer from page-cache eviction.
- Compare pressure with the actual node capacity, cgroup limit, process heap, and healthy workload.
- Separate container OOM, process heap failure, throttling, scheduling failure, and request latency. These are different mechanisms.
- Verify delivery of generated load. Producer enqueue calls do not prove that records reached Kafka.
- Account for probe overhead. An administration JVM inside a broker shares its container memory budget.
- Measure time to failure and recovery. Tune the mechanism before increasing timeouts or payloads.
- Check other faults that share a changed image, resource limit, or workload.

The missing-index review produced catalog OOM instead of silent slowdown. The Kafka review found discarded messages and heap failure without container restart. Busy helpers and configured limits were insufficient evidence.

## Controllers, scheduling, and networking

- Inspect effective objects after API defaulting, admission, controllers, and Conductor hooks.
- Observe across relevant reconciliation intervals. Calico or another controller can repair an injected route before grading.
- Check actual placement, allocatable capacity, storage topology, and scheduler events. Avoid collateral eviction of local-volume databases.
- Trace the real caller path through DNS, Service routing, network policy, TCP, protocol, and response content.
- Distinguish host-network, control-plane, and ordinary pod paths. A rendered policy does not prove enforcement on each path.
- Use current ownership and controller generation where serving identity matters. Do not freeze pod names or node placement unnecessarily.
- Verify the actual maintenance or controller operation. Healthy HTTP can coexist with a valid drain, admission, autoscaling, or storage incident.
- For limits and requests, inspect effective pod values. Removing a request can restore it through limit defaulting or a LimitRange.

An old healthy pod can hide a failed rollout. A matching label can select an unrelated responder. Check required controller state and the real application path, not labels alone.

## Data, database writes, and credentials

- Capture required record identities and content before injection. A count or one sentinel cannot prove preservation.
- Include non-fixture data where reseeding can hide loss. Restoring a built-in catalog does not restore later user records.
- Exercise reads and writes with the application principal through the application path.
- Check constraints by meaning. Renamed sequences, descending sequences, and equivalent uniqueness protection can be valid repairs.
- Verify practical write headroom and collision freedom. One successful insert does not prove continued writes.
- Permit legitimate new records. Check their authorization and content rather than requiring an exact frozen dataset.
- Match encryption-key durability to data durability. A temporary key cannot protect records that survive pod replacement.
- For credentials, check accepted and rejected credentials, active sessions, Secret propagation, and restart/bootstrap behavior.
- Define rotation requirements explicitly. A fixed password is not automatically the only valid repair.

The review-write fault exposed count-only preservation, root-only probes, and fixed sequence-name assumptions. The GitLab notification oracle rejected legitimate later notifications. Both required semantic checks, not more fixed names.

## Caches and response correctness

- Correlate output with the request: requested IDs, excluded IDs, tenant, authorization, filters, and result content.
- Verify behavior during upstream impairment and after recovery. Refresh after recovery does not prove bounded staleness during impairment.
- Accept zero backend calls from a valid warm cache. Distinguish a zero counter from missing telemetry.
- Exercise both cold and warm state where caching changes the result.
- Check more than HTTP status. A fake responder or fixed catalog can return 200 without the required behavior.

The stale-cache and thundering-herd reviews found stale data, ignored exclusions, and legitimate warm-cache repairs rejected as missing metrics.

## Queues, asynchronous work, and SLOs

- Track accepted work, acknowledged work, durable results, retries, and rejected requests separately.
- Verify acknowledgment boundaries. A failed write must not become a pending task that the client later reports as lost.
- Wait for bounded in-flight work before comparing accepted and completed records.
- Require traffic volume and progress. Empty histograms, absent samples, or NaN latency cannot prove health.
- Use fresh time windows and explicit time zones. Account for scrapes, batching, late exports, and startup samples.
- Keep baseline calibration below an absolute healthy ceiling. A broken baseline cannot define acceptable failure.
- Verify that validity flags actually gate admission or scoring. Recording an impact check without enforcing it proves nothing.
- Check data and required workloads separately from latency and error rate. Low latency can result from deleting work.

The generated-problem review found a fully broken baseline classified as healthy. Slack testing found workload bookkeeping errors that looked like application data loss.

## Persistent, recurring, and metastable faults

- Distinguish three models: a persistent bad state, a publisher that reapplies bad state, and a temporary trigger with a sustaining loop.
- Verify the actual cause and its operational evidence. A hidden Conductor variable or inert ConfigMap is not an application incident.
- For recurring faults, repair the source as well as the current state. Observe beyond the next publication or reconciliation.
- For metastability, end the trigger and prove that degradation remains. A queue that drains naturally is not sufficient.
- Use a realistic workload that remains active during the relevant agent phase. Do not create the only symptom inside private grading.
- Replay the trigger after mitigation when recurrence is part of the contract. Accept a repair that removes the sustaining loop.
- Reject restart-only repairs only when the cause remains and the failure returns.

Low model scores do not establish a bad fault. Verify discoverability, repair feasibility, and valid controls before judging task quality. Do not change benchmark prompts to make failures disappear without user direction.

## Images, ports, and environment variants

- Verify source commits, submodule pins, image-index digests, actual pod image IDs, entrypoints, and mounted overrides.
- Check anonymous pulls when normal users need public images. A maintainer's cached authenticated pull is not sufficient.
- Verify every promised architecture in the published index. Separate successful builds from native runtime qualification.
- Inspect the consumer override. A new chart default has no effect when SREGym still pins an older image.
- Check required files, binaries, dependencies, permissions, and real actions inside the published image.
- Compare original and ported applications under the same semantic contract. Similar service names do not prove equivalent configuration.
- Test shared hooks with their actual consumers: CLI, auth, proxy, stream upgrades, observability, and cleanup.
- For opt-in harness features, verify unchanged normal prompts, commands, credentials, stage transitions, and results when the feature is disabled.
- Separate submission acceptance, completed grading, and cleanup. Missing mitigation results are incomplete evidence, not automatically failed repairs.

The Train Ticket review found a stale installer override despite correct source. The FlightTicket regression omitted a runtime dependency. Successful image startup did not establish a working application.
