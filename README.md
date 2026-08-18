<h1 align="center">Codex Task Package</h1>

<p align="center">
  <strong>Auditable planning, execution, and review workflows for complex Codex tasks.</strong>
</p>

<p align="center">
  <a href="skills/organize-task-package/SKILL.md">
    <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-2563eb?style=flat-square">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-172554?style=flat-square">
  </a>
  <img alt="Task state" src="https://img.shields.io/badge/GOAL-3--state-0f8f88?style=flat-square">
  <img alt="Review modes" src="https://img.shields.io/badge/review-configurable-6b4fbb?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-active-d97706?style=flat-square">
</p>

<p align="center">
  <a href="#why-task-packages">Why</a>
  &middot;
  <a href="#workflow">Workflow</a>
  &middot;
  <a href="#quick-start">Quick Start</a>
  &middot;
  <a href="skills/organize-task-package/SKILL.md">Skill Reference</a>
</p>

Codex Task Package provides the `organize-task-package` skill: a reusable
workflow for turning a long or evolving discussion into an executable,
resumable, and reviewable task package.

It is designed for work where a checklist is not enough. The skill keeps user
decisions, implementation plans, execution facts, review findings, and
aggregate status separate so that each claim can be traced to evidence.

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Preserve Intent</strong><br><br>
      Recover confirmed decisions, rejected alternatives, boundaries, and open
      design gates before implementation starts.
    </td>
    <td width="33%" valign="top">
      <strong>Execute Deliberately</strong><br><br>
      Split work into verifiable items, freeze validation, select Worker and
      review mode, and record exact execution receipts.
    </td>
    <td width="33%" valign="top">
      <strong>Review Independently</strong><br><br>
      Bind findings and approvals to exact snapshots. Use the default inherited
      Reviewer, or explicitly select lightweight self-review.
    </td>
  </tr>
</table>

## Why Task Packages?

Complex Agent-assisted work tends to fail at the boundaries between planning,
execution, and verification:

- long discussions are compressed into incomplete implementation notes;
- planned behavior is accidentally reported as already implemented;
- test lists are chosen after the code instead of from the risk model;
- Worker completion is confused with independent approval;
- review findings live only in chat and disappear from the durable record;
- multi-Worker tasks lack explicit ownership, merge order, and cleanup rules;
- README, GOAL, implementation, and repository state drift apart over time.

`organize-task-package` makes those boundaries explicit. It does not replace
engineering judgment or the target repository's own rules. It gives Codex a
repeatable protocol for applying them.

## Workflow

```text
User discussion and repository facts
                 │
                 ▼
        Frozen decisions and gates
                 │
                 ▼
   Work items + risk-to-validation matrix
                 │
                 ▼
      User-confirmed launch configuration
                 │
        ┌────────┴────────┐
        ▼                 ▼
      Worker       pre-execution Reviewer
        │                 │
        ▼                 │
 execution receipts ──────┤
        │                 ▼
        └────────► exact-snapshot review
                          │
                          ▼
          pending → implemented_pending_review → approved
```

The default single-Worker workflow lets the Worker read the task and code, then
creates a full-history Reviewer before implementation reasoning. The Reviewer
inherits the Worker's model configuration and is reused for exact-snapshot
review. An explicit self-review mode skips the subagent while retaining labeled
receipts. Parallel execution adds explicit lanes,
worktrees, dependency gates, merge order, and integration receipts.

## Core Contract

| Surface | Responsibility |
| --- | --- |
| **Discussion decisions** | Preserve confirmed user intent, rejected alternatives, non-goals, evidence, and unresolved gates |
| **Design parts** | Define bounded work items, implementation impact, validation assets, exact commands, and acceptance criteria |
| **GOAL** | Aggregate task state and launch configuration without duplicating detailed evidence |
| **Execution record** | Store actual paths, deviations, commands, results, durations, commits, failures, and residual risks |
| **Review record** | Store inherited Reviewer findings or labeled self-review receipts and exact-snapshot verdicts |
| **Coordination** | Define Worker ownership, write lanes, worktrees, dependencies, notifications, merge order, and cleanup |

Each work item has exactly one state:

| State | Meaning |
| --- | --- |
| `pending` | Implementation or execution is incomplete |
| `implemented_pending_review` | Worker evidence exists, but the configured review mode has not approved it |
| `approved` | An exact REVIEW or SELF receipt approves the exact implementation or artifact snapshot |

## Supported Task Profiles

The same package structure adapts to multiple kinds of work:

- feature development and refactoring;
- bug diagnosis and repair;
- testing and validation campaigns;
- research and design investigations;
- data or schema migration;
- deployment and operational procedures;
- long-running or multi-Worker execution.

Task-specific details live in progressive-disclosure references so the core
skill remains compact.

## Quick Start

### Install

Clone the repository and link the skill into your Codex skills directory:

```bash
git clone https://github.com/xukp20/codex-task-package.git
cd codex-task-package
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/skills/organize-task-package" \
  "${CODEX_HOME:-$HOME/.codex}/skills/organize-task-package"
```

The final command fails safely if a skill already exists at that path. Remove
or relocate the existing installation only when you intentionally want to
replace it. Reload Codex after installation so the skill is discovered.

To update a linked installation:

```bash
git pull --ff-only
```

### Use

Invoke the skill explicitly:

```text
Use $organize-task-package to turn this design discussion into an executable
task package. Preserve the confirmed decisions and show me the launch
configuration before implementation starts.
```

Or ask it to resume or audit an existing package:

```text
Use $organize-task-package to audit this task against its GOAL, execution
receipts, Reviewer record, current repository state, and validation matrix.
```

Codex may also select the skill automatically when a request clearly requires
durable task documentation, Worker/Reviewer coordination, execution receipts,
parallel worktrees, or completion auditing.

## Generated Package Shape

A single-Worker package normally looks like this:

```text
YYYY-MM-DD_task-name/
├── README.md
├── GOAL.md
├── design/
│   ├── 00_discussion-decisions.md
│   └── 01_core.md
├── execution/
│   └── worker-main.md
└── review/
    └── reviewer-main.md
```

Parallel packages additionally use lane-specific GOAL, execution, review, and
coordination records. The target repository remains authoritative for branch,
test, documentation, and safety rules.

The bundled initializer can create the structural scaffold without overwriting
an existing task directory:

```bash
python skills/organize-task-package/scripts/init_task_package.py \
  --parent dev_docs/implementation \
  --slug provider-retry-repair \
  --title "Provider retry repair" \
  --part runtime="Runtime behavior" \
  --part validation="Validation and closeout"
```

Generated prose is then localized to the active conversation language and the
target repository's documentation policy. Machine-readable identifiers such as
the three GOAL states remain stable.

## Repository Layout

```text
codex-task-package/
├── README.md
└── skills/
    └── organize-task-package/
        ├── SKILL.md                 # core workflow and routing
        ├── agents/openai.yaml       # Codex UI metadata
        ├── assets/                  # task-package templates
        ├── references/              # detailed workflow guidance
        └── scripts/                 # deterministic package initializer
```

The skill directory contains only runtime-facing resources. This root README
is repository documentation and is not installed as part of the skill.

## Validation

Validate the skill with the `quick_validate.py` script distributed with
Codex's `skill-creator` system skill:

```bash
python /path/to/skill-creator/scripts/quick_validate.py \
  skills/organize-task-package
python -m py_compile \
  skills/organize-task-package/scripts/init_task_package.py
python skills/organize-task-package/scripts/init_task_package.py --help
```

The published package excludes generated Python caches, local task records,
provider credentials, repository-specific paths, and execution artifacts.

## Boundaries

- A task package records and coordinates work; it is not an Agent runtime or a
  replacement for Git, CI, project policy, or deterministic validation.
- The skill never treats the existence of `GOAL.md` as execution authority.
- Material schema, API, authorization, destructive-operation, and migration
  decisions remain explicit user gates.
- Independent mode never lets one context implement and approve a snapshot; explicit self-review receipts are labeled non-independent.
- Real providers, deployments, migrations, releases, pushes, and other
  external actions remain subject to the user's requested scope.

## Development Status

`organize-task-package` is actively used and refined against real multi-step
development and operational tasks. Its package schema is intentionally
human-readable and repository-local; future revisions may refine templates and
session topology guidance while preserving the separation between design,
execution, review, and aggregate status.
