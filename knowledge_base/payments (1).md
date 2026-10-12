# Payments service runbook

## Payment timeouts
1. Check provider response latency and timeout rates.
2. Compare application latency with external provider latency.
3. Review connection pools, retries, and circuit-breaker state.
4. Segment by provider, region, and payment method.
5. Never retry unsafe payment operations without idempotency protection.
