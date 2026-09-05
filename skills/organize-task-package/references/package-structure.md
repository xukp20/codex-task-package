# Package Structure

## Naming and placement

Use `YYYY-MM-DD_<task_slug>` when the target repository has no stronger convention. Freeze the creation date and use a business-readable slug. Update an existing canonical package rather than creating a synonymous directory.

## Design-first placement

When design is requested before detailed implementation planning, start with a canonical `DESIGN.md` containing the background, goals, constraints, current evidence, proposal, and open decisions. Split a substantial supporting basis into `BACKGROUND.md` only when useful. Small tasks can instead keep distinct design and implementation sections in `TASK.md`.

Do not fill speculative work items or create empty execution records during this stage. After design convergence and any requested user acceptance, add or expand `TASK.md` in the same directory. Keep design rationale in `DESIGN.md`, execution steps and validation in `TASK.md`, and link between them. The profiles below describe the package as implementation planning becomes useful, not a mandatory initial scaffold. Do not rerun the non-overwriting initializer on an existing design directory.

## Compact profile

Use one `TASK.md` for ordinary bounded work. It should contain only the sections that help the current implementer or reviewer:

- outcome and scope;
- confirmed decisions and material open choices;
- work items with implementation boundaries and validation;
- result or residual risk when useful.

Do not create empty design, execution, review, or coordination directories.

## Resumable profile

Add:

- `GOAL.md` for current progress, blockers, and resume location;
- `RESULTS.md` for meaningful implementation and validation facts.

Keep stable task meaning in `TASK.md`, changing progress in `GOAL.md`, and observed results in `RESULTS.md`. Avoid copying the same status or evidence between them.

## Coordinated profile

Add `COORDINATION.md` when multiple writers or worktrees require explicit ownership. Record:

- writer or lane ownership;
- write scope and shared hotspots;
- dependencies and pause conditions;
- integration order and current integration state;
- cleanup obligations.

One coordination file is normally enough. Split per-lane files only when lanes are long-lived and independently resumed.

## Optional review

Add `REVIEW.md` only for a durable independent or formal review. For a short task, review can remain in the conversation or final result. Review history need not be append-only; preserve prior findings only when they explain an unresolved issue or final decision.

## Extending a package

Extend a package only when the current shape has a demonstrated reader problem:

- split a long design into topical files when navigation is difficult;
- split results by lane when concurrent writers would conflict;
- add a dedicated migration or runbook file when operators need it;
- add per-worker goals only when workers must resume independently.

The number of files is not a proxy for rigor.
