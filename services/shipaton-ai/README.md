# PAUL Open Shipaton AI service

Minimal server-side Gemini runtime for the Shipaton mobile companion.

The service deliberately separates **product inference** from **PAUL Open research checkpoints**. It never claims the experimental DPO V6 adapter is being served.

## Run

```bash
cd services/shipaton-ai
cp .env.example .env
npm install
npm test
set -a && . ./.env && set +a
npm start
```

Required server-only value:

```text
GOOGLE_API_KEY=
```

The production model is selected through `GEMINI_MODEL`. Product copy displays only the family label "Gemini" so a backend model change does not create stale UI claims.

## Cloud Run

Example:

```bash
gcloud run deploy paul-open-companion-api \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_MODEL=gemini-flash-latest,ALLOWED_ORIGINS=https://localhost \
  --set-secrets GOOGLE_API_KEY=PAUL_OPEN_GEMINI_API_KEY:latest
```

Use Secret Manager for the API key. Never put the Gemini key in the mobile bundle or public repository.

## Privacy behavior

The server does not intentionally log prompt or response text. Operational logs contain request ID, mode, language and latency. Prompts are transmitted to the configured Google AI service to generate a response.
