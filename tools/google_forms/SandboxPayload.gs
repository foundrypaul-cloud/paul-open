// PAUL Open H2 disposable sandbox payload.
// Synthetic only: no PAUL benchmark, DHE, SHAE, SFT/DPO identity, or private A/B map.
// This file exists so the Google-account setup needs no local Python step.

const PAUL_HUMAN_EVAL_SPEC = {
  packets: [
    {
      form_packet_version: '1.1',
      protocol_version: '1.0',
      environment: 'sandbox',
      packet_id: 'HEF1-H2-SYNTHETIC-001',
      batch_id: 'HEB1-H2SANDBOX01',
      variant_id: 'V01',
      partition: 'development',
      reviewer_cohort: 'general_user',
      language: 'en',
      title: 'Help us compare AI responses',
      description:
          'Read each question and the two responses. Choose the response you would rather ' +
          'receive based on accuracy, clarity, usefulness and naturalness. If they are equally ' +
          'good, both poor, or you are unsure, you can say so.',
      settings: {
        collect_email: false,
        allow_response_edits: false,
        limit_one_response_per_user: false,
        progress_bar: true,
        publish_response_summary: false,
        show_submit_another_response_link: false,
        shuffle_questions: false,
        accepting_responses: true,
      },
      comparisons: [
        {
          ordinal: 1,
          comparison_id: 'HEV1-H2SYN000001',
          display_title: 'Comparison 1 of 3',
          prompt:
              'A learner asks why a metal spoon feels colder than a wooden spoon in the same ' +
              'room. Give a simple explanation.',
          response_a:
              'Metal moves heat away from your hand faster than wood, so your skin cools more ' +
              'quickly even though both spoons started at the same room temperature.',
          response_b:
              'The metal spoon is naturally much colder than the wooden spoon because metals ' +
              'contain less stored heat at room temperature.',
          question: 'Which response would you rather receive?',
          choices: [
            'Response A is better',
            'Response B is better',
            'They are about equally good',
            'Neither response is good',
            "I'm not sure / I can't judge this",
          ],
          required: true,
          domain: 'synthetic_science',
        },
        {
          ordinal: 2,
          comparison_id: 'HEV1-H2SYN000002',
          display_title: 'Comparison 2 of 3',
          prompt:
              'A student has twenty minutes before a quiz and feels overwhelmed. Suggest a ' +
              'practical way to use the time.',
          response_a:
              'Pick the two topics most likely to matter, spend eight minutes recalling each ' +
              'without notes, then use the last four minutes to check mistakes and breathe ' +
              'before the quiz.',
          response_b:
              'Try to review every chapter quickly so that nothing is missed, even if you can ' +
              'only spend a minute or two on each one.',
          question: 'Which response would you rather receive?',
          choices: [
            'Response A is better',
            'Response B is better',
            'They are about equally good',
            'Neither response is good',
            "I'm not sure / I can't judge this",
          ],
          required: true,
          domain: 'synthetic_learning',
        },
        {
          ordinal: 3,
          comparison_id: 'HEV1-H2SYN000003',
          display_title: 'Comparison 3 of 3',
          prompt: 'Explain to a school student why we see lightning before we hear thunder.',
          response_a:
              'Light travels enormously faster than sound, so the flash reaches your eyes almost ' +
              'immediately while the thunder takes longer to travel through air to your ears.',
          response_b:
              'Lightning happens first and thunder is created several seconds later, which is ' +
              'why the flash always arrives before the sound.',
          question: 'Which response would you rather receive?',
          choices: [
            'Response A is better',
            'Response B is better',
            'They are about equally good',
            'Neither response is good',
            "I'm not sure / I can't judge this",
          ],
          required: true,
          domain: 'synthetic_explanation',
        },
      ],
      reviewer_context: {
        enabled: true,
        title: 'Optional: Which best describes you?',
        choices: [
          'Student',
          'Teacher / educator',
          'Researcher / scientist / engineer',
          'Other working professional',
          'General user',
          'Prefer not to say',
        ],
        required: false,
      },
      optional_comment: {
        enabled: true,
        title: 'Optional: Anything else you want to tell us?',
        required: false,
      },
      confirmation_message: 'Thank you — your response has been recorded.',
      sandbox_auto_close_after_submissions: 3,
    },
  ],
};
