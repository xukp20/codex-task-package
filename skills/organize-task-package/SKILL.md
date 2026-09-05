---
name: organize-task-package
description: "Turn a substantial discussed task into the smallest useful, resumable documentation package. Explicit opt-in only: use when the user invokes $organize-task-package, or after Codex proposes it and the user approves; never auto-invoke merely because a task is large or multi-step."
---

# Organize Task Packages

Create only the records that have a real reader or recovery purpose. A task package should reduce ambiguity and handoff cost, not become a second project to maintain.

## Invocation boundary

This skill is opt-in. Use it only when the user explicitly invokes it, or after Codex briefly proposes it and the user explicitly agrees. Suggest it only when durable records have a concrete recovery, handoff, or coordination reader; do not interrupt routine multi-step work to ask. Task size alone is not permission to create a package. Companion skills may be considered automatically, but each still requires user approval before use.

## Language and local policy

Keep this skill and its bundled resources in English. Write generated documents in the language requested by the user, required by the target repository, or otherwise dominant in the conversation. Preserve identifiers, paths, commands, and quoted evidence.

Follow the target repository's documentation, coordination, Git, and safety rules. They override this skill's defaults.

For software development or architecture packages, actively consider whether the task has material tradeoffs in validation, compatibility, persistence, state, concurrency, public interfaces, or abstraction depth. If so, briefly ask the user whether to add `$right-sized-engineering`. Load and apply it only after approval. If it is not relevant, continue packaging independently without asking. When both skills are active, use `right-sized-engineering` to decide which artifacts, safeguards, validation, compatibility mechanisms, and review gates are justified.

## Route the request

- If the user is only discussing or evaluating a design, do not create files unless asked to record it.
- If the user asks to record a design before planning implementation, follow the design-first path below; do not invent detailed work items yet.
- If the user asks to record or organize work, create or update the smallest suitable package.
- If the user asks to execute, use the package as a guide; create an active Goal only when explicitly requested or required by the active runtime.
- If the user asks to audit, compare the current implementation and evidence with the task's accepted decisions. Do not repair without authorization.

The existence of a task package is never execution authorization.

## Design before implementation planning

When the approach is already settled, organize the implementation plan directly. When the user requests design first, record the background, requirements, constraints, relevant evidence, current proposal, and material open questions before expanding implementation work items.

Keep a substantial design in one canonical `DESIGN.md`; for small tasks, separate design and implementation sections in `TASK.md` are enough. A design-first package may initially contain only `DESIGN.md`. Add `BACKGROUND.md` only when the supporting basis needs its own reader-facing location. Do not create empty execution or result records merely to complete a profile.

If the user requests iterative design and `iterate-design-review` is available, load and use it on this same draft without asking again whether to enable it. It owns design convergence; this skill owns document placement and the later task breakdown. If unavailable, disclose that briefly and use ordinary evidence-grounded design review. Without a request for iteration, a single-pass design is sufficient; availability alone does not activate the companion.

Once the design is stable and any user-requested acceptance has occurred, expand `TASK.md` into implementation boundaries, dependencies, validation, and acceptance criteria, linking to the design rather than duplicating it. Design acceptance does not itself authorize execution. Reuse the existing package; the initializer is for new directories, not expanding a design-only directory.

## Choose the smallest package profile

### Compact — default

Use for bounded work that one context can complete without durable coordination.

```text
YYYY-MM-DD_<task_slug>/
└── TASK.md
```

`TASK.md` holds the outcome, boundaries, accepted decisions, open material choices, work items, and validation plan. Add a concise result section after execution when useful.

### Resumable

Use when work spans sessions, has several milestones, or needs a durable resume point.

```text
YYYY-MM-DD_<task_slug>/
├── TASK.md
├── GOAL.md
└── RESULTS.md
```

`GOAL.md` is the current progress and resume entry. `RESULTS.md` records meaningful implementation and validation outcomes without copying the plan.

### Coordinated

Use when multiple writers, worktrees, integration ordering, or explicit handoffs create real coordination risk.

```text
YYYY-MM-DD_<task_slug>/
├── TASK.md
├── GOAL.md
├── RESULTS.md
└── COORDINATION.md
```

Add `REVIEW.md` to any profile only when a separate review result must be durable. A requested design-first stage may use `DESIGN.md` as described above; otherwise add extra result or lane files only when the existing files have become difficult for their actual readers to use.

Read [package-structure.md](references/package-structure.md) when choosing or extending a profile. The bundled initializer creates these profiles without overwriting an existing directory. Replace its placeholders and localize its English scaffold before presenting the package as ready.

## Preserve decisions without preserving ceremony

Recover the current accepted meaning of the discussion:

- the outcome and explicit non-goals;
- confirmed corrections and decisions that constrain implementation;
- current code or runtime facts that matter;
- unresolved choices that would materially change behavior.

Do not reproduce an entire conversation, rejected brainstorming, source inventories, or review history unless it remains necessary to understand the task. Distinguish confirmed decisions from proposals.

Classify unresolved choices by who owns the decision, not merely by whether they mention a public interface, persistence, authority, or another high-consequence topic. Once implementation is authorized, the task owner may resolve in-scope, reversible implementation and unreleased-contract choices from current evidence. Use an independent reviewer when the consequence is material; if the task owner and reviewer converge, record the accepted current decision and continue without interrupting the user. A technical category alone is not a user approval gate.

Ask the user only when the choice changes confirmed user-owned product semantics or scope, breaks a real supported compatibility commitment, acts on real durable data, changes a security or permission boundary, causes an external or destructive effect not already authorized, incurs a material user-controlled cost, or otherwise depends on user preference rather than engineering evidence. Do not mark work blocked while an in-scope decision can still be resolved through implementation evidence or the configured review path.

## Define useful work items

Split work by coherent behavior or outcome. Each item normally needs only:

- target behavior;
- the implementation or execution boundary;
- validation that demonstrates success;
- dependencies or stop conditions when they exist.

Add failure evidence, impact matrices, exact commands, migration details, or negative cases only when they help implement, reproduce, review, or safely operate that item. Do not manufacture fields to fill a template.

Freeze important validation intent before implementation, but let exact commands follow current code and environment. If the impact surface changes materially, update the task before expanding the work.

Read [task-profiles.md](references/task-profiles.md) for concise task-type guidance.

## Track progress in one place

- Compact packages usually need no formal state machine; a short checklist or final result is enough.
- Resumable and coordinated packages use `GOAL.md` as the sole current progress truth.
- Use `pending`, `in_progress`, `pending_review`, or `done` only when those states are useful. Omit `pending_review` when no separate review is configured.
- Do not duplicate status across TASK, GOAL, RESULTS, REVIEW, and coordination records.

Record implementation facts at meaningful milestones, not after every trivial action. Preserve failed or interrupted evidence only when it affects diagnosis, acceptance, or safe resumption.

## Select review by risk

Self-check is sufficient for many local, reversible tasks. Use independent review when requested or when mistakes could materially affect durable state, authority, identity, concurrency, recovery, destructive operations, public contracts, or a broad refactor.

Review one coherent candidate rather than every tiny work item. Ask reviewers to return all material findings they can identify in the selected scope. Re-review accepted repairs and their immediate impact; do not repeatedly reopen unrelated hardening.

An exact commit or clearly identified diff is useful when a separate reviewer or integrator needs stable identity. Custom hashes, readiness receipts, model-enforcement receipts, and append-only review logs are not default requirements.

Read [execution-and-review.md](references/execution-and-review.md) when execution or review needs durable evidence.

## Launch and coordination

Before execution, summarize only user-owned choices that still need confirmation or operational facts the user needs to know: scope, writer ownership, branch/worktree when relevant, validation level, external actions, and any explicitly requested model or session configuration. Do not require a separate launch ceremony when the user has already authorized and configured the work.

Use parallel writers only for genuinely independent write scopes. For coordinated work, record ownership, dependencies, shared hotspots, integration order, and cleanup in `COORDINATION.md`. Do not require one GOAL, Reviewer, or worktree per Worker unless independent resumption or isolation actually needs it.

Read [parallel-orchestration.md](references/parallel-orchestration.md) only for coordinated execution.

## Completion

Completion means:

- the agreed outcome and acceptance criteria are satisfied;
- selected validation has completed, with material failures or omissions disclosed;
- no known blocking issue remains;
- current code, artifacts, and external state—not document ceremony—support the claim;
- resumable or coordinated records identify the final state and any residual work;
- temporary branches, worktrees, processes, and sensitive artifacts are handled within the user's scope.

Do not keep updating documents after they have served their reader. Prefer a concise final state over a complete diary.

## Initializer

```bash
python scripts/init_task_package.py \
  --parent <parent-directory> \
  --slug <task-slug> \
  --title "<task title>" \
  --profile compact
```

Use `--profile resumable` or `--profile coordinated` only when needed. Add `--review` when a durable review file has a real consumer.
