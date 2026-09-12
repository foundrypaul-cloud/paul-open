# PAUL Open — H4 P1 Failure Analysis

**Status:** COMPLETE  
**Date:** 2026-09-12  
**Evidence:** frozen H4 DHE SFT and DPO V2 Corrective outputs supplied from the completed private H4 generation artifact.  
**Scope:** development diagnosis only; H4 remains completed DHE and SHAE remains sealed.

## Method

Compare the frozen source-labelled SFT and DPO V2 responses case by case. Record observable response differences first, then development hypotheses. Do not copy evaluator comments into training data and do not treat the six H4 prompts as future clean evaluation cases.

## Case findings

### H4-DHE-001 — STEM / preservation

DPO V2 improves the central pressure explanation. It says cooling lowers internal pressure and the pressure difference deforms the flexible bottle. The SFT response instead says the air becomes denser and "takes up less volume" while also describing the bottle as a fixed container, which is a less coherent account of the mechanism.

**Development implication:** preserve DPO V2's explicit causal chain: cooling -> lower molecular collision force/frequency -> lower internal pressure -> external pressure exceeds internal pressure -> inward deformation.

### H4-DHE-002 — Educator / diagnostic

Both outputs satisfy the instruction to begin with a question, but both stop after one question and neither develops a Socratic sequence. The DPO question asks whether the mass of the water becomes smaller; the SFT question asks about mass before versus after adding salt. The SFT formulation more directly invites an observable before/after measurement, whereas the DPO formulation remains closer to the student's verbal misconception.

**Hypothesis:** DPO V2 may over-compress tutoring responses and may paraphrase the misconception rather than selecting a concrete test or measurement that creates productive cognitive conflict.

**Target behavior:** when asked for Socratic tutoring, begin with one focused, experimentally testable question and then, when the prompt permits, scaffold rather than immediately asserting the explanation.

### H4-DHE-003 — Scientific research assistance / neutral diagnostic

The SFT and DPO V2 outputs are textually identical in the supplied artifact. Therefore this case provides no evidence of a DPO-induced behavioral difference despite its human-evaluation allocation.

The shared response itself has two weaknesses worth tracking independently of DPO: it says a further reading "should" return to the cluster if instrument and technique were perfect, which is too strong, and it uses a >3 SD rule as if it could establish exclusion. A statistical threshold alone does not establish that an observation is erroneous.

**Development implication:** no DPO-specific corrective pair should be derived from this case. Future research-assistance data should emphasize provenance, instrument/notes checks, repeatability, sensitivity analysis with and without the unusual point, and documented exclusion criteria rather than automatic deletion by threshold.

### H4-DHE-004 — Hindi / preservation

Both responses are truncated before completing all requested parts, so neither is an ideal target. DPO V2 is somewhat more explicit about intended battery-longevity use, but it also introduces an inaccurate car-engine analogy and states that chemical reactions at 100% become "very fast," which is an oversimplification. SFT contains a different inaccurate explanation involving "electron accumulation."

**Development implication:** preserve the useful Hindi accessibility/structure signal but do not preserve these scientific mechanisms verbatim. Future Hindi scientific-explanation data should favor simple but physically grounded concepts: high state of charge and high voltage can accelerate some degradation processes; heat matters; partial charging can reduce long-term stress; 20–80 is a longevity heuristic, not a cliff at 80%.

### H4-DHE-005 — Bengali / diagnostic

This is the clearest DPO V2 factual regression in H4. DPO V2 says heating a closed pressure cooker makes the pressure over the water decrease and then claims that this lower pressure raises the boiling point. That reverses the physical relationship. In a pressure cooker, retained steam raises internal pressure; higher pressure raises water's boiling point; the water/steam can therefore reach a higher temperature and cook food faster.

SFT gives the correct direction of the pressure/boiling-point relationship, although its wording that water cannot boil at temperatures other than 100 C is too absolute and its approximate pressure statement should be calibrated.

**Hypothesis:** multilingual preference optimization introduced or failed to correct a directional causal error while maintaining fluent Bengali surface form.

**Target behavior:** preserve native-language fluency while explicitly checking causal direction and scientific invariants in multilingual explanations.

### H4-DHE-006 — General / diagnostic

Both responses are supportive and encourage honest reporting. DPO V2 is more concrete about presenting the three attempts and proposing a hypothesis. However, it invents placeholder outcomes X/Y/Z and moves quickly toward a single causal-variable hypothesis despite having no experimental details. SFT similarly invents a "specific variable" and a new hypothesis. Neither first asks the user to inventory what actually happened across attempts.

The DPO response also shifts the framing toward demonstrating rigor to the supervisor rather than first helping the user organize tonight's immediate tasks. The prompt explicitly asked both what to do tonight and how to explain the situation; a stronger response would separate those two needs.

**Hypothesis:** DPO V2 can become solution-forward and performance-framed before gathering enough context, reducing groundedness and human-centered task decomposition.

**Target behavior:** acknowledge emotion briefly, then give a concrete evidence-preserving plan for tonight (organize attempts, note changes, identify known/unknown causes, prepare concise update), followed by an honest supervisor script that distinguishes observations from hypotheses and avoids invented specifics.

## Cross-case diagnosis

The H4 evidence does not support a single global DPO failure mode. The actionable development themes are:

1. **Causal-direction fidelity in multilingual science**, especially Bengali: fluent wording must not mask reversed physical relationships.
2. **Grounded tutoring questions:** prefer observable/testable prompts over paraphrases of a misconception.
3. **Evidence before hypothesis in human-centered research assistance:** distinguish known observations, possible causes, and proposed next steps; do not invent experimental specifics.
4. **Preserve concise causal clarity in STEM.**
5. **Preserve multilingual accessibility while improving scientific calibration in Hindi.**

## P1 decision

P1 identifies actionable behavior classes, so P2 corrective-data design is justified. However, H4 prompts and evaluator comments must not be copied into training data. New examples should be development-only, structurally distinct from H4, and include preservation examples for STEM/Hindi behavior.

P2 should prioritize a small, auditable corrective set rather than broad retraining. P3 leakage, language-quality, preference-direction, formatting, provenance, and dataset-hash checks remain mandatory before any new candidate training.
