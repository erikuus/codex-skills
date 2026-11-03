# Forms and optional behavior

These rules apply to Joyful form templates. Keep default form presentation intact and share the existing submission, validation and editor behavior across both themes.

## Shared width and field groups

The title/action/underline and body share one `mx-auto w-full min-w-0 max-w-xl` wrapper on standalone form pages. Put a body-only shared form partial inside it, not another width wrapper. Preserve form action/method, submit names, CSRF, IDs, required/readonly/disabled state and existing validation. Normal forms are spaced `space-y-6`; keep error summaries inside the outer column without negative margins.

For a titled field group, the heading remains at the outer edge and the body uses `space-y-6 xl:mx-6`: 24px per side at 1280px+, no extra inset below. Do not double-inset partials or already padded panels. Later source form headings may have a light top separator; this does not apply to titled read-only detail groups, which have no group separator lines or form-body inset.

Ordinary label: `mb-2 block text-base font-semibold leading-6 text-gray-800`. Ordinary input: `block w-full rounded border border-gray-200 px-4 py-3 text-gray-900 hover:border-gray-300 focus:border-gray-500 focus:outline-hidden focus:ring-2 focus:ring-green-300 sm:text-base sm:leading-6`, plus actual disabled/error states. Keep `<label for>` associations and error descriptions. File inputs, native selects and editor widgets may need their own structural styling; do not apply text-input classes indiscriminately.

Use the HTML specimen's **fixed-width wrappers** for compact controls: years `w-24`, centuries `w-20`, measurements `w-28` as starting points. Keep start/dash/end in `flex flex-nowrap items-center gap-2`, with distinct labels for endpoints; keep a measurement's input and nonwrapping unit in `inline-flex items-center gap-2`. Do not stretch them with `flex-1`. Adjust for actual signs/decimals/masks/maximum values. Preserve parser/input-type semantics. Check nested radio panels on phones; keep errors below the control row so they cannot displace the dash or unit. Remove conflicting inline/plugin width rules instead of layering contradictory utilities. Associate a unit using a unique `aria-describedby` ID, merging existing descriptions.

Radio groups use a fieldset/legend and vertically stacked native radio + inline-label rows. Circles 16px, approximately12px label gap; dependent fields below their option in `ml-8 mt-4 mb-8 space-y-4`. Keep label wrapping readable. Preserve the app's existing conditional-show and submission/disabled semantics: hiding a panel is not permission to disable its values. Inspect any script's sibling/selector contract before moving DOM nodes. Do not convert radios to cards or horizontal segmented buttons.

## Field tips and buttons

Existing field help, including bulb icons, becomes a filled circled-i 23px at the label row's right, above the control. Use the specimen's flex label row, gray-600 and 4px top/right offset. Help links keep their real URL, popup class, translated content and handler; tooltip-only help uses a non-submitting button tied to the existing content/tooltip. Provide keyboard/touch access. Do not widen a compact control, place help inside the input, or replace persistent inline guidance/errors with a popup. No empty decorative help icons.

Secondary buttons: white → preset gray-100 hover, dark text, gray-200 border, rounded 8px, normal form padding 12px×16px. Primary normal form buttons are dark with white text. Compact page-title Add buttons use the different 8px×12px padding and 13px text in the design reference. Preserve native submit versus cancel/link semantics. The specimen's sample form is not a real save implementation.

A single search field with Go and Cancel/Clear uses the shop pattern: rounded white one-row bar, growing input, active-query clear × and search magnifier. Keep Enter/icon submission, original route/query parameters and a functional clear URL (including a query value of `"0"`). Put it above the existing side menu and make it available above content on phones; do not create a sidebar solely for search. This does not reduce a genuine multi-field search to one field.

## Optional fading text

**Before collapsing any identified text, ask whether the user wants it collapsed on small screens and how many rendered lines should remain visible, including the final faded line.** Show which blocks/pages you propose and the breakpoint (source: below 1280px). Keep full text until both choices are confirmed. General design approval is not collapse approval. If the answer is full text, omit clipping/fade/toggle. When explaining the confirmation, link this section and quote its explicit requirement. Reuse a prior explicit choice for the same blocks/count.

VAU's enquiry intro uses a 96px clipped area, a background-colored bottom gradient, and a down/up chevron with “Näita rohkem”/“Näita vähem”; at 1280px+ it exposes all text. The yellow palette is page-specific. Its fixed 96px cap is **not a line-count promise**. Use the agreed count and actual typography; rich paragraphs/lists have margins and mixed line heights, so measure the rendered boundary or agree a preview height explicitly instead of guessing.

After approval, implement a scoped disclosure with the app's existing frontend tools:

```html
<!-- Only after approval; this example illustrates three 24px lines, not a default. -->
<div class="ra-text-preview" style="--preview-height: 4.5rem; --preview-surface: #fff;">
  <div class="relative">
    <div id="intro-text" class="ra-text-preview-content leading-6">Original full text remains here.</div>
    <div class="ra-text-preview-fade" aria-hidden="true"></div>
  </div>
  <button type="button" hidden aria-controls="intro-text" aria-expanded="false"
          class="mt-6 inline-flex items-center gap-2 rounded border border-gray-200 bg-white px-4 py-3 text-base font-medium text-gray-900 hover:bg-gray-100">
    <!-- Inline decorative chevron 20px and translated visible label. -->Näita rohkem
  </button>
</div>
```

```css
.ra-text-preview-fade { display: none; }
@media screen and (max-width: 1279.98px) {
  .ra-text-preview[data-collapsed="true"] .ra-text-preview-content {
    max-height: var(--preview-height); overflow: hidden;
  }
  .ra-text-preview[data-collapsed="true"] .ra-text-preview-fade {
    display: block; position: absolute; inset-inline: 0; bottom: 0;
    height: min(3rem, var(--preview-height)); pointer-events: none;
    background: linear-gradient(to top, var(--preview-surface), transparent);
  }
}
```

This is a markup/CSS recipe, **not a working toggle by itself**. Bind the real behavior before setting `data-collapsed`: measure overflow, expose the button only when needed below the breakpoint, toggle collapse state/`aria-expanded`, translated More/Less text and chevron, and recompute after fonts/content/container resize. Retain expanded text and hide the button at desktop sizes, for short content and in print. With no JS the data attribute is absent, full text stays visible and the button stays hidden. Each block has independent state and unique IDs. Match the actual composited background, not always white. Do not use ellipsis or modify stored content.

Keep full content accessible; if it contains focusable links, reveal a focused descendant instead of letting focus remain clipped. Keep focus on the toggle during normal activation. Do not hide the whole block with aria-hidden/inert. If animation is added, respect reduced motion; smooth height animation is optional. Test the approved line count and every state on the actual content, not just this specimen.
