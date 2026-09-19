# Shipaton 2026 — release checklist

## Code gate

- [ ] Shipaton Mobile CI passes: typecheck, web build, API tests, Android debug build.
- [ ] No secret or private research material in the mobile bundle.
- [ ] Public-boundary CI passes.
- [ ] Production app fetches research status from the public repository.
- [ ] App clearly states production runtime is separate from experimental PAUL Open checkpoints.

## AI service gate

- [ ] Cloud Run service deployed.
- [ ] Gemini key stored in Secret Manager, not GitHub/client code.
- [ ] `/healthz` returns 200.
- [ ] English Explain flow succeeds.
- [ ] Hindi Tutor flow succeeds in native script.
- [ ] Bengali Tutor flow succeeds in native script.
- [ ] Research lens distinguishes evidence/inference on a causal-confounding prompt.
- [ ] Logs do not contain prompt/response text.

## RevenueCat gate

- [ ] Android app created in RevenueCat.
- [ ] Public SDK key added to release configuration.
- [ ] `pro_access` entitlement created.
- [ ] Monthly and annual Google Play subscription products imported.
- [ ] Products attached to the active offering.
- [ ] Native Paywall opens.
- [ ] Sandbox purchase activates `pro_access`.
- [ ] App updates to Pro immediately after purchase.
- [ ] Restore works after reinstall/test reset.
- [ ] Customer Center opens for Pro customer.
- [ ] MainActivity launchMode is `singleTop`.

## Store gate

- [ ] App ID/package: `com.paulfoundry.paulopen`.
- [ ] Privacy policy publicly reachable.
- [ ] Support URL publicly reachable.
- [ ] 1024×1024 app icon.
- [ ] Required phone screenshots captured from real build.
- [ ] Data Safety form matches actual implementation.
- [ ] Signed AAB uploaded.
- [ ] Store listing submitted/released under current Shipaton rules.
- [ ] App reachable in the geography required by the rules.
- [ ] Judge access/trial instructions prepared if required.

## Evidence / impact gate

- [ ] At least 10 real external testers, not synthetic accounts.
- [ ] Record language used and mode used without collecting unnecessary PII.
- [ ] Ask one short optional usefulness question after testing.
- [ ] Record at least 3 product changes attributable to tester feedback.
- [ ] Do not claim impact from fabricated or self-generated usage.

## Submission gate

- [ ] Devpost copy reconciled with the final build.
- [ ] Public store URL added.
- [ ] <=2-minute public demo video added.
- [ ] App icon and screenshot uploaded.
- [ ] RevenueCat integration described accurately.
- [ ] Relevant prize categories selected.
- [ ] #Shipaton / #BuildInPublic URLs added.
- [ ] Final submission reviewed against official rules before deadline.
