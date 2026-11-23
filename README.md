# RAJ AI Reels Factory

Instagram-only, faceless Reels draft pipeline for **psychology, heartbreak and long-distance relationships**.

## What it does
- Runs twice daily at **12:30 and 20:30 Asia/Kolkata**.
- Uses the MIT-licensed [Automated Video Generator](https://github.com/itsPremKumar/Automated-Video-Generator) engine.
- Creates vertical 9:16 MP4 drafts and supporting review materials.
- Uploads each run as a GitHub Actions artifact for manual review.

## Approval and publishing
**Nothing is published automatically.** Review and approve each MP4 yourself. This repository does not connect to Instagram publishing.

## Run manually
Open **Actions → RAJ Reels Drafts → Run workflow**. Choose a slot and optionally provide a topic override.

## Cost and limitations
The workflow uses GitHub-hosted runners and upstream free media/voice sources where available. Public-repository runner usage is subject to GitHub's current Actions policies and availability. External media providers can change availability or rate limits.
