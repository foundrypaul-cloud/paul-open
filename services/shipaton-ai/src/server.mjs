import { createServer } from 'node:http';
import { randomUUID } from 'node:crypto';
import { GoogleGenAI } from '@google/genai';
import { buildPrompt } from './prompt.mjs';

const port = Number(process.env.PORT || 8080);
const apiKey = process.env.GOOGLE_API_KEY;
const model = process.env.GEMINI_MODEL || 'gemini-flash-latest';
const allowedOrigins = new Set(
  (process.env.ALLOWED_ORIGINS || 'https://localhost,http://localhost')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean),
);

if (!apiKey) {
  console.error('GOOGLE_API_KEY is required.');
  process.exit(1);
}

const ai = new GoogleGenAI({ apiKey });
const windows = new Map();
const WINDOW_MS = 60_000;
const MAX_REQUESTS = 30;

function corsHeaders(origin) {
  const allowed = origin && (allowedOrigins.has(origin) || origin === 'capacitor://localhost');
  return {
    'access-control-allow-origin': allowed ? origin : 'https://localhost',
    'access-control-allow-methods': 'GET,POST,OPTIONS',
    'access-control-allow-headers': 'content-type',
    'access-control-max-age': '600',
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'x-content-type-options': 'nosniff',
  };
}

function send(res, status, payload, origin) {
  res.writeHead(status, corsHeaders(origin));
  res.end(JSON.stringify(payload));
}

function clientKey(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (typeof forwarded === 'string') return forwarded.split(',')[0].trim();
  return req.socket.remoteAddress || 'unknown';
}

function rateLimited(req) {
  const key = clientKey(req);
  const now = Date.now();
  const current = windows.get(key);
  if (!current || now - current.startedAt >= WINDOW_MS) {
    windows.set(key, { startedAt: now, count: 1 });
    return false;
  }
  current.count += 1;
  return current.count > MAX_REQUESTS;
}

async function readJson(req) {
  let body = '';
  for await (const chunk of req) {
    body += chunk;
    if (body.length > 24_000) throw new Error('REQUEST_TOO_LARGE');
  }
  return JSON.parse(body || '{}');
}

function validate(payload) {
  const question = typeof payload?.question === 'string' ? payload.question.trim() : '';
  const language = ['English', 'Hindi', 'Bengali'].includes(payload?.language)
    ? payload.language
    : 'English';
  const mode = ['explain', 'tutor', 'research'].includes(payload?.mode)
    ? payload.mode
    : 'explain';

  if (question.length < 3 || question.length > 2000) {
    return { error: 'Question must be between 3 and 2000 characters.' };
  }
  return { question, language, mode };
}

const server = createServer(async (req, res) => {
  const origin = typeof req.headers.origin === 'string' ? req.headers.origin : '';

  if (req.method === 'OPTIONS') {
    res.writeHead(204, corsHeaders(origin));
    return res.end();
  }

  if (req.method === 'GET' && req.url === '/healthz') {
    return send(res, 200, { status: 'ok', provider: 'Gemini' }, origin);
  }

  if (req.method === 'GET' && req.url === '/v1/meta') {
    return send(
      res,
      200,
      {
        providerLabel: 'Gemini',
        researchCheckpointServed: false,
        researchSource: 'https://github.com/foundrypaul-cloud/paul-open',
      },
      origin,
    );
  }

  if (req.method !== 'POST' || req.url !== '/v1/assist') {
    return send(res, 404, { error: 'Not found.' }, origin);
  }

  if (rateLimited(req)) {
    return send(res, 429, { error: 'Too many requests. Try again shortly.' }, origin);
  }

  const requestId = randomUUID();
  const started = Date.now();

  try {
    const raw = await readJson(req);
    const input = validate(raw);
    if (input.error) return send(res, 400, { error: input.error }, origin);

    const response = await ai.models.generateContent({
      model,
      contents: buildPrompt(input),
    });

    const answer = response.text?.trim();
    if (!answer) throw new Error('EMPTY_MODEL_RESPONSE');

    console.log(
      JSON.stringify({
        event: 'assist_complete',
        requestId,
        latencyMs: Date.now() - started,
        mode: input.mode,
        language: input.language,
      }),
    );

    return send(
      res,
      200,
      {
        answer,
        providerLabel: 'Gemini',
        requestId,
        note: 'AI can make mistakes. Verify important scientific or real-world decisions.',
      },
      origin,
    );
  } catch (error) {
    const code = error instanceof Error ? error.message : 'UNKNOWN';
    console.error(
      JSON.stringify({
        event: 'assist_error',
        requestId,
        latencyMs: Date.now() - started,
        errorType: code === 'REQUEST_TOO_LARGE' ? code : 'MODEL_OR_RUNTIME_ERROR',
      }),
    );
    return send(
      res,
      code === 'REQUEST_TOO_LARGE' ? 413 : 500,
      {
        error:
          code === 'REQUEST_TOO_LARGE'
            ? 'Request is too large.'
            : 'The learning service could not answer this request. Please try again.',
        requestId,
      },
      origin,
    );
  }
});

server.listen(port, '0.0.0.0', () => {
  console.log(JSON.stringify({ event: 'server_started', port, provider: 'Gemini' }));
});
