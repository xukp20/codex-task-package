# Execution and Review

## Execution records

Record facts that another reader needs to verify or resume the work:

- relevant baseline;
- material changes or actions;
- validation performed and its result;
- deviations from accepted design;
- unresolved blockers or residual risk;
- final commit, artifact, or external-state locator when one exists.

Exact commands, counts, durations, and failure output are useful for reproducibility, long-running tests, performance work, and diagnosis. They are optional for routine fast checks whose result is already clear.

Do not turn `RESULTS.md` into a command transcript. Full output belongs in normal tool logs or an artifact when it has a consumer.

## Review selection

Use the least expensive review that matches consequence and reachability:

- self-check for local, reversible work;
- one independent pass for material behavior or broad changes;
- multiple reviewers only for distinct, high-value dimensions.

Reviewer independence matters only when the result is claimed as independent. A reviewer must inspect the implementation or artifact rather than only the summary, but it does not need a prescribed creation time, model handshake, or readiness receipt unless the user explicitly requires those controls.

## Findings

A blocking finding needs:

- an owned contract or acceptance criterion;
- a plausible supported path;
- concrete evidence;
- material impact.

Group all material findings from the selected scope into one pass when possible. Treat speculative defense-in-depth and style preferences as non-blocking follow-up. Re-review only the repairs and directly affected behavior unless those repairs change the architecture broadly.

## Stable review identity

Use a commit, staged diff, artifact locator, or other existing stable identity when separate review requires it. Do not invent custom content hashes or receipt protocols when existing identity is sufficient.

## Result

A durable review record, when used, should state:

- reviewed scope and snapshot;
- material findings and their state;
- validation gaps;
- verdict and residual risk.

It need not repeat session topology, model provenance, task history, or every earlier review iteration unless those facts affect trust in the result.
