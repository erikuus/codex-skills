# Complexity diagnostics

Use this reference to translate a developer's maintenance experience into concrete complexity findings. It adapts the human-centered design philosophy described by John Ousterhout in *A Philosophy of Software Design* and his Stanford software-design materials. Paraphrase the ideas; do not reproduce book text.

## Contents

- [Diagnostic hierarchy](#diagnostic-hierarchy)
- [Core symptoms](#core-symptoms)
- [Primary causes](#primary-causes)
- [Design red flags as explanatory hypotheses](#design-red-flags-as-explanatory-hypotheses)
- [Confounders](#confounders)
- [Question-selection rule](#question-selection-rule)

Primary public sources:

- John Ousterhout, [The Nature of Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity)
- John Ousterhout, [Discussion of A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter21/lecture.php?topic=bookReview)
- John Ousterhout, [A Philosophy of Software Design, second-edition overview](https://web.stanford.edu/~ouster/cgi-bin/book.php)
- John Ousterhout, [Working Isn't Good Enough](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=working)

Treat a module generically: it may be a function, module, package, component, context, service, process, object, endpoint, template, data type, or subsystem. Do not import class-specific assumptions into functional or data-oriented code.

## Diagnostic hierarchy

Diagnose in this order:

1. **Observation:** what the developer did, reported, changed, missed, or verified.
2. **Experienced symptom:** change amplification, cognitive load, or unknown-unknown risk.
3. **Likely cause:** dependency or obscurity, optionally refined by a design red flag.
4. **Maintenance consequence:** extra work, inconsistent behavior, fragile confidence, or future defect risk.

Do not start with a favored principle and search for evidence to justify it.

## Core symptoms

### Change amplification

A conceptually small change requires many coordinated modifications.

Evidence includes:

- the same decision edited in multiple files or representations;
- tests, fixtures, schemas, UI, configuration, and runtime code each restating one fact;
- compatibility or synchronization edits that do not add behavior;
- a change that cannot be completed through one authoritative owner.

Ask:

- Which edits represented the actual behavior change?
- Which edits only kept another place synchronized?
- If this decision changes again, which places must change together?
- Did any location feel like a duplicate but still had to be edited?

Do not count files blindly. A legitimate vertical slice may cross several independent responsibilities without duplicating knowledge.

### Cognitive load

The developer must hold too much relevant information in working memory to make the change safely.

Evidence includes:

- remembering call order, state transitions, flags, formats, or special cases across distant locations;
- repeatedly reopening files to reconstruct context;
- understanding implementation details that should be irrelevant to the task;
- mentally simulating several interacting representations or lifecycle stages;
- inability to explain the change through one stable mental model.

Ask:

- What facts did you have to keep in your head at the same time?
- What would you need to reconstruct after an interruption?
- Which implementation detail did you need even though it was not part of the requested behavior?
- Where did you have to reread code because local context was insufficient?
- What was the simplest accurate mental model you could form?

Do not equate unfamiliar syntax with cognitive load created by the repository.

### Unknown-unknown risk

Important information or affected behavior is not discoverable before the developer needs it. This is a risk assessment, not something the developer can reliably self-report.

Evidence includes:

- a required location discovered only after a failing test or late search;
- an affected path omitted from the change despite high confidence;
- convention, registration, generation, configuration, or runtime dispatch hiding a dependency;
- surprising side effects or distant coupling;
- no credible method for establishing that all affected paths were found.

Ask:

- What did you discover later than you wish you had?
- What caused you to search beyond the first apparent owner?
- What evidence tells you there is not another affected path?
- Did a test or runtime result reveal a dependency you had not considered?
- If the relevant test did not exist, what would probably have been missed?

Do not ask only “Were there unknown unknowns?” Compare the developer's result with the evaluator's hidden model and available verification. Report uncertainty when neither can establish completeness.

## Primary causes

### Dependency

One area cannot be understood or changed without knowledge of another. Dependencies are not automatically bad; diagnose those that make ordinary changes require unnecessary coordination or leaked knowledge.

Ask:

- Which other area did you need to understand before this one made sense?
- Which files would have to change together if this rule changed again?
- Could you change the owner without knowing the caller's internal assumptions?
- Did the interface let you ignore the implementation?

### Obscurity

Important information is difficult to discover, or reasonable first guesses are wrong.

Ask:

- Where did you look first, and what made that seem correct?
- What did a name or directory structure lead you to expect?
- Which behavior was visible only after reading implementation details?
- Which convention or side effect was not signaled locally?
- What was the first moment you became uncertain?

Obscurity is strongest when the developer's reasonable first guess fails, not merely when they have not memorized the repository.

## Design red flags as explanatory hypotheses

Use these only after identifying an experienced symptom.

### Information leakage

The same design decision or internal representation is known in multiple places.

Experiential questions:

- Did the same rule need to be understood in more than one place?
- Which caller knew details that felt internal to another module?
- Could one representation have been derived from an authoritative one?

### Shallow boundary

The interface costs almost as much to learn as the work it hides.

Experiential questions:

- How many operations or call-order rules did you need for one goal?
- How far did you traverse before reaching code that made a decision?
- Which wrapper changed your understanding, and which merely redirected you?

Do not assume short modules are shallow or long modules are deep. Compare useful capability with interface burden.

### Mixed responsibility or abstraction level

A location combines concerns that change for different reasons, or adjacent layers express nearly the same abstraction.

Experiential questions:

- Did each layer simplify the problem in a different way?
- Which details belonged to a different concern than the requested behavior?
- Were policy, formatting, persistence, and orchestration distinguishable?

### Temporal decomposition

Code is divided by execution stage even though one decision spans those stages.

Experiential questions:

- Was one rule scattered across setup, processing, completion, and cleanup?
- Could you understand the behavior in one place, or only reconstruct it chronologically?

### Special-case accumulation

Exceptions, flags, modes, and fallbacks multiply combinations the developer must consider.

Experiential questions:

- Which branches were relevant to this change?
- Which branches had to be ruled out before you felt safe?
- Did any flag alter assumptions outside the place where it was checked?

### Misleading or vague naming

Names fail to support a correct first guess.

Experiential questions:

- What behavior did this name make you expect?
- Which two concepts were difficult to distinguish by name?
- Did the same word mean different things in different locations?

### Missing rationale

The code shows what happens but not a consequential constraint or reason.

Experiential questions:

- Which decision looked arbitrary until you found information elsewhere?
- What constraint could not be derived reasonably from the code?
- Did documentation explain the guarantee and rationale, or repeat syntax?

### Tactical residue

Repeated local fixes make the next change harder even though each patch once appeared expedient.

Experiential questions:

- Did you add another branch or representation because the existing structure offered no clear owner?
- Would the easiest patch increase the number of places involved next time?
- What small structural investment would remove repeated coordination?

## Confounders

Separate structural complexity from:

- unfamiliar language or framework syntax;
- missing domain requirements;
- broken environment or dependency setup;
- slow tools or tests;
- lack of repository access;
- unrelated dirty-worktree changes;
- a deliberately rare or adversarial task;
- developer fatigue, interruption, or accessibility needs;
- prior familiarity that makes a difficult structure feel easy through memorization.

Record confounders; do not “correct” a developer's rating mathematically. Explain which conclusions remain supported despite them.

## Question-selection rule

Ask the fewest questions that distinguish between plausible causes. Prefer one concrete follow-up over a general survey. A useful sequence is:

1. Overall difficulty.
2. First destination and why.
3. Greatest uncertainty or memory burden.
4. Late discovery or completeness evidence.
5. Verification source.
6. One counterfactual: what structural change would have helped most?

Skip questions already answered by the developer's narrative. Ask follow-ups when the rating, diff, and confidence conflict.
