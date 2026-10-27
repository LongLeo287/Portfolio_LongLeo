# Portfolio resource map

This map turns the read-only research from `Repo Inventory - Classified` into a
small, reviewable catalog for `Portfolio_LongLeo`.

The machine-readable source is [`assets/data/resource-links.json`](../assets/data/resource-links.json).
It is a research index, not a package manifest and not a replacement for
`assets/data/projects.json`.

Project-specific provenance for child landing-page claims is maintained in
[`assets/data/project-evidence.json`](../assets/data/project-evidence.json).
That catalog points to read-only local repositories and names documented
claims separately from content limits; it is the source to consult before
adding a metric, integration, release status or capability to a landing page.

For runtime-oriented repositories, the review also uses the public
[REA analyzer](https://github.com/morluto/rea) as a static evidence pass over
selected source files. REA output is treated as derived evidence with explicit
coverage limits; it does not replace browser QA or prove runtime reachability.

Landing-page implementation recipes are maintained separately in
[`assets/data/landing-architectures.json`](../assets/data/landing-architectures.json)
and explained in [`LANDING-PAGE-STUDIO.md`](LANDING-PAGE-STUDIO.md). The recipe
catalog references this resource map without turning research links into
runtime dependencies.

The catalog combines the read-only Sheet with external research checked on
2026-10-17. External research prioritizes normative and official sources:
W3C/WAI for WCAG and ARIA patterns, MDN for platform behavior, Google for
YouTube and Fonts, Web3Forms for the current form contract, web.dev/Chrome for
performance, and official repositories/docs for Playwright, axe, Web Vitals,
Lenis, adaptive frame/runtime scheduling and design-system references.

## How the catalog is used

- `use-now`: browser and interaction contracts that directly support the current motion-rich portfolio.
- `qa-candidate` / `release-reference`: sources for accessibility, performance and security gates.
- `reference-only`: design or motion guidance; no runtime dependency is implied.
- `future-project`: candidates for dedicated video, media or provenance workflows, not the portfolio shell.

The current portfolio remains HTML/CSS/vanilla JavaScript with a custom motion
engine. The catalog does not authorize installing GSAP, axe-core, FFmpeg or any
other dependency. A runtime adoption requires a separate change with license,
bundle-size, security and browser verification.

The catalog is intentionally not shipped to visitors: `resource-links.json` is
research metadata for maintainers, while `projects.json` remains the runtime
portfolio data source. The current open-source section has nine cards: eight
records in `scripts/build-labs.py` (two local `labs/` pages and six staged
external landings), plus the external-only AniBox card. AniBox's live site and
release repository are represented by `aniboxvn-live` and `anibox-release-repo`.
Run `python scripts/check-catalog.py` after changing either catalog boundary.
Run `python scripts/check-landing-architectures.py` after changing an
architecture recipe or a `data-lab-architecture` card mapping.

## Quality dimensions covered

The JSON catalog now includes a `qualityContract` for the areas that must be
reviewed whenever the Portfolio changes:

- UX/UI: hierarchy, scanability, semantics, focus order and interaction affordances.
- Design system: tokens, type scale, spacing, variants, states and motion timing.
- Color: text/UI contrast, non-color status signals, theme pairs and gradient backgrounds.
- Hover and interaction: hover enhancement, focus-visible, pressed states and pointer gating.
- Mobile/responsive: 320px, 390px, desktop, touch targets, no-hover behavior and overflow.
- QA/QC: static checks, keyboard/screen reader, contrast, visual regression, Web Vitals and runtime errors.
- Popup/modal: focus trap and restore, Escape/backdrop, `aria-hidden`, `aria-expanded`, inert background, scroll lock and media cleanup.
- Embed: click-to-load facade, allowlisted YouTube parsing, `youtube-nocookie`, iframe title/referrer policy, lazy loading and close fallback.
- Font: Vietnamese diacritics, fallback stack, `font-display: swap`, weight budget, FOIT/CLS and consistency with CV/landing pages.
- Form: labels, native validation, honeypot, length limits, pending/success/error/timeout states, third-party endpoint and privacy review.
- Media/SEO/i18n/browser: responsive sources, alt/error states, metadata/social cards, language parity, feature detection, hidden-tab behavior and autoplay policy.
- Standards/research: WCAG 2.2 AA target, WAI-ARIA dialog/carousel patterns, dated evidence and explicit unresolved assumptions.
- Privacy/third-party: deferred media, CSP, referrer/Permissions Policy, form processing, public access keys, retention and abuse controls.
- Testing automation: user-flow coverage for dynamic states with Playwright/axe/Lighthouse candidates plus manual keyboard, screen-reader and touch review.
- Adaptive runtime: frame-time feedback, shared scheduling, lifecycle pause, capability hints, hysteresis and explicit quality tiers.
- Lightweight loading: critical-path budgets, responsive media, fetch priority, idle/task scheduling, below-the-fold rendering and cautious prefetch.
- Adaptive motion/effects: hard reduced-motion behavior, Save-Data handling, low-end fallbacks, off-screen cleanup and preservation of semantics.

## AFR, loading and adaptive motion policy

In this repository, `AFR` means **adaptive frame/rendering policy**, not a
standard browser API. `requestAnimationFrame()` follows the display's refresh
rate, so animation progress must use the callback timestamp and must not assume
60Hz. A quality controller may change the amount of work or effect fidelity,
but it must not change the meaning of the content or make interaction harder.

Use a small, explicit ladder:

- `full`: normal motion and decorative effects when the page is responsive.
- `balanced`: fewer particles, blur/shadow layers or continuous updates when
  frame time or long tasks degrade.
- `lite`: transform/opacity-only motion, lower media quality and no optional
  background work on constrained devices or connections.
- `static`: reduced-motion or unsupported-API fallback; preserve content,
  focus, keyboard operation and status communication.

Signals are ranked by authority. `prefers-reduced-motion` and `Save-Data` are
hard constraints for non-essential motion or speculative loading. Visibility,
intersection, observed frame time, long tasks and supported network/device
hints are soft signals. `navigator.connection`, `navigator.deviceMemory` and
similar APIs must be feature-detected and must never be treated as a precise
device identity. Avoid user-agent sniffing.

The controller should require consecutive samples before changing tier, apply
a cooldown to prevent oscillation, and expose a manual override when the UI
has a meaningful preference. Pause timers, rAF loops, media and observers when
the document or component is hidden/off-screen. Batch DOM reads and writes;
chunk non-critical work; keep the critical path limited to first-view HTML,
CSS, fonts and media. `loading`, `decoding`, responsive sources,
`content-visibility`, `fetchpriority`, idle callbacks and task priorities are
separate hints, not substitutes for reserved dimensions and measurement.

The catalog's `adaptiveFrameRuntime`, `lightweightLoading` and
`adaptiveMotionEffects` contracts are the checklist for future implementation.
The new repository and agent-skill entries are reference-only: they do not
authorize adding a package, CDN, framework, telemetry or deployment-specific
integration to the current static site.

## Coverage gaps tracked honestly

The Sheet has no dedicated row for the YouTube Embed API/iframe contract,
popup/modal implementation, Google Fonts provider contract or Web3Forms. Those
items are therefore represented in `qualityContract` and the implementation,
not fabricated as Sheet resources. The Sheet does contain relevant typography,
Font Awesome, lazy-loading and responsive-QA references; they are cataloged as
reference or QA candidates and are not runtime dependencies.

## Release checklist for this motion-rich portfolio

- Popup: open from keyboard and pointer, trap focus, restore focus, close with Escape/backdrop, lock scroll, and stop iframe playback.
- Carousel: expose previous/next and slide pickers, provide stop/restart rotation, pause on keyboard focus/hover, and keep hidden slides out of the accessibility tree.
- YouTube: facade does not load third-party media before intent; URL is allowlisted; iframe has title, lazy loading, referrer policy and a fallback link.
- Font: Vietnamese text is readable during font load and with network failure; check line breaks, clipping, fallback and layout shift.
- Motion: hover is enhancement only; keyboard focus works; reduced motion disables cursor/card/slider motion and hidden tabs stop timers.
- Adaptive performance: exercise `full`, `balanced`, `lite`, `static`, hidden-tab, off-screen, Save-Data, slow-network and unsupported-API paths; record the signal and evidence for every tier change.
- Responsive: verify desktop, 390px and 320px, including modal media, form controls, slider controls and no horizontal overflow.
- Responsive matrix: `320, 360, 390, 414, 768, 834, 1024, 1280, 1440, 1920px`; verify the page keeps content inside the viewport at every width.
- QA/QC: run static checks, keyboard/screen reader review, contrast, runtime error checks, then Lighthouse/Web Vitals on representative devices.

## Priority order

1. Use Pointer Events, Page Visibility, Web Audio, typography QA and CSP/OWASP references when changing the interactive shell.
2. Use the UX/UI, design-system, open-design, Superdesign and HTML-artifact references when shaping a page or landing experience.
3. Add browser QA with axe-core and Lighthouse, then use Web Vitals gates on representative mobile devices.
4. Use GSAP/GSAP Skills/Impeccable, motion-dev and microinteraction references before considering a new motion dependency.
5. Keep FFmpeg, OpenTimelineIO, whisper.cpp, PySceneDetect, c2pa-rs and PixiJS scoped to future media/game-like projects.

## Source provenance

The catalog was derived from these read-only ranges in the source workbook:

- `Resource_Links!A4:H4`, `A13:H13`, `A20:H20`, `A29:H33`, `A32:H33`, `A38:H50`
- `Repos_Classified!A35:T35`, `A146:T146`, `A461:T461`, `A606:T606`, `A627:T627`, `A741:T741`, `A1022:T1022`, `A1310:T1310`, `A1339:T1339`, `A1559:T1559`, `A1678:T1678`, `A1685:T1685`, `A1708:T1708`
- `Repo_Verdicts!A9:K10`, `A24:K24`, `A34:K34`, `A38:K38`

External research references are stored in the same JSON catalog with
`origin: "external-research"` and `checkedAt: "2026-10-17"`. The main groups
are W3C WCAG/WAI-ARIA, MDN platform APIs, Google YouTube/Fonts, Web3Forms,
web.dev/Chrome performance, Playwright/axe/Web Vitals QA, adaptive frame/runtime
repositories and agent-skill references, and Material/Carbon/Radix/Motion design
references.

Source workbook:
<https://docs.google.com/spreadsheets/d/1IgJ_RvV9FfBkeFmXJpYUWfBJ6nkww1j1yjC9F0WMyo0/edit>
