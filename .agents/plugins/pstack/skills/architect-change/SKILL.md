---
name: architect-change
description: Design a change with a consequential interface, state-ownership decision, or migration boundary. Compare caller sketches and use a prototype or phased plan when evidence warrants it.
---

# Architect a change

Trace a representative caller through the current implementation and identify who owns the state. Establish the user-visible outcome, supported inputs, existing data and callers that must keep working. Express the design question as a decision someone could settle.

Sketch two materially different shapes if both are credible. Use the language of the repo: a PHP caller, SQL relation, Elixir message, external contract or UI event can express the design. Show the same realistic use in each sketch. Trace a read and a write where relevant. Explain what the caller must know, who can mutate state, and what happens across a failure, retry or compatibility boundary. If the existing interface already suffices, show that caller and stop expanding the design.

Choose the shape that best fits the evidence and name the tradeoff. If a material question is observable, use the [prototype playbook](references/prototype.md). For a migration with real dependencies use the [phased plan](references/phased-plan.md). A design-only request ends with the design and evidence. During authorized implementation, revisit the sketch if independent callers require the same workaround.
