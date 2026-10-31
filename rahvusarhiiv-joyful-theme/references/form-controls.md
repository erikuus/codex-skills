# Secondary buttons and radio groups

## Secondary buttons: white to gray on hover

The reference is VAU's Cancel action in `themes/joyful/views/bookmark/link/_form.php` and the shared `XTHtml::$buttonLinkCssClass` in `extensions-1.1.8/components/tailwind/XTHtml.php`. The bundled upgraded XTHtml already preserves this style.

| State/property | Required style |
| --- | --- |
| Resting background | `bg-white`: `#FFFFFF` |
| Hover background | **`hover:bg-gray-100`: `#E8EBF0`** from the Rahvusarhiiv preset |
| Text | `text-gray-900`, retained on hover |
| Border | `border border-gray-200`, retained on hover |
| Shape/spacing | `rounded py-3 px-4 text-center text-base font-medium` |
| Keyboard focus | `focus-visible:ring-2 focus-visible:ring-green-300` |

This is a required **white → light gray** background transition, not a dark/green fill, text-only color change, or an unchanged white hover state. Use the preset token, not Tailwind's stock gray hex value. Keep native disabled and action behavior. Touch devices need no persistent simulated hover; check the hover state on a hover-capable pointer, since Tailwind 4 gates hover rules by device capability.

For a navigation Cancel link, use `XTHtml::buttonLink($label,$existingReturnUrl,...)`. The complete secondary class string is:

```text
focus-visible:ring-2 focus-visible:ring-green-300 cursor-pointer border border-gray-200 rounded bg-white py-3 px-4 text-center text-base font-medium text-gray-900 hover:bg-gray-100
```

For a real secondary button, preserve its button type and handler and apply this same style without primary defaults, for example through `CHtml::button()` or `CHtml::htmlButton()` with explicit options. The bundled `XTHtml::button()`/`submitButton()`/`htmlButton()` add **primary** classes (`bg-gray-900 text-white hover:bg-gray-700`); appending secondary classes to them leaves conflicting utilities. Do not assume the last class in the HTML wins. Remove conflicting primary/legacy rules instead of layering more background classes or broad `a:hover` overrides.

Keep the target's return URL, click/confirmation behavior and form semantics. The Cancel button is still needed on forms even when breadcrumbs eliminate a separate standalone Back button.

## Radio groups: bookmark/link/update pattern

`themes/joyful/views/bookmark/link/update.php` renders `_form.php`. Its Collection group offers existing/new collection choices, with a dropdown or text field under the selected option. Reuse its **vertical choice-and-dependent-panel layout** for similar groups, preserving the target's own choices and fields.

- Group wrapper: `space-y-2`; group title `font-semibold` with the existing required marker. Prefer a semantic `fieldset`/`legend` to the source's generic div heading, keeping the same visual rhythm and resetting unintended fieldset borders/padding. Give the legend a clear gap before the choices.
- Put **each radio and its associated inline label on one choice row**, with rows stacked vertically. Keep the radio before its label; do not render a full-width block label above each radio, squeeze the choices into a horizontal strip, or turn them into cards/segmented buttons.
- The source radio uses `h-4 w-4 -mt-0.5 mr-3`: a 16px circle, 12px right gap and a small baseline adjustment. It uses `text-green-500 border-gray-200 hover:border-gray-300 focus:border-gray-500 focus:ring-offset-0 focus:ring-2 focus:ring-green-300`. Preserve the native checked state, label association and keyboard behavior. Do not apply the text-field `block w-full px-4 py-3` style or the form's block `labelEx` style to individual radio labels.
- Each dependent panel sits **below its own choice**, using `ml-8 mt-4 mb-8 space-y-4`: 32px left indentation, 16px top gap, 32px bottom gap, and 16px spacing between its fields. Keep the inner controls full-width within that indented space and validation errors beside their corresponding fields. Avoid another left margin on the field itself.
- Keep the same vertical hierarchy on phones. Let long labels wrap readably; prevent a wrapped label or wide child input from overlapping the radio or overflowing the form. Plain radio groups without dependent fields use the same stacked choice rows but do not acquire empty panels or their large bottom gaps.

### Preserve the dynamic helper's DOM contract

For a group with conditional fields, explicitly set `enableRadioToggle=>true` on `XTActiveForm` (its default is false). The source obtains keyed option markup through `explodeRadioButtonList($model,$attribute,$options)`, then uses:

```php
<?php $form->beginDynamicArea($radio[$optionValue], array(), array(
    'class'=>'ml-8 mt-4 mb-8 space-y-4',
)); ?>
    <!-- Render this option's existing fields and validation messages here. -->
<?php $form->endDynamicArea(); ?>
```

`beginDynamicArea()` renders the radio input and label followed by the content div **inside one option container**. The bundled `joyfulToggle` finds the panel among the input's siblings. Keep that relationship: wrapping just the input/label in an extra flex div, moving the panel outside the option container, breaks the existing toggle behavior. Do not add competing `display: none !important` or `visibility: hidden` rules that keep the selected panel invisible. Use the helper's container/content options and inspect the actual DOM when adapting wrapping/alignment. Group-level fieldset/legend markup can surround the option containers without changing this relationship.

Preserve model names, option values/order, unique IDs, selected/default state, hidden uncheck values, readonly/disabled behavior, validators and target-specific callbacks. Selection must show the right panel on initial render and after mouse or keyboard changes. **Radio toggles preserve the source's visibility-only behavior**: they do not disable hidden panel fields. Do not silently apply the dropdown helper's disabling semantics to radios or change submitted values while restyling them. If the target already has different conditional submission behavior, preserve it deliberately.

## Verify the integrated form

Inspect actual rendered controls at desktop and narrow widths. For secondary buttons, measure white at rest and the preset's `rgb(232, 235, 240)` on hover, with unchanged dark text/border and visible keyboard focus. For radios, check stacked rows, label wrapping, 16px circles, indented dependent fields, validation errors, initial selection, label clicks and arrow-key changes. With two forms on a page, toggling one must not affect the other. Inspect submitted values and existing disabled fields; do not call the migration complete based only on class strings.
