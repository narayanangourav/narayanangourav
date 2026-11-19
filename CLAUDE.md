# CLAUDE.md

GitHub profile README for `narayanangourav` (this repo name = username, so README.md renders on the profile).

## How the page is built

README.md is almost only `<picture>` tags (dark + light SVG pairs). All visible text lives inside SVGs.

| Path | What |
|---|---|
| `README.md` | Masthead, typing line, 3 link buttons, then 7 numbered section panels |
| `tools/build_assets.py` | Generates every SVG in `assets/sheet/` (except `typing.svg`) and `assets/buttons/`. **Content lives in its constants** (ABOUT, CODE, FOCUS, STACK, EXTRA, COLLAB, ASK, TAG) |
| `tools/icons/` | skillicons.dev rows (`<row>-<dark/light>.svg`), embedded into the stack panel |
| `assets/sheet/` | masthead, about, mindset, focus, stack, collaborate, ask, closing (+ `typing.svg`, downloaded from readme-typing-svg) |
| `assets/buttons/` | portfolio, linkedin, email buttons (links are set in README.md) |

To change content: edit the constants in `tools/build_assets.py`, run `python tools/build_assets.py`, and update the matching `alt` text in README.md if needed. Never hand-edit generated SVGs.

Section order: 01 About Me, 02 Engineering Mindset, 03 Current Focus, 04 Technology Stack, 05 Building Better, Together, 06 Ask Me About, 07 Thanks for stopping by (tagline reveal).

## Design system ("engineering spec sheet")

- Canvas 880px wide; left label column (green mono index + section title), content column from x=240 (640px wide); hairline rules between sections.
- Transparent backgrounds. One typeface stack (Geist, then system sans), Geist Mono for labels/code/chips. One accent: green (`#3DD68C` dark, `#1A7F37` light).
- No dotted/patterned backgrounds, no gradients except the masthead name, no emoji headings, no stock GIFs, no colourful badges.
- Every SVG ships dark + light variants; animations respect `prefers-reduced-motion`.

## Owner's content rules (do not break)

- Keep all existing content; never drop sections or data without asking. Design changes are fine, content changes are not.
- Role "Software Engineer" appears once (masthead badge only).
- Never mention location (city/state/country) or a year anywhere.
- No GitRex section, no featured projects, no GitHub stats cards.
- Avoid repeating the same phrasing across sections.
- All assets go in subfolders of `assets/` (nothing loose at its top level).
- Confirmed tech: Python, Java, TypeScript/JavaScript, SQL; React.js, Next.js, Tailwind; Django/DRF, Flask, FastAPI, Node.js/Express; REST, RPC/gRPC, WebSockets; AWS (EC2, Lambda, S3) and GCP in production; Terraform, GitHub Actions, Jenkins, Docker, Kubernetes, Python/Bash scripting; PostgreSQL, MySQL, MongoDB, Firebase, Supabase, SQLite, BigQuery, SQLAlchemy; Jest, React Testing Library, SonarQube; OpenAI Codex, Claude Code. Not confirmed (ask before adding): pytest, JUnit, Helm, monitoring stacks. No certifications yet.
