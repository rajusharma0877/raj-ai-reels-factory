# Raj AI Workspace

A zero-budget, on-demand AI workspace powered by GitHub Actions.

## Purpose

This repository is the shared runtime for general-purpose AI tasks. YouTube automation is one project, not the only purpose.

Planned components:
- **Hermes Agent** — task orchestration and tool use.
- **FreeLLMAPI** — model/API gateway used by Hermes.
- **GitHub Actions** — temporary runner that starts the services for a requested task and shuts down when the job ends.

## Important runtime behavior

This is **on-demand**, not 24/7 hosting. Services exist only while a GitHub Actions job is running. Start a run from the Actions tab or via a configured schedule. When the job ends, the runner and its processes are discarded.

## Security

- Never commit API keys, tokens, passwords, or personal data.
- Add credentials only as GitHub Actions repository secrets.
- Keep generated media and large temporary files out of Git history.
- Review third-party actions and container images before use.

## Status

Initial repository reset completed. The reusable runner, FreeLLMAPI service startup, Hermes setup, and task entry points are being added in stages. No credentials are stored in this repository yet.
