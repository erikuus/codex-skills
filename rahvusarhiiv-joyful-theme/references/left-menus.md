# Left menus and extension skins

## What VAU actually renders

The left menus on `/shop/home/index` and `/page/article/index` share this design:

| Element | Source classes / behavior |
| --- | --- |
| Desktop sidebar | `mr-10 hidden w-56 flex-initial shrink-0 lg:block`: 224px wide with a 40px content gap at the reference root size |
| Menu wrapper | `lg:-ml-4`; page menu additionally has `lg:mt-0.5` |
| Group spacing | First section `pb-5`; subsequent groups `py-5` |
| Group title | `mb-2 border-b border-gray-500 px-4 py-2.5 text-sm font-bold uppercase text-gray-700` |
| List | `space-y-1`: 4px between items |
| Link | `block rounded px-4 py-2`: full row, 16px horizontal/8px vertical padding, 8px radius; regular body text |
| Current link | `bg-green-50` (`#E9F7EE` from the institutional preset) |
| Other link hover | `hover:bg-green-50`, keeping normal text color/weight |

The preset’s `text-sm` is **13px**, not Tailwind’s default 14px; menu links use 16px body text.

This matches the supplied “UURIMISSAALID” screenshot: an uppercase dark-gray group title above a thin rule and a pale-green rounded active row. There is **no gray portlet card, centered title bar, border around the whole menu, red active text or bullet list**. The underline belongs to the navigation group title; the no-horizontal-lines rule for titled *detail groups* does not remove this menu underline. Keep links outside `prose` styling or use `not-prose` where needed so article typography does not add bullets, underlines or weight.

Source files:

- `vau/themes/joyful/views/ShopMenuWidget/shopMenuWidget.php` and `shop/layouts/shop.php`: search above the menu, selected state from `selectedMenuId`, item/header models, desktop left column. The shop layout's extra `xl:mx-24 2xl:mx-32` margins are page-specific, not universal sidebar margins.
- `vau/themes/joyful/views/PageMenuWidget/pageMenuWidget.php` and `page/layouts/page.php`: same left-link design, active state from `menuId`, existing admin controls preserved.
- `vau/protected/modules/{shop,page}/components/{ShopMenuWidget,PageMenuWidget}.php`: both extend **CWidget**, load data/permissions, then render a view. Joyful supplies the concrete widget view and the module layout sets `cssFile=>false`.
- `page/article/index.php` contains a separate right-side “ON THIS PAGE” table of contents with vertical indicators. Do not mistake that component for the left navigation or apply its indicator design to ManageMenu.

Preserve the target's existing sidebar structure and content. Use the source width/gap when implementing this left-menu layout; do not blindly keep the starter's different generic `.joyful-columns-left` width/gap and call it source-identical. The negative left margin only offsets matching parent padding: omit it when it would protrude outside the target container. On small screens, retain access through the existing drawer or a suitable stacked/collapsible menu. Do not merely copy `hidden lg:block` and make navigation disappear; keep the same authorized items and active state in its mobile presentation. Preserve print layout exclusions.

## How a Yii extension gets its Joyful skin

VAU `themes/joyful/views/skins/XAlert.php` returns `array('default'=>array(...))`. Its properties include `cssFile=>false`, the success/warning/error classes, and close-control markup. The widget factory applies these properties to the existing **XAlert** before `init()`; the extension continues to render its content and handle behavior. It does not require a replacement application component or a copied extension implementation.

Use that mechanism for supported extension presentation properties:

1. Resolve and read the target's actual extension class (for XPortlet, commonly `ext.widgets.portlet.XPortlet`), then its concrete subclass. Inspect `init()`, `renderContent()`, public properties/setters, CSS registration, child widget calls and explicit invocation options. Do not infer its API from CPortlet or a different XPortlet version.
2. Ensure `widgetFactory.enableSkin=true`. When `skinnableWidgets` is restricted, add the **concrete class name** while retaining the existing allowlist.
3. Skin lookup is **exact-class**, not inheritance-aware: `ManageMenu` needs `themes/joyful/views/skins/ManageMenu.php`. A skin named `XPortlet.php` applies only to widgets instantiated as XPortlet. The same applies to AdminMenu and other subclasses.
4. A default skin is selected unless a specific `skin` is passed; `skin=>false` bypasses skins. A theme skin overrides the same-named application skin; explicit widget properties override skin properties through Yii's merge. A subclass assigning a presentation property in `init()` can overwrite the skin afterward. Find the actual winning assignment before adding CSS specificity.

These rules were checked against local Yii 1.1.33-dev `web/CWidgetFactory.php`. Do not assume skins propagate to a child CMenu or that changing a parent widget skins every descendant.

## Apply the pattern to ManageMenu extending XPortlet

The inspected extension at `/Users/erikuus/dev/yii/extensions-1.1.8/widgets/portlet/XPortlet.php` exposes `cssFile`, `cssClass`, `headerCssClass`, `contentCssClass`, `width`, `title`, `visible`, and `hideOnEmpty`. Its `init()` generates the outer/header/content divs and registers legacy `portlet.css` unless `cssFile` is false. `run()` retains visibility/empty-content behavior and calls the subclass's `renderContent()`.

Pitserid's `protected/portlets/ManageMenu.php` sets a translated title, builds menu data in `getMenuData()`, and invokes `zii.widgets.CMenu` directly in `renderContent()`. Therefore:

- Apply the [bundled concrete skin example](../assets/examples/skins/ManageMenu.php) as `themes/joyful/views/skins/ManageMenu.php`, after checking the target's API. It disables the old stylesheet and sets the three presentation class properties. For another concrete XPortlet menu, adapt the filename after inspecting that class. The staging script intentionally does **not** auto-install this example into every app.
- The example's `contentCssClass` opts into `joyful-sidebar-menu`. The supplied `tailwind/yii.css` styles only lists and direct item anchors **inside that wrapper**, with source padding/radius/hover and `.active > a` selection. Nested lists receive a modest indentation; direct-child active selectors prevent an active parent from painting every descendant link green. Other portlets and global CMenu instances are unaffected.
- Keep the actual XPortlet implementation in the resolved extension tree and keep ManageMenu's data, translations, URLs, permissions, ordering, active rules, callbacks, visibility and empty-content behavior. There is no need to change its PHP for the inspected direct-CMenu case. Do not copy XPortlet into application components or replace the subclass with hardcoded links.
- Preserve native CMenu selection. Its default active class is `active`, placed on `li`; if the target uses another marker, adapt the **scoped** selector accordingly. Do not replace real route/context-based active logic with the first item, current label text or a broad URL substring check. Respect `activateParents`, disabled items, item options and nested menus.
- XPortlet has no `htmlOptions`, `headerTagName` or `menuOptions` property in the inspected version. Do not put those imaginary properties in a skin. Its header is a div; styling it does not magically make it an h3. If extra semantics are needed, make a small supported rendering adaptation without discarding its behavior.

Example skin properties:

```php
return array('default'=>array(
    'cssFile'=>false,
    'cssClass'=>'joyful-sidebar-portlet pb-5',
    'headerCssClass'=>'mb-2 border-b border-gray-500 px-4 py-2.5 text-sm font-bold uppercase text-gray-700',
    'contentCssClass'=>'joyful-sidebar-menu text-base text-gray-900',
));
```

Disabling the widget's stylesheet cannot remove a separate global `<link>` or legacy CSS bundle. Inspect the rendered head and cascade; remove or scope obsolete `.portlet` rules rather than retaining the gray card and compensating with broad important overrides. The example replaces legacy `portlet/header/content` classes; retain a legacy hook only if target code actually uses it, and resolve its visual rules deliberately.

If `renderContent()` does call `$this->render('menu')`, a theme view may be placed at `themes/joyful/views/<ConcreteClass>/menu.php`. But a guessed `views/ManageMenu/manageMenu.php` cannot affect the inspected implementation: it never renders that file. For richer markup unsupported by existing properties/scoped styling, make the smallest rendering change, retaining data and behavior; do not add a global CMenu default skin that restyles unrelated navigation.

Rebuild Tailwind after installing the concrete skin. The real theme skin path must be scanned so its header utility classes are generated; the scoped list rules are compiled from `yii.css`. Do not scan the example/reference folder merely to hide a missing integration step.

## Verification

Render the actual subclass through Yii's widget factory with the theme enabled. Confirm the concrete skin's properties before/after `init()`, no old portlet stylesheet registration, correct title and list contents, and preserved `visible=false`/`hideOnEmpty` behavior. Test a custom active item and nested inactive descendants; do not infer correct selection from green hover alone.

Compare with the source: uppercase left-aligned group title, thin gray underline, 16px horizontal link padding, 8px vertical padding/radius, 4px row gaps, and `#E9F7EE` current/hover background. Check normal/hover/focus/current states, long labels, nested entries, permissions, working destinations and mobile access. Confirm other CMenu widgets and non-menu XPortlets retain their own design. A styled outer header alone is not a completed menu adaptation.
