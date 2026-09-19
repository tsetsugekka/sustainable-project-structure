<div align="center">

# Sustainable Project Structure

**Keep development, research, and hybrid projects clear, maintainable, and reproducible as they evolve with AI-assisted work.**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=flat-square)](skills/sustainable-project-structure/SKILL.md)
![Version](https://img.shields.io/badge/version-1.3.0-2563eb?style=flat-square)

![Public Safe](https://img.shields.io/badge/public--safe-no%20secrets-16a34a?style=flat-square)

[中文](README.zh-CN.md) · **English**

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

- **Root governance** — document stable responsibilities and reuse existing conventions; numbering and strict allowlists are optional.
- **Ownership alignment** — keep component-specific source, APIs, tests, tools, and documentation together.
- **Distributed documentation** — keep docs with their owners, merge duplicate facts into one current source, and preserve useful history.
- **Lifecycle-aware navigation** — separate durable guides, active tasks, short-lived records, and archives; short-lived batches stay out of the root index.
- **Generated indexes** — regenerate marked README sections from paths and titles, detect stale indexes, and add concrete closeout commands to generated AGENTS / CLAUDE files.
- **Temporary lifecycle** — keep downloads, conversions, screenshots, and AI intermediates out of permanent structure.
- **Safe migration** — map paths before moving files, then update references, deployment manifests, and tests.
- **Independent maintenance** — leave project-owned rules and self-contained checks; this external governance skill need not remain installed in the project.
- **Development kits and progress records** — separate reusable tooling from case deliverables, and consolidate fragmented logs without changing task state or evidence.

## Recommended Layouts

The numbered layouts below are optional scaffolds for new projects. Existing repositories can retain structures such as `modules/catalog/docs/`, `services/search/docs/`, and a small shared `docs/` entry point. Documentation responsibilities matter more than a mandatory set of filenames.

### Development project

```text
ExampleProject/
├── 01_Account/
├── 10_Service/
├── 80_SharedRuntime/
├── 90_ProjectDocs/
├── 91_ProjectTools/
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
├── 98_Archive/
├── 99_Temporary/
├── AGENTS.md
├── PROJECT_STRUCTURE.md
└── MOVED_PATHS.md
```

These names are starting points, not mandates. Existing projects should retain mature, understandable domain language. Shared development kits organize reusable generators, templates and guidance; consuming projects own their data, task history and deliverables. A genuine long-term project-specific workflow may warrant a skill directory, but ordinary directory/document maintenance does not.

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
Give each module a clear owner and reuse the project's existing conventions.
```

```text
Reorganize this existing project's root, but propose a migration map first.
Do not break old sessions, deployment manifests, or uncommitted work.
```

```text
This is a planning and data-analysis project, not a website.
Organize it around evidence sources, meetings, deliverables, and reusable assets.
```

```text
Use $sustainable-project-structure to maintain this distributed documentation library.
Merge duplicates, preserve valuable history, keep short-lived records out of the root index,
and automate index updates through the existing tools and AGENTS instructions.
```

```text
Organize this shared development kit and its example projects.
Leave sustainable rules and independent checks in each project; do not install the governance skill there.
```

## Sustainable Documentation

Update the existing canonical document before creating another one. Durable guides describe current behavior; task entries hold remaining work; dated records preserve useful evidence; changelogs summarize important changes. Promote reusable lessons into durable guides while leaving batch details in history. Do not delete material solely because it is old or unlinked.

Merging must preserve unique constraints, open work, and recovery information. Verify conflicts against implementation and evidence, repair relative incoming/outgoing links, and check programs that read Markdown paths or fields. Valid links alone do not demonstrate that the knowledge is current.

Fragmented WBS or dashboard progress can be reduced to current conclusions, pending verification and key milestones, with useful original evidence kept in history. Documentation cleanup must preserve IDs, task states, dates and acceptance conditions.

New scaffolds include a self-contained index generator and task-closeout instructions. From a generated development project root:

```bash
python3 91_ProjectTools/doc_index.py --write
python3 91_ProjectTools/doc_index.py
```

Research templates use `90_ReusableAssets/tools/doc_index.py`. The read-only command fails for stale indexes; regeneration preserves manual prose and is deterministic. It installs no hooks, scheduled jobs, or CI. Existing projects should reuse their tooling; `--allow-existing` does not inject this generator or markers into a nonempty project.

Indexing uses explicit scopes and H1 headings, omits short-lived and historical directories, and respects Git ignore rules. It is not a full Markdown link checker or an automatic archive classifier. See [the helper contract](skills/sustainable-project-structure/README.md) and [the documentation policy](skills/sustainable-project-structure/references/documentation-lifecycle.md) for boundaries and lifecycle rules.

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

No project skill directory is created or required by default. Use `--skill-dir` only to opt into a real project-specific workflow; it does not install this governance skill. Project rules and generated checks must work without the external skill.

Add `--apply` only after reviewing the preview. Even with `--allow-existing`, the helper creates missing files only and never overwrites existing ones.

Audit a project using the selected scaffold baseline (not arbitrary repository compliance):

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
│   ├── documentation-lifecycle.md
│   ├── migration-and-governance.md
│   └── research-projects.md
└── scripts/
    ├── scaffold_project.py
    ├── doc_index.py
    └── test_doc_index.py
```

The helpers require Python 3.10+ and the standard library; Git is required for indexing Git repositories. The skill instructions are in Chinese and can be used with Codex or Claude Code.

## Security Rules

- Do not bulk-move or delete existing files without authorization.
- Do not overwrite existing files or use archives as permanent dumping grounds.
- Do not store live credentials, personal data, private logs, or machine-specific absolute paths in the skill.
- Do not change production URLs, APIs, permissions, or data locations merely because local folders move.
- Treat structural audits as complements to project tests, builds, and deployment checks—not substitutes.

## Disclaimer

Folder templates are not the goal; stable ownership boundaries are. Adapt the final structure to project scale, team conventions, compliance needs, and existing deployment behavior. Review version-control state and backup strategy before any high-impact migration.
