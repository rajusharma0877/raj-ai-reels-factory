# One-time setup

The workflow is manual and on-demand: it starts FreeLLMAPI in a temporary Docker container, installs Hermes, configures Hermes against the local gateway, runs one task, uploads the log, and shuts down the container. It is not a 24/7 server.

## Add these GitHub Actions secrets

Open **Settings → Secrets and variables → Actions → New repository secret**.

### 1. FREEAPI_ENCRYPTION_KEY

Generate a random 32-byte (64 hex-character) value. Example command:

```bash
openssl rand -hex 32
```

Save the output as the secret value. Do not put it in a committed file. Keep this value stable if you later restore an encrypted FreeLLMAPI database backup.

### 2. FREEAPI_CONFIG_JSON

FreeLLMAPI supports declarative startup provisioning through this environment variable. It creates the first dashboard account and adds provider credentials on each fresh runner boot.

Use this JSON shape, replacing the example values with your own. Paste it as a single-line JSON value in the GitHub secret:

```json
{
  "admin": {
    "email": "your-private-admin-email@example.com",
    "password": "choose-a-long-unique-password"
  },
  "keys": [
    { "platform": "groq", "key": "YOUR_GROQ_API_KEY", "label": "groq-main" },
    { "platform": "google", "key": "YOUR_GOOGLE_API_KEY", "label": "google-main" }
  ],
  "routing": { "strategy": "balanced" }
}
```

Only include provider entries for which you have actual API keys. The example providers are illustrative; this does not grant free API access. You can add more provider keys later by editing this secret. Treat the entire JSON as a password because it contains plaintext credentials.

### 3. FREELLMAPI_UNIFIED_KEY

This is the client-facing `freellmapi-...` bearer key used by Hermes. It is not an upstream provider API key. Create/copy a unified key in FreeLLMAPI's dashboard **Keys** page after provisioning.

Because this GitHub Actions setup starts with a fresh temporary database each run, the unified key must be stable and accepted by the declarative config / initial setup. If your FreeLLMAPI build generates the unified key only interactively and cannot provision it declaratively, the first workflow run will need a small bootstrap step to create/capture it; do not paste an upstream provider key in its place.

## Run a task

After the secrets exist:

1. Open the repository's **Actions** tab.
2. Select **AI Workspace**.
3. Press **Run workflow**.
4. Enter your task. Leave model blank to use the catalog default, or enter an exact model ID.
5. When the run finishes, open it and download the `hermes-task-output` artifact.

## Important limitations

- GitHub Actions runners are temporary. FreeLLMAPI's SQLite database and Hermes memory/session files are not retained between runs in this first version.
- Provider keys and dashboard provisioning are reapplied from GitHub Secrets on every run.
- The FreeLLMAPI port is bound to runner loopback only; it is not exposed publicly.
- The workflow uploads task logs only. It does not publish to YouTube, Instagram, or any other service.
- Never commit API keys, passwords, `.env` files, database files, or personal tokens to Git.
- This workflow has not yet completed a live end-to-end run. Do not treat the setup as operational until the first Actions run passes.
