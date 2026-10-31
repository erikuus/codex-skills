# Layout, breadcrumbs and exact footer

The authoritative shell is `/Users/erikuus/Documents/Github/tailwindui-playground/views/layouts/advanced-layout-alt.html`; a [byte-for-byte snapshot](../assets/reference/advanced-layout-alt.html) and [source CSS](../assets/reference/advanced-layout-alt.css) are bundled. Use its actual utility markup and the institutional preset, not a CSS reconstruction that merely has the same heights. Reference snapshots are not staged into the target app.

## Shell structure

1. Body: `flex min-h-screen flex-col bg-gray-50`.
2. First white surface: `flex grow flex-col rounded-b bg-white shadow-md lg:m-2 lg:rounded`.
3. Upper institutional header: `flex h-12 flex-wrap content-center`; RA mark `h-7 opacity-70`; language control and mobile opener on the right.
4. Nested gradient surface: `bg-theme-vau flex grow flex-col rounded`. It contains the 128px application header, optional breadcrumb strip, and third white surface.
5. Application header: `relative flex h-32 flex-wrap content-center z-0`. Target logo `h-11 sm:h-12` (app-name fallback when no logo), desktop menu groups, then account control. Desktop nav `hidden lg:flex lg:gap-x-4 xl:gap-x-8 2xl:gap-x-12 font-medium`; links `py-1.5 px-4 rounded hover:backdrop-brightness-105`. Use the target's real menu grouping and permissions; no invented items.
6. Third white surface: `flex grow flex-col rounded rounded-b bg-white shadow-md`. Main container `2xl:max-w-xxl mx-auto flex w-full max-w-7xl px-4 py-6 md:px-6 lg:px-8 xl:py-10`; inner content `w-full min-w-0`.
7. Fourth white surface/footer: exact source subtree, a sibling of the first white surface, not part of the main content or gradient.

The horizontal container is 80rem, increasing to 90rem at 1536px, with 16/24/32px horizontal padding. Preserve the custom 8px radius and multi-layer shadows from the preset. Sidebars belong inside main content only where the target already has that layout. Do not add a sidebar or narrow the page just because another application has one. Avoid double padding or double nested main layouts.

## Login button

A guest Login control must include the **same account-circle SVG as VAU**, immediately before the translated Login label. The source is `/Users/erikuus/dev/php/vau/themes/joyful/views/AccountMenu/loginButton.php`:

- Icon: account/person inside a circle, `viewBox="0 0 20 20"`, `fill="currentColor"`, `mr-1.5 h-3 w-3 text-white` (12×12px with 6px gap at the reference root size). Add `aria-hidden="true"` to the decorative SVG. Do not substitute an arrow, omit the icon, or turn Login into an icon-only control.
- Link: `inline-flex cursor-pointer items-center rounded bg-gray-900 py-2 pl-3 pr-4 text-center text-sm font-medium text-white hover:bg-gray-700`. Correct the source's typo to `focus-visible:ring-2 focus-visible:ring-green-300` and retain visible keyboard focus.
- Position: the account/sign-in slot in the application header. Keep the target's existing login URL, return URL, authentication/guest visibility and event hooks. Preserve an existing ID when used by scripts; do not blindly impose VAU's `AccountMenu_login` on another app. The source wrapper `flex justify-end w-24` is only suitable if the target's translated label fits.

The exact source glyph, for use inside the link (label remains outside the SVG):

```html
<svg class="mr-1.5 h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 0C4.48 0 0 4.48 0 10C0 15.52 4.48 20 10 20C15.52 20 20 15.52 20 10C20 4.48 15.52 0 10 0ZM5.07 16.28C5.5 15.38 8.12 14.5 10 14.5C11.88 14.5 14.51 15.38 14.93 16.28C13.57 17.36 11.86 18 10 18C8.14 18 6.43 17.36 5.07 16.28ZM16.36 14.83C14.93 13.09 11.46 12.5 10 12.5C8.54 12.5 5.07 13.09 3.64 14.83C2.62 13.49 2 11.82 2 10C2 5.59 5.59 2 10 2C14.41 2 18 5.59 18 10C18 11.82 17.38 13.49 16.36 14.83ZM10 4C8.06 4 6.5 5.56 6.5 7.5C6.5 9.44 8.06 11 10 11C11.94 11 13.5 9.44 13.5 7.5C13.5 5.56 11.94 4 10 4ZM10 9C9.17 9 8.5 8.33 8.5 7.5C8.5 6.67 9.17 6 10 6C10.83 6 11.5 6.67 11.5 7.5C11.5 8.33 10.83 9 10 9Z" />
</svg>
```

## Top-right utility icons

If the target has `XVauBookmark` and/or `XVauHelpdesk`, place each available enabled widget as icons in the **right-hand utility group of the first, 48px institutional header**, opposite the RA mark. This is the position occupied by the language picker in VAU's main template, not the account area in the 128px application header. Keep an actual language picker and the mobile opener in that same group when the app uses them; do not invent a language control. Make the utility icons available on narrow screens without overlapping the RA mark or mobile opener.

Use the existing `ext.widgets.vau.*` implementations from the target's resolved extension root. Preserve feature flags/`visible`, `lang`, titles, permissions, `addTag`/`listTag`, `addUrl`, `removeParam`, helpdesk `subject`/`devUrl`, URL parameters and popup behavior. Move an existing header instance instead of rendering duplicate instances. Availability does not override a disabled feature flag. Do not install or invent these services for an app that lacks them.

- Bookmark: supply trusted SVG markup through `addLabel` and `listLabel`; retain distinct “bookmark this page” and “open bookmarks” actions when enabled, not one ambiguous bookmark icon. The inspected class generates its own anchors with `.vauBookmark` and does **not** expose `htmlOptions`. Include translated `sr-only` labels in each icon label, retain `addTitle`/`listTitle`, and style its generated anchors through a narrowly scoped header wrapper if necessary. Do not nest new links/buttons inside its labels or pass unsupported properties.
- Helpdesk: supply its feedback/mail SVG through `label`; this class does support `htmlOptions` for the anchor class and accessible name. Keep `.vauHelpdesk`, which its implementation appends, and the original generated URL/click behavior.
- Use consistent 20px (`w-5 h-5`) decorative SVGs, inline-flex centered controls, spacing and the reference's rounded/gray hover treatment. Preserve visible keyboard focus and understandable accessible names; do not rely on old Foundation icon fonts or tiny GIF fallbacks when rendering the new icon labels.

Inspect the actual widget version: the original extensions-1.1.8 bookmark uses removed jQuery `.live()`, whereas upgraded Pitserid copies use delegated `.on()`. If the target still has the old handler, modernize it in the **extension implementation**, preserving popup options and binding once; do not add a second competing click handler in the layout. Verify that a click opens exactly one expected popup. Both widgets must remain functional, not decorative links rebuilt from guessed service URLs.

This header placement is a user-requested adaptation. The mandated exact footer, including its original Tagasiside button, remains unchanged even when the header has a helpdesk icon.

## Breadcrumbs: integrate the concrete VAU pattern

`advanced-layout-alt.html` intentionally has no breadcrumbs. For existing target breadcrumbs, use the source pattern in VAU `themes/joyful/views/layouts/main.php` and playground `views/pages/vau-bookmark-list.html`, not a generic plain breadcrumb row.

Insert one `nav` with `-mt-6 flex` on the gradient, after the application header and before the white content surface. It uses the same responsive horizontal container. The bundled `CBreadcrumbs` skin supplies:

- `my-4 flex items-center rounded border-none text-sm backdrop-brightness-105` list;
- white rounded home-icon anchor with `p-2`, `ring-4 ring-white`, `my-1 mr-4`, green hover;
- SVG chevron separators, source label padding/type, and `aria-current` on the current item;
- encoded labels/URLs from current Yii and one interactive anchor per link (fixing the source's invalid nested button/anchor).

**A page with breadcrumbs must not also render a standalone Back button.** Remove that redundant view/toolbar action and an empty action-row wrapper, while retaining form Cancel, dialog Close and workflow Previous controls with distinct behavior. Do not change their return URLs or remove other actions.

Main owns this strip. Preserve `$this->breadcrumbs` construction and remove only duplicate rendering in nested layouts. Check long labels and narrow screens without changing it to a white-content text list. Do not retain the earlier skill's relocated breadcrumb guidance.

## Footer: preserve verbatim

The user explicitly requires footer information exactly as in the authoritative template. `assets/app/themes/joyful/views/layouts/_footer.php` is its complete byte-for-byte footer subtree; main renders this partial. Preserve all visible information, markup structure and interactions:

- Tagasiside and its original VAU feedback popup URL/window options;
- Rahvusarhiiv, Arhiivi infosüsteem, Virtuaalne uurimissaal link labels and destinations;
- Rahvusarhiiv, **Nooruse 3, Tartu 50411**, **Tel: 738 7500**, **E-mail: rahvusarhiiv@ra.ee**;
- the original Facebook, blog, Flickr, Instagram, Twitter and YouTube destinations and SVGs;
- stacked mobile / divided desktop links-and-contact sections, spacing, height, radii and shadows.

Do not replace details with the target's adminEmail, app name, copyright, bookmark links or another footer. Do not modernize links or contact details as part of theming. Keep the local Alpine script loaded once for the feedback behavior; do not leave a visually correct button inert. Verify the footer source hash and compare the rendered footer. Print/dialog layouts retain their own contracts and need not render this web footer.

## Mobile navigation

Follow the reference's right-side drawer: `fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white sm:max-w-sm`, 48px header, gray overlay, and mobile links `hover:bg-gray-100 block px-8 py-3 rounded` inside `space-y-1 px-3 text-gray-700 text-base font-medium`. Convert obsolete opacity syntax for the modern build while keeping appearance.

Use the target's same authorized links on desktop/mobile. Supply `aria-expanded`, Escape, focus trapping/return, background inertness, and scroll restoration for close, outside click and desktop resize. The prototype lacks some of these behaviors; its visual pattern remains authoritative. Ensure the overlay is not trapped under the header's stacking context. Main already loads local Alpine for the footer; do not add a duplicate runtime.

The application slots in main must be populated and the drawer implemented before claiming completion. Do not copy Menuipsum, logoipsum, Lorem ipsum, a fake language switch or an unconnected sign-in button. These exclusions do not apply to the mandated exact footer, which is copied intact.
