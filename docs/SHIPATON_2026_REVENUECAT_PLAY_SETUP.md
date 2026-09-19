# Shipaton 2026 — RevenueCat + Google Play account setup

This is the account-level handoff for the PAUL Open Android build. Do not place service-account JSON, RevenueCat secret keys, Play signing keys, or Gemini keys in this public repository.

## Recommended execution order

1. **Google Play app**
   - Create/select the Android app for package `com.paulfoundry.paulopen`.
   - Upload a signed APK/AAB to an appropriate testing track so Google Play enables product configuration.

2. **Google Play subscriptions**
   - Create the subscription products/base plans that will back PAUL Open Pro.
   - Keep identifiers stable. Suggested PAUL naming:
     - `paul_open_pro_monthly`
     - `paul_open_pro_annual`
   - Activate the base plans and set real localized pricing in Play Console.
   - Do not hard-code those prices in app UI.

3. **RevenueCat Android app + Play credentials**
   - Add the Android app/package to the RevenueCat project.
   - Create the least-privilege Google Play service account RevenueCat requires, grant the documented Play Console permissions, and upload the JSON credential only through RevenueCat's secure dashboard.
   - RevenueCat notes that new Google Play service credentials can take up to 36 hours to become valid, so do this early.

4. **RevenueCat products and entitlement**
   - Import the Google Play products/base plans into RevenueCat.
   - Create entitlement `pro_access`.
   - Attach both subscription products/base plans to `pro_access`.

5. **RevenueCat offering + paywall**
   - Create one Offering and make it the current/default Offering.
   - Add monthly and annual Packages with the matching Google Play products.
   - Attach a RevenueCat Paywall to that Offering.
   - Configure Customer Center so subscribers can inspect/manage access.

6. **Native public SDK key**
   - Copy only the RevenueCat Android **public SDK key** into the release build as `VITE_REVENUECAT_ANDROID_API_KEY`.
   - Never put a RevenueCat secret API key into the mobile client or this repository.

7. **Sandbox validation**
   - Use a Play license tester / supported test track.
   - Verify: Paywall renders → purchase completes → `pro_access` is active → Research lens unlocks → app restart retains Pro → Restore succeeds → Customer Center opens.

## Source-of-truth links

- RevenueCat Capacitor installation: https://www.revenuecat.com/docs/getting-started/installation/capacitor
- RevenueCat Google Play product setup: https://www.revenuecat.com/docs/getting-started/entitlements/android-products
- RevenueCat entitlements: https://www.revenuecat.com/docs/getting-started/entitlements
- RevenueCat Offerings: https://www.revenuecat.com/docs/offerings/overview
- RevenueCat Play service credentials: https://www.revenuecat.com/docs/service-credentials/creating-play-service-credentials

## Stop conditions

Do not record the Shipaton RevenueCat gate as complete unless a real native test purchase activates `pro_access`.

Do not record the store-release gate as complete unless the final store URL and required availability can be verified.

Do not commit dashboard screenshots containing service credentials, API secrets, signing material, private customer identifiers, or Play account information.
