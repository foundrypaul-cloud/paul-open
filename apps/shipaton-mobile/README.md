# PAUL Open — Shipaton mobile client

Android-first Capacitor client for the RevenueCat Shipaton 2026 product submission.

## Product boundary

This client **does not redefine PAUL Open research claims** and does not pretend the experimental DPO V6 adapter is the production inference model.

- Research status is read from `public/research-status.json` on the canonical public repository.
- The companion runtime calls a separately deployed hosted AI service.
- The current backend implementation uses the official Google Gen AI SDK and identifies the runtime only as **Gemini**, avoiding a stale hard-coded model version in product copy.
- PAUL Open research remains the evidence/provenance layer.

## Local web preview

```bash
cd apps/shipaton-mobile
cp .env.example .env
npm install
npm run dev
```

The web preview intentionally disables native purchases.

## Android

```bash
npm install
npm run build
npx cap add android
npm run android:patch
npx cap sync android
npx cap open android
```

The patch step changes the generated MainActivity launch mode to `singleTop`, matching RevenueCat's Capacitor guidance for payment flows that temporarily background the app.

## RevenueCat contract

Create these objects in RevenueCat / Google Play:

- entitlement: `pro_access`
- offering: use the project's current/default offering
- products: monthly + annual subscriptions, attached to `pro_access`

Set the native public SDK key in `.env`:

```text
VITE_REVENUECAT_ANDROID_API_KEY=
VITE_REVENUECAT_ENTITLEMENT_ID=pro_access
```

The SDK API key is a public client key by design. Never place a RevenueCat secret API key in this mobile app.

The app uses RevenueCat for entitlement checks, native Paywalls, purchase restoration, and Customer Center.

## AI endpoint

Deploy `services/shipaton-ai`, then set:

```text
VITE_PAUL_AI_ENDPOINT=https://YOUR_SERVICE_HOST
```

Do not ship a Gemini API key in the mobile app.
