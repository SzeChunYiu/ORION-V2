# Saturation Pass K — Adversarial Epistemic Integrity, Secure Research Supply Chains and Privacy V1

**Canonical owner:** issue #41  
**Predecessor material pass:** J  
**Status:** material formal/statistical/systems pass. It adds one broad family, resets the clean-pass counter to zero and grants no new kernel family, law, paper or field authority.

## 1. Search question

What remains invisible when Machine Epistemics models uncertainty, dependence, provenance, numerical validity, consensus and authority but assumes that the sources, tools, models and interfaces are merely fallible rather than strategically compromised?

This pass changes vocabulary toward:

- confidentiality, integrity and availability;
- threat models and trust boundaries;
- poisoning, backdoors, evasion and model extraction;
- prompt injection and confused-deputy behavior;
- software/model/data supply chains;
- differential privacy and disclosure control;
- privacy–robustness–utility trade-offs;
- secure development, acquisition and incident response.

## 2. Expert cell

1. **Computer-security and threat-modelling reviewer** — assets, adversaries, capabilities, attack surfaces, trust boundaries and residual risk.
2. **Adversarial-ML reviewer** — poisoning, evasion, privacy, misuse, backdoors and adaptive attacks across the ML lifecycle.
3. **Agent-security reviewer** — indirect prompt injection, tool authorization, instruction–data confusion and causal attribution of actions.
4. **Privacy and statistical-disclosure reviewer** — differential privacy, composition, sensitivity and utility trade-offs.
5. **Secure-software/supply-chain reviewer** — provenance, acquisition, dependencies, build/test/release practices and compromise recovery.
6. **Scientific-method reviewer** — distinguishes security integrity from scientific validity and protects open inquiry/replication controls.
7. **Hostile ORION reviewer** — attempts to absorb all mechanisms into K0–K6 and rejects security theatre or universal restriction.

## 3. Finding K1 — benign-failure semantics do not cover strategic epistemic attack

### Native reconstruction

Security models an adversary with goals, knowledge, access and capabilities. Failures are intentionally induced and may adapt to detection or evaluation. Adversarial-ML taxonomies distinguish attacks by lifecycle stage and objective, including:

- training-data poisoning;
- model poisoning/backdoors;
- evasion/adversarial examples;
- privacy inference and model/data extraction;
- generative misuse and indirect prompt injection;
- availability, integrity and confidentiality compromise.

The scientific consequence differs from ordinary noise or unknown dependence. An attacker can choose evidence specifically to exploit the current evaluator, search route, model, receipt structure or authority boundary.

### ORION collision

ORION records source identity, dependence, evidence, evaluator and authority. These do not by themselves state:

- who can manipulate which object;
- which asset/claim is targeted;
- what the attacker knows about the pipeline/evaluator;
- whether the source, model or tool is inside the trust boundary;
- how a defense changes utility or scientific reach;
- whether the attack is adaptive to the defense;
- whether post-compromise history and derived claims must reopen.

### Candidate research object

`AdversarialEpistemicIntegrityReceipt = (`
`episode, protected_assets, scientific_claims_at_risk, adversary_identity_or_class, goals, knowledge, capabilities, access, attack_surface, lifecycle_stage, trust_boundaries, attack_or_incident_identity, detection_evidence, mitigations, adaptive_attack_status, affected_claims, reopen_reach, residual_risk, recovery_and_revalidation, authority)`.

### Candidate failures

- `STRATEGIC_POISONING_LAUNDERED_AS_RANDOM_NOISE`;
- `AUTHENTIC_SOURCE_COMPROMISED_CONTENT`;
- `DEPENDENCE_GRAPH_POISONED_BY_FALSE_LINEAGE`;
- `EVALUATOR_AWARE_ATTACK`;
- `DEFENSE_VALIDATED_ONLY_AGAINST_STATIC_ATTACK`;
- `POST_COMPROMISE_DERIVATIONS_NOT_REOPENED`;
- `SECURITY_CONFIDENCE_LAUNDERED_AS_SCIENTIFIC_VALIDITY`.

### Disposition

Material broad-family pressure. Native mechanisms are owned by cybersecurity, adversarial ML and secure systems. K0/K3/K4/K6 can host the interface; no K7 is admitted.

---

## 4. Finding K2 — external content can become an unauthorized control channel

### Native reconstruction

Tool-integrated language-model agents consume external documents, websites, messages and retrieval results. Indirect prompt injection embeds attacker instructions in content that the agent is supposed to treat as data. The vulnerability is structural: the model may not reliably separate informational content from control instructions and may call tools or disclose information outside the user's intent.

Agent benchmarks show that apparently benign retrieval/tool tasks can be converted into harmful actions or exfiltration. Later defenses increasingly examine action-level causal attribution rather than only classifying input strings.

### ORION collision

Machine Epistemics deliberately broadens source ecology and encourages cross-domain retrieval. That increases the control surface. A source can be:

- scientifically relevant evidence;
- untrusted data;
- a malicious instruction;
- a mixture of all three.

Source/evidence binding is therefore insufficient unless control authority is separated from evidential content.

### Candidate specialization

`InstructionDataBoundaryReceipt = (`
`user_or_problem_intent, trusted_instruction_sources, untrusted_content_sources, proposed_action, evidence_support_for_action, causal_attribution_to_intent, tool_permissions, side_effects, data_disclosure, counterfactual_without_untrusted_control, decision)`.

### Hostile cases

- retrieved paper contains hidden action instructions;
- a malicious email becomes a high-privilege tool request;
- a scientifically relevant source also asks the agent to exfiltrate data;
- a defense blocks legitimate methodological instructions in a trusted protocol;
- same wording appears as trusted instruction and untrusted evidence under different identities;
- tool call survives after the malicious portion is attenuated, indicating genuine user-intent support.

### Disposition

Specialization of K0/K3/K4 and the distributed/causal-action parents. It is not a universal semantic classifier and does not solve prompt injection by naming a boundary.

---

## 5. Finding K3 — secure provenance is not content validity, but content validity requires secure provenance

### Native reconstruction

Software and AI supply-chain security treats development, dependencies, data, models, build systems, release artifacts, acquisition and updates as attack surfaces. Secure-development frameworks aim to reduce vulnerabilities, protect artifacts and respond to compromise throughout the lifecycle.

Cryptographic hashes, signatures and provenance can authenticate identity and detect unauthorized mutation. They cannot establish that the signed artifact was scientifically correct or that its creator was uncompromised.

### ORION collision

ORION already states that provenance is not corroboration. Pass K adds the inverse necessity:

> Scientific evaluation cannot recover trustworthy evidence if the identities, dependencies or execution environment were maliciously substituted and the substitution is invisible.

### Candidate research object

`ResearchSupplyChainReceipt = (`
`source_code, models, datasets, dependencies, build_and_training_environment, acquisition_route, signatures_or_attestations, reproducible_build_or_training_status, vulnerability_and_incident_history, trusted_roots, compromise_indicators, deployment_identity, update_policy, affected_scientific_outputs, revocation_and_rebuild_plan)`.

### Candidate failures

- `SIGNED_BUT_MALICIOUS_ARTIFACT`;
- `VALID_SCIENTIFIC_METHOD_SUBSTITUTED_IN_SUPPLY_CHAIN`;
- `DEPENDENCY_UPDATE_CHANGES_RESULT_WITHOUT_EPOCH`;
- `MODEL_WEIGHT_IDENTITY_UNBOUND`;
- `COMPROMISED_BUILD_REPRODUCES_CONSISTENTLY`;
- `SECURE_BUILD_WRONG_SCIENCE`.

### Disposition

Parent-owned secure-development and supply-chain mechanism; research-interface and benchmark pressure only.

---

## 6. Finding K4 — privacy changes what evidence can be observed and how accurately

### Native reconstruction

Differential privacy defines a bounded change in output distribution when one person's record is added or removed. Privacy depends on the adjacency relation, sensitivity, mechanism and composition across queries. Noise or restricted access can reduce utility, identifiability and calibration.

Privacy is not secrecy in every sense, consent, fairness or collective data governance. Conversely, data governance without a technical disclosure model may not prevent inference attacks.

### ORION collision

A privacy mechanism modifies the evidence available to the research process. The scientific system must distinguish:

- uncertainty caused by the world/model;
- uncertainty introduced intentionally for privacy;
- bias or clipping from the mechanism;
- composition across repeated research queries;
- privacy guarantees versus data-use authority;
- scientific decisions that remain valid under the private release.

### Candidate research object

`PrivacyScientificValidityReceipt = (`
`data_identity_and_governance, adjacency_or_secret_definition, mechanism, epsilon_delta_or_native_guarantee, sensitivity, clipping_and_preprocessing, composition_accountant, threat_model, released_object, statistical_bias_and_variance, downstream_claims, utility_and_coverage, prohibited_reidentification, residual_privacy_risk, authority)`.

### Candidate failures

- `PRIVACY_PARAMETER_WITHOUT_ADJACENCY_SEMANTICS`;
- `PRIVATE_RELEASE_LAUNDERED_AS_UNBIASED_EVIDENCE`;
- `REPEATED_QUERY_COMPOSITION_IGNORED`;
- `PRIVACY_LAUNDERED_AS_CONSENT_OR_CARE`;
- `UTILITY_GAIN_PURCHASED_BY_WEAKER_PRIVACY`;
- `PRIVACY_DEFENSE_DESTROYS_IDENTIFIABILITY`;
- `GROUP_OR_COLLECTIVE_HARM_OUTSIDE_RECORD_LEVEL_GUARANTEE`.

### Fundamental trade-off pressure

Distributed learning results show that privacy, robustness to malicious participants and utility can form an unavoidable trade-off. Therefore the framework cannot require each coordinate to improve independently. It must expose the Pareto frontier and non-compensatory scientific/authority constraints.

### Disposition

Material parent and benchmark pressure inside F12/F16/F19/F20 and the new F22. No universal privacy mechanism is added.

---

## 7. Finding K5 — consensus and Byzantine tolerance do not cover common-mode epistemic attacks

### Native reconstruction

Byzantine-fault protocols often assume limits on the number or relation of faulty replicas. Adversarial ML and agent systems frequently violate the useful independence assumptions:

- many agents share one poisoned model;
- all retrieve one compromised corpus;
- a trusted root or evaluator is attacked;
- an adaptive attacker targets the aggregation rule;
- malicious content controls honest agents through the same interface.

### ORION collision

The dependence model must interact with the threat model. A protocol can tolerate several independent arbitrary replicas while failing completely against one common source or supply-chain compromise.

### Candidate benchmark

`THREAT_DEPENDENCE_INTERACTION` compares:

- independent replica faults;
- common-model fault;
- poisoned shared corpus;
- adaptive aggregation attack;
- evaluator compromise;
- authenticated but strategically misleading evidence.

### Disposition

Strengthens L31/F08/F22 and P-D; no new coordinate.

---

## 8. Finding K6 — security controls can become epistemic drag or censorship

### Native reconstruction

Security restrictions can reduce attack surface, but they can also:

- block legitimate sources/tools;
- prevent replication or independent scrutiny;
- centralize control in one trusted evaluator;
- increase false refusals;
- hide proprietary mechanisms;
- create uninspectable data or model boundaries;
- shift rather than remove risk.

### ORION collision

“Secure” cannot be a universal trump coordinate. The protected decision is a vector:

`scientific validity × integrity × confidentiality/privacy × availability × authority × cost × justified reach`.

Hard legal/ethical/authority constraints remain non-compensatory, but among admissible configurations the system must measure security-related scientific loss and concentration of trust.

### Candidate failures

- `SECURITY_THEATRE_NO_ATTACK_REDUCTION`;
- `LOCKDOWN_DESTROYS_REPLICATION`;
- `SINGLE_TRUSTED_ROOT_COMMON_MODE`;
- `PROPRIETARY_SECURITY_LAUNDERED_AS_CANNOT_AUDIT`;
- `FALSE_POSITIVE_DEFENSE_SUPPRESSES_REMOTE_PARENT`;
- `ATTACK_REDUCTION_WITH_UNREPORTED_SCIENTIFIC_UTILITY_LOSS`.

### Disposition

Component-value and resilience pressure; security methods remain contextual.

---

## 9. Broad-family addition

Pass K adds:

### F22 — adversarial security, privacy and epistemic integrity

Native questions:

- How can a scientific research process preserve confidentiality, integrity and availability under strategic attack?
- Which assets, trust boundaries, adversary capabilities and lifecycle stages determine the threat?
- How do poisoning, evasion, backdoors, prompt injection and supply-chain compromise affect scientific claims and authority?
- How should privacy guarantees and utility loss be propagated into scientific conclusions?
- When do security controls reduce justified reach or create common-mode trust?

Parent examples:

- computer and software security;
- adversarial machine learning;
- privacy and differential privacy;
- cryptography and authenticated provenance;
- secure software/model/data supply chains;
- agent/tool security;
- Byzantine and intrusion-resilient systems;
- security assurance and incident response.

F22 is broad enough to deserve explicit coverage because malicious adaptation changes the meaning of otherwise adequate evidence, evaluation and control. It does not create a new kernel family.

## 10. New candidate research objects

- `AdversarialEpistemicIntegrityReceipt`;
- `InstructionDataBoundaryReceipt`;
- `ResearchSupplyChainReceipt`;
- `PrivacyScientificValidityReceipt`.

All must survive parent replacement and component-value experiments.

## 11. New contradiction/tension pressure

- reproducibility/openness versus confidentiality, privacy and security;
- authenticated provenance versus trustworthy content;
- autonomous source/tool use versus instruction–data separation;
- privacy versus robustness versus scientific utility;
- decentralized review versus common security/trust roots;
- adaptive adversary versus frozen benchmark/evaluator;
- secure restriction versus exploratory and replication reach.

## 12. Protected benchmark additions

- `POISONED_EVIDENCE_SOURCE_WITH_VALID_IDENTITY`;
- `EVALUATOR_AWARE_ATTACK`;
- `INDIRECT_PROMPT_INJECTION_SCIENTIFIC_AGENT`;
- `TOOL_CALL_CAUSAL_ATTRIBUTION`;
- `SIGNED_BUT_MALICIOUS_RESEARCH_ARTIFACT`;
- `COMPROMISED_DEPENDENCY_REOPENS_DERIVATIONS`;
- `PRIVACY_COMPOSITION_AND_CLAIM_VALIDITY`;
- `PRIVACY_ROBUSTNESS_UTILITY_FRONTIER`;
- `COMMON_MODE_MODEL_ATTACK_VS_BYZANTINE_ASSUMPTIONS`;
- `SECURITY_LOCKDOWN_SCIENTIFIC_DRAG`.

## 13. Reduction against K0–K6

- K0 binds identities, trust/authority roots and permitted action surfaces.
- K1 retains compromised/contested state and unresolved attack status.
- K2 binds context and transport after privacy/security transformations.
- K3 records secure provenance, dependence, attack lineage and affected support.
- K4 selects mitigation, recovery, revalidation and safe tool actions.
- K5 governs secure exploration/escalation under changing attack surface.
- K6 evaluates attacks, residual risk, privacy/utility and scientific impact.

No eighth family is required at the interface level. Security/privacy are a broad parent family and cross-cutting benchmark/adapter programme.

## 14. Primary/authoritative anchors

- Barreno, M., Nelson, B., Joseph, A. D. & Tygar, J. D. The Security of Machine Learning. *Machine Learning* 81, 121–148 (2010).
- Biggio, B., Nelson, B. & Laskov, P. Poisoning Attacks against Support Vector Machines. *ICML* (2012).
- Vassilev, A. et al. *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*. NIST AI 100-2 E2025. DOI `10.6028/NIST.AI.100-2e2025`.
- Greshake, K. et al. Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. arXiv:2302.12173.
- Zhan, Q. et al. InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents. arXiv:2403.02691.
- Dwork, C., McSherry, F., Nissim, K. & Smith, A. Calibrating Noise to Sensitivity in Private Data Analysis. *TCC* (2006).
- Allouah, Y. et al. On the Privacy–Robustness–Utility Trilemma in Distributed Learning. *ICML* (2023).
- NIST SP 800-218A. *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models* (2024). DOI `10.6028/NIST.SP.800-218A`.
- Castro, M. & Liskov, B. Practical Byzantine Fault Tolerance. *OSDI* (1999); *ACM TOCS* (2002).

## 15. Current terminal

```text
CANONICAL_PASS_ID = K
FINDING_KIND = MATERIAL_COORDINATE_AND_BENCHMARK_PRESSURE
NEW_BROAD_FAMILY = F22
DECLARED_FAMILY_COUNT = 22
POST_K_CLEAN_FULL_PASSES = 0
CLEAN_FULL_PASSES_REQUIRED = 3
NEW_KERNEL_FAMILY = NO
NEW_FOUNDATION_LAW = NO
NEW_PAPER_IDENTITY = NO
FOUNDATION_SYNTHESIS = BLOCKED
```
