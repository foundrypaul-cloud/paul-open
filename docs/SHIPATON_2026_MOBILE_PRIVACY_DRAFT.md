# PAUL Open Mobile — Privacy Notice Draft

**Status:** release-review draft for the Shipaton 2026 Android MVP  
**Operator:** Paul Foundry Technologies Private Limited  
**Product:** PAUL Open — Multilingual Science Companion

This draft is intentionally narrower than PAUL Foundry's general website privacy policy. Publish an app-specific final version on a stable HTTPS URL before the production Play listing is submitted.

## What the MVP processes

### Learning prompts and AI responses

When a user asks a question, the app sends the prompt, selected language, and selected learning mode to the PAUL Open Companion backend. The backend sends the material needed to generate the answer to the configured Google Gemini service.

The MVP backend is designed not to intentionally log prompt or response text. Operational logs may contain non-content metadata such as a generated request identifier, language, learning mode, latency, and error category.

Do not promise that upstream infrastructure retains no data unless the deployed Google account/model configuration independently supports that statement.

### Purchases and subscriptions

The Android app uses Google Play Billing through RevenueCat. Google Play and RevenueCat process purchase/subscription information required to complete transactions, determine entitlement state, restore purchases, and provide subscription management.

The client uses RevenueCat entitlement `pro_access` to unlock PAUL Open Pro.

### Local usage counter

The MVP stores a daily session counter locally on the user's device to support the Free/Pro usage experience. This local counter is not intended as a durable analytics identity or a secure server-side quota.

### Public research status

The Research screen fetches public, versioned PAUL Open status information from the project's public GitHub repository.

## What the MVP does not require

The initial mobile MVP does not require the user to create a PAUL Open account or provide a name/email to use the learning companion.

This statement must be revised if sign-in, cloud history, teacher accounts, analytics identity, or other account features are added.

## Why data is processed

The above data is processed to:

- generate the requested educational response;
- operate and secure the service;
- enforce product access/entitlements;
- restore and manage purchases;
- diagnose failures and measure basic service reliability;
- display the project's public research status.

## Third-party processors/services

The released app may interact with:

- Google Play for Android distribution and billing;
- RevenueCat for subscription and entitlement infrastructure;
- Google Gemini / Google AI infrastructure for response generation;
- the deployed hosting provider for the PAUL Open Companion backend;
- GitHub for public research-status retrieval.

The final published notice should link to the applicable third-party privacy information and should match the exact production deployment.

## AI limitations

PAUL Open uses generative AI. AI responses may be incomplete or incorrect. Users should independently verify important scientific, medical, safety-critical, legal, financial, or other consequential information with appropriate sources or qualified professionals.

## Children and education

Before intentionally offering the app to children or configuring a Play target audience that includes children, complete a separate child-safety/privacy review and ensure the app, SDK configuration, ads/analytics choices, content, and store disclosures comply with the applicable Google Play families/target-audience requirements and applicable law.

The current Shipaton MVP should not make an unreviewed claim that it is specifically designed for children.

## User choices and requests

The final published notice should provide a stable support/privacy contact and explain how users may submit applicable data-access or deletion questions. Purchase cancellation/refund/subscription controls are also governed by Google Play and RevenueCat flows.

## Release verification

Before publishing this notice:

- verify the production Gemini/Google data configuration;
- verify Cloud Run/service logging configuration;
- verify RevenueCat and Google Play data actually used;
- verify whether any analytics/crash SDKs were added after this draft;
- reconcile the Google Play Data Safety form with the released binary;
- add the final effective date, support contact, legal jurisdiction, and stable public HTTPS URL;
- have company counsel/authorized governance owner review the final text.

This document is product-engineering preparation, not legal advice.
