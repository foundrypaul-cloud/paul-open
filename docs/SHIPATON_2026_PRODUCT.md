# RevenueCat Shipaton 2026 — PAUL Open product execution

**Product:** PAUL Open — Multilingual Science Companion  
**Primary platform:** Android via Capacitor  
**Submission deadline:** 2026-09-30 11:45 PM PDT  
**Competition source:** https://revenuecat-shipaton-2026.devpost.com/rules

## Product thesis

PAUL Open turns a rigorous open-research methodology into a focused learning product:

- **Explain** — concise scientific explanation with assumptions and misconception correction.
- **Tutor me** — diagnostic question + guided explanation + checkpoint.
- **Research lens (Pro)** — observation vs inference, confounders, uncertainty, and validation plan.
- **Languages** — English, Hindi, Bengali in the first mobile release.
- **Research transparency** — live status comes from the canonical PAUL Open public repository.

The production companion uses a hosted Gemini service. It must **not** be described as serving DPO V6. The PAUL Open research line is the evidence and evaluation layer; production inference is a separate implementation choice.

## RevenueCat product contract

Entitlement:

`pro_access`

Recommended store products:

- `paul_open_pro_monthly`
- `paul_open_pro_annual`

Attach both to `pro_access` and the current/default offering.

Free:

- 5 learning sessions per day;
- Explain;
- Tutor me;
- English/Hindi/Bengali;
- public research-status view.

Pro:

- 40 learning sessions per day;
- Research lens;
- store-managed subscription controls through RevenueCat Customer Center.

Do not hard-code prices in product copy. Let the native store / RevenueCat Paywall show localized pricing.

## Shipaton eligibility implementation

The mobile client includes the official RevenueCat Capacitor SDK and UI package and uses them for entitlement status, Paywalls, restore purchases and Customer Center. This satisfies the technical integration direction; competition eligibility still requires a real configured store product, qualifying purchase path, and the required public store release/submission evidence under the current rules.

## Impact story

The strongest competition narrative is not "we trained the best model." The research explicitly rejected that claim.

The story is:

> Science learning should be accessible across language boundaries, and AI products should show what is known, what is uncertain, and what failed in evaluation. PAUL Open combines a multilingual learning companion with an unusually transparent research record.

## Manual external dependencies

The repository cannot create or approve these account-level assets by itself:

1. RevenueCat project/app + public Android SDK key.
2. Google Play app record + subscription products.
3. Cloud Run deployment + Secret Manager value for the Gemini key.
4. Signed Android App Bundle and Play Console release.
5. Store listing review/public availability in the required geography.
6. Devpost authenticated submission fields.
7. Public #Shipaton posts on the user's chosen social accounts.

All code, copy and execution contracts for those steps are versioned here.
