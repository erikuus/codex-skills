---
name: rahvusarhiiv-design-system
description: Build or adapt responsive Rahvusarhiiv interfaces using the institutional design system recovered from tailwindui-playground. Use for Rahvusarhiiv app shells, layouts, forms, navigation, data views, and content pages, in automatic or human-guided mode. Preserve the target app's domain and technology; do not recreate VAU branding or workflows by default.
---

# Rahvusarhiiv design system

Reproduce the quiet institutional interface: gray page canvas, layered white surfaces, restrained pastel header gradient, Roboto body, Raleway page headings, dark primary buttons, blue links, green interaction accents, and carefully staged responsive layouts.

This is a reusable system inferred from the templates, not an official replacement for institutional brand guidance. Component names below are proposed extraction boundaries. Exact values and original behavior are evidence; accessibility repairs and defaults are explicitly identified as adaptations.

## Choose the working mode

- **Automatic** (default unless the user asks to choose): infer choices from the task and existing app, record a short decision summary, then implement. Do not turn the guided questionnaire into a prerequisite. Preserve choices already supplied.
- **Human-guided**: start with the three shell choices in [decisions.md](references/decisions.md): horizontal/mobile navigation, standard Rahvusarhiiv/custom footer, and header gradient. Give concrete alternatives and a recommendation. Ask subsequent layout/content questions only when they affect the requested screen. Wait for answers to required choices while inspecting the app and preparing independent work.
- A request to switch modes applies immediately. Carry previous answers forward. Never silently replace an explicit choice with the automatic default.

Both modes use the same components, tokens, assets, responsiveness, and validation. Guidance changes who makes decisions, not the quality of the result.

## Implementation workflow

1. Inspect the target project's instructions, stack, existing shell, routes, assets, and content needs. Use the existing component conventions. Do not migrate its framework just to use this skill.
2. Read [foundations.md](references/foundations.md) and [layouts.md](references/layouts.md). Select the shell and a content structure by information density and relationships, not by source template filename.
3. Use [composition.md](references/composition.md) to distinguish information shapes and place the title in its owning region. Read the relevant families in [components.md](references/components.md) and [interactions.md](references/interactions.md). Build only those needed by the request. The asset recipes are starting points; wire them to actual app data and behavior.
4. Keep responsive classes/media rules inside their owning component. Give callers content, items, actions, and a small number of meaningful variants. Do not ask each page to supply breakpoint classes.
5. Build the requested screen or app. For a multi-screen task, implement and visually check one representative of each required family before expanding it across the batch. Reuse the supplied CSS/recipes when applicable; when translating them, preserve their exact tokens and breakpoint behavior. Use [composer.md](references/composer.md) when a standalone runnable starting page helps; otherwise translate the contracts into the existing stack. The composer is optional and does not implement every family or business workflow.
6. Validate the resulting interface using [validation.md](references/validation.md). Render it; exercise relevant controls; report unresolved integration gaps honestly.

## Boundaries that matter

- `AppShell` owns the institutional top strip, configurable generic app header, navigation drawer, content surface, and shared white footer card. Standard and customized footers always use the same rounded white card, shadow, responsive margins, and inner frame; only the content inside changes. `InstitutionalFooter` remains a complete reusable unit with its links, contact details, social icons, and feedback behavior.
- `ContentContainer` owns outer gutters, vertical spacing, and width profile (`narrow`, `medium`, `full`; add the documented specialist profiles only when justified).
- `PageTitle` owns heading, divider, spacing, and optional actions. Actions may be buttons or quiet links; both can keep their icons while visually hiding labels below 640px. Accessible names remain available.
- `SplitLayout` owns its two related content slots, collapse point, gap schedule, and optional sticky first region. A sidebar workspace is a different composition with nested field reflow; do not force it into equal columns.
- `ArticleLayout` owns section navigation, article content, table of contents, scroll tracking, and alternate phone/tablet navigation. Keep these together; do not export a free-floating TOC that callers must synchronize.
- `DataCollection` supports read-only record rows and interactive collections; `LineItemTable` preserves repeated items, aligned numeric columns and a separate total. A label/value `DetailSummary` describes one entity, not a substitute for either table.
- `DataCollection` owns toolbar, selection, optional filter/bulk panels, responsive rows, row actions, and pagination as one coherent surface. Smaller internal components are fine, but pages must not rebuild its responsive data relocation.
- `Field`, `Action`, `Notice`, `Disclosure`, `ChoiceGroup`, `FileCollection`, `StepProgress`, `ContentList`, `MediaDetail`, and `DetailSummary` are shared families where evidence supports reuse. Use slots/composition for content; do not create `NewsList`, `OrderTable`, `AccessForm`, or other source-domain components in the shared system.

Do not create a wrapper for every div, a separate component per breakpoint, or a giant component with dozens of unrelated flags. Split a family when its state, information structure, or responsive contract differs; merge variants that differ only in content or presentation.

## Evidence and portable assets

- [Source map](references/source-map.md): the active included templates, their role and selection rationale. Honor its manifest exclusions; excluded templates are not design authorities or recipes, even if they remain in the repository.
- [tokens.json](assets/tokens.json): serializable values extracted from the preset. [rahvusarhiiv.preset.cjs](assets/rahvusarhiiv.preset.cjs) preserves the original typography function and Tailwind configuration values.
- [style.css](assets/style.css): a compiled foundation/utility snapshot with excluded legacy widget skins removed. It makes the bundled recipes runnable without a build. It is a finite snapshot, not a compiler for new utility classes.
- [Base CSS](assets/base.css), local fonts, and `ra_logo.svg`: reusable foundations. The institutional mark is distinct from the app's own logo.
- [Runnable pattern gallery](assets/examples/patterns.html): neutral line items, detail variants, complete progress, form actions, title actions and workspace placement; uses [patterns.css](assets/patterns.css) with the bundled foundation/starter CSS. Inspect relevant patterns before implementing these families. This gallery is a component reference, not a page template or business runtime.
- [Recipes](references/components.md#recipe-files): neutral HTML fragments with responsive ownership. No original user records, model field names, session values, product prices, or form endpoints belong in generated apps.
- [Footer card](assets/starter/footer.html) wraps both standard and customized content. [Standard footer content](assets/fragments/footer-standard.html) preserves the institutional links, functional feedback link, and accessibility repairs.

Use `views/layouts/advanced-layout-alt.html` as the canonical shell: the mobile menu trigger belongs in the narrow institutional top strip, beside the optional language switch. `advanced-layout.html` is the nonpreferred comparison variant, with its trigger in the app header. Never derive the shell from `views/layouts/vau-layout.html` or copy the VAU header from included page templates; use only their content patterns.

## Completion

Deliver the implementation, the important automatic decisions or human selections, what was exercised at which widths, and any remaining integrations. Do not describe mock filtering, static pagination, upload decoration, payment links, or copied plugin markup as working functionality.
