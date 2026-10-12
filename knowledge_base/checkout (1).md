# Checkout service runbook

## Elevated checkout latency
1. Compare p50/p95/p99 latency with baseline.
2. Check recent deployments, feature flags, and configuration changes.
3. Inspect distributed traces to identify the slow dependency.
4. Compare checkout with pricing, inventory, and payment dependencies.
5. Compare request volume and queue depth to identify load-related delays.

## Elevated checkout errors
1. Group errors by status code and exception.
2. Check dependency timeout rates and retry amplification.
3. Correlate logs and traces around the first affected timestamp.
