# Contributing to DroidRun Examples

Thanks for your interest in improving this examples repository! This guide helps you propose changes smoothly and keep examples consistent.

## Ways to contribute

- Fix typos, broken links, and small bugs
- Improve documentation or add quickstart sections
- Add tests or lightweight validation scripts
- Create a new example project (see template below)

## Project structure conventions

Each example should be self-contained:

- `main.py` — entrypoint to run the example
- `requirements.txt` — minimal, pinned dependencies where possible
- `agents/` — reusable components (submodules allowed)
- `agents/prompts/` — prompt files if the example uses LLMs
- `data/`, `images/` — sample inputs and outputs (small only)
- `README.md` — what it does, how to run, configuration knobs, optimally with a demo video

Keep any API keys out of the repo; prefer environment variables with clear placeholders in README.
ME.

## Coding style and quality

- Prefer Python 3.10+ features available broadly; keep dependencies lean
- Add type hints where obvious; avoid over-typing
- Handle errors gracefully and log actionable messages
- Keep network or scraping code respectful of target sites (rate limits, robots, ToS)

## Git and PR checklist

- Branch from `main` and keep PRs focused
- Update top-level `Readme.md` to include your new example (2 lines)
- Ensure `requirements.txt` installs cleanly in a fresh venv
- Verify basic run works: `python <example>/main.py`

## Licensing and assets

- Only include images/data you own or that are under a permissive license
- Avoid large binaries; link to external sources when necessary

## Questions

Open an issue or start a discussion in the main Droidrun repository. Happy hacking!
