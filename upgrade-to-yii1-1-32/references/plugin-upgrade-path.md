# Legacy frontend plugin upgrade path

Use this playbook for Select2, Fancybox, and similar legacy widgets during Yii 1.1.32 + jQuery upgrade.

## Policy

- Do not update all plugins in one batch.
- Do not auto-download unknown latest versions.
- Upgrade one plugin at a time behind existing Yii wrapper classes.

## Decision rule: should assets be downloaded/updated now?

Yes, if all are true:
1. Wrapper file(s) and call sites are inventoried.
2. Baseline behavior is captured.
3. Exact target version is chosen and pinned.
4. Plugin-specific test checklist exists.

No, if any of the above is missing.

## Select2 path

1. Inventory
- Wrapper: `protected/extensions/widgets/select2/XSelect2.php`
- Assets: `protected/extensions/widgets/select2/assets/*`
- View bindings for select2 events and value handling.

2. Compatibility pass
- Replace deprecated handlers in app code first (`.live()` etc.).
- Retest current Select2 behavior on upgraded jQuery.

3. Versioned upgrade
- Choose specific target Select2 version compatible with current jQuery window.
- Update wrapper internals for event API differences.
- Keep wrapper interface used by views stable.

4. Test checklist
- open dropdown
- search with keyboard
- select single/multiple
- clear value
- async data loading
- dependent field behavior

## Fancybox path

1. Inventory
- Wrapper: `protected/extensions/widgets/fancybox/*`
- Assets: `jquery.fancybox-1.3.4.*`
- View snippets that initialize Fancybox or rely on callbacks.

2. Compatibility pass
- Fix app-level jQuery deprecations first.
- Validate existing Fancybox behavior.

3. Versioned upgrade
- Choose exact target Fancybox version and pin it.
- Adapt wrapper/init options for changed API names.

4. Test checklist
- open and close modal
- image and iframe content
- keyboard navigation / ESC
- overlay click behavior
- focus/scroll lock behavior

## Recommended output in upgrade plans

For each plugin include:
- current version
- target version
- wrapper files
- risky API/event changes
- exact test cases
- fallback plan (temporary shim or rollback)
