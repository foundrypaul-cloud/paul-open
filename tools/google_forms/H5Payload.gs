// PAUL Open H5 DHE V3 reviewer-safe Google Forms payload.
// Generated only from GitHub Actions reviewer-safe artifact 10297811566.
// Batch: HEB1-64CDCC9521D3
//
// IMPORTANT:
// - This file contains blinded reviewer material only; it contains no source/model mapping.
// - `environment: "sandbox"` is required by the existing H2/H3/H4 Forms runtime validator.
//   The research partition is explicitly `development`; H5 remains DHE, not SHAE.
// - Initial allocation is exactly 3 judgments/case with alternating 2/1 complementary
//   variant targets, giving 9 submissions per display variant across six cases.
// - Do not unblind before the blinded analysis lock and durability audit pass.
//
// Use with the existing tools/google_forms/Code.gs runtime in the already-authorized
// standalone Apps Script project. Run createPaulHumanEvalH5Forms() once.

const PAUL_HUMAN_EVAL_SPEC = {
  "packets": [
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-STEM-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "stem_capable",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Stem A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-27EBEB2CECB1",
          "display_title": "Comparison 1 of 1",
          "prompt": "A person is spinning on a low-friction stool while holding small weights with their arms outstretched. When they pull the weights close to their body, they spin faster. Explain why in terms of moment of inertia and angular momentum, and avoid saying that extra rotational energy appeared from nowhere.",
          "response_a": "Here is the explanation:\n\nWhen the person is spinning with their arms outstretched, the small weights act as weights placed far from the axis of rotation. These weights contribute significantly to the total rotational inertia (moment of inertia) of the system. A larger moment of inertia means the body has more resistance to changes in its rotational state, so they must exert more torque to achieve a certain angular acceleration.\n\nWhen they pull the weights closer to their body, the moment of inertia decreases because the weights are now closer to the axis of rotation. Since the rotational inertia is smaller, the same amount of torque applied by the person's muscles results in a much greater angular acceleration, causing them to spin faster.\n\nIn this case, the angular momentum (L = Iω) is conserved. When the person reduces the moment of inertia (I), their angular velocity (ω) must increase proportionally to keep the angular momentum constant.",
          "response_b": "Here's a breakdown of why the person speeds up:\n\n1. **Moment of Inertia (I):** This is a measure of how hard it is to change an object's rotation. For a spinning person, the further their mass (the weights) is from their center of rotation, the larger their moment of inertia. Think of a spinning dancer with their arms wide apart versus tucked in—the dancer with the arms out has a much larger moment of inertia.\n\n2. **Angular Momentum (L):** This is a rotational equivalent of linear momentum (mass times velocity). It's calculated as L = I × ω (where ω is angular velocity, or rotational speed).\n\n3. **Conservation of Angular Momentum:** In the absence of any external rotational forces (like a wind pushing them), angular momentum must remain constant. L_initial = L_final.\n\n**The Action:**\nWhen the person pulls the weights in, their moment of inertia (I) decreases significantly. To keep the equation L = I × ω balanced, if I goes down, ω (their spin speed) must go up.\n\n**Conclusion:**\nThe person is not gaining energy. They are simply rearranging their mass. By making their moment of inertia smaller (by",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "science_reasoning"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the scientific accuracy of this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-STEM-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "stem_capable",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Stem B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-4748278B155D",
          "display_title": "Comparison 1 of 1",
          "prompt": "A person is spinning on a low-friction stool while holding small weights with their arms outstretched. When they pull the weights close to their body, they spin faster. Explain why in terms of moment of inertia and angular momentum, and avoid saying that extra rotational energy appeared from nowhere.",
          "response_a": "Here's a breakdown of why the person speeds up:\n\n1. **Moment of Inertia (I):** This is a measure of how hard it is to change an object's rotation. For a spinning person, the further their mass (the weights) is from their center of rotation, the larger their moment of inertia. Think of a spinning dancer with their arms wide apart versus tucked in—the dancer with the arms out has a much larger moment of inertia.\n\n2. **Angular Momentum (L):** This is a rotational equivalent of linear momentum (mass times velocity). It's calculated as L = I × ω (where ω is angular velocity, or rotational speed).\n\n3. **Conservation of Angular Momentum:** In the absence of any external rotational forces (like a wind pushing them), angular momentum must remain constant. L_initial = L_final.\n\n**The Action:**\nWhen the person pulls the weights in, their moment of inertia (I) decreases significantly. To keep the equation L = I × ω balanced, if I goes down, ω (their spin speed) must go up.\n\n**Conclusion:**\nThe person is not gaining energy. They are simply rearranging their mass. By making their moment of inertia smaller (by",
          "response_b": "Here is the explanation:\n\nWhen the person is spinning with their arms outstretched, the small weights act as weights placed far from the axis of rotation. These weights contribute significantly to the total rotational inertia (moment of inertia) of the system. A larger moment of inertia means the body has more resistance to changes in its rotational state, so they must exert more torque to achieve a certain angular acceleration.\n\nWhen they pull the weights closer to their body, the moment of inertia decreases because the weights are now closer to the axis of rotation. Since the rotational inertia is smaller, the same amount of torque applied by the person's muscles results in a much greater angular acceleration, causing them to spin faster.\n\nIn this case, the angular momentum (L = Iω) is conserved. When the person reduces the moment of inertia (I), their angular velocity (ω) must increase proportionally to keep the angular momentum constant.",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "science_reasoning"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the scientific accuracy of this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-EDUCATOR-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "educator",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Educator A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-9B50C7E743E3",
          "display_title": "Comparison 1 of 1",
          "prompt": "A student says: 'The phases of the Moon happen because Earth's shadow covers different parts of the Moon each month.' Respond as a Socratic tutor. Start with one focused observation or comparison that could help the student test that idea before you explain the correct mechanism.",
          "response_a": "That's a very logical guess! It makes sense to think that if we see the Moon changing shape, it must be because something is blocking the light.\n\nBut if the Moon is orbiting us, and Earth is blocking the sunlight during a lunar eclipse, what happens during a *solar* eclipse? In a solar eclipse, the Moon passes directly between the Sun and Earth, casting its own tiny shadow on us.\n\nIf the Moon is blocking the sun's light during a solar eclipse, does that mean the Earth's shadow is the only thing causing the phases we see every month?",
          "response_b": "That's a very logical guess! It makes sense to think that if we see the Moon changing shape, it must be because something is blocking the light.\n\nBut if the Moon is orbiting us, and Earth is blocking the sunlight during a lunar eclipse, what happens during a *solar* eclipse? If Earth's shadow is covering the Moon, is it possible that the Sun's shadow is covering the Earth?",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "socratic_tutoring"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Optional: How familiar are you with teaching or tutoring?",
        "choices": [
          "Teacher / educator",
          "Tutor / mentor",
          "Student / learner",
          "Other / prefer not to say"
        ],
        "required": false
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-EDUCATOR-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "educator",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Educator B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-C872A4CD1508",
          "display_title": "Comparison 1 of 1",
          "prompt": "A student says: 'The phases of the Moon happen because Earth's shadow covers different parts of the Moon each month.' Respond as a Socratic tutor. Start with one focused observation or comparison that could help the student test that idea before you explain the correct mechanism.",
          "response_a": "That's a very logical guess! It makes sense to think that if we see the Moon changing shape, it must be because something is blocking the light.\n\nBut if the Moon is orbiting us, and Earth is blocking the sunlight during a lunar eclipse, what happens during a *solar* eclipse? If Earth's shadow is covering the Moon, is it possible that the Sun's shadow is covering the Earth?",
          "response_b": "That's a very logical guess! It makes sense to think that if we see the Moon changing shape, it must be because something is blocking the light.\n\nBut if the Moon is orbiting us, and Earth is blocking the sunlight during a lunar eclipse, what happens during a *solar* eclipse? In a solar eclipse, the Moon passes directly between the Sun and Earth, casting its own tiny shadow on us.\n\nIf the Moon is blocking the sun's light during a solar eclipse, does that mean the Earth's shadow is the only thing causing the phases we see every month?",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "socratic_tutoring"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Optional: How familiar are you with teaching or tutoring?",
        "choices": [
          "Teacher / educator",
          "Tutor / mentor",
          "Student / learner",
          "Other / prefer not to say"
        ],
        "required": false
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-RESEARCH-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "domain_expert",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Research A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-14AACB9FCC99",
          "display_title": "Comparison 1 of 1",
          "prompt": "A small randomized pilot study shows an apparent benefit in one subgroup but not in the others. I have the raw outcomes, subgroup labels, and randomization records. Give me a careful plan for checking whether the subgroup pattern is credible before I claim a subgroup-specific effect.",
          "response_a": "Given the raw outcomes, subgroup labels, and randomization records, here is a plan to assess the credibility of the observed subgroup effect:\n\n### 1. Check for Pre-Specified Analysis\nBefore any analysis, verify that the subgroups were defined *before* seeing the outcome data. If the subgroups were created based on patterns in the outcome data (data-driven), the observed effect is likely due to chance.\n\n### 2. Test for Random Assignment\nUse the randomization records to see if the assignment to subgroups was balanced across baseline covariates. If there are significant imbalances (e.g., one subgroup has much more men than the other), the subgroup effect might be a result of confounding, not a true biological interaction.\n\n### 3. Re-run the Analysis\nIf the subgroup was pre-specified, run the primary analysis again *without* using the subgroup variable. If the apparent effect disappears or significantly diminishes when the subgroups are ignored, the subgroup effect is likely a spurious finding.\n\n### 4. Sensitivity Analysis\nPerform a sensitivity analysis by intentionally misclassifying the subgroup labels (e.g., flipping labels for 10% of subjects). If the effect remains robust despite this manipulation, it strengthens the credibility of the finding.\n\n### 5",
          "response_b": "Given the raw outcomes, subgroup labels, and randomization records, here is a plan to assess the credibility of the observed subgroup effect:\n\n### 1. Check for Pre-Randomization Balance (Baseline)\nBefore looking at the outcomes, you must ensure the subgroups were balanced at the start.\n*   **Compare Baseline Covariates:** Compare the mean (or median) of key baseline variables (e.g., age, disease severity, demographics) between the subgroups *before* any treatment was given.\n*   **Check Randomization Integrity:** Use the randomization records to verify that the assignment mechanism was followed correctly. If the groups were already different before randomization, any observed outcome difference might just be due to baseline differences, not the treatment.\n\n### 2. Conduct a Subgroup Analysis (Primary Test)\nOnce you are confident the baseline was balanced, you can perform the analysis you intended.\n*   **Stratified Analysis:** Run the primary statistical test (e.g., t-test, regression) separately for each subgroup.\n*   **Interaction Test:** The most rigorous approach is to include an interaction term in a statistical model (e.g., Outcome ~ Treatment + Subgroup + Treatment*Subgroup). A significant interaction term suggests the",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_research_assistance"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the research-methodology and statistical reasoning in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-RESEARCH-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "domain_expert",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — Research B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-DBCDCD2E38FA",
          "display_title": "Comparison 1 of 1",
          "prompt": "A small randomized pilot study shows an apparent benefit in one subgroup but not in the others. I have the raw outcomes, subgroup labels, and randomization records. Give me a careful plan for checking whether the subgroup pattern is credible before I claim a subgroup-specific effect.",
          "response_a": "Given the raw outcomes, subgroup labels, and randomization records, here is a plan to assess the credibility of the observed subgroup effect:\n\n### 1. Check for Pre-Randomization Balance (Baseline)\nBefore looking at the outcomes, you must ensure the subgroups were balanced at the start.\n*   **Compare Baseline Covariates:** Compare the mean (or median) of key baseline variables (e.g., age, disease severity, demographics) between the subgroups *before* any treatment was given.\n*   **Check Randomization Integrity:** Use the randomization records to verify that the assignment mechanism was followed correctly. If the groups were already different before randomization, any observed outcome difference might just be due to baseline differences, not the treatment.\n\n### 2. Conduct a Subgroup Analysis (Primary Test)\nOnce you are confident the baseline was balanced, you can perform the analysis you intended.\n*   **Stratified Analysis:** Run the primary statistical test (e.g., t-test, regression) separately for each subgroup.\n*   **Interaction Test:** The most rigorous approach is to include an interaction term in a statistical model (e.g., Outcome ~ Treatment + Subgroup + Treatment*Subgroup). A significant interaction term suggests the",
          "response_b": "Given the raw outcomes, subgroup labels, and randomization records, here is a plan to assess the credibility of the observed subgroup effect:\n\n### 1. Check for Pre-Specified Analysis\nBefore any analysis, verify that the subgroups were defined *before* seeing the outcome data. If the subgroups were created based on patterns in the outcome data (data-driven), the observed effect is likely due to chance.\n\n### 2. Test for Random Assignment\nUse the randomization records to see if the assignment to subgroups was balanced across baseline covariates. If there are significant imbalances (e.g., one subgroup has much more men than the other), the subgroup effect might be a result of confounding, not a true biological interaction.\n\n### 3. Re-run the Analysis\nIf the subgroup was pre-specified, run the primary analysis again *without* using the subgroup variable. If the apparent effect disappears or significantly diminishes when the subgroups are ignored, the subgroup effect is likely a spurious finding.\n\n### 4. Sensitivity Analysis\nPerform a sensitivity analysis by intentionally misclassifying the subgroup labels (e.g., flipping labels for 10% of subjects). If the effect remains robust despite this manipulation, it strengthens the credibility of the finding.\n\n### 5",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_research_assistance"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the research-methodology and statistical reasoning in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-HI-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "bilingual",
      "language": "hi",
      "title": "PAUL Open — Human Evaluation — Hindi A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so. Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation when that is clearer or more accurate.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-B82FF1A88196",
          "display_title": "Comparison 1 of 1",
          "prompt": "गाड़ी के टायर का दबाव ठंडे और गर्म मौसम में अलग क्यों दिख सकता है? सरल हिंदी में तापमान और गैस के दबाव का संबंध समझाइए, और यह भी बताइए कि निर्माता द्वारा दिया गया टायर-प्रेशर मान उपयोगी मार्गदर्शक है लेकिन हर तापमान पर जादुई रूप से बिल्कुल वही संख्या क्यों नहीं रहेगा।",
          "response_a": "यह एक बहुत ही अच्छा और तार्किक सवाल है! हम सभी देखते हैं कि सर्दियों में टायर का दबाव थोड़ा कम लगता है, और गर्मियों में थोड़ा ज्यादा। ऐसा क्यों होता है?\n\nइसे समझने के लिए हमें गैस के व्यवहार को याद करना होगा। क्या आपने कभी गैस का डिब्बा या हवाई गुब्बारे में हवा भरने का अनुभव किया है?\n\nजब हम किसी गैस (जैसे हवा) को एक सीमित जगह (जैसे टायर के अंदर) में रखते हैं और उसे गर्म करते हैं, तो क्या होता है?\n\n1.  **गर्म करना:** जब हम हवा को गर्म करते हैं, तो हवा के अंदर मौजूद सभी गैस के कण बहुत तेजी से हिलने लगते हैं। वे और ज्यादा तेजी से टकराने लगते हैं।\n2.  **टक्कर का बल:** ये कण जिस टायर की दीवार से टकराते हैं, वे जितना जोर से टकराते हैं, उतना ही ज्यादा दबाव (pressure) महसूस होता है।\n3.  **ठंडा करना:** जब हवा ठंडी होती है, तो ये कण शांत हो जाते हैं और धीरे-धीरे चलते हैं। वे उतने जोर से नहीं टकराते, इसलिए दबाव कम लगता है।\n\nयही कारण है कि तापमान और गैस का दबाव सीधे तौर पर जुड़े होते हैं।\n\n### निर्माता का दबाव क्यों",
          "response_b": "यह एक बहुत ही अच्छा और तार्किक सवाल है! हम सभी देखते हैं कि सर्दियों में टायर का दबाव थोड़ा कम लगता है, और गर्मियों में थोड़ा ज्यादा। ऐसा क्यों होता है?\n\nइसे समझने के लिए हमें गैस के व्यवहार को याद करना होगा। क्या किसी ने कभी साइकिल के टायर में हवा भरी हुई एक गैस को गर्म करने की कोशिश की है?\n\nमान लीजिए आपके पास एक बंद गुब्बारे में हवा भरी हुई है। अगर आप उस गुब्बारे को किसी गर्म पानी के बर्तन में डुबो देते हैं, तो क्या गुब्बारे की हवा गर्म पानी की भाप जितनी तेज़ी से हिलेगी, या धीमी गति से?\n\nतापमान बढ़ने पर गैस के कणों की गति पर क्या असर पड़ता है?",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_explanation"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the Hindi language and scientific explanation in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-HI-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "bilingual",
      "language": "hi",
      "title": "PAUL Open — Human Evaluation — Hindi B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so. Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation when that is clearer or more accurate.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-27BDFFEE98E1",
          "display_title": "Comparison 1 of 1",
          "prompt": "गाड़ी के टायर का दबाव ठंडे और गर्म मौसम में अलग क्यों दिख सकता है? सरल हिंदी में तापमान और गैस के दबाव का संबंध समझाइए, और यह भी बताइए कि निर्माता द्वारा दिया गया टायर-प्रेशर मान उपयोगी मार्गदर्शक है लेकिन हर तापमान पर जादुई रूप से बिल्कुल वही संख्या क्यों नहीं रहेगा।",
          "response_a": "यह एक बहुत ही अच्छा और तार्किक सवाल है! हम सभी देखते हैं कि सर्दियों में टायर का दबाव थोड़ा कम लगता है, और गर्मियों में थोड़ा ज्यादा। ऐसा क्यों होता है?\n\nइसे समझने के लिए हमें गैस के व्यवहार को याद करना होगा। क्या किसी ने कभी साइकिल के टायर में हवा भरी हुई एक गैस को गर्म करने की कोशिश की है?\n\nमान लीजिए आपके पास एक बंद गुब्बारे में हवा भरी हुई है। अगर आप उस गुब्बारे को किसी गर्म पानी के बर्तन में डुबो देते हैं, तो क्या गुब्बारे की हवा गर्म पानी की भाप जितनी तेज़ी से हिलेगी, या धीमी गति से?\n\nतापमान बढ़ने पर गैस के कणों की गति पर क्या असर पड़ता है?",
          "response_b": "यह एक बहुत ही अच्छा और तार्किक सवाल है! हम सभी देखते हैं कि सर्दियों में टायर का दबाव थोड़ा कम लगता है, और गर्मियों में थोड़ा ज्यादा। ऐसा क्यों होता है?\n\nइसे समझने के लिए हमें गैस के व्यवहार को याद करना होगा। क्या आपने कभी गैस का डिब्बा या हवाई गुब्बारे में हवा भरने का अनुभव किया है?\n\nजब हम किसी गैस (जैसे हवा) को एक सीमित जगह (जैसे टायर के अंदर) में रखते हैं और उसे गर्म करते हैं, तो क्या होता है?\n\n1.  **गर्म करना:** जब हम हवा को गर्म करते हैं, तो हवा के अंदर मौजूद सभी गैस के कण बहुत तेजी से हिलने लगते हैं। वे और ज्यादा तेजी से टकराने लगते हैं।\n2.  **टक्कर का बल:** ये कण जिस टायर की दीवार से टकराते हैं, वे जितना जोर से टकराते हैं, उतना ही ज्यादा दबाव (pressure) महसूस होता है।\n3.  **ठंडा करना:** जब हवा ठंडी होती है, तो ये कण शांत हो जाते हैं और धीरे-धीरे चलते हैं। वे उतने जोर से नहीं टकराते, इसलिए दबाव कम लगता है।\n\nयही कारण है कि तापमान और गैस का दबाव सीधे तौर पर जुड़े होते हैं।\n\n### निर्माता का दबाव क्यों",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_explanation"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the Hindi language and scientific explanation in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-BN-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "bilingual",
      "language": "bn",
      "title": "PAUL Open — Human Evaluation — Bengali A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so. Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation when that is clearer or more accurate.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-998FE19D4692",
          "display_title": "Comparison 1 of 1",
          "prompt": "Answer in Bengali. Explain why white light passing through a glass prism spreads into a band of colors. Connect wavelength-dependent refractive index to the different bending angles, using language suitable for a higher-secondary student.",
          "response_a": "সাদা আলো যখন কাঁচের প্রিজমের মধ্য দিয়ে যায়, তখন সেটি বিভিন্ন রঙের আলোর মিশ্রণ। কিন্তু প্রিজমের ভেতরের কাঁচের মাধ্যমে যাওয়ার সময় এটি রঙের আলাদা আলাদা রশ্মিতে বিভক্ত হয়ে যায়। এই ঘটনাটিকে বলা হয় আলোর বিচ্ছুরণ (Dispersion)।\n\nএর মূল কারণ হলো কাঁচের মধ্যে আলোর প্রতিসরাঙ্ক (Refractive Index) আলোর তরঙ্গদৈর্ঘ্যের (Wavelength) ওপর নির্ভর করে। আমরা জানি, আলোর রং এবং তার তরঙ্গদৈর্ঘ্যের মধ্যে সম্পর্ক আছে। যেমন, বেগুনি রং বা নীল রঙের আলোর তরঙ্গদৈর্ঘ্য কম হয়, আর লাল রঙের আলোর তরঙ্গদৈর্ঘ্য বেশি হয়।\n\nকাঁচের ভেতরের কাঁচের প্রতিসরাঙ্ক আসলে একটি ফ্রিকোয়েন্সি বা তরঙ্গদৈর্ঘ্যের ওপর নির্ভর করে। সহজভাবে বলতে গেলে, কাঁচের মধ্যে যাওয়ার সময় কম তরঙ্গদৈর্ঘ্যের আলো (যেমন বেগুনি) বেশি বেঁকে যায়, আর বেশি তরঙ্গদৈর্ঘ্যের আলো (যেমন লাল) তুলনামূলকভাবে কম বেঁকে যায়।\n\nএই ভিন্ন ভিন্ন বেঁকে যাওয়ার (বা প্রতিসরণের) কারণেই সাদা আলো যখন প্রিজমের মধ্যে দিয়ে যায়, তখন এটি রঙের আলাদা আলাদা ব্যান্ডে বিভক্ত হয়ে যায়। প্রতিসরণের কারণে এই রঙগুলো আমাদের চোখে আলাদা",
          "response_b": "সাদা আলো যখন কাঁচের প্রিজমের মধ্য দিয়ে যায়, তখন সেটি বিভিন্ন রঙের আলোর মিশ্রণ। কিন্তু যখন এটি কাঁচের মধ্য দিয়ে যায়, তখন এটি বেঁকে যায় এবং আমরা বর্ণালী দেখতে পাই। কেন এমন হয়?\n\nআমরা জানি, আলোর গতি প্রতিমাধ্যমে ভিন্ন হয়। যখন আলো বায়ুমণ্ডল থেকে কাঁচের মতো ঘন মাধ্যমে প্রবেশ করে, তখন এটি ধীর হয়ে যায় এবং বেঁকে যায়। এই ঘটনাকেই প্রতিসরণ বলে।\n\nএখানেই আসল রহস্য লুকিয়ে আছে। আলোর বিভিন্ন রঙের তরঙ্গদৈর্ঘ্য (wavelength) ভিন্ন হয়। সূর্যের আলোতে থাকা লাল এবং বেগুনী রঙের আলোর তরঙ্গদৈর্ঘ্য আলাদা।\n\nকাঁচের মধ্যে দিয়ে যাওয়ার সময়, প্রতিসরণের ডিগ্রি আলোর তরঙ্গের ওপর নির্ভর করে। একে বলা হয় **তরঙ্গদৈর্ঘ্য-নির্ভর প্রতিসরাঙ্ক (wavelength-dependent refractive index)**।\n\nসংক্ষেপে বললে, কাঁচের প্রতিসরাঙ্ক (n) আলোর রঙের ওপর নির্ভর করে। লাল আলোর (যা কম তরঙ্গদৈর্ঘ্যের) জন্য কাঁচের প্রতিসরাঙ্ক বেগুনী আলোর (যা বেশি তরঙ্গদৈর্ঘ্যের) থেকে সামান্য আলাদা হয়।\n\nযেহেতু বিভিন্ন রঙের আলোর প্রতিসরাঙ্ক ভিন্ন, তাই প্রিজমের মধ্য দিয়ে যাওয়ার সময় তাদের বেঁকে যাওয়ার কো",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_explanation"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the Bengali language and scientific explanation in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-BN-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "bilingual",
      "language": "bn",
      "title": "PAUL Open — Human Evaluation — Bengali B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so. Standard scientific terms, formulas, units and abbreviations may stay in familiar English or standard notation when that is clearer or more accurate.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-265C7AA3A592",
          "display_title": "Comparison 1 of 1",
          "prompt": "Answer in Bengali. Explain why white light passing through a glass prism spreads into a band of colors. Connect wavelength-dependent refractive index to the different bending angles, using language suitable for a higher-secondary student.",
          "response_a": "সাদা আলো যখন কাঁচের প্রিজমের মধ্য দিয়ে যায়, তখন সেটি বিভিন্ন রঙের আলোর মিশ্রণ। কিন্তু যখন এটি কাঁচের মধ্য দিয়ে যায়, তখন এটি বেঁকে যায় এবং আমরা বর্ণালী দেখতে পাই। কেন এমন হয়?\n\nআমরা জানি, আলোর গতি প্রতিমাধ্যমে ভিন্ন হয়। যখন আলো বায়ুমণ্ডল থেকে কাঁচের মতো ঘন মাধ্যমে প্রবেশ করে, তখন এটি ধীর হয়ে যায় এবং বেঁকে যায়। এই ঘটনাকেই প্রতিসরণ বলে।\n\nএখানেই আসল রহস্য লুকিয়ে আছে। আলোর বিভিন্ন রঙের তরঙ্গদৈর্ঘ্য (wavelength) ভিন্ন হয়। সূর্যের আলোতে থাকা লাল এবং বেগুনী রঙের আলোর তরঙ্গদৈর্ঘ্য আলাদা।\n\nকাঁচের মধ্যে দিয়ে যাওয়ার সময়, প্রতিসরণের ডিগ্রি আলোর তরঙ্গের ওপর নির্ভর করে। একে বলা হয় **তরঙ্গদৈর্ঘ্য-নির্ভর প্রতিসরাঙ্ক (wavelength-dependent refractive index)**।\n\nসংক্ষেপে বললে, কাঁচের প্রতিসরাঙ্ক (n) আলোর রঙের ওপর নির্ভর করে। লাল আলোর (যা কম তরঙ্গদৈর্ঘ্যের) জন্য কাঁচের প্রতিসরাঙ্ক বেগুনী আলোর (যা বেশি তরঙ্গদৈর্ঘ্যের) থেকে সামান্য আলাদা হয়।\n\nযেহেতু বিভিন্ন রঙের আলোর প্রতিসরাঙ্ক ভিন্ন, তাই প্রিজমের মধ্য দিয়ে যাওয়ার সময় তাদের বেঁকে যাওয়ার কো",
          "response_b": "সাদা আলো যখন কাঁচের প্রিজমের মধ্য দিয়ে যায়, তখন সেটি বিভিন্ন রঙের আলোর মিশ্রণ। কিন্তু প্রিজমের ভেতরের কাঁচের মাধ্যমে যাওয়ার সময় এটি রঙের আলাদা আলাদা রশ্মিতে বিভক্ত হয়ে যায়। এই ঘটনাটিকে বলা হয় আলোর বিচ্ছুরণ (Dispersion)।\n\nএর মূল কারণ হলো কাঁচের মধ্যে আলোর প্রতিসরাঙ্ক (Refractive Index) আলোর তরঙ্গদৈর্ঘ্যের (Wavelength) ওপর নির্ভর করে। আমরা জানি, আলোর রং এবং তার তরঙ্গদৈর্ঘ্যের মধ্যে সম্পর্ক আছে। যেমন, বেগুনি রং বা নীল রঙের আলোর তরঙ্গদৈর্ঘ্য কম হয়, আর লাল রঙের আলোর তরঙ্গদৈর্ঘ্য বেশি হয়।\n\nকাঁচের ভেতরের কাঁচের প্রতিসরাঙ্ক আসলে একটি ফ্রিকোয়েন্সি বা তরঙ্গদৈর্ঘ্যের ওপর নির্ভর করে। সহজভাবে বলতে গেলে, কাঁচের মধ্যে যাওয়ার সময় কম তরঙ্গদৈর্ঘ্যের আলো (যেমন বেগুনি) বেশি বেঁকে যায়, আর বেশি তরঙ্গদৈর্ঘ্যের আলো (যেমন লাল) তুলনামূলকভাবে কম বেঁকে যায়।\n\nএই ভিন্ন ভিন্ন বেঁকে যাওয়ার (বা প্রতিসরণের) কারণেই সাদা আলো যখন প্রিজমের মধ্যে দিয়ে যায়, তখন এটি রঙের আলাদা আলাদা ব্যান্ডে বিভক্ত হয়ে যায়। প্রতিসরণের কারণে এই রঙগুলো আমাদের চোখে আলাদা",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "scientific_explanation"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Can you confidently judge the Bengali language and scientific explanation in this response pair?",
        "choices": [
          "Yes — confidently",
          "Mostly — with minor uncertainty",
          "No — I can’t confidently judge this"
        ],
        "required": true
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-GENERAL-A-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V01",
      "partition": "development",
      "reviewer_cohort": "general_user",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — General A",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-17CCA9FF1679",
          "display_title": "Comparison 1 of 1",
          "prompt": "I have to give my team an update tomorrow, but tonight I discovered that a spreadsheet formula error may have affected some of the numbers I was planning to present. I'm anxious and embarrassed. Help me decide what to do tonight and how to explain the uncertainty honestly without pretending the conclusions are still valid.",
          "response_a": "It's completely understandable to feel anxious when you discover a potential error right before a big presentation. This is a common situation in any data-heavy role.\n\nBefore you make a decision, let's consider the following:\n\n1. **Can you verify the potential error?** Take a few minutes to re-run the formula or manually check a few rows to see if the error is widespread or isolated.\n2. **What is the deadline for the data?** Is the data meant to be finalized today, or is there a natural review period tomorrow?\n3. **What is the level of the error?** Is it a minor rounding issue, or does it fundamentally change the conclusion (e.g., a projected profit turning into a loss)?\n\nOnce you have a clearer picture of the scope of the error, we can discuss how to communicate the situation to your team in a professional and transparent way.",
          "response_b": "It's completely understandable to feel anxious when you discover a potential error right before a big presentation. This is a common situation in any data-heavy role.\n\nBefore you make a decision, let's consider the following:\n\n1. **Can you verify the error?** If you can quickly test the formula with a few different inputs or check a small section of the data manually, you might be able to confirm if the error is widespread or localized.\n2. **What is the deadline for the update?** If the presentation is tomorrow morning, you might have a limited time to find the root cause.\n3. **What is the organizational culture around errors?** In some teams, data integrity is sacrosanct, while in others, the process of discovery is valued as much as the final number.\n\nIf the error is confirmed, how might you structure an update that shows you caught it? Would it be more helpful to present a \"Draft 1\" with a clear caveat that the numbers are subject to review, or to present the current numbers with a caveat that the methodology is under active review?",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "empathy_human_centered"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Optional: Which best describes you?",
        "choices": [
          "Student",
          "Teacher / educator",
          "Researcher / scientist / engineer",
          "Other working professional",
          "General user",
          "Prefer not to say"
        ],
        "required": false
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 1
    },
    {
      "form_packet_version": "1.1",
      "protocol_version": "1.0",
      "environment": "sandbox",
      "packet_id": "HEF1-H5-GENERAL-B-20260912",
      "batch_id": "HEB1-64CDCC9521D3",
      "variant_id": "V02",
      "partition": "development",
      "reviewer_cohort": "general_user",
      "language": "en",
      "title": "PAUL Open — Human Evaluation — General B",
      "description": "Help us compare two AI responses. Read Response A and Response B and choose the one you would rather receive. Consider accuracy, clarity, usefulness and naturalness. If they are equally good, both poor, or you are unsure, you can say so.",
      "settings": {
        "collect_email": false,
        "allow_response_edits": false,
        "limit_one_response_per_user": false,
        "progress_bar": true,
        "publish_response_summary": false,
        "show_submit_another_response_link": false,
        "shuffle_questions": false,
        "accepting_responses": true
      },
      "comparisons": [
        {
          "ordinal": 1,
          "comparison_id": "HEV1-DFE85FA27109",
          "display_title": "Comparison 1 of 1",
          "prompt": "I have to give my team an update tomorrow, but tonight I discovered that a spreadsheet formula error may have affected some of the numbers I was planning to present. I'm anxious and embarrassed. Help me decide what to do tonight and how to explain the uncertainty honestly without pretending the conclusions are still valid.",
          "response_a": "It's completely understandable to feel anxious when you discover a potential error right before a big presentation. This is a common situation in any data-heavy role.\n\nBefore you make a decision, let's consider the following:\n\n1. **Can you verify the error?** If you can quickly test the formula with a few different inputs or check a small section of the data manually, you might be able to confirm if the error is widespread or localized.\n2. **What is the deadline for the update?** If the presentation is tomorrow morning, you might have a limited time to find the root cause.\n3. **What is the organizational culture around errors?** In some teams, data integrity is sacrosanct, while in others, the process of discovery is valued as much as the final number.\n\nIf the error is confirmed, how might you structure an update that shows you caught it? Would it be more helpful to present a \"Draft 1\" with a clear caveat that the numbers are subject to review, or to present the current numbers with a caveat that the methodology is under active review?",
          "response_b": "It's completely understandable to feel anxious when you discover a potential error right before a big presentation. This is a common situation in any data-heavy role.\n\nBefore you make a decision, let's consider the following:\n\n1. **Can you verify the potential error?** Take a few minutes to re-run the formula or manually check a few rows to see if the error is widespread or isolated.\n2. **What is the deadline for the data?** Is the data meant to be finalized today, or is there a natural review period tomorrow?\n3. **What is the level of the error?** Is it a minor rounding issue, or does it fundamentally change the conclusion (e.g., a projected profit turning into a loss)?\n\nOnce you have a clearer picture of the scope of the error, we can discuss how to communicate the situation to your team in a professional and transparent way.",
          "question": "Which response would you rather receive?",
          "choices": [
            "Response A is better",
            "Response B is better",
            "They are about equally good",
            "Neither response is good",
            "I'm not sure / I can't judge this"
          ],
          "required": true,
          "domain": "empathy_human_centered"
        }
      ],
      "reviewer_context": {
        "enabled": true,
        "title": "Optional: Which best describes you?",
        "choices": [
          "Student",
          "Teacher / educator",
          "Researcher / scientist / engineer",
          "Other working professional",
          "General user",
          "Prefer not to say"
        ],
        "required": false
      },
      "optional_comment": {
        "enabled": true,
        "title": "Anything important you noticed? (optional)",
        "required": false
      },
      "confirmation_message": "Thank you — your PAUL Open evaluation response has been recorded.",
      "sandbox_auto_close_after_submissions": 2
    }
  ]
};


// H5-specific resilient launcher.
// Use this instead of createPaulHumanEvalSandboxForms() for H5 collection.
// It preserves the existing runtime/data model but retries the Google Forms
// response-destination link, which can fail transiently immediately after a
// new Spreadsheet is created.
function createPaulHumanEvalH5Forms() {
  if (typeof PAUL_HUMAN_EVAL_SPEC === 'undefined') {
    throw new Error('PAUL_HUMAN_EVAL_SPEC is missing. Add H5Payload.gs.');
  }
  const packets = PAUL_HUMAN_EVAL_SPEC.packets;
  if (!Array.isArray(packets) || packets.length === 0) {
    throw new Error('PAUL_HUMAN_EVAL_SPEC.packets must be a non-empty array.');
  }

  const created = [];
  for (const packet of packets) {
    created.push(createPaulHumanEvalH5Form_(packet));
  }
  ensureRecoveryTrigger_();
  console.log(JSON.stringify(created, null, 2));
  return created;
}

function createPaulHumanEvalH5Form_(packet) {
  validatePacket_(packet);

  const form = FormApp.create(packet.title, false);
  form
      .setDescription(packet.description)
      .setCollectEmail(false)
      .setAllowResponseEdits(false)
      .setLimitOneResponsePerUser(false)
      .setProgressBar(true)
      .setPublishingSummary(false)
      .setShowLinkToRespondAgain(false)
      .setShuffleQuestions(false)
      .setConfirmationMessage(packet.confirmation_message)
      .setAcceptingResponses(false);

  const spreadsheet = SpreadsheetApp.create(
      `PAUL Human Eval — ${packet.packet_id} — Responses`,
  );
  const metadataSheet = spreadsheet.getSheets()[0];
  metadataSheet.setName(PAUL_METADATA_SHEET);
  const normalizedSheet = spreadsheet.insertSheet(PAUL_NORMALIZED_SHEET);
  normalizedSheet.appendRow([
    'response_id',
    'submitted_at_utc',
    'packet_id',
    'batch_id',
    'variant_id',
    'reviewer_cohort',
    'language',
    'comparison_id',
    'choice',
    'reviewer_context',
    'optional_comment',
  ]);

  const backupSpreadsheet = SpreadsheetApp.create(
      `PAUL Human Eval — ${packet.packet_id} — Backup Ledger`,
  );
  const backupSheet = backupSpreadsheet.getSheets()[0];
  backupSheet.setName(PAUL_BACKUP_SHEET);
  backupSheet.appendRow([
    'response_id',
    'submitted_at_utc',
    'packet_id',
    'batch_id',
    'variant_id',
    'reviewer_cohort',
    'language',
    'reviewer_context',
    'snapshot_json',
    'sha256',
    'backup_written_at_utc',
  ]);

  const choiceItemToComparison = {};
  for (const comparison of packet.comparisons) {
    form.addSectionHeaderItem()
        .setTitle(comparison.display_title)
        .setHelpText(comparisonHelpText_(comparison));
    const choiceItem = form.addMultipleChoiceItem()
        .setTitle(comparison.question)
        .setChoiceValues(comparison.choices)
        .setRequired(true);
    choiceItemToComparison[String(choiceItem.getId())] = comparison.comparison_id;
  }

  let reviewerContextItemId = null;
  if (packet.reviewer_context && packet.reviewer_context.enabled) {
    const contextItem = form.addMultipleChoiceItem()
        .setTitle(packet.reviewer_context.title)
        .setChoiceValues(packet.reviewer_context.choices)
        .setRequired(packet.reviewer_context.required === true);
    reviewerContextItemId = String(contextItem.getId());
  }

  let optionalCommentItemId = null;
  if (packet.optional_comment && packet.optional_comment.enabled) {
    const commentItem = form.addParagraphTextItem()
        .setTitle(packet.optional_comment.title)
        .setRequired(false);
    optionalCommentItemId = String(commentItem.getId());
  }

  setH5ResponseDestinationWithRetry_(form, spreadsheet.getId(), packet.packet_id);

  const runtimeConfig = {
    environment: packet.environment,
    packet_id: packet.packet_id,
    batch_id: packet.batch_id,
    variant_id: packet.variant_id,
    reviewer_cohort: packet.reviewer_cohort,
    language: packet.language,
    spreadsheet_id: spreadsheet.getId(),
    backup_spreadsheet_id: backupSpreadsheet.getId(),
    choice_item_to_comparison: choiceItemToComparison,
    reviewer_context_item_id: reviewerContextItemId,
    optional_comment_item_id: optionalCommentItemId,
    sandbox_auto_close_after_submissions: packet.sandbox_auto_close_after_submissions,
  };
  PropertiesService.getScriptProperties().setProperty(
      PAUL_FORM_PROPERTY_PREFIX + form.getId(),
      JSON.stringify(runtimeConfig),
  );

  writeMetadataSheet_(
      metadataSheet,
      form,
      packet,
      choiceItemToComparison,
      backupSpreadsheet.getId(),
  );
  ScriptApp.newTrigger('onPaulHumanEvalSubmit').forForm(form).onFormSubmit().create();
  form.setPublished(true).setAcceptingResponses(true);

  return {
    packet_id: packet.packet_id,
    form_id: form.getId(),
    respondent_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    spreadsheet_id: spreadsheet.getId(),
    spreadsheet_url: spreadsheet.getUrl(),
    backup_spreadsheet_id: backupSpreadsheet.getId(),
    backup_spreadsheet_url: backupSpreadsheet.getUrl(),
  };
}

function setH5ResponseDestinationWithRetry_(form, spreadsheetId, packetId) {
  const maxAttempts = 5;
  let lastError = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      SpreadsheetApp.openById(spreadsheetId);
      SpreadsheetApp.flush();
      Utilities.sleep(1000 * attempt);
      form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheetId);
      return;
    } catch (error) {
      lastError = error;
      console.warn(
          `H5 ${packetId}: response destination attempt ${attempt}/${maxAttempts} failed: ${error}`,
      );
      if (attempt < maxAttempts) {
        Utilities.sleep(1500 * attempt);
      }
    }
  }
  throw new Error(
      `H5 ${packetId}: failed to set response destination after ${maxAttempts} attempts. ` +
      `Spreadsheet ID: ${spreadsheetId}. Last error: ${lastError}`,
  );
}
