# Portfolio_LongLeo — Orca workspace contract

- Project: `Portfolio_LongLeo`
- Repository: `D:/OrcaWorkspaces/Portfolio_LongLeo`
- Remote: `https://github.com/LongLeo287/Portfolio_LongLeo.git`
- Branch/base: `main` / `origin/main`
- Delivery architecture: static HTML + CSS + vanilla JavaScript; UI behavior is interactive and motion-rich
- Utilities: Python scripts; Pillow is required only for image generation
- Live site: `https://portfolio-longleo.vercel.app`

## Workspace roles

- `Portfolio — 00 Coordinator`: planning, task routing and integration review.
- `Portfolio — 01 UI & Design`: HTML/CSS, design tokens, responsive and motion.
- `Portfolio — 02 Content & Data`: `projects.json`, bilingual copy, SEO and media metadata.
- `Portfolio — 03 Landing & Scripts`: `landing/` and Python generation/check scripts.
- `Portfolio — 04 Independent QA`: read-only accessibility, links, responsive and regression review.

Workers must use isolated worktrees and disjoint write-sets. Coordinator is the
only integration authority. No automatic deploy, push or cross-repository write.

## Verification

- Preview: `python -m http.server 8000`
- Page/accessibility check: `python scripts/check-pages.py`
- Contrast check: `python scripts/check-contrast.py`
- Labs generation: `python scripts/build-labs.py` only when the task scopes generated pages.

The project has no Node package manifest and no Vercel CLI configured locally;
do not invent a package-install or deployment workflow.

## Browser QA connector

ORCA browser QA for this workspace uses Tencent BrowserSkill with the existing
Chrome profile `LongLeo` only:

- Browser instance: `3b097077`
- Start action: `BrowserSkill — LongLeo`
- CLI command: `bsk session start --browser 3b097077 --json`
- Existing user tabs require explicit borrowing before interaction.
- If this instance is disconnected, stop and ask the user to reconnect
  `LongLeo`; never create a profile or switch to another browser instance.

The workspace action delegates to
`scripts/start-browser-skill-longleo.ps1`, which validates the local CLI and
uses the fixed instance selector.
