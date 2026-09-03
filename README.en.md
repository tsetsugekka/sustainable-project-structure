<div align="center">

# Sustainable Project Structure

**Keep development, research, and hybrid projects clear, maintainable, and reproducible as they evolve with AI-assisted work.**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=flat-square)](skills/sustainable-project-structure/SKILL.md)
![Version](https://img.shields.io/badge/version-1.1.0-2563eb?style=flat-square)
![Primary README](https://img.shields.io/badge/README-Chinese-dc2626?style=flat-square)
![Public Safe](https://img.shields.io/badge/public--safe-no%20secrets-16a34a?style=flat-square)

[中文](README.md) · **English**

</div>

---

## What This Is

`sustainable-project-structure` is a Codex skill for governing project structure. It does not impose one universal folder template. It first identifies how the project actually works, then helps establish:

- a controlled set of root-level directories;
- clear ownership for pages, services, research material, and deliverables;
- temporary-file and archive lifecycles;
- direct mappings from old paths to their final locations;
- maintainable documentation for long-lived development units;
- reproducible project skills, scripts, and references.

It works for both new projects and existing repositories that have accumulated historical files, AI-generated intermediates, and stale path references.

## Project Profiles

| Profile | Best for | Primary organizing principle |
| --- | --- | --- |
| `development` | Websites, SaaS products, APIs, and automation tools | Component ownership, source, tests, deployment, and specifications |
| `research` | Planning, investigation, meetings, analysis, and deliverables | Sources, workflow, decisions, editable originals, and delivery relationships |
| `hybrid` | Research projects with dashboards or development projects with substantial research | Use the dominant workflow at the root and development rules inside real software subprojects |

## Features

- **Root governance** — define an allowlist, numbering scheme, and approval boundary for new top-level directories.
- **Ownership alignment** — keep component-specific source, APIs, tests, tools, and documentation together.
- **Layered documentation** — maintain `READMECHS.md`, `SPEC.md`, and `CHANGELOG.md` for long-lived development units.
- **Temporary lifecycle** — keep downloads, conversions, screenshots, and AI intermediates out of permanent structure.
- **Safe migration** — map paths before moving files, then update references, deployment manifests, and tests.
- **Skill reproducibility** — avoid authoritative copies that depend on temporary folders, credentials, or one computer.

## Recommended Layouts

### Development project

```text
ExampleProject/
├── 01_Account/
├── 10_Service/
├── 80_SharedRuntime/
├── 90_ProjectDocs/
├── 91_ProjectTools/
├── 92_ProjectSkills/
├── 98_Archive/
├── 99_Temporary/
├── AGENTS.md
├── PROJECT_STRUCTURE.md
└── MOVED_PATHS.md
```

### Research or planning project

```text
ResearchProject/
├── 01_Research/
├── 02_Meetings/
├── 03_Sources/
├── 04_Deliverables/
├── 80_Reference/
├── 90_ReusableAssets/
├── .agents/skills/
├── 98_Archive/
├── 99_Temporary/
├── AGENTS.md
├── PROJECT_STRUCTURE.md
└── MOVED_PATHS.md
```

These names are starting points, not mandates. Existing projects should retain mature, understandable domain language.

## Installation

### Agent Skills CLI

```bash
npx skills add tsetsugekka/sustainable-project-structure \
  --skill sustainable-project-structure
```

Keep the explicit `--skill sustainable-project-structure` selector so only the intended skill is installed when repository layouts evolve.

### Manual installation

```bash
git clone https://github.com/tsetsugekka/sustainable-project-structure.git
mkdir -p ~/.codex/skills
cp -R sustainable-project-structure/skills/sustainable-project-structure \
  ~/.codex/skills/
```

## Example Prompts

```text
Use $sustainable-project-structure to design the directory layout for this new website.
Give each page a clear owner and place non-page areas in high-numbered shared sections.
```

```text
Reorganize this existing project's root, but propose a migration map first.
Do not break old sessions, deployment manifests, or uncommitted work.
```

```text
This is a planning and data-analysis project, not a website.
Organize it around evidence sources, meetings, deliverables, and reusable assets.
```

## Safe Scaffolding and Audit

The helper defaults to a dry run and writes nothing:

```bash
python3 skills/sustainable-project-structure/scripts/scaffold_project.py init \
  --root /path/to/project \
  --name ExampleProject \
  --profile development \
  --unit 01_Account \
  --unit 10_Service \
  --agent codex
```

Add `--apply` only after reviewing the preview. Even with `--allow-existing`, the helper creates missing files only and never overwrites existing ones.

Audit an existing structure:

```bash
python3 skills/sustainable-project-structure/scripts/scaffold_project.py audit \
  --root /path/to/project \
  --profile development \
  --unit 01_Account \
  --unit 10_Service
```

## Repository Layout

```text
skills/sustainable-project-structure/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── development-projects.md
│   ├── migration-and-governance.md
│   └── research-projects.md
└── scripts/scaffold_project.py
```

## Security Rules

- Do not bulk-move or delete existing files without authorization.
- Do not overwrite existing files or use archives as permanent dumping grounds.
- Do not store live credentials, personal data, private logs, or machine-specific absolute paths in the skill.
- Do not change production URLs, APIs, permissions, or data locations merely because local folders move.
- Treat structural audits as complements to project tests, builds, and deployment checks—not substitutes.

## Disclaimer

Folder templates are not the goal; stable ownership boundaries are. Adapt the final structure to project scale, team conventions, compliance needs, and existing deployment behavior. Review version-control state and backup strategy before any high-impact migration.
