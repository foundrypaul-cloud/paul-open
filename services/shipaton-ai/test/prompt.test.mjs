import test from 'node:test';
import assert from 'node:assert/strict';
import { buildPrompt } from '../src/prompt.mjs';

test('prompt keeps research and production identities separate', () => {
  const text = buildPrompt({
    question: 'Why does pressure rise?',
    language: 'English',
    mode: 'explain',
  });
  assert.match(text, /hosted Gemini service/);
  assert.match(text, /Do not claim to be the experimental PAUL Open DPO checkpoint/);
  assert.match(text, /Why does pressure rise\?/);
});

test('research mode requires evidence-first reasoning without invented certainty', () => {
  const text = buildPrompt({
    question: 'Did a printer cause headaches?',
    language: 'English',
    mode: 'research',
  });
  assert.match(text, /Separate observation from inference/);
  assert.match(text, /confounders/);
  assert.match(text, /Never invent/);
});

test('Hindi mode requires native script while preserving technical notation', () => {
  const text = buildPrompt({
    question: 'Explain induction heating',
    language: 'Hindi',
    mode: 'tutor',
  });
  assert.match(text, /Devanagari/);
  assert.match(text, /standard scientific notation/);
});
