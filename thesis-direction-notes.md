# Thesis direction: working notes (private)

Last updated: 3 November 2026. Source: thesis-planning conversation, July to November 2026.

**Do not commit this file to the public site repository.** Keep it in a private repo.

Tags: **[established]** supported by evidence · **[preliminary]** partial evidence · **[proposed]** not yet tested · **[planned]** not started · **[to confirm]** open fact or decision.

---

## 1. Controlling idea

- **One sentence.** In multi-stakeholder systems without continuous connectivity, an access decision is only as trustworthy as the weakest stage of its lifecycle: how its rule was agreed, whether enforcement provably implements that rule, and when, and under whose authority, it became final. [proposed]
- **Centre of gravity.** Authorization when no single authority can decide. Intermittent connectivity is the stressor under which claims are tested, not the thesis identity.
- **Where it is going.** A thesis on authority and finality for decisions made across organisations. The open question is how a system should treat a decision whose author's right to make it is later contested. AI agents acting for people during disconnection are the case that forces that question into practice. [proposed]

## 2. Structure

### Lifecycle

- **Agree:** Paper A.
- **Assure:** Paper B.
- **Bind:** EQuack and AAS. Who may decide, and when a decision becomes final.

Auditability is the invariant across all stages: each stage produces evidence from which a decision can be reconstructed and defended afterwards. [proposed]

### Design axis: authority structure × binding time [preliminary]

- **EQuack:** plural authority. Decisions stay tentative until deterministic replay, and revocation reaches backwards.
- **AAS:** one designated authority. Decisions are final when written at the command edge, and partitions must not move authority.
- **Paper B:** the degenerate pole (single domain, online, binds before deployment). It seeds the recurring method: mechanical checking of mechanism against intent (SMT in B, replay in EQuack, TLA+/Hypothesis in AAS).

### Eligibility vs command [preliminary: two case studies, no general criterion yet]

- **Eligibility** decides who may act. Plural, revisable, deny-wins mergeable. This is EQuack's territory.
- **Command** decides which act binds now. Designated, non-commutative, often irreversible. This is AAS's territory.
- **Candidate criterion:** plurality of legitimate deciders × reversibility or commutativity of the effect. It must be decidable at admission and stable under reconciliation (RQ6.1). Until it exists, the synthesis is asserted rather than argued.

## 3. Research questions

- **RQ-A** (licentiate, verbatim): How can mutually acceptable access-control agreements be systematically established at the level of joint policy selection for co-owned resources in decentralised systems where governance, policy, and enforcement are distributed across independent actors with conflicting interests? [established: answered in licentiate]
- **RQ-B** (licentiate, verbatim): What design principles enable security and consistency in federated access control without sacrificing stakeholder autonomy or system adaptability? [established: answered in licentiate]
- **RQ-C** (new): How should authority structure and binding time be assigned across decision classes, and how do the resulting regimes compose? Plain form: who may decide, and when does a decision become final, when no single authority is in charge and connectivity cannot be assumed? [proposed]

## 4. Corpus and status (as of 3 November 2026)

| Paper | Status | Thesis role |
|---|---|---|
| A. Objective- and Utility-Based Negotiation for Access Control. ICISSP 2025, vol. 2, pp. 493–501. DOI 10.5220/0013130000003899 | Published | Agree; RQ-A |
| B. Formal Verification for Preventing Misconfigured Access Policies in Kubernetes Clusters. IEEE Access 13, pp. 141798–141813, 2025. DOI 10.1109/ACCESS.2025.3597504 | Published | Assure; RQ-B; seeds verification method |
| Licentiate: Multi-Stakeholder Access Control in Data Ecosystems. LTU, January 2026 | Published | RQ-A and RQ-B |
| C. EQuack: Deterministic Replay for Eventually Consistent Access Control. IEEE Internet of Things Journal | Under review (submitted 3 June 2026) | Bind, plural-authority pole; RQ-B, RQ-C |
| 4. AAS, formerly AAL ("Authority-Aligned Linearization for Rescue-Service Incident Response over Intermittent Edge Networks"). IEEE NCA 2026 | Submitted, double-blind. Keep off the public site until the decision | Bind, designated-authority pole; RQ-C |
| Command Succession under Intermittent Connectivity: Enforcing and Reconciling Human Authority in Incident Response (repo rescue-ois) | In preparation, about halfway. Venue possibly ACM TCPS [to confirm] | See §6 |
| Task-Scoped Authorization for Local AI Agents, with Casper Lundberg (repo agentsAndAccessControl) | Exploratory | See §6 |

[to confirm] The NCA decision for AAS, and what "AAS" stands for.

## 5. Planned papers

### Paper 5: the bridge [planned]

**Core claim to falsify:** negotiated agreements can be compiled into offline-enforceable artifacts such that the reconciled state provably conforms to the agreement in force at each operation, even when the agreement changes mid-partition.

- **Framing rule:** semantics-preserving cross-domain policy translation with checkable conformance. Never "integrating the artefacts". Licentiate §5.2 calls that pipeline "unglamorous engineering" and ranks cross-domain end-to-end verification as the higher payoff.
- **Paper A's limitation:** Paper A selects from a pre-scored catalogue and emits no machine-readable agreement semantics. The bridge must therefore define the agreement representation itself (an ODRL-core profile or a custom IR). Paper A becomes the selection stage over candidates expressed in that IR.
- **Lane check (July 2026):** ODRL-to-OpenFGA compilation exists for data spaces, but every published target is online and strongly consistent. Offline, eventually consistent targets with post-partition conformance appeared unoccupied. Re-check quarterly.

Research questions, each with its failure condition:

- **RQ5.1 Representation.** Which fragment of agreement semantics compiles into epoch-bounded credentials plus deny-overrides policies, and what is provably outside it? Fails if the compilable fragment covers only a minority of real clause patterns.
- **RQ5.2 Conformance.** What is the formal definition of "the reconciled state conforms to a time-varying agreement", and does compilation preserve it under deterministic replay? Fails if the predicate needs information no replica can hold.
- **RQ5.3 Lifecycle under partition.** Renegotiation, expiry and breach-revocation become epoch transitions, with a bound on recorded-but-nonconforming behaviour. Fails if any transition requires coordination.
- **RQ5.4 Obligations (the headline).** Which duty classes are deterministically auditable from the reconciled log, and what evidence must operations carry? Delete-by is the known hard case.
- **RQ5.5 Deployability.** A real multi-node deployment under a circular-economy workload, designed from day one to close the evaluation-reality gap.

### Paper 6: the capstone [planned]

**Core claim to falsify:** eligibility and command require different binding semantics, and a principled composition preserves both classes' guarantees where either parent system alone fails.

- **RQ6.1 Classification.** Is plurality × reversibility decidable at admission and stable under reconciliation? Test it against both parents' operation vocabularies, including awkward cases such as hazard annotations and actuator parameters.
- **RQ6.2 Retroactivity collision.** How should the system treat command entries issued during a tenure whose commander's own eligibility is later retroactively invalidated? Candidate options: finality wins (flag in audit), eligibility wins (retroactive void), or quarantine and compensation.
- **RQ6.3 Impossibility (minimum viable result).** Conjecture: retroactive revocation safety and write-time finality cannot both hold for the same operation under partition. Find the weakest jointly achievable per-class guarantee triple (binding time, reconciliation behaviour, audit obligation).
- **RQ6.4 Mechanism.** Express fenced promotion as a (REVOKE, GRANT) epoch transition inside the eligibility substrate, without the command journal ever being reordered.
- **RQ6.5 Falsification.** Run partition scenarios with autonomous agents as principals.

**Sequencing:** start after both parent papers clear review. Fallback thesis shape: five papers plus a heavier kappa.

## 6. Decisions open now [to confirm]

- **Command Succession overlaps the capstone.** Its public description includes "how orders given in the meantime are reconciled", which is RQ6.2/6.3 territory. Decide whether it is AAS's journal extension, the capstone itself, or a separate paper. The answer changes the paper count and the RQ-C mapping.
- **Corpus size.** There are 2 published, 2 under review, 1 in preparation, 1 exploratory and 2 planned: 8 candidates. Decide which go into the doctoral thesis.
- **Task-Scoped Authorization.** It belongs in the thesis only if framed under RQ-C (delegated authority: who decides on whose behalf, and when it binds) or RQ-B (enforcement outside the model). The earlier plan had agents only as capstone evaluation subjects.
- **Sequencing constraint stated earlier:** no new paper until the self-study AI course is complete. Check this against the two papers now active.
- **Doctoral supervisory team.** The licentiate lists Bodin, Chiquito and Kristiansson.

## 7. Framing rules

- **Scope every ordering or tie-break mechanism to its decision class.** AAS's claim that deterministic resolution rules "invent authority" must be limited to command decisions. Otherwise it reads as an attack on EQuack's HLC tie-break.
- **Connectivity is a stressor, not the identity.**
- **Tag every claim** as proved, model-checked, measured, argued or designed. Generalise AAS's evidence-level table across the thesis.
- **Avoid "first ever" claims**, and never name a tool or paper as the contribution.

## 8. Examiner traps and prepared answers

- **"AAS says tie-breaks invent authority. Doesn't that undermine EQuack?"** EQuack orders eligibility evidence, where deny-by-default is defensible and effects are revisable. AAS refuses to merge commands, where no merge is defensible.
- **"Give me the criterion that classifies an arbitrary operation."** That is RQ6.1. Until it is answered, label the split preliminary.
- **"Isn't AAS just Raft with a hand-picked leader?"** The mechanisms are not claimed as new. The contribution is which operations sit under the single writer, and the fenced-promotion rule for moving it. Raft follows reachability by design (12 of 12 runs).
- **"Why not a blockchain?"** Ordering needs online consensus, which a partition removes.
- **"What would change your conclusion?"** An operation classified as eligibility before reconciliation and as command after it. Then the split is a spectrum, not two poles.

## 9. Defensibility gaps, ranked by impact

1. **Mechanise EQuack's ordering and gate kernel** (TLA+/Apalache). This converts argued theorems into checked ones and completes the verification-as-method thread. It is the highest-leverage task.
2. **Evaluation-reality gap.** No experiment has left one machine, and all workloads are synthetic. The thesis needs one real multi-node deployment and one non-synthetic or practitioner-validated workload (DPP via RemaNet, or rescue services). AAS also needs a multi-edge promotion run, because SingleAuthority and SingleCommand are model-only.
3. **The capstone needs its minimum viable result** (RQ6.3).
4. **The synthesis is asserted, not argued.** It needs a formal eligibility/command criterion, and the axis must be grounded in literature it extends: RedBlue, ECAC, Zanzibar Zookies, "Making CRDTs not so eventual".
5. **Publication floor.** EQuack and AAS are not yet accepted. Resubmission targets: AAS at SRDS/DSN/ICDCS class, EQuack at TDSC class. Aim at least one doctoral paper at a strong venue.
6. **Printed debts in the licentiate.**
   - Trust negotiation (§5.1, "an obvious place to dig deeper"): re-scope it openly as orthogonal to binding.
   - The methodology confession about tool-shaped problems: show the loop closed in the later papers.
   - Paper A's self-reported weights: state the non-claim (decision support, not incentive-compatible mechanism design).
7. **Novelty audit** per contribution, refreshed quarterly.

## 10. Adoption-gap findings (research report, October 2026)

- **Paper A: practice routes around it.** Data spaces (Catena-X, EDC) use framework agreements plus accept/reject ODRL offers, and counter-offers are unimplemented. It becomes relevant with multilateral co-ownership (DPP tiered access) or DSP counter-offers.
- **Paper B: a deployed pain point, but cheaper tools win.** AWS Zelkova validates SMT-based authorization analysis at scale: from a thousand to about a billion SMT calls a day over five years (Rungta et al., CAV 2022). However, it runs vendor-side, and AWS removed customer-authored specifications to scale it. Practice uses OPA/Gatekeeper, Kyverno and CEL ValidatingAdmissionPolicy; XACML is dead in cloud-native settings. Follow-up work should use Cedar or CEL rather than XACML, with a curated invariant library.
- **EQuack: an anticipated, high-assurance problem.** Practice accepts token-expiry windows (Let's Encrypt shut down OCSP on 6 August 2025; Greengrass caches trust). It matters where the stale window is intolerable, such as the defence edge or critical infrastructure. Align with mdoc and SD-JWT VC, the primary eIDAS 2.0 formats.
- **AAS: not yet a software problem in practice.** Command authority is ICS doctrine layered over best-effort sync, and Rakel is voice-centric. The window opens with Rakel G2/Swen, the data-rich edge, around 2028–2030.
- **Honest relevance case: regulatory tailwinds.** eIDAS 2.0 wallets (member states, end of 2026), the EU Data Act (in force September 2025), and the battery passport (mandatory 18 February 2027).
- **Caveats.** Adoption numbers are mostly vendor-reported. Verify the Kyverno CNCF graduation and the XACML 4.0 draft against primary sources before citing.

## 11. Supervisor discussion points (trajectory)

1. Intermittent connectivity was never load-bearing in the licentiate RQs. Centre the kappa on authority, with partition as the stressor.
2. EQuack and AAS are sunk work. The open choice is the capstone: partition-heavy composition, or cross-domain end-to-end verification.
3. Whose agenda is the rescue line: a one-off, or the doctoral centre? Which projects obligate more intermittent-edge work?
4. Opponent risk: the centre of gravity selects the examiner (distributed systems vs. security).
5. Identity preference: "authorization in decentralized multi-stakeholder systems".

**Asks:** agree the kappa's centre; confirm the bridge as Paper 5; pick the capstone variant; list project obligations.

## 12. Supervisors' predictions document (Kristiansson, extended by Bodin)

- **Implication 7** (explicit agreements across organisations, renegotiation, arbitration) corresponds to RQ-A and the bridge paper.
- **Implication 9** (permissions enforced outside the model; untrusted content gains no authority by being read; controls across organisational boundaries) corresponds to RQ-B, RQ-C and Task-Scoped Authorization.
- **Prediction 4** (whom an agent represents, what it is authorised to do, who remains responsible) corresponds to AAS's attributable command authority and EQuack's audit chain.
- **Implication 8** (a plant cannot move to the cloud; often no Internet) is the reason disconnection is a realistic stressor.
- **Prediction 8** (decentralisation is not blockchain) supports EQuack's no-consensus design.
- **Weak fit:** frugality. Do not claim it.

## 13. CPS days poster (26 October 2026)

- **Main message:** "When several organisations share a system, the hard part is not granting access. It is deciding who may decide, and when a decision counts."
- **Feedback question:** "In your CPS system, which decisions could tolerate being undone after reconnection, and which must be final the moment they're made?"
- **Feedback received:** [to add]

## 14. Reusable one-liners for Claude Code

**Any paper** (replace [PAPER]):

> This paper is one chapter of a doctoral thesis arguing that, in multi-stakeholder systems where no single authority can decide, an access decision is only as trustworthy as the weakest stage of its lifecycle — how its rule was agreed (RQ-A), whether enforcement provably implements that rule (RQ-B), and who may decide and when that decision becomes final (RQ-C), with authority structure × binding time as the central design axis, the eligibility/command distinction as its organizing split (plural, revisable, deny-wins-mergeable vs. designated, write-time-final, non-commutative), intermittent connectivity as the stressor rather than the identity, and auditable evidence as the invariant running through every stage — so revise [PAPER] so its introduction, contribution statements, related-work positioning, and limitations state explicitly which lifecycle stage and decision class it addresses, scope every ordering or tie-break mechanism to its decision class, tag each claim as proved, model-checked, measured, or argued, and never frame the work as tool integration or claim beyond its evidence.

For the bridge paper, append: "frame it as semantics-preserving cross-domain policy translation with checkable conformance, closing the RQ-A↔RQ-B edge."

**AAS:**

> AAS is one paper in a doctoral thesis arguing that, in multi-stakeholder systems where no single authority can decide, an access decision is only as trustworthy as the weakest stage of its lifecycle — how its rule was agreed (RQ-A), whether enforcement provably implements that rule (RQ-B), and who may decide and when that decision becomes final (RQ-C) — with authority structure × binding time as the central axis, intermittent connectivity as the stressor rather than the identity, and auditable evidence as the invariant; AAS is the designated-authority, write-time-binding pole of RQ-C (the dual of the thesis's EQuack paper, which is the plural-authority, reconciliation-binding pole), so revise it to state that it governs *command* decisions (designated, non-commutative, irreversible) while *eligibility* decisions (plural, revisable, deny-wins-mergeable) stay out of scope, narrow its claim that deterministic resolution rules "invent authority" to the command class only, tag each claim as proved, model-checked, measured, or argued, and never claim beyond the evidence.
