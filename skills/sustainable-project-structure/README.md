# Sustainable Project Structure

Version 1.2.0. A Codex / Claude Code skill for maintaining project ownership, distributed documentation, and reproducible project tools. Instructions are in Chinese; the Python helpers require Python 3.10+ and the standard library. Git is required when indexing a Git repository.

Use [SKILL.md](SKILL.md) as the agent entry point. Existing projects retain their directory conventions and module-local docs. New projects can use the optional numbered scaffold; it is not a universal compliance standard.

## Documentation maintenance

- Keep one current source per fact. Compare and merge duplicate content while preserving unique constraints, evidence, open work, and recovery information.
- Maintain durable guides in place; keep current tasks separate from completed batches. Preserve useful historical records with dates, scope, and links to current guidance.
- Keep short-lived records within their owning modules, outside the root index. Old or unlinked does not by itself mean disposable.
- Generate indexes from paths and H1 titles; use AGENTS / CLAUDE to require regeneration and read-only checks at task closeout. No background watcher or CI is installed.

The detailed policy is [documentation-lifecycle.md](references/documentation-lifecycle.md). Project-specific rules, private paths, credentials, and logs must not be copied into a reusable skill.

## Helpers

Preview a new project, then add `--apply` to create it:

```bash
python3 scripts/scaffold_project.py init --root /path/to/project --name ExampleProject --profile development --unit 01_Catalog --agent codex
```

Use `--profile research` for a research template. `--allow-existing` creates missing baseline files without overwriting existing ones; it does not inject a new index tool or markers into a nonempty project. Prefer the project's existing tooling there.

New development templates include `91_ProjectTools/doc_index.py`; research templates include `90_ReusableAssets/tools/doc_index.py`. From the generated project root:

```bash
python3 91_ProjectTools/doc_index.py --write
python3 91_ProjectTools/doc_index.py
```

The second command is read-only: exit 0 means current, 1 means stale, 2 means invalid markers, missing H1, or another error. Use the research tool path for that profile. The copied tool is self-contained and does not depend on this installed skill.

README indexes use exactly one marker pair per participating README:

```html
<!-- DOC_INDEX:START scopes="*.md */README.md docs/**/*.md" -->

<!-- DOC_INDEX:END -->
```

Scopes are space-separated glob patterns relative to that README. `*` stays within one directory; `**` recurses. Configure ownership scopes, not individual filenames. The tool replaces only the marked region and leaves surrounding prose intact. For an existing project, add markers only after reviewing its needs and existing automation.

Root template indexes include module READMEs and shared long-lived documents; module indexes include their own docs. The helper excludes records/history/archive/temporary directories (including numbered prefixes), hidden/dependency/build directories, TASK/CHANGELOG/agent/migration files, symlinks, and nested Git repositories. Git roots use tracked plus unignored files. Short-lived material must have an appropriate home; the script cannot infer lifecycle from arbitrary prose. Local history navigation can use manual links or a separate existing record-index tool.

This is an index generator, not a full Markdown link checker or a truth/expiry classifier. Use the project's link checks for incoming links, outgoing links and anchors, including records omitted from the root. Check scripts that consume Markdown paths or fields before moving documents.

## Validation

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`scaffold_project.py audit` checks the selected scaffold baseline only. Run affected project tests when changing code or paths; do not trigger production tasks for documentation-only cleanup.
