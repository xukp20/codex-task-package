---
name: organize-task-package
description: Organize discussed or evolving development, repair, testing, research, migration, or complex operational work into an executable, resumable, independently reviewable task documentation package, then derive a launch configuration from the current request and relevant task-family history for user confirmation. Use when Codex needs to record a task, create a dated task directory, split verifiable work items, freeze implementation and validation plans, create GOAL documents, arrange or reuse Worker and Reviewer sessions, coordinate parallel worktrees, confirm execution settings, maintain execution receipts, or audit task completion. Do not use for a short one-off task that does not need durable records.
---

# Organize Task Packages

## Core principles

Manage one bounded task as one directory and keep these concerns separate:

- user discussion and frozen decisions;
- executable design and validation plans;
- factual Worker execution receipts;
- independent Reviewer findings and verdicts;
- aggregate GOAL state.

Always follow the target repository's `AGENTS.md`, coordination files, branch rules, documentation-language rules, and latest user instructions. This skill supplies defaults; it does not override project policy.

## Select the output language

Keep this skill and all bundled resources in English. Select the language used for user-facing messages and generated task documents in this order:

1. explicit user instruction for the current task;
2. target repository or documentation-path language policy;
3. dominant language of the current conversation;
4. English as the fallback.

Use one language consistently across a task package unless the project requires file-specific exceptions. Preserve code identifiers, paths, commands, schema fields, model names, status values, and quoted source text in their original form.

Bundled templates are canonical English semantic scaffolds, not a mandate that generated documents remain English. When the selected output language is not English, localize every human-facing heading, explanation, placeholder, table label, and sample sentence before presenting the package as ready. Do not translate machine-readable identifiers such as `pending`, `implemented_pending_review`, `approved`, or `launch_config_status`.

## Determine the current action

1. If the user only requests discussion or analysis, continue discussing; do not create a directory or active Goal.
2. If the user explicitly asks to record, organize, or create task documents, create or update a task package without starting implementation automatically.
3. If the user explicitly asks to execute a referenced GOAL, let the assigned Worker create an active Goal and execute it.
4. If the user asks to audit an existing implementation, read the design, execution, review records, and current implementation; do not repair it without authorization.
5. Enable multiple Workers only after the user confirms a parallel launch configuration; otherwise use one Worker.

Never interpret the existence of `GOAL.md` as authorization to create an active Goal.

## Stage 1: Recover discussion facts

Before writing design documents:

1. Read the user's original requirements, material follow-ups, confirmed decisions, rejected alternatives, and boundaries from the complete conversation.
2. If context was compacted and the source task is readable, reread it. If it is unavailable, identify the missing evidence rather than inventing decisions from memory.
3. Inspect the target repository's current implementation, existing task records, coordination state, and `git status`; distinguish current facts from plans and historical behavior.
4. Record confirmed decisions, explicit non-goals, open questions, and evidence sources separately in `design/00_discussion-decisions.md`.
5. Write files only after the user authorizes recording. Do not promote an unaccepted proposal into frozen design.

Read [design-and-planning.md](references/design-and-planning.md) for the full decision and design rules.

## Stage 2: Close material design gates

Resolve ordinary local implementation details independently, but return to the user when any of these material choices remain open:

- durable schema, file layout, migration, or compatibility policy;
- names and basic parameters of important public APIs, Agent tools, or commands;
- cross-module ownership, authorization, safety boundaries, external state, or destructive behavior;
- a bug fix choice that changes intended product semantics rather than restoring already-frozen behavior.

Mark unresolved gates as `OPEN`. Do not proceed by inserting a temporary default.

## Stage 3: Create the task package

Use the local creation date and a stable slug by default: `YYYY-MM-DD_<task_slug>`. Freeze the date after creation. Let the user or project choose the parent directory; do not force `dev_docs/implementation`.

Prefer the bundled initializer:

```bash
python scripts/init_task_package.py \
  --parent <parent-directory> \
  --slug <task-slug> \
  --title "<task title>" \
  --part core="Core behavior"
```

The script path is relative to this skill directory and refuses to overwrite an existing directory. After generation, localize the scaffold to the selected output language and replace every placeholder with task facts. See [package-structure.md](references/package-structure.md).

Default single-Worker structure:

```text
YYYY-MM-DD_<task_slug>/
├── README.md
├── GOAL.md
├── design/
│   ├── 00_discussion-decisions.md
│   └── 01_<part>.md
├── execution/
│   └── worker-main.md
└── review/
    └── reviewer-main.md
```

Do not append execution results to design prose, and do not leave Reviewer findings only in chat.

## Stage 4: Split verifiable work items

Split by capability, defect, investigation question, or operational stage rather than arbitrary file boundaries. Each work item must include:

- a stable ID and target behavior;
- frozen decisions that govern it;
- current evidence or a failure reproduction;
- implementation or execution method and impact scope;
- validation assets to add or change;
- exact commands or observable evidence;
- acceptance criteria, non-goals, dependencies, and risks.

End each part with an integrated audit across its work items: combined behavior, adjacent risks, documentation, and stale symbol or entry-point residue. Read [task-profiles.md](references/task-profiles.md) for task-type adaptations.

## Stage 5: Maintain three-state GOAL truth

Each work item has exactly one state:

1. `pending`: implementation or execution is incomplete;
2. `implemented_pending_review`: the Worker completed it and recorded evidence, but independent review has not approved it;
3. `approved`: the Reviewer approved an exact snapshot and the Worker applied that receipt to the GOAL.

The Reviewer writes a per-item verdict only in the review record and notifies the Worker. The Worker may mark `approved` only when an exact review receipt exists. Never replace this state machine with binary checkboxes.

Use README only for navigation and derived status. Use GOAL as the aggregate state index and execution/review documents as evidence truth. Reconcile all three at every milestone.

## Stage 5.5: Derive and confirm the launch configuration

After the task documents, design gates, and validation plan are ready, do not immediately fork or execute. Derive a recommended configuration in this priority order:

1. explicit instructions in the current user request;
2. configuration already frozen in the current task package;
3. the most recent user-confirmed, successfully used Worker/Reviewer, model, and topology from the same project and task family;
4. project defaults;
5. skill defaults.

Inherit history only when the task family matches, sessions remain usable, no incompatible active Goal exists, and permissions and worktrees are compatible. Show each concrete value and its source. If a historical value is invalid, show the fallback reason instead of guessing silently.

Present one concise launch confirmation covering: single or parallel execution, current-session role, Worker/Reviewer task and session modes, requested models and reasoning, the mechanism that will enforce those settings, GOAL, branch/worktree/baseline, review cadence, validation scope, commit/notification/cleanup policy, and external actions such as real providers, servers, migrations, Release, or push. Freeze and execute only after the user confirms the bundle or explicitly edits individual fields.

Use human-readable task titles or stable role labels in every user-facing launch summary. Resolve the Codex sidebar title when task tools expose it. Do not lead with opaque task, thread, host, or subagent IDs; keep those only in durable execution/review receipts for exact routing. If no title exists, derive a readable label such as `<task title> — Worker` or `<Worker label> / Pre-execution Reviewer`.

For every current-session, Worker, Reviewer, and Orchestrator entry, state its construction type and source explicitly. At minimum report: readable label; context kind (`current task`, `existing sidebar task`, `new sidebar task`, or `nested subagent`); session mode (`current_task`, `reuse_fixed`, `fork_current`, `fresh`, `isolated_subagent`, or another supported mode); whether it is reused, forked, or newly created; the source context it inherits; requested model/reasoning; and the enforcement/independence boundary. Never make the user infer topology from a role name alone.

Store a single-Worker configuration in the root `GOAL.md`. Store parallel aggregate settings in the root GOAL and per-lane settings in `coordination/lanes.md`. Read [launch-configuration.md](references/launch-configuration.md) for provenance, validity checks, and the confirmation format.

## Stage 6: Run the Worker and Reviewer loop

Defaults:

- Worker: `gpt-5.6-sol`, reasoning `high`;
- Reviewer: `gpt-5.6-sol`, reasoning `xhigh`.

Treat role models as requested configuration, not as facts, until the target context accepts them. Enforce and record them as follows:

- `current_task`: record the actual model and reasoning; a turn cannot change its own model mid-turn;
- `fresh`: pass the confirmed model and reasoning when creating the task and record the accepted launch receipt;
- `fork_current`, `fork_worker_pre_execution`, `shared_planning_base`, or `reuse_fixed`: after selecting the target, send a short configuration-only liveness turn with the confirmed model and reasoning, wait for `READY`, then send the formal dispatch with the same explicit settings;
- `isolated_subagent`: pass the confirmed model and reasoning on spawn and use no inherited turns or a finite context that preserves the required independence; a full-history child inherits its parent and is not an override mechanism.

Do not silently fall back while claiming the confirmed configuration. If the target rejects the model/reasoning pair, reports a mismatch, or cannot provide the required isolation, stop before execution and return the discrepancy for a new decision. The Reviewer must also remain independent of the implementation under review.

For a single Worker, choose among four supported topologies: separate Worker and Reviewer tasks; current task as Worker with an independent Reviewer; separate Worker with current task as Reviewer; or separate Worker with a Worker-managed isolated Reviewer subagent. Fixed and fresh tasks remain available.

Choose the least expensive topology that preserves required independence and auditability. A context may implement or approve a snapshot, never both. A Reviewer subagent created after implementation is valid only when it inherits no implementation reasoning. Apply all role, isolation, selection, and lineage rules in [session-topology.md](references/session-topology.md).

Default single-Worker topology: use the selected Worker plus a Worker-managed pre-execution Reviewer subagent. After launch confirmation and Worker configuration enforcement, the Worker reads the frozen package and creates the Reviewer before creating the active Goal, beginning implementation reasoning, or modifying product state. Give the Reviewer a finite inherited slice containing the frozen design and formal dispatch, explicit Reviewer model/reasoning, and a readiness-only prompt. Wait for its `READY_REVIEW` receipt, then let the Worker implement. Reuse that same Reviewer for exact-snapshot review and re-review. Use another topology only when the user chooses it or current constraints make this construction invalid.

Execution loop:

1. The Worker rereads the task package, project rules, coordination state, current HEAD, and working tree.
2. After explicit execution authorization, the Worker creates the pre-execution Reviewer subagent, records its enforced configuration and `READY_REVIEW` receipt, and keeps it available for later review. The Reviewer does not create a Goal.
3. Only after that receipt does the Worker create an active Goal referencing the assigned `GOAL.md` and begin implementation.
4. The Worker completes one item, self-checks it, and appends actual paths, deviations, commands, results, durations, commits, and residual risks to the execution record.
5. The Worker marks the item `implemented_pending_review` and asks the same Reviewer to inspect the exact snapshot.
6. The Reviewer writes findings, evidence, recommended validation, and an item verdict only in the review record.
7. The Worker fixes findings and requests another iteration. After approval, the Worker marks the item `approved`.
8. After all items in a part are approved, run the part-level integrated audit.
9. After all parts pass, complete final validation, commit-scope inspection, document reconciliation, and cleanup.

Read [execution-and-review.md](references/execution-and-review.md) for exact responsibilities, receipts, and notifications.

## Stage 7: Coordinate parallel execution

Recommend parallelism when current task boundaries or validated same-family history support it, but enable it only after user confirmation. Without a confirmed parallel configuration, remain single-Worker. In parallel mode, the current session becomes an event-driven Orchestrator, normally without an active Goal or continuous polling.

Add `goals/` and `coordination/` to parallel packages:

- give every Worker an independent GOAL, execution record, and one-to-one Reviewer record;
- freeze ownership, write scope, dependencies, shared hotspots, pause gates, and notification targets in `coordination/lanes.md`;
- record commits, merge order, conflicts, integration validation, and cleanup in `coordination/integration.md`;
- normally isolate code-writing Workers in separate worktrees/branches unless project rules and disjoint write scopes make a shared tree safe;
- let Workers notify the Orchestrator about cross-lane decisions, blockers, pauses, completion, and integration needs;
- fork each Worker from the same frozen planning boundary, then fork its Reviewer before that Worker starts implementation;
- clean a worktree only after review, commit, clean-state verification, and confirmed integration. Preserve any unmerged or dirty lane.

Read [parallel-orchestration.md](references/parallel-orchestration.md) for the full protocol.

## Notification boundaries

- A Worker dispatched by another task must notify its dispatcher when coordination is needed and when it completes.
- A Worker operating directly in the user's current task reports normally to the user and does not message itself.
- Default to selecting or creating the Worker only after execution is authorized; then have that Worker create its Reviewer subagent at the frozen pre-execution boundary. Create separate fresh Reviewer tasks only when the confirmed topology selects them.
- Reuse a user-designated fixed Worker/Reviewer instead of creating duplicate equivalent sessions.

## Completion conditions

Claim completion only when all conditions hold:

- every work item is `approved`;
- every part-level integrated audit passes;
- execution and validation evidence is complete, with failures and interruptions preserved;
- current implementation or artifacts agree with the documents, and planned behavior is not presented as implemented;
- Git, worktrees, external runs, and sensitive data are closed within user boundaries;
- no blocking Reviewer finding remains open;
- GOAL, README, execution, review, and coordination state agree.

Use [observed-lessons.md](references/observed-lessons.md) as the final audit checklist.
