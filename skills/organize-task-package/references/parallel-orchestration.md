# Parallel Orchestration

Use parallel writers only when independent ownership reduces elapsed time more than it increases integration cost.

## Good parallel boundaries

- independent modules with stable interfaces;
- separate provider adapters after their shared contract is frozen;
- read-only planning or review alongside implementation;
- tests or experiments that do not mutate shared state.

Avoid parallel writes to one schema, transaction, registry, state machine, generated surface, lockfile, or unresolved public interface.

## Minimum coordination record

For each writer or lane, record only:

- outcome and owner;
- write scope and no-touch hotspots;
- upstream dependencies;
- branch or worktree when used;
- completion or integration condition.

Record integration order and one integration owner. Do not require separate lane GOAL, execution, and review files when the shared record is sufficient.

## Worktrees

Use isolated worktrees when writers touch the same repository concurrently, need independent commits, or the current checkout is dirty. A shared tree is acceptable for clearly disjoint writes under one integrator.

Never delete a dirty, unmerged, running, or user-preserved worktree. Clean temporary branches and worktrees after integration when the user has not requested preservation.

## Review and communication

Review a frozen candidate, not a range that is still changing. One reviewer may cover several related lanes when context remains manageable. Notifications should report blockers, material decisions, review readiness, and completion; routine progress need not generate durable receipts.
