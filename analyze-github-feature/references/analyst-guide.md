# Analyst guide

Use this reference to calibrate investigation depth, select the next question, and draft concise Estonian GitHub comments.

## Contents

1. [Core stance](#core-stance)
2. [Evidence and proportional depth](#evidence-and-proportional-depth)
3. [Choosing the next question](#choosing-the-next-question)
4. [Requirements maturity](#requirements-maturity)
5. [Estonian public-writing style](#estonian-public-writing-style)
6. [Examples](#examples)

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

1. Current executable behavior and focused tests show what the system does.
2. Direct observations, repeated support cases, logs, or measured workflow costs show that a problem occurs.
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
- **Assumption:** plausible but not yet verified.
- **Decision:** an option explicitly chosen by relevant participants.
- **Open question:** missing information that could change the decision or scope.

Before asking, test the candidate question:

1. Can code, tests, documentation, issue history, or repository history answer it? Inspect those first.
2. Could the answer change whether to build, what to build, or a material boundary? If not, defer it.
3. Is it the highest-value remaining uncertainty? Ask that one first.
4. Would concrete options make the choice easier? Offer two or three real alternatives and recommend one.
5. Can the question be written without technical vocabulary? Translate it to visible user behavior.

Avoid mechanical questionnaires. Each answer should determine the next move.

Useful question themes include:

- Who encounters this situation, and how often?
- What are they trying to finish when the problem appears?
- What happens today, including the workaround?
- What makes the current result slow, confusing, unsafe, or unreliable?
- What observable result would make the change successful?
- Which roles may see or change the information?
- What is the smallest change that would solve the validated need?
- What happens if no change is made?

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
