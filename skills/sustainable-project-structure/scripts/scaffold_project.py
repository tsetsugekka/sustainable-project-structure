#!/usr/bin/env python3
"""Safely scaffold or audit a sustainable project directory structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath


PROFILE_DIRS = {
    "development": [
        "80_SharedRuntime",
        "90_ProjectDocs",
        "91_ProjectTools",
        "98_Archive",
        "99_Temporary",
    ],
    "research": [
        "01_Research",
        "02_Meetings",
        "03_Sources",
        "04_Deliverables",
        "80_Reference",
        "90_ReusableAssets",
        "98_Archive",
        "99_Temporary",
    ],
}

DEFAULT_SKILL_DIR = {
    "development": "92_ProjectSkills",
    "research": ".agents/skills",
}

TRANSIENT_ROOT_NAMES = {
    "downloads",
    "generated",
    "output",
    "outputs",
    "temp",
    "tmp",
    "work",
}

DEV_DOCS = (
    "docs/READMECHS.md",
    "docs/SPEC.md",
    "docs/CHANGELOG.md",
)


def safe_relative(value: str, *, single_root: bool = False) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value.strip() in {"", "."}:
        raise argparse.ArgumentTypeError(f"unsafe relative path: {value}")
    if single_root and len(path.parts) != 1:
        raise argparse.ArgumentTypeError(f"unit must be one root directory: {value}")
    return path.as_posix()


def heading(name: str) -> str:
    return name.replace("_", " ")


def instruction_text(profile: str, roots: list[str]) -> str:
    root_list = "\n".join(f"- `{item}/`" for item in roots)
    docs_rule = (
        "- 每个开发页面／模块必须维护根 README 以及 "
        "`docs/READMECHS.md`、`docs/SPEC.md`、`docs/CHANGELOG.md`。\n"
        if profile == "development"
        else "- 固定分区和多文件主题维护 README；只有独立开发子项目才需要 SPEC 和 CHANGELOG。\n"
    )
    return f"""# Project Directory Governance

## Root policy

根目录仅使用以下已批准分区：

{root_list}

- 未经用户明确批准，不新增根目录类别；批准后同步更新 `PROJECT_STRUCTURE.md` 和结构检查。
{docs_rule}- 临时文件进入 `99_Temporary/YYYYMMDD-topic/`，任务结束时正式化或删除。
- 项目级 Skill 只能有一个权威位置，不依赖临时目录或敏感输入。
- 旧路径不存在时才查询 `MOVED_PATHS.md`；普通新建文件不登记。
"""


def project_structure_text(name: str, profile: str, roots: list[str], units: list[str], skill_dir: str) -> str:
    rows = "\n".join(f"| `{item}/` | 固定分区 | 参见该目录 README |" for item in roots)
    unit_note = (
        "每个开发单元拥有源码、专属 API、测试、工具和文档；当前语义以 `docs/SPEC.md` 为准。"
        if profile == "development"
        else "按事实来源和工作流归类；多文件主题用 README 说明输入、输出、版本和限制。"
    )
    return f"""# {name} 项目结构

项目类型：`{profile}`

| 根目录 | 类型 | 说明 |
| --- | --- | --- |
{rows}

## 长期规则

{unit_note}

- 项目 Skill 权威路径：`{skill_dir}/`。
- `98_Archive/` 只保留需追溯资料，不充当回收站。
- `99_Temporary/` 只存放有明确生命周期的中间产物。
- 已有路径移动时更新 `MOVED_PATHS.md`；新建文件无需登记。
"""


def root_readme(name: str, profile: str) -> str:
    return f"""# {name}

这是一个 `{profile}` 类型项目。目录白名单和文件归属见 `PROJECT_STRUCTURE.md`；旧路径失效时再查看 `MOVED_PATHS.md`。
"""


def moved_paths_text() -> str:
    return """# 路径移动索引

本索引只记录已有路径的移动、重命名或被替代删除。普通新建文件不登记，日常任务不需要预读。

旧路径失效时先查本表；目标路径必须直接写当前最终位置。

| 日期 | 原路径 | 当前路径／处理结果 | 原因 |
| --- | --- | --- | --- |
"""


def section_readme(directory: str, profile: str) -> str:
    return f"""# {heading(directory)}

本目录属于 `{profile}` 项目的固定分区。请在首次放入正式内容时补充：收录范围、不收录内容、输入输出、敏感边界和维护方式。
"""


def dev_unit_files(unit: str) -> dict[str, str]:
    title = heading(unit)
    return {
        f"{unit}/README.md": f"# {title}\n\n本目录是独立开发单元。维护说明、当前规格和历史变更见 `docs/`。\n",
        f"{unit}/docs/READMECHS.md": f"# {title} 维护说明\n\n记录运行、测试、部署、依赖和排障方式。\n",
        f"{unit}/docs/SPEC.md": f"# {title} 当前规格\n\n记录当前有效功能、接口、权限、数据流和限制。\n",
        f"{unit}/docs/CHANGELOG.md": f"# {title} 变更记录\n\n## Unreleased\n\n- 初始化页面／模块文档。\n",
    }


def build_files(args: argparse.Namespace) -> tuple[list[str], dict[str, str]]:
    skill_dir = safe_relative(args.skill_dir or DEFAULT_SKILL_DIR[args.profile])
    units = [safe_relative(item, single_root=True) for item in args.unit]
    roots = list(units) + list(PROFILE_DIRS[args.profile])
    if skill_dir.split("/", 1)[0] not in roots:
        roots.append(skill_dir.split("/", 1)[0])
    roots = list(dict.fromkeys(roots))

    files: dict[str, str] = {
        "README.md": root_readme(args.name, args.profile),
        "PROJECT_STRUCTURE.md": project_structure_text(args.name, args.profile, roots, units, skill_dir),
        "MOVED_PATHS.md": moved_paths_text(),
        ".gitignore": "99_Temporary/*/\n__pycache__/\n.DS_Store\nnode_modules/\n",
    }
    rules = instruction_text(args.profile, roots)
    if args.agent in {"codex", "both"}:
        files["AGENTS.md"] = rules
    if args.agent in {"claude", "both"}:
        files["CLAUDE.md"] = rules
    for directory in PROFILE_DIRS[args.profile]:
        files[f"{directory}/README.md"] = section_readme(directory, args.profile)
    if args.profile == "development":
        for unit in units:
            files.update(dev_unit_files(unit))
    else:
        for unit in units:
            files[f"{unit}/README.md"] = section_readme(unit, args.profile)
    return roots, files


def init_project(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    roots, files = build_files(args)
    skill_dir = safe_relative(args.skill_dir or DEFAULT_SKILL_DIR[args.profile])
    directories = list(roots)
    if skill_dir not in directories:
        directories.append(skill_dir)
    existing_entries = list(root.iterdir()) if root.exists() else []
    if existing_entries and not args.allow_existing:
        print("ERROR: target is not empty; inspect it first or pass --allow-existing", file=sys.stderr)
        return 2

    action = "CREATE" if args.apply else "WOULD CREATE"
    for directory in directories:
        target = root / directory
        if not target.exists():
            print(f"{action} DIR  {target}")
            if args.apply:
                target.mkdir(parents=True, exist_ok=True)
    for relative, content in files.items():
        target = root / relative
        if target.exists():
            print(f"SKIP EXISTING {target}")
            continue
        print(f"{action} FILE {target}")
        if args.apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    if not args.apply:
        print("DRY RUN: add --apply to write these missing paths")
    return 0


def audit_project(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project root not found: {root}", file=sys.stderr)
        return 2
    skill_dir = safe_relative(args.skill_dir or DEFAULT_SKILL_DIR[args.profile])
    units = [safe_relative(item, single_root=True) for item in args.unit]
    errors: list[str] = []
    warnings: list[str] = []

    for required in ("README.md", "PROJECT_STRUCTURE.md", "MOVED_PATHS.md"):
        if not (root / required).is_file():
            errors.append(f"missing governance file: {required}")
    if not (root / "AGENTS.md").is_file() and not (root / "CLAUDE.md").is_file():
        errors.append("missing agent governance: AGENTS.md or CLAUDE.md")
    for directory in PROFILE_DIRS[args.profile]:
        if not (root / directory).is_dir():
            errors.append(f"missing fixed directory: {directory}/")
        elif not (root / directory / "README.md").is_file():
            errors.append(f"missing directory README: {directory}/README.md")
    for entry in root.iterdir():
        if entry.is_dir() and entry.name.lower() in TRANSIENT_ROOT_NAMES:
            warnings.append(f"transient-looking root directory: {entry.name}/")

    if args.profile == "development":
        if not units:
            for entry in root.iterdir():
                match = re.match(r"^(\d{2})_", entry.name)
                if entry.is_dir() and match and int(match.group(1)) < 80:
                    units.append(entry.name)
        for unit in units:
            for relative in ("README.md",) + DEV_DOCS:
                if not (root / unit / relative).is_file():
                    errors.append(f"missing development document: {unit}/{relative}")
    else:
        for unit in units:
            if not (root / unit / "README.md").is_file():
                errors.append(f"missing workflow README: {unit}/README.md")

    skills_root = root / skill_dir
    if not skills_root.is_dir():
        errors.append(f"missing project skill directory: {skill_dir}/")
    else:
        for child in sorted(skills_root.iterdir()):
            if child.is_dir() and not (child / "SKILL.md").is_file():
                warnings.append(f"skill-like directory missing SKILL.md: {child.relative_to(root)}/")

    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    if errors:
        print(f"AUDIT FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"AUDIT PASS: {len(warnings)} warning(s)")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", required=True, help="project root")
    common.add_argument("--profile", choices=sorted(PROFILE_DIRS), required=True)
    common.add_argument("--unit", action="append", default=[], help="top-level page or workflow directory")
    common.add_argument("--skill-dir", help="authoritative project skill path relative to root")

    init = subparsers.add_parser("init", parents=[common], help="preview or create a new structure")
    init.add_argument("--name", required=True, help="project display name")
    init.add_argument("--agent", choices=("codex", "claude", "both"), default="codex")
    init.add_argument("--apply", action="store_true", help="write missing paths")
    init.add_argument("--allow-existing", action="store_true", help="allow a non-empty target without overwriting")
    init.set_defaults(handler=init_project)

    audit = subparsers.add_parser("audit", parents=[common], help="audit the expected baseline")
    audit.set_defaults(handler=audit_project)
    return result


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
