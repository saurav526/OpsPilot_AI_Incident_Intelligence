# Infrastructure runbook

## High CPU or memory
1. Compare CPU, memory, throttling, garbage collection, and restart counts.
2. Check whether the spike is isolated to one instance or shared.
3. Compare traffic with autoscaling events and capacity limits.
4. Review recent deployments and background jobs.
5. Do not scale or restart production resources from an anomaly score alone.

## Incident communication
Record observed symptoms and impact, separate facts from hypotheses, assign an owner, document mitigations, and verify recovery with service-level indicators.
