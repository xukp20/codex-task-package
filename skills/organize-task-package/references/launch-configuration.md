# Launch Configuration Recommendation and Confirmation

## Contents

- Configuration provenance
- History inheritance boundaries
- Fields to present
- Defaults and validity checks
- Model enforcement and receipts
- User confirmation
- Persistence and changes

## 1. Purpose and timing

After the task package, design gates, and validation plan are ready, propose the execution configuration before creating or forking Workers, Reviewers, active Goals, worktrees, or external runs.

The goal is one transparent recommendation bundle that the user can confirm or edit, rather than a repeated questionnaire.

## 2. Configuration provenance

Choose each value in this order:

1. `explicit_current`: explicit current user instruction;
2. `task_package`: configuration frozen in this task's GOAL or coordination record;
3. `inherited_task_family`: most recent user-confirmed and successfully used configuration in the same project and task family;
4. `project_default`: repository rules, coordination documents, or project configuration;
5. `skill_default`: this skill's default;
6. `derived_current_state`: a necessary fallback derived from Git, worktree, session availability, or conflict state.

Show the concrete recommendation, provenance, and a short reason. Never write only “same as before”; identify the source task, session, model, or policy.

## 3. History inheritance boundaries

Eligible historical values include:

- fixed Worker/Reviewer task titles or stable names, with internal IDs retained only for routing receipts;
- models and reasoning levels;
- single or parallel topology;
- same-family worktree and branch conventions;
- review cadence;
- commit, integration, and notification policy;
- durable no-touch or default-off actions.

Use `inherited_task_family` only when all conditions hold:

- same project and business task family;
- the user confirmed the source configuration;
- the source execution was reviewed successfully, or the configuration remains an explicit active default;
- target sessions still exist and are usable;
- no incompatible active Goal, command, pending review, or worktree exists;
- the current user did not override it.

When history conflicts, is ambiguous, or belongs to another project, fall back to the current planning task and explain why.

Do not create a global Worker registry by default. Read current conversation history, same-family GOAL/lanes documents, and explicitly designated fixed tasks. Design a registry only if the number of durable roles creates a demonstrated need.

## 4. Fields to present

### 4.1 Task and authorization

- absolute task-package and GOAL paths;
- whether every design gate is closed;
- current execution authorization, normally `not_authorized` before confirmation;
- active Goal ownership: Worker only by default;
- token budget, unset by default;
- selected output/document language and its source.

### 4.2 Execution topology

- `single` or `parallel`;
- recommendation reason;
- for parallel execution, Worker count, part/lane ownership, and integration owner;
- `single` unless parallelism has been explicitly confirmed.

History may justify recommending parallel execution, but it cannot activate it before user confirmation.

### 4.3 Sessions and models

For every Worker/Reviewer show:

- a human-readable sidebar title or stable role label as the primary identifier;
- context kind: current task, existing sidebar task, new sidebar task, or nested subagent;
- construction: reused, forked, or newly created;
- source context: the readable task title or Worker label from which it is reused, forked, or spawned;
- current-task role: planning, Worker, Reviewer, or Orchestrator;
- Worker mode: `current_task`, `reuse_fixed`, `fork_current`, or `fresh`;
- Reviewer mode: `current_task`, `reuse_fixed`, `fork_worker_pre_execution`, `shared_planning_base`, `fresh`, or `isolated_subagent`;
- for an isolated subagent, owner and context mode;
- fork or reuse source;
- requested model and reasoning;
- enforcement mechanism and status: `planned`, `confirmed`, `enforced`, or `mismatch`;
- acceptance receipt or concrete mismatch evidence;
- any difference between the target context's actual model and the confirmed request.

Never lead a user-facing configuration with an opaque task/thread/subagent ID. If task tooling is available, resolve the current sidebar title. If it is unavailable, derive a readable role label from the package. Store exact task, host, and subagent IDs in GOAL technical lineage, execution, review, or coordination receipts only.

Use these topology descriptions consistently:

| Session mode | User-facing type description |
| --- | --- |
| `current_task` | existing current task; no fork or new context |
| `reuse_fixed` | reuse an existing named sidebar task; no fork |
| `fork_current` | create a new sidebar task by forking the named source task |
| `fresh` | create a new sidebar task without inherited conversation history |
| `fork_worker_pre_execution` | create a separate Reviewer task from the named Worker before implementation |
| `isolated_subagent` | create a new nested subagent owned by the named Worker or coordinator; state inherited-turn mode |

For a nested Reviewer also report whether it is visible in the sidebar, who owns it, when it is spawned, whether it inherits no turns or a finite pre-execution slice, and how the same instance is resumed for re-review.

For a `current_task` role, show its actual model and reasoning rather than the role default. If they are unsuitable, recommend another task or isolated subagent.

A role default or user-confirmed request is not proof that the target context uses that configuration. Do not write it into an `actual` field until the target creation, configuration handshake, or subagent spawn has accepted it.

### 4.4 Git, worktrees, and baseline

- exact HEAD or baseline;
- whether the working tree is clean;
- current checkout or isolated worktree;
- branch and integration target;
- shared hotspots and no-touch scope;
- worktree and branch cleanup conditions.

Prefer an isolated worktree per parallel code-writing Worker unless project policy and fully disjoint write scopes permit a shared tree.

### 4.5 Review, validation, and commits

- per-item review and part-level integrated audit by default;
- focused, adjacent, full, and real validation summary;
- tests expected to exceed 60 seconds and their stop gates;
- commit granularity, integration owner, and push policy;
- no push by default.

### 4.6 Notifications, external actions, and cleanup

- Worker/Reviewer notification targets;
- blocker, review-ready, approved, and completion receipts;
- real provider, server, migration, Release, push, and destructive-cleanup authorization;
- explicit current-task confirmation for every external action. Never inherit external authorization silently from history.

## 5. Skill defaults

| Setting | Default |
| --- | --- |
| Output language | Project rule, otherwise current conversation language |
| Execution mode | `single` |
| Current session | Planning/coordinator, no active Goal, unless assigned Worker or Reviewer |
| Worker | Reuse a valid fixed Worker for the same task family; otherwise create/fork one Worker |
| Reviewer | Worker-managed pre-execution Reviewer subagent |
| Worker model | `gpt-5.6-sol/high` |
| Reviewer model | `gpt-5.6-sol/xhigh` |
| Review | Per work item plus part-level audit |
| Token budget | unset |
| Push | false |
| Real or external mutation | false unless explicitly confirmed now |

When the same task family consistently uses a fixed Worker, recommend it as `reuse_fixed` instead of creating a duplicate. Prefer a fresh pre-execution Reviewer subagent owned by that Worker over reusing a Reviewer that may carry prior implementation context.

For the default single-Worker execution, require the Worker to create its Reviewer subagent before the active Goal, implementation reasoning, or product writes. The subagent inherits only the frozen pre-execution context and later receives exact snapshots and evidence. A current-task Reviewer or separate Reviewer task remains available when explicitly selected. Do not reduce independence merely to save a task.

## 6. Fixed-session validity checks

Before recommending reuse, verify that:

- the task or session is accessible and not incompatibly archived;
- no unfinished active Goal or running process conflicts;
- the previous review is closed or explicitly continues here;
- model, authorization, and repository match;
- worktree and branch do not conflict;
- the fixed Reviewer did not implement this batch.

When a check fails, choose a pre-execution fork or fresh session and record the fallback reason.

## 7. Model enforcement and receipts

Use the topology-specific procedure below after launch configuration is confirmed and before implementation or review begins.

| Session mode | Enforcement procedure | Required receipt |
| --- | --- | --- |
| `current_task` | Read and record the current task's actual settings. Do not claim that the role default changed the current turn. | Actual model/reasoning and a suitability verdict |
| `fresh` | Create the task with the confirmed `model` and `thinking` values in the creation request. The initial task prompt may be the formal dispatch. | Created task ID plus accepted creation settings |
| `fork_current`, `fork_worker_pre_execution`, `shared_planning_base` | Fork only to establish lineage. Then send a short configuration-only liveness message using the confirmed `model` and `thinking`, wait for `READY`, and send the formal dispatch with the same explicit settings. | Fork ID, handshake message/response, and formal-dispatch acceptance |
| `reuse_fixed` | Verify the task is idle and compatible, then use the same configuration-only liveness handshake and explicit formal dispatch as a fork. | Reused task ID, handshake message/response, and formal-dispatch acceptance |
| `isolated_subagent` | By default, the Worker spawns it before implementation with explicit `model` and `reasoning_effort` plus the smallest finite inherited-turn count that includes the frozen design and formal dispatch. Require `READY_REVIEW` before the Worker creates its active Goal or writes product state. Use `fork_turns="none"` only for an explicitly selected blind/no-history review. | Readable Reviewer label, internal subagent ID, requested settings, inherited boundary, `READY_REVIEW`, and spawn acceptance |

The configuration-only liveness message must not start task work or create an active Goal. Use a short payload such as: `Configuration preflight only; do not start the task or create a Goal. Reply READY_CONFIG.` The receipt is the task tool's acceptance of the explicit settings plus the target's liveness response; do not rely on the model to identify its own runtime configuration. For a fork or reused task, send the formal dispatch with the same explicit settings even after the handshake; this avoids relying only on persistence from a prior turn. Later follow-ups may omit settings only after the enforcement receipt is durable and no UI or API override has intervened.

Task-level configuration and nested subagent configuration are separate. Configuring a Worker task does not guarantee the model used by subagents it later creates. For native Codex subagents, record the applicable custom-agent file, explicit spawn override, `[agents]` default, or parent inheritance. Explicit spawn settings take precedence over defaults; a full-history spawn cannot enforce a different Reviewer model and must not be used for the default Worker-high / Reviewer-xhigh pair. Use a finite inherited slice for that pair.

Fail closed when the requested pair is unsupported or the tool cannot enforce it: keep execution unauthorized, record `mismatch`, and ask for a replacement model, reasoning level, or topology. Never silently run a fallback and label it with the requested configuration.

## 8. User confirmation summary

Keep the summary concise and write it in the selected interaction language. For example, in English:

```text
The task package is ready. Recommended launch configuration:

- Mode: single Worker (source: no parallel request)
- Current task: "Lite Design"
  - Type: existing current task (`current_task`); planning/coordinator; no fork or new context
- Worker: "Mode 1 Direct Repair", gpt-5.6-sol/high
  - Type: reuse existing sidebar task (`reuse_fixed`); no fork and no new task
  - Source: most recent confirmed same-family configuration
  - Enforcement: configuration-only liveness handshake, then explicit formal dispatch
- Reviewer: "Mode 1 Direct Repair / Pre-execution Reviewer", Worker-managed subagent, gpt-5.6-sol/xhigh
  - Type: new nested subagent (`isolated_subagent`), owned by "Mode 1 Direct Repair"; not a sidebar task
  - Source: finite inherited pre-execution context from "Mode 1 Direct Repair"
  - Creation: finite inherited design/dispatch context before active Goal or product work; require `READY_REVIEW`
- GOAL: <absolute path>
- Workspace: <branch/worktree>, baseline <sha>
- Review: each work item plus a part-level audit
- Validation: focused and adjacent; no full or real run
- External actions: no migration, restart, Release, or push
- Commit, notification, and cleanup: <summary>

Confirm the bundle to start, or name only the fields to change.
```

For parallel work, replace repeated paragraphs with one row per lane.

## 9. Persistence and change control

- Single Worker: root `GOAL.md` stores recommendations, provenance, user confirmation, and actual values.
- Parallel: root GOAL stores aggregate settings and `coordination/lanes.md` stores per-lane values.
- Execution and review records store requested settings, enforcement method/status, acceptance receipts, actual settings when observable, readable labels, internal task/subagent IDs, fork points, and deviations.
- README stores only whether launch configuration is confirmed.

After confirmation, change `launch_config_status` from `proposed` to `confirmed` and record confirmation time or message locator. Only then create or reuse sessions and enforce their settings. Execution begins only after each assigned context has an `enforced` receipt and the required fork/isolation boundary is frozen.

Reconfirm any later change to parallelism, Worker/Reviewer identity, branch/worktree, validation scope, or external action. Ordinary work-item progress needs no repeated confirmation.
