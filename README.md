# Codex Task Package

`codex-task-package` provides a reusable Codex skill for turning complex development,
repair, research, migration, testing, and operational work into executable and
independently reviewable task packages.

The included `organize-task-package` skill helps Codex preserve discussion decisions,
freeze implementation and validation plans, coordinate Worker and Reviewer contexts,
track three-state GOAL progress, and keep execution and review evidence separate.

## Included skill

### `organize-task-package`

Use this skill when a task needs durable planning and execution records rather than a
short one-off response. It supports:

- dated task-package directories;
- discussion, design, execution, and review separation;
- verifiable work-item decomposition;
- `pending` → `implemented_pending_review` → `approved` GOAL state;
- single-Worker and parallel Worker coordination;
- pre-execution independent Reviewer construction;
- branch, worktree, validation, commit, and cleanup receipts;
- development, repair, research, migration, testing, and operational task profiles.

## Repository layout

```text
skills/
└── organize-task-package/
    ├── SKILL.md
    ├── agents/
    ├── assets/
    ├── references/
    └── scripts/
```

The skill directory contains only runtime-facing skill resources. This root README is
repository documentation and is not part of the installed skill package.

## Install

Clone the repository and copy or symlink the skill into your Codex skills directory:

```bash
git clone https://github.com/xukp20/codex-task-package.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R codex-task-package/skills/organize-task-package \
  "${CODEX_HOME:-$HOME/.codex}/skills/organize-task-package"
```

Restart or reload Codex after installation so the new skill is discovered.

## Use

Invoke the skill explicitly:

```text
Use $organize-task-package to turn this design discussion into an executable task
package, then show me the launch configuration before implementation starts.
```

Codex may also select the skill automatically when a request clearly requires durable
task documentation, Worker/Reviewer coordination, execution receipts, or completion
auditing.

## Validate

Validate the skill with the `quick_validate.py` script distributed with Codex's
`skill-creator` system skill:

```bash
python /path/to/skill-creator/scripts/quick_validate.py \
  skills/organize-task-package
python -m py_compile skills/organize-task-package/scripts/init_task_package.py
```

The package initializer can be inspected with:

```bash
python skills/organize-task-package/scripts/init_task_package.py --help
```

## Language behavior

The skill implementation and bundled templates are written in English. Generated task
documents and user-facing messages follow the active conversation language and the
target repository's documentation policy.
