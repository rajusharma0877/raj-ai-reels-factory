# One-time setup

The workflow is intentionally manual: it starts temporary services, runs one Hermes task, uploads the log, and shuts everything down. It is not a 24/7 server.

## Required GitHub Actions secrets

Open **Settings → Secrets and variables → Actions → New repository secret**.

### 1. FREEAPI_ENCRYPTION_KEY

Generate a random 32-byte hex value anywhere you trust, for example:

```bash
openssl rand -hex 32
```

Save the result as the secret value. Do not put it in a committed file.

### 2. FREEAPI_CONFIG_JSON

This is FreeLLMAPI's declarative startup configuration. It provisions its first dashboard account and your upstream provider API keys on every fresh runner. The JSON must be one line when pasted as a GitHub secret.

Shape (replace every example value; do not use these placeholders literally):

```json
{
  "admin": {
    "email": "your-private-admin-email@example.com",
    "password": "choose-a-long-unique-password"
  },
  "keys": [
    { "platform": "google", "key": "YOUR_GOOGLE_API_KEY", "label": "google-main" },
    { "platform": "groq", "key": "YOUR_GROQ_API_KEY", "label": "groq-main" }
  ],
  "routing": { "strategy": "balanced" }
}
```

Only include providers for which you actually have API keys. A free model catalogue does not itself supply provider credentials. Keep the admin password and upstream keys private.

### 3. FREELLMAPI_UNIFIED_KEY

This is the client-facing `freellmapi-...` key used by Hermes to call the router. It is separate from upstream provider keys. Create/copy it from FreeLLMAPI's Keys / client-key interface after first-run provisioning, then save it as this secret.

## Run a task

After all three secrets exist:

1. Open the repository's **Actions** tab.
2. Select **AI Workspace**.
3. Press **Run workflow**.
4. Enter the task and leave model as `auto`, unless you want an exact FreeLLMAPI model ID.
5. After completion, open the run and download the `hermes-task-output` artifact.

## Important limitations

- GitHub Actions runners are temporary. FreeLLMAPI's SQLite database and Hermes memory/session files are not retained between runs in this first version.
- Provider keys and admin provisioning are re-applied from the encrypted GitHub Secrets inputs at each run; the FreeLLMAPI encryption key must remain the same for any database backup you later restore.
- The workflow currently stores the task log as an artifact. It does not publish to YouTube, Instagram, or any other service.
- Never add API keys, passwords, `.env` files, database files, or personal tokens to Git.
