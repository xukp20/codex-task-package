<h1 align="center">Codex Task Package</h1>

<p align="center">
  <strong>Right-sized, resumable task documentation for Codex.</strong>
</p>

<p align="center">
  <a href="skills/organize-task-package/SKILL.md">
    <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-2563eb?style=flat-square">
  </a>
  <img alt="Default profile" src="https://img.shields.io/badge/default-compact-0f8f88?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-active-d97706?style=flat-square">
</p>

`organize-task-package` turns a substantial discussion or multi-step assignment into the smallest useful documentation package. It preserves accepted intent, implementation boundaries, validation, and resume state without forcing every task into a heavyweight review protocol.

## Profiles

| Profile | Use when | Files created by default |
| --- | --- | --- |
| Compact | One context can complete bounded work | `TASK.md` |
| Resumable | Work spans sessions or milestones | `TASK.md`, `GOAL.md`, `RESULTS.md` |
| Coordinated | Multiple writers or worktrees need durable ownership | Resumable files plus `COORDINATION.md` |

`REVIEW.md` is optional in every profile. Extra design or lane files are added only when an actual reader needs them.

## Principles

- Preserve confirmed decisions, not the entire history of discussion.
- Give each work item a clear outcome, implementation boundary, and sufficient validation.
- Keep current progress in one place.
- Record meaningful evidence rather than a command diary.
- Scale review to business risk and plausible reachability.
- Introduce worktrees, per-worker records, receipts, and exact snapshot identity only when coordination or auditability requires them.

## Install

```bash
git clone https://github.com/xukp20/codex-task-package.git
cd codex-task-package
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/skills/organize-task-package" \
  "${CODEX_HOME:-$HOME/.codex}/skills/organize-task-package"
```

Reload Codex after installation. A linked installation can be updated with `git pull --ff-only`.

## Use

```text
Use $organize-task-package to record this implementation task. Choose the
smallest package that preserves the decisions, work items, validation, and
resume information we actually need.
```

The skill does not create an active Goal or authorize implementation merely because documentation exists.

The Skill is explicit opt-in. Invoke it by name, or approve its use after Codex suggests it; task size alone does not activate it. Once active for software architecture or development, it evaluates whether `right-sized-engineering` would help and, when relevant, asks for separate approval before loading that companion.

## Initializer

Create the default compact package:

```bash
python skills/organize-task-package/scripts/init_task_package.py \
  --parent dev_docs/implementation \
  --slug provider-retry-repair \
  --title "Provider retry repair"
```

Create a resumable package:

```bash
python skills/organize-task-package/scripts/init_task_package.py \
  --parent dev_docs/implementation \
  --slug provider-runtime-refactor \
  --title "Provider runtime refactor" \
  --profile resumable \
  --part core="Core runtime" \
  --part recovery="Recovery behavior" \
  --review
```

For multiple writers, use `--profile coordinated` and optional `--worker` / `--assign` arguments. The script refuses to overwrite an existing package.

## Repository layout

```text
codex-task-package/
├── README.md
└── skills/
    └── organize-task-package/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── assets/
        ├── references/
        └── scripts/init_task_package.py
```

## Validation

```bash
python /path/to/skill-creator/scripts/quick_validate.py \
  skills/organize-task-package
python -m py_compile \
  skills/organize-task-package/scripts/init_task_package.py
python skills/organize-task-package/scripts/init_task_package.py --help
```

## Boundaries

- Target repository policy and current implementation facts remain authoritative.
- Material user-owned product decisions remain explicit gates.
- Review, model selection, session topology, exact receipts, and parallel worktrees are conditional tools rather than package-wide defaults.
- Real providers, deployments, migrations, releases, pushes, and destructive actions still require appropriate authorization.
