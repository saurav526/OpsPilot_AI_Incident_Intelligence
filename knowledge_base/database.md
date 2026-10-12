# Database and connection-pool runbook

## High connection utilization
1. Compare active, idle, and maximum connections.
2. Inspect acquisition wait time and pool timeout counts.
3. Review slow queries, lock waits, transaction duration, and query plans.
4. Check if recent changes increased concurrency or leaked connections.
5. Do not restart databases or kill sessions without owner approval.
