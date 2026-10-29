# Source map and extraction coverage

Repository: [tailwindui-playground](https://github.com/erikuus/tailwindui-playground). Snapshot commit `184e12e788f10db3eefa2e587e130af1f73d689f`, inspected 2026-10-28. All included HTML was structurally inventoried; representative family implementations were read closely. Visual coverage is a representative subset, specified in validation.md; this is not a claim that every state of every page was rendered.

Canonical shell: `views/layouts/advanced-layout-alt.html`, following the corrected user preference. `advanced-layout.html` is retained only as a comparison variant. Excluded entirely as a design authority: `views/layouts/vau-layout.html`. Shared VAU headers repeated in page files were not used for the generic shell. Static assets/preset were inspected independently. This skill does not require the original checkout: it bundles tokens, fonts, mark, CSS snapshot, footer, neutral recipes and a runnable composer.

## Canonical choices

| Family | Canonical evidence | Why |
|---|---|---|
| Shell/footer | advanced-layout-alt | Menu trigger in institutional top strip; generic app header; complete shared institutional footer |
| Minimal shell | basic-layout | Confirms same geometry with alternate pastel gradient |
| Narrow container | vau-news-list | Reading-oriented inset schedule |
| Medium container | vau-access-files | Form/record inset schedule |
| Full container | vau-order-archived | Dense collection within global cap |
| Split | vau-order-copy-confirm | Equal regions at xl; first summary sticky |
| Page title | access-files, bookmark-folder-list, order-draft-empty | Plain, button actions, quiet utility actions |
| Article composition | vau-page | Section menu + article + responsive TOC as one owner |
| Workspace | order-draft, enquiry-form | Sidebar form/help with nested responsive behavior |
| Core fields | forms, register, login | Normal, disabled, invalid, grouped controls |
| Data collection | order-archived, bookmark-folder-list, access-files | Divided/striped surfaces and relocated mobile metadata |
| Content/cards | news-list, account-picker, home, enquiry-list | Neutral list/card anatomy across different tasks |
| Prose/disclosure/media | vau-page, feedback-faq, shop-product, carousel | Article typography, FAQ disclosure, media detail and related-media strip |

## Included inventory after scope cleanup

The active extraction set contains **101 HTML templates: 92 pages, 6 component examples and 3 layouts**, plus foundation files. The reconstruction prompt has one additional explicit VAU layout case, which remains excluded from generic skill extraction. The remaining component examples are account-picker, alerts, carousel, forms, print and radio-cards.

The exclusion list and wildcard in [source-manifest.json](source-manifest.json) are authoritative: those templates are not design evidence, recipes or validation targets. Do not reintroduce them through future inventory passes. Historical evaluations remain outside the active design contract.

The mapping is structural discovery, followed by family-level synthesis in the other references. A mention here does not make an app-specific field or experiment a recommended component. Closely related pages intentionally collapse into the same families rather than creating one component per file. Exact paths, source hashes, line counts and inset evidence are in [source-manifest.json](source-manifest.json).

| Source | Extracted family / evidence role |
|---|---|
| `rahvusarhiiv.preset.js` | Foundation / build evidence |
| `tailwind.css` | Foundation / build evidence |
| `style.css` | Foundation / build evidence |
| `views/layouts/basic-layout.html` | AppShell, InstitutionalFooter |
| `views/layouts/advanced-layout-alt.html` | Canonical AppShell, InstitutionalFooter |
| `views/layouts/advanced-layout.html` | Nonpreferred shell placement comparison; same footer |
| `views/pages/print.html` | Print adaptation |
| `views/pages/vau-access-files-refine.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, FileCollection, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-access-files.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, StepProgress, FileCollection, Split/Workspace, Media/Prose |
| `views/pages/vau-access-form-refine.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-access-form.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, StepProgress, Split/Workspace, Media/Prose |
| `views/pages/vau-access-purpose.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, StepProgress, Media/Prose |
| `views/pages/vau-access-sign.html` | ContentContainer, PageTitle, StepProgress |
| `views/pages/vau-access-signed.html` | ContentContainer, PageTitle, StepProgress |
| `views/pages/vau-account-company-invoice.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-account-company-update.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-account-company-view.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Disclosure, Split/Workspace, Media/Prose |
| `views/pages/vau-account-order-template-update.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-account-order-templates.html` | ContentContainer, PageTitle, Split/Workspace |
| `views/pages/vau-account.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, LinkCardGroup, Notice/Status, Media/Prose |
| `views/pages/vau-bookmark-folder-list.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-bookmark-folder-update.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-bookmark-labels-add.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-bookmark-labels-remove.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-bookmark-list-empty.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-bookmark-list.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Disclosure, Split/Workspace, Media/Prose |
| `views/pages/vau-bookmark-update.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-connect-id.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-copy-payment-banklink.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-copy-payment-confirm.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-copy-payment-invoice.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-copy-payment-outdated-emp.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-copy-payment-outdated.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-copy-payment-pickup.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-disconnect-id.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-emp-connected.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-emp-not-connected.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-enquiry-form.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-list.html` | ContentContainer, PageTitle, LinkCardGroup, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-payment-confirm-letter.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-enquiry-payment-confirm-notice.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-enquiry-payment-download.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-payment.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-enquiry-preview.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, FileCollection, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-refine.html` | ContentContainer, PageTitle, Field/ActionGroup, FileCollection, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-refined.html` | ContentContainer, PageTitle, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-enquiry-submitted.html` | ContentContainer, PageTitle, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-feedback-faq.html` | ContentContainer, PageTitle, Disclosure, Media/Prose |
| `views/pages/vau-feedback-submit.html` | ContentContainer, PageTitle, Field/ActionGroup, Media/Prose |
| `views/pages/vau-home-emp-2.html` | ContentContainer, PageTitle, ArticleLayout, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-home-emp.html` | ContentContainer, PageTitle, LinkCardGroup, Notice/Status, Media/Prose |
| `views/pages/vau-home.html` | ContentContainer, PageTitle, LinkCardGroup, Notice/Status, Media/Prose |
| `views/pages/vau-ial-payment-confirm.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-ial-payment.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-login-bookmark.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-login-order.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-login.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace, Notice/Status |
| `views/pages/vau-news-list.html` | ContentContainer, PageTitle, LinkCardGroup |
| `views/pages/vau-news.html` | ContentContainer, LinkCardGroup, Media/Prose |
| `views/pages/vau-openid.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace |
| `views/pages/vau-order-archived-empty.html` | ContentContainer, PageTitle |
| `views/pages/vau-order-archived.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Disclosure, Media/Prose |
| `views/pages/vau-order-copy-confirm-batch.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-order-copy-confirm.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Notice/Status, Media/Prose |
| `views/pages/vau-order-draft-empty.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace |
| `views/pages/vau-order-draft-update.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-order-draft.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Disclosure, Split/Workspace, Media/Prose |
| `views/pages/vau-order-ial-confirm-batch.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-order-ial-confirm.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-order-labels-add.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-order-labels-remove.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-order-labels-update.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-order-submitted-empty.html` | ContentContainer, PageTitle |
| `views/pages/vau-order-submitted.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Disclosure, Media/Prose |
| `views/pages/vau-page-2.html` | ContentContainer, PageTitle, ArticleLayout, Media/Prose |
| `views/pages/vau-page-3.html` | ContentContainer, PageTitle, ArticleLayout, Media/Prose |
| `views/pages/vau-page.html` | ContentContainer, PageTitle, ArticleLayout, DataCollection/DetailSummary, Disclosure, LinkCardGroup, Media/Prose |
| `views/pages/vau-password-change.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-password-forgot.html` | ContentContainer, PageTitle, Field/ActionGroup |
| `views/pages/vau-pick-theme.html` | ContentContainer, PageTitle, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-register.html` | ContentContainer, PageTitle, Field/ActionGroup, FileCollection, Notice/Status, Media/Prose |
| `views/pages/vau-shop-cart-empty.html` | ContentContainer, PageTitle, Media/Prose |
| `views/pages/vau-shop-cart.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Media/Prose |
| `views/pages/vau-shop-category.html` | ContentContainer, PageTitle, Field/ActionGroup, Disclosure, Media/Prose |
| `views/pages/vau-shop-emp.html` | ContentContainer, PageTitle, Field/ActionGroup, Disclosure, Media/Prose |
| `views/pages/vau-shop-form.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-shop-home.html` | ContentContainer, PageTitle, Field/ActionGroup, Media/Prose |
| `views/pages/vau-shop-payment-banklink.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-shop-payment-confirm.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-shop-payment-invoice.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Notice/Status, Media/Prose |
| `views/pages/vau-shop-product-vert.html` | ContentContainer, Media/Prose |
| `views/pages/vau-shop-product.html` | ContentContainer, Media/Prose |
| `views/pages/vau-shop-search.html` | ContentContainer, PageTitle, Field/ActionGroup, Disclosure, Media/Prose |
| `views/pages/vau-social-media-connect-2.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-social-media-connect.html` | ContentContainer, PageTitle, Split/Workspace, Media/Prose |
| `views/pages/vau-theme-progress.html` | ContentContainer, PageTitle |
| `views/pages/vau-virtual-order-apply-access-revise-selection.html` | ContentContainer, PageTitle, DataCollection/DetailSummary, Field/ActionGroup, Split/Workspace, Media/Prose |
| `views/pages/vau-virtual-order-apply-access.html` | ContentContainer, DataCollection/DetailSummary, Field/ActionGroup, Notice/Status, Media/Prose |
| `views/components/account-picker.html` | LinkCardGroup |
| `views/components/alerts.html` | Disclosure, Notice/Status |
| `views/components/carousel.html` | RelatedMediaStrip |
| `views/components/forms.html` | Field/ActionGroup |
| `views/components/print.html` | Print adaptation |
| `views/components/radio-cards.html` | ChoiceGroup |

## Assets and exclusions within included files

Bundled: seven font files, institutional RA SVG, original preset and compiled CSS, normalized base stylesheet, standard-footer SVGs. App marks, avatars, book covers, provider logos, theme screenshots and subject illustrations remain caller-selected assets; they are not universal components. `identity.css`, `dokobit.css`, `labels.css`, and `jquery-ui.css` were classified as integration skins, not copied into the global foundation. Never import hidden form fields or concrete business URLs from source examples.
