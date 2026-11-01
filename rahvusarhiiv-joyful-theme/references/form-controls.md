# Form controls

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

## Field tips: info icon on the right of the label row

**Required whenever a legacy field has a tip/help affordance**, including a bulb image, `hint.png`, `XHtml::imageLink()`, a question-mark link, or a field-bound tooltip: use the `order/index?scope=clientDraft` “Koosta tellimus” pattern. Put a small filled-circle **i** on the far right of that field's label row, above the input. The label and required marker stay on the left. Remove the old icon/placement so there is only one help icon. This is field-local help; page-level Print/help actions still follow the title-row rule.

### Source geometry and markup

In VAU `themes/joyful/views/order/_form.php`, the `labels` (“Märksõnad”), `type` and `pricelist` fields render the help link **before** the block label. Its `float-right mt-1 mr-1 text-gray-600` classes place it on the right of the label line; the glyph is `fi-info text-xl`. With the institutional preset, this means gray `#5F6874`, a **23px** icon font size (`1.4375rem`, not stock Tailwind's `text-xl`), and 4px top/right margins. `XTActiveForm` labels use `mb-2 block text-base font-semibold leading-6 text-gray-800`. The full-width field follows below. Keep the icon out of the input, outside the label element, and away from the validation/error line.

A source-faithful help-link template is below. `$existingHelpUrl` must be the target field's existing route and parameters, and `$fieldHelpLabel` its translated accessible help label (preferably naming the field). Preserve any existing IDs, data attributes and event hooks in the link options as well.

```php
<div class="space-y-2">
    <?php echo CHtml::link(
        '<i class="fi-info text-xl" aria-hidden="true"></i>',
        $existingHelpUrl,
        array(
            'class'=>'openhelp float-right mt-1 mr-1 text-gray-600 focus-visible:ring-2 focus-visible:ring-green-300',
            'title'=>$fieldHelpLabel,
            'aria-label'=>$fieldHelpLabel,
        )
    ); ?>
    <?php echo $form->labelEx($model, $attribute); ?>
    <!-- Render the existing input/widget and persistent inline hint here. -->
    <?php echo $form->error($model, $attribute); ?>
</div>
```

Use `fi-info` only when the Foundation icon font is actually loaded. Otherwise use an equivalent filled-circle-i SVG, `aria-hidden="true"`, sized to `1.4375rem`; do not leave an invisible font glyph or retain the bulb. A flex label row is acceptable for long/wrapping labels if it preserves this geometry: label on the left, nonshrinking icon on the right, input on the next row spanning the same field width. On narrow screens neither the label nor its required marker may collide with the icon. Preserve the label's `for` association and a visible focus indicator on the separate help control.

### Preserve what the help control does

- VAU's screenshot icon is an **`openhelp` link**, not a hover-only tooltip. `themes/joyful/views/layouts/main.php` binds `a.openhelp` to `XFancyBox2` with AJAX content, padding 30 and no title. Preserve the target's real help URL/code, localization, content, visibility rules and popup handler; ensure that handler is available in Joyful. Do not substitute an empty `href="#"`, native `title` alone, or copy VAU's `order_tag` code into another app. Apply the existing [dialog close-control rules](dialog-close-buttons.md) to the popup.
- Concrete migration: Pitserid `protected/views/seal/_form.php` puts `XHtml::imageLink('hint.png', array('help/default/view','code'=>'hint_page_file'), ...)` after `page_file`. Replace that image with the circled-i control above the field, right of the label, retaining that relative route, `hint_page_file`, `openhelp`, and the input's binding/readonly/validation behavior.
- For an existing inline/hover tooltip rather than a help URL, keep its content and HTML/encoding policy and bind the existing tooltip to the new info control explicitly. Use a non-submitting `type="button"` trigger, with an accessible name and keyboard-focus/touch access to the same tip. Inspect the extension's selector/ID contract; do not assume adding `openhelp` converts tooltip content into a help page. VAU's separate `XTipsy` configuration for `client_comment` targets the input and does **not** implement the screenshot's info link. Preserve existing input-trigger behavior if needed while adding the required label-row affordance.
- Persistent inline guidance (for example “Separate keywords by commas”) and validation errors remain below their input; they are not replaced by the info icon. Do not invent help text or add empty help controls to fields without a tip.

## Verify the integrated form

Inspect actual rendered controls at desktop and narrow widths. For secondary buttons, measure white at rest and the preset's `rgb(232, 235, 240)` on hover, with unchanged dark text/border and visible keyboard focus. For radios, check stacked rows, label wrapping, 16px circles, indented dependent fields, validation errors, initial selection, label clicks and arrow-key changes. With two forms on a page, toggling one must not affect the other. Inspect submitted values and existing disabled fields; do not call the migration complete based only on class strings.

For every migrated field tip, compare the label row against the order-form reference at desktop and narrow widths: circled-i at the right above the field, correct size/color, no remaining bulb or duplicate trigger, no overlap with wrapped labels. Activate it by mouse, keyboard and touch; verify the original localized content/help route, popup close behavior or tooltip access, and that it does not submit the form. Confirm required markers, label-to-input focus, persistent hints and validation errors remain intact.
