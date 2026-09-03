#!/usr/bin/env python3
"""Create a minimal, non-overwriting task documentation package."""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SAFE_SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"
PROFILES = ("compact", "resumable", "coordinated")


@dataclass(frozen=True)
class Part:
    item_id: str
    title: str


@dataclass(frozen=True)
class Worker:
    worker_id: str
    label: str


def parse_named_value(raw: str, *, option: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(f"{option} must use id=value syntax: {raw!r}")
    key, value = (item.strip() for item in raw.split("=", 1))
    if not key or not value:
        raise ValueError(f"{option} requires non-empty id and value: {raw!r}")
    if not SAFE_SLUG.fullmatch(key):
        raise ValueError(f"{option} id must be lowercase slug text: {key!r}")
    return key, value


def parse_parts(values: list[str]) -> list[Part]:
    raw_parts = values or ["main=Main outcome"]
    parts: list[Part] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_parts, start=1):
        slug, title = parse_named_value(raw, option="--part")
        if slug in seen:
            raise ValueError(f"duplicate part slug: {slug}")
        seen.add(slug)
        parts.append(Part(item_id=f"T{index:02d}", title=title))
    return parts


def parse_workers(values: list[str]) -> list[Worker]:
    workers: list[Worker] = []
    seen: set[str] = set()
    for raw in values:
        worker_id, label = parse_named_value(raw, option="--worker")
        if worker_id in seen:
            raise ValueError(f"duplicate worker id: {worker_id}")
        seen.add(worker_id)
        workers.append(Worker(worker_id=worker_id, label=label))
    return workers


def parse_assignments(
    values: list[str], *, parts: list[Part], workers: list[Worker]
) -> dict[str, list[str]]:
    worker_ids = {worker.worker_id for worker in workers}
    part_ids = {part.item_id for part in parts}
    assignments = {worker.worker_id: [] for worker in workers}
    assigned: set[str] = set()

    for raw in values:
        worker_id, item_list = parse_named_value(raw, option="--assign")
        if worker_id not in worker_ids:
            raise ValueError(f"--assign references unknown worker: {worker_id}")
        item_ids = [item.strip().upper() for item in item_list.split(",") if item.strip()]
        for item_id in item_ids:
            if item_id not in part_ids:
                raise ValueError(f"--assign references unknown item: {item_id}")
            if item_id in assigned:
                raise ValueError(f"item assigned more than once: {item_id}")
            assignments[worker_id].append(item_id)
            assigned.add(item_id)
    return assignments


def render(template_name: str, values: dict[str, str]) -> str:
    content = (ASSET_DIR / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", content)))
    if unresolved:
        raise ValueError(
            f"unresolved placeholders in {template_name}: {', '.join(unresolved)}"
        )
    return content


def write_template(
    root: Path, filename: str, template_name: str, values: dict[str, str]
) -> None:
    (root / filename).write_text(render(template_name, values), encoding="utf-8")


def work_item_sections(parts: list[Part]) -> str:
    sections = []
    for part in parts:
        sections.append(
            "\n".join(
                [
                    f"### {part.item_id}: {part.title}",
                    "",
                    "- Target behavior: To fill.",
                    "- Implementation or execution boundary: To fill.",
                    "- Validation: To fill.",
                    "- Dependencies or stop conditions: None / To fill.",
                ]
            )
        )
    return "\n\n".join(sections)


def goal_rows(parts: list[Part]) -> str:
    return "\n".join(
        f"| `{part.item_id}` {part.title} | `pending` | To fill |" for part in parts
    )


def lane_sections(
    workers: list[Worker], assignments: dict[str, list[str]]
) -> str:
    if not workers:
        return "- Add a writer or lane only when ownership needs durable coordination."
    sections = []
    for worker in workers:
        item_ids = assignments.get(worker.worker_id) or []
        assigned = ", ".join(f"`{item}`" for item in item_ids) or "To assign"
        sections.append(
            "\n".join(
                [
                    f"### {worker.label} (`{worker.worker_id}`)",
                    "",
                    f"- Assigned items: {assigned}.",
                    "- Write scope and shared hotspots: To fill.",
                    "- Dependencies and completion condition: To fill.",
                    "- Branch or worktree: To fill only when used.",
                ]
            )
        )
    return "\n\n".join(sections)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create the smallest useful task documentation package."
    )
    parser.add_argument("--parent", required=True, type=Path, help="Parent directory")
    parser.add_argument("--slug", required=True, help="Stable lowercase task slug")
    parser.add_argument("--title", required=True, help="Human-readable task title")
    parser.add_argument("--date", help="Frozen YYYY-MM-DD date; default: local date")
    parser.add_argument(
        "--profile", choices=PROFILES, default="compact", help="Package depth"
    )
    parser.add_argument(
        "--review", action="store_true", help="Add a durable REVIEW.md"
    )
    parser.add_argument(
        "--part", action="append", default=[], metavar="SLUG=TITLE", help="Work item"
    )
    parser.add_argument(
        "--worker",
        action="append",
        default=[],
        metavar="ID=LABEL",
        help="Coordinated-profile writer",
    )
    parser.add_argument(
        "--assign",
        action="append",
        default=[],
        metavar="WORKER=T01,T02",
        help="Optional coordinated-profile item assignment",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if not SAFE_SLUG.fullmatch(args.slug):
            raise ValueError("--slug must use lowercase letters, digits, '-' or '_'")
        if not args.title.strip():
            raise ValueError("--title must not be blank")
        date = args.date or datetime.now().astimezone().date().isoformat()
        if not DATE_PATTERN.fullmatch(date):
            raise ValueError("--date must use YYYY-MM-DD")
        if args.profile != "coordinated" and (args.worker or args.assign):
            raise ValueError("--worker and --assign require --profile coordinated")

        parts = parse_parts(args.part)
        workers = parse_workers(args.worker)
        assignments = parse_assignments(args.assign, parts=parts, workers=workers)

        parent = args.parent.expanduser().resolve()
        parent.mkdir(parents=True, exist_ok=True)
        task_dir_name = f"{date}_{args.slug}"
        target = parent / task_dir_name
        if target.exists():
            raise ValueError(f"target already exists; refusing to overwrite: {target}")

        common = {
            "TASK_TITLE": args.title.strip(),
            "WORK_ITEM_SECTIONS": work_item_sections(parts),
            "GOAL_ROWS": goal_rows(parts),
            "LANE_SECTIONS": lane_sections(workers, assignments),
        }
        temp_root = Path(tempfile.mkdtemp(prefix=f".{task_dir_name}.", dir=parent))
        try:
            write_template(temp_root, "TASK.md", "task.md.tmpl", common)
            if args.profile in {"resumable", "coordinated"}:
                write_template(temp_root, "GOAL.md", "goal.md.tmpl", common)
                write_template(temp_root, "RESULTS.md", "results.md.tmpl", common)
            if args.profile == "coordinated":
                write_template(
                    temp_root, "COORDINATION.md", "coordination.md.tmpl", common
                )
            if args.review:
                write_template(temp_root, "REVIEW.md", "review.md.tmpl", common)
            temp_root.rename(target)
        except Exception:
            shutil.rmtree(temp_root, ignore_errors=True)
            raise
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
