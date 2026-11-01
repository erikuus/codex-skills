# Optional small-screen text disclosure

## Ask before collapsing text

**Do not apply this pattern automatically. Before hiding any text, ask the user whether the identified block should collapse on smaller screens and how many rendered text lines should remain visible.** General approval to apply Joyful is not approval to truncate content. Keep full text visible until the user confirms both choices; continue unrelated theme work while waiting. If they prefer full text, leave it fully visible and omit the fade/toggle. Reuse an explicit choice already given for the same blocks; do not ask again unnecessarily. The instruction to document this pattern is not approval to apply it to an app.

Identify the proposed pages/blocks first and ask, for example: “For the introductory text on [page], should smaller screens show the full text, or a fading preview with ‘Näita rohkem’? If a preview, how many lines should remain visible (including the final faded line)?” Name the proposed breakpoint (VAU uses below 1280px) and clarify whether the choice covers other blocks too. When explaining why confirmation is needed, link this reference and quote its explicit ask-before-collapsing requirement. Do not choose three lines merely because the screenshot happens to show three.

## VAU evidence and visual behavior

`/Users/erikuus/dev/php/vau/themes/joyful/views/enquiry/application/create.php` renders the intro in an Alpine `x-data="{ expanded: false }"` block:

- Collapsed wrapper: `relative overflow-hidden`, `max-h-24 xl:max-h-full`; expanded: `max-h-full`.
- Bottom overlay: `absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-yellow-50/60 to-transparent`, hidden when expanded and at `xl`.
- Button: `mt-6 flex items-center gap-x-2 rounded py-3 pl-3 pr-4 text-center text-base font-medium ... xl:hidden`, with a 20px down/up chevron and translated Show More/Show Less text (“Näita rohkem” / “Näita vähem”).
- `xl` in the institutional preset is 1280px. At/above it the complete text is visible and the toggle/fade disappear. Yellow panel/button colors belong to this particular page, not to the disclosure pattern.

The text itself is not recolored line by line: a bottom gradient makes it appear progressively lighter. Match the fade to the **actual composited background** of its panel; an opaque white overlay is suitable on white, but not on a tinted panel. Keep the overlay decorative and `pointer-events:none`. The source's `max-h-24` is a **96px height cap**, not a line-count contract. Do not copy it when the user has requested a particular number of visible lines. The source's `transition-max-height` is not a standard Tailwind utility; do not assume it supplies animation or that CSS can smoothly animate to unlimited height. A working instant toggle is sufficient.

## Example after explicit approval

This minimal example covers one text block with a uniform 24px line height and no paragraph/list margins. `$confirmedPreviewLines` is a positive integer from the user's answer, `$disclosureId` is unique on the page, and `$existingText` is the original plain text. Keep the app's existing HTML sanitization/rendering for rich text instead of encoding it as plain text; see the rich-text guidance below. Load the app's existing Alpine once; do not add a second copy. Put CSS in the theme build source, and bind behavior only after initialization so no-JavaScript rendering remains complete.

```php
<div class="joyful-disclosure"
     style="--preview-lines: <?php echo (int)$confirmedPreviewLines; ?>; --preview-surface: #fff;"
     x-data="{ expanded: false, ready: false, overflows: false, mobile: false,
       measure() {
         this.mobile = window.innerWidth < 1280;
         const text = this.$refs.text;
         const lines = parseInt(getComputedStyle(this.$el).getPropertyValue('--preview-lines'), 10);
         const cap = lines * parseFloat(getComputedStyle(text).lineHeight);
         this.overflows = text.scrollHeight > cap + 1;
         this.ready = true;
       }
     }"
     x-init="$nextTick(() => { measure(); if (document.fonts) document.fonts.ready.then(() => measure()); })"
     @resize.window.debounce.100ms="measure()"
     :data-collapsed="ready && overflows && !expanded ? 'true' : 'false'">
    <div class="relative">
        <div x-ref="text" class="joyful-disclosure-text text-base leading-6 text-gray-700"
             id="<?php echo CHtml::encode($disclosureId); ?>"
             @focusin="expanded = true"><?php echo CHtml::encode($existingText); ?></div>
        <div class="joyful-disclosure-fade" aria-hidden="true"></div>
    </div>
    <button type="button" x-cloak x-show="ready && overflows && mobile"
            @click="expanded = !expanded"
            :aria-expanded="expanded ? 'true' : 'false'"
            aria-controls="<?php echo CHtml::encode($disclosureId); ?>"
            class="mt-6 inline-flex items-center gap-x-2 rounded border border-gray-200 bg-white py-3 pl-3 pr-4 text-base font-medium text-gray-900 hover:bg-gray-100 focus-visible:ring-2 focus-visible:ring-green-300 print:hidden">
        <svg class="h-5 w-5 shrink-0" :class="expanded ? 'rotate-180' : ''"
             viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
        </svg>
        <span x-show="!expanded"><?php echo CHtml::encode(Yii::t('ui', 'Show More')); ?></span>
        <span x-show="expanded"><?php echo CHtml::encode(Yii::t('ui', 'Show Less')); ?></span>
    </button>
</div>
```

```css
/* In the compiled theme source. [x-cloak] is already provided by the baseline. */
.joyful-disclosure-text { overflow: visible; }
.joyful-disclosure-fade { display: none; }
@media screen and (max-width: 1279.98px) {
  .joyful-disclosure[data-collapsed="true"] .joyful-disclosure-text {
    max-height: calc(var(--preview-lines) * 1.5rem);
    overflow: hidden;
  }
  .joyful-disclosure[data-collapsed="true"] .joyful-disclosure-fade {
    display: block;
    position: absolute;
    inset-inline: 0;
    bottom: 0;
    height: min(3rem, calc(var(--preview-lines) * 1.5rem));
    background: linear-gradient(to top, var(--preview-surface), transparent);
    pointer-events: none;
  }
}
```

Here the final one or two lines fade into the white surface; the button follows with VAU's 24px gap. Use the standard secondary white-to-gray button on a neutral page; preserve a justified page-specific palette when present. The confirmed preview includes the faded lines. If the user wants N **fully readable** lines plus a faded continuation, clarify and implement that different height deliberately.

For rich paragraphs, lists, headings or changing content, line height multiplied by N is not enough: block margins and mixed typography also occupy height. Preserve the original markup and measure the agreed rendered-line boundary (including intervening spacing), or agree a preview height with the user instead. Do not silently replace their requested line count with `max-h-24`, truncate stored text, remove paragraphs, or strip links. Recalculate overflow after fonts/content changes and container resize (use a scoped ResizeObserver when window resize is insufficient); hide the toggle and fade if all content fits. Keep each block's state, IDs and measurements independent. Put literal Tailwind class names in scanned sources, not interpolated `max-h-${n}` strings.

Keep all text present in the DOM and accessible. For linked/interactive content, expanding on `focusin` must reveal a focused descendant before it is used; verify keyboard navigation never leaves focus hidden in the clipped area. Do not add `aria-hidden` or `inert` to the whole content block. Use a non-submitting button with `aria-expanded`/`aria-controls`, translated visible text and a decorative chevron. Keep focus on the toggle during expand/collapse. Print and no-JavaScript views show the complete text without fade/toggle. If adding animation, respect reduced-motion preferences and verify both directions.

## Acceptance

Record which blocks and line count the user approved. Before approval or after a full-text choice, verify no new clipping is applied. After approval, check the confirmed preview at phone/tablet widths, actual fade color, long and short content, localized labels, font loading, expand/collapse, keyboard/touch, form non-submission, independent blocks, and resizing through 1280px. Desktop, print and JavaScript-disabled rendering must expose the complete text. Rebuild CSS and compare against VAU's disclosure behavior without importing its yellow page palette by default.
