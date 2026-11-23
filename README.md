# Raj AI Workspace

A zero-budget, on-demand AI workspace powered by GitHub Actions.

## Purpose

This repository is the shared runtime for general-purpose AI tasks. YouTube automation is one project, not the only purpose.

- **Hermes Agent** — task orchestration and tool use.
- **FreeLLMAPI** — OpenAI-compatible model/API gateway.
- **GitHub Actions** — temporary runner that starts the services for a requested task and shuts down when the job ends.

## Run a task

1. Complete the one-time setup in [SETUP.md](SETUP.md).
2. Open **Actions → AI Workspace → Run workflow**.
3. Enter a task and optionally choose a FreeLLMAPI model.
4. Download the `hermes-task-output` artifact when the run finishes.

## Runtime behavior

This is **on-demand**, not 24/7 hosting. Services exist only while a GitHub Actions job is running. The first version uploads task logs as artifacts; Hermes memory/session state and FreeLLMAPI's SQLite database are not yet persisted between runs.

## Security

- Never commit API keys, tokens, passwords, or personal data.
- Store credentials only as GitHub Actions repository secrets.
- The FreeLLMAPI port is bound to runner loopback, not exposed publicly.
- Review third-party actions and container images before use.

## Current status

- [x] Remove the old Instagram Reels workflow and scripts from the active tree.
- [x] Add an on-demand GitHub Actions workflow.
- [x] Start FreeLLMAPI in a temporary container.
- [x] Install Hermes and route it to FreeLLMAPI.
- [x] Upload task logs as a run artifact.
- [ ] Add the required repository secrets and perform the first live run.
- [ ] Add durable encrypted state backup / restore for memory and provider configuration.
