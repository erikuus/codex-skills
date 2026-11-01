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

## Grouped forms: inset fields below an outdented heading

First apply the [shared page-title/form width rule](patterns.md#form-pages-title-and-body-share-one-width). The group-body inset below is inside that outer form column; it does not define the page title’s width.

**When a form has titled field groups, keep each group heading at the form's outer left edge and inset the group's field body on large screens.** Follow VAU `themes/joyful/views/enquiry/application/_form.php`, used by `enquiry/application/create`: the “Application content” / “Päringu sisu” heading precedes `<section class="space-y-6 pb-6 xl:mx-6">`, which renders `forms/_work.php` and other form partials. Applicant Data and Applicant Preferences use `space-y-6 xl:mx-6` too. The heading stands out because the **fields move inward**, not because the heading itself is indented.

- Use **`xl:mx-6` on one field-body wrapper per group**: 24px on both sides at the preset's `xl` breakpoint (1280px), with no extra group inset below that breakpoint. Keep the heading outside that wrapper. All ordinary labels, inputs, field-help rows and errors share the inset; do not shift only the input or add margins again inside a rendered partial.
- Preserve `space-y-6` (24px) between field blocks and the form's 24px heading-to-body gap. Group headings use `text-lg font-medium`, with semantic heading levels appropriate to the page, or a fieldset/legend where suitable. The example assumes the parent form already has `space-y-6`.
- VAU's later form headings additionally use `pt-6 border-t border-gray-50`; its first heading has no separator. Preserve this distinction when matching a form that uses it. The required hierarchy is the heading/body inset; do not add dividing lines to titled **detail views**, which retain the separate no-separators rule.
- Do not duplicate the inset around an already padded group panel (VAU's company group instead has `rounded p-6 bg-gray-50/60`). Preserve intentional panels and keep dynamic-radio indentation relative to the group body, without altering the helper's input/panel sibling contract.

```php
<h2 class="text-lg font-medium">
    <?php echo CHtml::encode($existingGroupTitle); ?>
</h2>
<section class="space-y-6 xl:mx-6">
    <div>
        <?php echo $form->labelEx($model, $attribute); ?>
        <?php echo $form->textField($model, $attribute); ?>
        <?php echo $form->error($model, $attribute); ?>
    </div>
    <!-- Other existing fields/partials in this group; no second group inset. -->
</section>
```

## Compact fields: ranges and measurements

**Full width is the default for ordinary text fields, not for every input.** Retain meaningful compact relationships from the legacy form: `[start year/century] – [end year/century]` stays on one line, and a measurement stays `[value] mm` or `[value] cm` with its unit immediately after the input on the same line. Do not stretch either range endpoint or a measurement across the form, distribute endpoints to opposite edges, stack endpoints at ordinary phone widths, or push the unit to the far edge/below the field.

Pitserid `protected/views/seal/_form.php` provides concrete cases: `datum_year_start`/`datum_year_end` use `size=>4`, century endpoints use `size=>2`, and `shape_x`/`shape_y` are followed by `mm`. These legacy sizes signal compact intent; do not discard that intent when removing old pixel/size attributes. The examples below are adaptations for these cases, not claims that VAU's enquiry form has these controls.

### Width and helper contract

For skinned inputs such as `CMaskedTextField` and `CJuiDatePicker`, inspect the emitted wrapper/input before applying compact sizing. The masked-field skin supplies `w-full`; the default datepicker skin also supplies `sm:w-32`, which can override a smaller wrapper’s intended width. When a caller needs a different compact width, replace that input’s conflicting width tokens while retaining the other skin classes and functional widget options. Explicit `htmlOptions` classes can replace skin classes through Yii’s merge; do not accidentally discard the border, padding and focus design. Keep the existing date format and mask.

`XTActiveForm::textField()` **appends** its `fieldCssClass`, including `block w-full`, even when `htmlOptions['class']` is supplied. Adding `w-24 inline-block` on the same input creates conflicting utilities; HTML class order does not resolve this. Prefer an explicitly sized wrapper with the ordinary full-width input inside it. Keep shared widget defaults unchanged.

Useful starting widths (adjust to actual allowed values and typography): years `w-24` (6rem/96px), centuries `w-20` (5rem/80px), measurements `w-28` (7rem/112px). These are fixed, content-appropriate control widths, not percentages or `flex-1`. Check maximum permitted values, signs, decimals and any select arrow/mask with the normal input padding; enlarge the wrapper when necessary. Do not narrow widths blindly to the digit count or rely on `size` against `w-full`. Keep widths as literal Tailwind utilities so the build detects them.

### Range example: two compact endpoints and a separator

Put both inputs and the separator in one `flex flex-nowrap items-center gap-2` row. Give each endpoint an accessible start/end label; a shared group title alone cannot distinguish them. Keep validation messages below the control row so they do not displace the dash or the other input. In an existing radio-dependent area, put this markup **inside its content panel**, preserving the dynamic helper's outer structure and visibility/submission behavior.

```php
<fieldset class="m-0 min-w-0 border-0 p-0">
    <legend class="mb-2 text-base font-semibold leading-6 text-gray-800">
        <?php echo CHtml::encode($existingRangeTitle); ?>
    </legend>
    <div class="flex flex-nowrap items-center gap-2">
        <div class="w-24 shrink-0">
            <?php echo CHtml::activeLabel($model, 'datum_year_start', array('class'=>'sr-only')); ?>
            <?php echo $form->textField($model, 'datum_year_start'); ?>
        </div>
        <span class="shrink-0 text-gray-700" aria-hidden="true">–</span>
        <div class="w-24 shrink-0">
            <?php echo CHtml::activeLabel($model, 'datum_year_end', array('class'=>'sr-only')); ?>
            <?php echo $form->textField($model, 'datum_year_end'); ?>
        </div>
    </div>
    <?php echo $form->error($model, 'datum_year_start'); ?>
    <?php echo $form->error($model, 'datum_year_end'); ?>
</fieldset>
```

For century ranges substitute the existing century attributes and `w-20` wrappers. Use the target's actual translated start/end labels (supply explicit label text if its model labels do not distinguish endpoints), required indicators and existing field options. At phone widths, retain the single compact row; check its total width within any radio indentation. If a genuinely narrower container cannot fit it, adapt widths within readable limits or wrap the pair as a whole within its parent. Do not introduce page overflow or orphan the dash. Do not change input types, date masks, numeric parsing, validation, allowed values or hidden/disabled behavior as a styling shortcut.

### Measurement example: compact input with adjacent unit

Use an `inline-flex items-center gap-2` row around a fixed-width input wrapper and nonwrapping unit text. Render the existing field label above the row and its error below it. Associate the unit text with the input via `aria-describedby`, merging any existing description/error IDs rather than replacing them. The example's ID must be unique per rendered form.

```php
<?php $unitId=CHtml::activeId($model, 'shape_x').'-unit'; ?>
<div>
    <?php echo $form->labelEx($model, 'shape_x'); ?>
    <div class="inline-flex items-center gap-2">
        <div class="w-28 shrink-0">
            <?php echo $form->textField($model, 'shape_x', array('aria-describedby'=>$unitId)); ?>
        </div>
        <span id="<?php echo CHtml::encode($unitId); ?>" class="shrink-0 whitespace-nowrap text-gray-700">mm</span>
    </div>
    <?php echo $form->error($model, 'shape_x'); ?>
</div>
```

Retain the target's actual unit (`mm`, `cm`, etc.), its localization policy and stored-value semantics; never infer a conversion from the design. Use the same pattern for each relevant dimension. Existing field-tip icons still belong to the label row above, not between the input and unit.

## Field tips: info icon on the right of the label row

**Required whenever a legacy field has a tip/help affordance**, including a bulb image, `hint.png`, `XHtml::imageLink()`, a question-mark link, or a field-bound tooltip: use the `order/index?scope=clientDraft` “Koosta tellimus” pattern. Put a small filled-circle **i** on the far right of that field's label row, above the input. The label and required marker stay on the left. Remove the old icon/placement so there is only one help icon. This is field-local help; page-level Print/help actions still follow the title-row rule.

### Source geometry and markup

In VAU `themes/joyful/views/order/_form.php`, the `labels` (“Märksõnad”), `type` and `pricelist` fields render the help link **before** the block label. Its `float-right mt-1 mr-1 text-gray-600` classes place it on the right of the label line; the glyph is `fi-info text-xl`. With the institutional preset, this means gray `#5F6874`, a **23px** icon font size (`1.4375rem`, not stock Tailwind's `text-xl`), and 4px top/right margins. `XTActiveForm` labels use `mb-2 block text-base font-semibold leading-6 text-gray-800`. The control follows below: ordinary fields are full width, while ranges and measurements retain the compact layout specified above. Adding a field tip must not widen a compact control. Keep the icon out of the input, outside the label element, and away from the validation/error line.

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

For grouped forms, compare a viewport below 1280px and one at/above it: heading at the outer edge, group body inset 24px on each side only at `xl`, with no double indentation. For range and measurement controls, check real maximum-length values, normal and validation-error states, and phone widths including indented radio panels: both endpoints and dash stay together, units remain adjacent to compact inputs, labels/units are accessible, and no horizontal overflow or change in submitted values occurs. Rebuild CSS and inspect actual computed widths; class-string assertions alone are insufficient.
