# Repository Publishing Rules

- Before staging or committing, confirm the current branch is the intended target branch.
- Do not continue work on an old temporary branch by default.
- Never commit credentials, tokens, private logs, local configuration, or generated caches.
- Keep the repository description, Topics, README files, and examples aligned with the implemented skill.
- Push directly to `main` only when the user explicitly requests publication or an update.

## Skill Maintenance

- Maintain the public source in `skills/sustainable-project-structure/`; keep its entry point concise and use `references/documentation-lifecycle.md` as the documentation-policy source.
- When behavior changes, align the helper contract, generated project instructions, and English/Chinese READMEs. Preserve existing-project conventions and describe only automation that actually runs.
- Run `python3 -m unittest discover -s skills/sustainable-project-structure/scripts -p 'test_*.py'` and the available skill format validator before publishing script changes; review `git diff --check` and the complete public package for private information.
- Keep the skill metadata version and README badges aligned. Distribution-specific metadata belongs in temporary publication bundles, not in the reusable source.
