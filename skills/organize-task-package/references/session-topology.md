# Worker and Reviewer Session Topology

## Contents

- Independence invariant
- Supported single-Worker topologies
- Current-task roles
- Isolated Reviewer subagents
- Fixed and fresh sessions
- Selection guidance and lineage
- Review handoff

## 1. Independence invariant

The Worker needs complete discussion and design context. The Reviewer needs enough of the same domain context to evaluate the exact result, but must not inherit or participate in the implementation reasoning under review.

Independence is about implementation context, not necessarily a separate user-visible task. A current task, forked task, fixed task, fresh task, or isolated subagent may be the Reviewer when the role constraints below are satisfied.

Never let one context both implement and approve the same snapshot. If no independent context is available, record only self-review and keep the item `implemented_pending_review`.

## 2. Supported single-Worker topologies

### 2.1 Separate Worker task and separate Reviewer task

```text
planning task
  -> Worker task
  -> Reviewer task with implementation-independent context
```

This has the strongest user-visible lineage and is preferred for high-risk, long-running, reusable-role, or manually supervised work.

### 2.2 Current task as Worker

```text
current task = Worker
  -> independent Reviewer task or isolated Reviewer subagent
```

Use this when the user wants the current task to implement directly and a separate planning coordinator is unnecessary. The current task owns the active Goal, execution record, implementation, and fixes. It may not approve its own work.

### 2.3 Separate Worker task and current task as Reviewer

```text
current task = planning + Reviewer
  -> separate Worker task implements
  -> current task reviews exact snapshots
```

Use this when the current task already understands the frozen design and should supervise a separate Worker. Once execution starts, the current task must remain read-only for product implementation, must not take over Worker fixes, and normally has no active Goal. Planning participation does not invalidate review independence; implementation participation does.

### 2.4 Separate Worker task with a Worker-managed Reviewer subagent

```text
current task dispatches Worker task
  -> Worker reads the frozen package and formal dispatch
  -> Worker creates Reviewer subagent at the pre-execution boundary
  -> Reviewer returns READY_REVIEW without implementation work
  -> Worker creates the active Goal and implements
  -> Worker invokes the same Reviewer on an exact snapshot
  -> Reviewer writes or returns an exact review receipt
  -> Worker repairs and repeats
```

This is the default single-Worker topology. Use it for a self-contained package where the Worker runs the review loop autonomously without another user-visible Reviewer task. The parent Worker orchestrates the Reviewer but must create it before implementation, must not provide implementation reasoning, and must not edit the Reviewer's verdict.

## 3. Current-task role constraints

Record `current_task` as the session mode when the current task is assigned directly.

When current task is Worker:

- it creates the active Goal after authorization;
- it writes execution and applies Reviewer receipts to GOAL;
- its Reviewer must be a separate independent task or isolated subagent;
- the current task cannot also be the Reviewer.
- record the current task's actual model and reasoning; if they do not satisfy the confirmed Worker configuration, select another Worker instead of claiming the default.

When current task is Reviewer:

- a separate Worker owns the active Goal and all product mutation;
- current task writes only the review record for review work;
- it may coordinate scope and receive progress, but must not co-author implementation decisions after dispatch;
- every requested repair returns to the Worker.
- record the current task's actual model and reasoning; if they do not satisfy the confirmed Reviewer configuration, use another Reviewer context.

## 4. Isolated Reviewer subagents

An isolated Reviewer subagent is valid only if its context excludes the Worker's implementation reasoning. Use one of these constructions:

1. default: create it from the Worker at the pre-execution boundary with a finite inherited slice containing the frozen package and formal dispatch, obtain `READY_REVIEW`, and later provide exact review artifacts; or
2. explicit alternative: create it after implementation with no inherited turns, then provide only frozen design, execution receipts, exact snapshot, and known validation.

A full-history child spawned from the Worker after implementation is not independent and cannot approve.

Record:

- human-readable Reviewer label, internal subagent ID, and owner (`worker` or `coordinator`);
- requested model and reasoning, enforcement status, and spawn receipt;
- actual model and reasoning when observable;
- context mode (`pre_execution` or `isolated_no_implementation_history`);
- exact reviewed snapshot;
- writable review-record path;
- receipt returned to the Worker and notification target.

The Reviewer subagent never creates an active Goal. In the default construction, the Worker must receive `READY_REVIEW` before creating its own active Goal, beginning implementation reasoning, or writing product state. The Reviewer's durable output belongs in the same independent review document used by a task-based Reviewer. For repeated re-review, follow up with the same Reviewer; do not replace an unfavorable Reviewer silently.

For an exact subagent override, spawn with an explicit model/reasoning pair and a finite inherited-turn count for the default pre-execution construction. Use the smallest slice that contains the frozen design and formal dispatch, normally the last few turns, and repeat the canonical package paths in the spawn prompt. A full-history spawn inherits the parent configuration and does not accept an override; after Worker implementation it also violates Reviewer independence. Native Codex custom-agent settings, explicit spawn settings, `[agents]` defaults, and parent inheritance are separate precedence layers, so record which layer selected the effective configuration rather than assuming the parent task controls every nested Agent.

## 5. Fixed and fresh sessions

When the user designates a long-lived Worker or Reviewer, reuse it instead of creating a duplicate role. Before reuse, verify that earlier Goals, commands, and reviews are closed; reread current GOAL, HEAD, coordination state, and scope; and treat old schema and baselines as history.

Use fresh sessions when the planning context is excessively long, blind review is important, fixed context is stale, or repository, environment, or permissions differ.

A fresh Worker receives GOAL, frozen decisions, exact baseline, write/no-touch scope, validation matrix, stop gates, and notification targets. A fresh Reviewer receives the same design package and later the exact execution evidence, but not the Worker implementation conversation.

Create a fresh task with the confirmed model/reasoning in the creation request. A fork operation establishes lineage but does not itself establish a new model configuration. After a fork, or before reusing a fixed task, send a configuration-only liveness turn with the confirmed model/reasoning, wait for `READY`, and repeat the same explicit settings on the formal dispatch. Record both acceptances. If either is rejected or mismatched, do not start the Goal or implementation.

## 6. Selection guidance

Choose the least expensive topology that preserves the required independence and auditability:

| Situation | Recommended topology |
| --- | --- |
| High-risk, long-running, or reusable roles | Separate Worker and Reviewer tasks |
| User asks this task to implement directly | Current task as Worker plus isolated Reviewer |
| Existing fixed/forked Worker does implementation | Current task as Reviewer when it remains read-only |
| Default single-Worker package | Selected Worker plus Worker-managed pre-execution Reviewer subagent |
| Strict blind review or stale planning context | Fresh Reviewer task or isolated no-history subagent |

Current-task roles reuse the current task's actual model and reasoning level; they do not acquire the role default automatically. An isolated subagent must receive an explicit model override when the confirmed configuration differs from inheritance, and the spawn receipt must report acceptance.

Apply configuration provenance in this order:

1. current explicit user choice;
2. confirmed topology in this task package;
3. most recent confirmed, successful same-family topology;
4. project default;
5. selected Worker plus a Worker-managed pre-execution Reviewer subagent as the default fallback.

Show human-readable task titles or role labels in the launch confirmation. Keep opaque IDs in technical lineage only. Do not create any task or subagent before confirmation merely to test the choice.

## 7. Lineage record

GOAL, execution, review, and lane records include:

| Field | Meaning |
| --- | --- |
| planning/coordinator label | user-readable sidebar title or stable role label |
| planning/coordinator task ID | task-design source |
| current-task role | `planning`, `worker`, `reviewer`, or `orchestrator` |
| Worker label | user-readable sidebar title or stable role label |
| Worker task or subtask ID | implementation context |
| Worker session mode | `current_task`, `fork_current`, `reuse_fixed`, or `fresh` |
| Worker source | current, parent, or fixed task |
| Reviewer label | user-readable role label, normally `<Worker label> / Pre-execution Reviewer` |
| Reviewer task or subagent ID | review context |
| Reviewer session mode | `current_task`, `fork_worker_pre_execution`, `shared_planning_base`, `reuse_fixed`, `fresh`, or `isolated_subagent` |
| Reviewer owner | `coordinator`, `worker`, or `external_task` |
| Reviewer context mode | implementation-independent construction |
| pre-execution boundary | time, message boundary, or handoff receipt |
| execution dispatch time | must respect the selected independence construction |
| requested model/reasoning | user-confirmed role configuration |
| enforcement method/status | creation, handshake plus dispatch, current actual, or explicit subagent spawn; `planned / confirmed / enforced / mismatch` |
| configuration receipt | accepted creation/message/spawn evidence, or exact mismatch |

If lineage cannot establish independence, do not claim approval.

## 8. Review handoff

At each review, provide:

- work-item ID;
- exact design location;
- exact commit, diff, artifact, or checkpoint;
- execution record;
- validation already run;
- untested scope and known risks;
- the single review document the Reviewer may update.

Do not copy the complete Worker implementation conversation. Let the Reviewer reconstruct judgment from frozen design, current code or artifacts, and evidence.
