# Analyst guide

Use this reference to calibrate investigation depth, select the next question, and draft concise Estonian GitHub comments.

## Contents

1. [Core stance](#core-stance)
2. [Evidence and proportional depth](#evidence-and-proportional-depth)
3. [Choosing the next question](#choosing-the-next-question)
4. [Ambiguity-first question ladder](#ambiguity-first-question-ladder)
5. [Requirements maturity](#requirements-maturity)
6. [Estonian public-writing style](#estonian-public-writing-style)
7. [Examples](#examples)

## Core stance

A feature request proves that somebody has expressed a desire. It does not yet prove:

- that the stated problem is widespread or costly;
- that the proposed feature is the right solution;
- that implementation is more valuable than an existing workaround;
- that the requester's description matches current system behavior;
- that doing nothing is unacceptable.

Use this sequence:

1. Understand the situation.
2. Validate the need and evidence.
3. Separate the underlying need from the proposed solution.
4. Define the desired observable outcome.
5. Analyze scope and consequences.
6. Formulate requirements and options.
7. Ask explicitly for agreement.
8. Hand off either an implementation plan or a no-build decision.

Do not seek certainty about irrelevant details. The goal is enough confidence to make a responsible decision.

## Evidence and proportional depth

### Prefer stronger evidence

Use available evidence in roughly this order while accounting for context:

1. Current executable behavior, focused tests, and scoped observation of the designated test UI show what the system does.
2. Direct user observations, repeated support cases, logs, or measured workflow costs show that a problem occurs.
3. Several experienced users independently describing the same situation show reach and consistency.
4. Current maintained documentation shows intended rules and terminology.
5. One participant's recollection or preference is a useful lead but weak evidence by itself.

Code is the primary source for technical context, not proof that the current user experience is acceptable. Documentation may describe intended behavior while code reveals divergence. Ask participants only about knowledge that artifacts cannot provide, such as frequency, impact, and organizational value.

### Scale the analysis

Use a light pass when the change is narrow, reversible, cheap, and affects no rules or permissions. Use a deeper pass when it changes data, roles, workflow states, integrations, privacy, business-critical behavior, or many users.

Increase depth when any of these rise:

- uncertainty about the real problem;
- number or diversity of affected users;
- severity of failure or risk;
- difficulty of reversal;
- implementation and maintenance cost;
- security, privacy, or compatibility exposure.

Decrease depth when repository and issue evidence already answer the important questions.

### Allow every responsible conclusion

Valid conclusions include:

- build as requested;
- build a smaller version;
- change an existing workflow;
- use an existing feature;
- improve instructions or training;
- gather more evidence and revisit later;
- do nothing.

Do not frame a no-build conclusion as a failure. It prevents unnecessary cost when supported by evidence and explicit participant agreement.

## Choosing the next question

Maintain these private categories:

- **Fact:** directly supported by a named artifact or participant statement.
- **Settled intent or constraint:** scope, outcome, starting context, or boundary stated unambiguously or explicitly confirmed by a relevant participant.
- **Assumption:** plausible but not yet verified.
- **Decision:** an option explicitly chosen by relevant participants.
- **Open question:** missing information that could change the decision or scope.

Before asking, test the candidate question:

1. Has the issue or a relevant participant already stated or confirmed the answer? If so, record it as settled instead of asking again.
2. Can code, tests, documentation, the designated test UI, issue history, or repository history answer it? Inspect those first.
3. Could the answer change whether to build, what to build, or a material boundary? If not, defer it.
4. Is it the highest-value remaining uncertainty? Ask that one first.
5. Would concrete options make the choice easier? Offer only alternatives that satisfy every settled constraint.
6. Can the question be written without technical vocabulary? Translate it to visible user behavior.

Avoid mechanical questionnaires. Each answer should determine the next move.

### Preserve settled intent when generating options

Do not confuse the existence of another technically possible workflow with an open product decision. Generate options only for the unresolved dimension currently under discussion.

Filter every candidate option before showing it:

- Does it preserve the stated need and outcome?
- Does it preserve explicit scope, starting context, source object, and prior decisions?
- Is it a genuine alternative on the open question rather than a different request?
- Would choosing it advance the current analysis?

If any answer is no, omit the option. Do not pad a list to reach two or three choices. A single compatible proposal is acceptable.

If evidence justifies challenging settled intent, state the conflict separately: explain what cannot safely or reasonably work and ask whether participants want to reconsider the constraint. Do not disguise that challenge as an ordinary option.

### Make conclusions auditable, not exhaustive

Keep the full comparison of material interpretations in the private Codex ledger. For each reasonably plausible interpretation, record the decisive supporting or rejecting evidence. Do not store or publish an exhaustive stream of intermediate reasoning.

In GitHub, normally show only:

1. the selected interpretation or conclusion;
2. the decisive evidence in product language;
3. a material assumption or uncertainty, if one remains; and
4. the correction or confirmation being requested.

Mention a dismissed interpretation only when a reasonable participant could still choose it from the known facts and choosing it would materially change the actor, workflow, scope, or outcome. Give the rejection reason in one short sentence.

Use confidence to control detail:

- **One interpretation clearly dominates:** state it, give the decisive reason, and ask for confirmation. Omit clearly incompatible alternatives.
- **Two or more interpretations remain materially plausible:** present them briefly and ask which one applies.
- **An assumption cannot yet be tested:** label it and ask the smallest question that would resolve it.

This pattern protects against hidden assumptions without making issue comments read like internal analysis notes.

Useful question themes include:

- Who encounters this situation, and how often?
- What are they trying to finish when the problem appears?
- What happens today, including the workaround?
- What makes the current result slow, confusing, unsafe, or unreliable?
- What observable result would make the change successful?
- Which roles may see or change the information?
- What is the smallest change that would solve the validated need?
- What happens if no change is made?

## Ambiguity-first question ladder

Use this ladder when the request does not identify a unique workflow. Do not jump from an ambiguous noun directly to feature design.

### 1. Confirm the probable context

Infer the most plausible actor and workflow from the issue, supplied documentation, and code. Present it as an inference, not a fact, and ask for confirmation.

Good form:

> Saan soovist praegu aru nii, et … See tundub kõige tõenäolisem, sest … Kas peame silmas just seda olukorda?

If two interpretations are similarly plausible, present both briefly. Do not list every theoretical procedure.

### 2. Identify the starting surface and source object

After the context is confirmed, establish where the user expects to begin and what they expect to act on only when the request has not already fixed those points. A request may say “old application” while the selectable objects are actually orders, archival items, attachments, or another child record.

Useful form when the starting point is genuinely open:

> Kust peaks kasutaja seda tegevust alustama ja mida ta seal valib?

Prefer named current screens or objects discovered from evidence over abstract wording. If the title, body, or a confirmation already says the action starts from an old application, preserve that constraint; do not offer an unrelated item view as a peer starting point.

### 3. State the current representation

Tell participants what the current screen actually provides before proposing controls. A PDF, email, summary row, or generated attachment cannot host row selection without a new interactive representation.

Useful form:

> Praegu saab kasutaja vana taotluse avada PDF-ina. Seal ei ole valitavat materjalide loendit.

This is not a reason to reject the need. It identifies the real design boundary.

### 4. Establish relevant lifecycle rules

Ask only about states that change feasibility or expected behavior: active versus expired access, approved versus denied items, duplicates, ownership, permissions, or whether previously valid items remain eligible.

Do not enumerate every lifecycle state when only one distinction affects the request.

### 5. Offer the smallest feasible choices

Give user-facing options only when at least two materially different choices remain compatible after the scope, starting point, and current representation are known. Put the smallest sufficient option first.

For reuse from an old non-interactive record, options might be:

1. Start from the old record and reuse every still-eligible item without individual selection.
2. Add an interactive item view where the user can select individual items before continuing.
3. Keep the current flow and improve guidance when the need is too rare to justify either change.

Recommend based on the confirmed outcome. Do not recommend the simplest option when it fails an essential need such as selecting only some items.

## Requirements maturity

The analysis is mature enough for a consensus request when evidence supports:

- a concise problem statement;
- affected users and relevant roles;
- the current-state workflow and failure point;
- evidence that the need is real or evidence that it is not justified;
- the desired observable outcome;
- the selected smallest sufficient approach or no-build rationale;
- scope and important exclusions;
- permissions, states, data, rules, integrations, and compatibility where relevant;
- important edge and failure cases;
- observable acceptance criteria;
- no material unresolved disagreement.

Ask for agreement only when a response can responsibly close analysis. A useful Estonian form is:

> Minu arusaam on järgmine: …
>
> Palun kinnitage, kas see kirjeldus ja pakutud suund on õiged. Kui jah, käsitlen seda meie kokkuleppena.

For a no-build recommendation:

> Praeguse info põhjal ei ole uut arendust vaja, sest …
>
> Palun kinnitage, kas nõustute selle järeldusega. Pärast kinnitust võtan otsuse kokku ja sulgen teema.

Do not interpret silence as agreement.

## Estonian public-writing style

Participants know the application well. Respect that knowledge without assuming technical expertise.

Prefer:

- short sentences;
- familiar screen, action, role, and state names;
- concrete examples from the current workflow;
- one decision at a time;
- visible consequences instead of implementation mechanics;
- a recommendation with a short reason.

Avoid:

- code symbols and file paths;
- database, API, schema, migration, architecture, framework, or test terminology;
- long introductions and repeated summaries;
- generic praise or filler;
- unexplained technical constraints;
- twenty-question checklists;
- suggesting that experienced users do not understand their own work.

Translate technical findings into user effects. For example:

- Instead of “The authorization middleware excludes external users,” write “Väliskasutaja seda vaadet praegu avada ei saa.”
- Instead of “The export query is synchronous,” write “Suure tulemuse koostamisel peaks kasutaja ootama samal lehel.”
- Instead of “The records have no stable foreign key,” write “Süsteem ei saa praegu neid kirjeid alati kindlalt omavahel siduda.”

## Examples

### 1. Trivial wording change

**Request:** Change a confusing button label.

**Repository evidence:** The same action uses the clearer term on every other screen. The button does not trigger a special workflow.

**Analysis behavior:** Inspect the affected view, translations, and nearby tests. Do not start a broad interview. Restate the small consistency fix and ask for confirmation only if the desired wording is not already explicit.

**Possible GitHub comment:**

> Kontrollisin teisi sama tegevuse vaateid. Seal kasutatakse läbivalt nimetust „Salvesta ja jätka”. Sellel lehel teeb nupp sama asja.
>
> Soovitan kasutada ka siin nimetust „Salvesta ja jätka”. Kas see sõnastus sobib?

### 2. “Export to Excel” hides the real need

**Request:** Add an “Export to Excel” button.

**Repository and documentation evidence:** Results can already be downloaded as CSV. The code shows that the result may include thousands of rows, while the visible table shows only one page.

**Underlying need:** Not yet established. Users may need offline archiving, comparison with another system, printing, or calculations.

**Possible first GitHub comment:**

> Tulemusi saab praegu alla laadida CSV-failina. Uus Exceli nupp oleks eraldi lahendus, kuid vajadus ei ole veel selge.
>
> Mida kasutajad allalaaditud andmetega kõige sagedamini teevad?
>
> 1. Võrdlevad neid teise süsteemi andmetega.
> 2. Koostavad arvutusi või aruandeid.
> 3. Säilitavad tulemuse muutmata kujul.
>
> Soovitan lähtuda kõige tavalisemast tegevusest. Siis saame otsustada, kas olemasolevast failist piisab või on vaja teistsugust lahendust.

Do not define Excel export as the requirement until the answer establishes why the existing capability fails.

### 3. Workflow involving several roles and permissions

**Request:** Let one role send a case back to the previous workflow step.

**Code evidence:** Three roles can view the case, only two can edit it, and moving backward currently reopens data that another role has approved. Notifications depend on the workflow state.

**Analysis behavior:** Trace permissions, state transitions, reopened fields, notifications, audit history, and what happens to prior approval. Ask the highest-impact user-facing question first.

**Possible GitHub comment:**

> Tagasi saatmisel muutuks varem kinnitatud info uuesti muudetavaks. See mõjutab nii kinnitajat kui ka juhtumi menetlejat.
>
> Kumb käitumine on õige?
>
> 1. Varasem kinnitus tühistatakse ja kinnitaja peab pärast parandust uuesti kinnitama.
> 2. Kinnitus jääb alles ning muuta saab ainult tagasi saatmise põhjuses nimetatud andmeid.
>
> Soovitan esimest varianti. Nii on kõigile selge, milline versioon on kinnitatud.

Continue with notification and role questions only after this rule is decided.

### 4. Analysis concludes that the feature is unnecessary

**Request:** Add a new warning panel for a rare condition.

**Evidence:** The existing summary already shows the same warning. Code and support history show no missed cases. The requester had not noticed the existing indicator.

**Possible recommendation:**

> Kontrollisin praegust vaadet ja kirjeldatud juhtumeid. Sama hoiatus on juba kokkuvõtte ülaosas. Seni ei ole näiteid, kus kasutaja oleks õige info puudumise tõttu eksinud.
>
> Soovitan uut paneeli mitte lisada. Vajaduse lahendab olemasoleva hoiatuse selgem kirjeldus kasutusjuhendis.
>
> Palun kinnitage, kas nõustute selle järeldusega. Pärast kinnitust võtan otsuse kokku ja sulgen teema.

After explicit agreement, post the no-build summary, close the issue, pause the monitor, and return a decision handoff. Do not produce an implementation plan.

### 5. Repository inspection answers the question

**Request:** Ask whether archived records appear in search results.

**Code and test evidence:** The search query excludes archived records by default and includes them only when the user selects “Näita arhiveeritud”. Tests cover both cases.

**Analysis behavior:** Do not ask participants to explain current behavior. State the verified behavior and ask only whether the desired outcome differs.

**Possible GitHub comment:**

> Kontrollisin praegust otsingut. Arhiveeritud kirjeid tavavaates ei näidata. Need ilmuvad siis, kui kasutaja valib „Näita arhiveeritud”.
>
> Kas soov on seda käitumist muuta või oli küsimus praeguse töökorralduse täpsustamiseks?

This keeps the conversation focused on product intent rather than making participants rediscover system behavior.

### 6. Vague request to create a new application from an old one

**Request:** “Create a new application based on a selection from an old application.”

**Documentation evidence:** Several application procedures exist. The most plausible interpretation is a client reusing records from an earlier restricted-digital-material application. The client's consolidated history opens old applications as PDFs and has no interactive historical item list.

**First GitHub comment — confirm context only:**

> Saan soovist praegu aru nii, et klient tahab varasema virtuaalse juurdepääsutaotluse materjalide põhjal teha uue taotluse. See tundub kõige tõenäolisem, sest selles töövoos valib klient taotlusse konkreetsed materjalid.
>
> Kas peame silmas just seda olukorda?

Do not ask about checkboxes, copying rules, or expired permissions in the same comment.

**After context is confirmed — preserve the settled starting point:**

The request already says that the new action is based on the previous application. Record that as settled. Do not ask whether the client should instead start from an unrelated material view.

State the current design boundary and move to the next open decision:

> Uus tegevus algab seega varasema taotluse juurest. Praegu saab klient selle oma konto all avada ainult PDF-ina. PDF-is ei ole valitavat materjalide loendit.
>
> Valiku tegemiseks on vaja varasema taotluse rea juurest avanevat säilikute vaadet. Järgmine küsimus on, millised varasema taotluse säilikud on uue taotluse jaoks sobivad.

**Offer alternatives only within the settled constraint:**

After eligibility is clear, a genuine open decision could be the initial selection state:

> Sobivate säilikute valimiseks on kaks varianti.
>
> 1. Kõik sobivad säilikud on alguses märgitud. Klient eemaldab need, mida ta ei soovi uude taotlusse lisada.
> 2. Ükski säilik ei ole alguses märgitud. Klient valib vajalikud säilikud ise.
>
> Soovitan esimest varianti, sest see toetab nii kõigi kui ka ainult osa varasemate säilikute uuesti taotlemist väiksema tööga.

Only then clarify eligibility rules such as expired access, prior denial, duplicates, and items that are no longer available. Each answer should narrow the next question.
