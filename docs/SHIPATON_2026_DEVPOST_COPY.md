# Shipaton 2026 — Devpost copy

## Project name

**PAUL Open — Multilingual Science Companion**

## Tagline

**Understand the science. Question the evidence. Learn in your language.**

## One-line description

A multilingual science-learning companion that combines clear explanations, Socratic tutoring and evidence-first research reasoning, with transparent open research behind the product.

## Inspiration

AI learning tools are easy to make impressive in a demo and much harder to make trustworthy. PAUL Open started as an open research effort around multilingual scientific explanation, tutoring and evaluation. During development, one experimental checkpoint improved an automated diagnostic but did not pass the fresh human-comparison gate, so we did not promote it.

That experience shaped the product: instead of hiding uncertainty behind a single score, the companion helps learners understand assumptions, challenge misconceptions and distinguish observation from inference.

## What it does

PAUL Open offers three focused learning modes:

- **Explain** gives a concise concept explanation, key mechanism, assumptions and likely misconception.
- **Tutor me** starts with a diagnostic question and guides the learner toward understanding.
- **Research lens** helps separate evidence from inference, identify confounders and design a practical validation plan.

The first release supports English, Hindi and Bengali. A Research tab reads the current versioned PAUL Open research status rather than hard-coding claims into the app.

## How we built it

The mobile app is React + Vite packaged with Capacitor for Android. RevenueCat's official Capacitor SDK powers subscription entitlement checks, native Paywalls, purchase restoration and Customer Center.

The AI runtime is a small server-side service using Google's current Gen AI SDK and a Gemini model selected in deployment configuration. API credentials never ship in the mobile bundle.

The PAUL Open GitHub repository remains the research source of truth. Product inference and experimental research checkpoints are deliberately separated.

## RevenueCat

RevenueCat is part of the actual access-control experience rather than a decorative integration.

The free tier remains useful: 5 learning sessions per day with Explain and Tutor modes. PAUL Open Pro raises the daily limit to 40 sessions and unlocks Research lens. Store-localized prices are shown through the RevenueCat Paywall, and subscribers can restore or manage access using RevenueCat.

## Challenges

The hardest challenge was deciding what **not** to claim. Our automated V6 diagnostic improved relative to the SFT reference, but a fresh H8 development comparison preferred SFT on more cases. We kept SFT as the research reference instead of presenting the higher automated score as proof of a better model.

On the product side, we also kept AI credentials server-side and separated the production Gemini runtime from the experimental PAUL Open checkpoints.

## Accomplishments

- A functioning Android-first multilingual learning companion.
- Meaningful RevenueCat entitlement, Paywall, restore and Customer Center flows.
- English, Hindi and Bengali learning UX.
- Explain, Socratic Tutor and evidence-first Research modes.
- Live research-status transparency backed by a public versioned repository.
- A reproducible research trail that includes negative results rather than hiding them.

## What we learned

The biggest product lesson was that trustworthy AI UX is not only about refusal messages or disclaimers. It comes from product structure: asking what evidence exists, surfacing assumptions, avoiding false causal claims, and making evaluation boundaries visible.

Building in public also made the product narrower and clearer: science learning first, with research transparency as a differentiator rather than an overwhelming wall of model metrics.

## What's next

After Shipaton: stronger source-grounded science answers, teacher workflows, saved learning paths, broader Indian-language coverage, and a production-grade usage/entitlement backend.

## Research disclosure

The production companion currently uses a hosted Gemini service. It does **not** claim that the experimental DPO V6 checkpoint is the production model. PAUL Open research remains an independent open evaluation program and its current evidence does not establish DPO V6 superiority.

## Submission links to fill only when real

- Google Play: **ADD FINAL PUBLIC STORE URL**
- Demo video: **ADD FINAL PUBLIC VIDEO URL**
- Source: https://github.com/foundrypaul-cloud/paul-open
- Product website: https://www.paulfoundry.com/
- Build-in-public posts: **ADD PUBLIC POST URLS**
