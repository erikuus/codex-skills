# Add the design as a separate application theme

Replace `/absolute/path/to/app`, then copy:

```text
Use $rahvusarhiiv-new-design to implement the established Rahvusarhiiv design as a separate joyful theme in /absolute/path/to/app. Preserve the existing default design and assets. Read the skill and its relevant references, inspect public/admin rendering and assets, then implement the theme.

Select default or joyful through one application-wide configuration setting, shared by all entry points. Reuse a suitable theme mechanism or add minimal centralized template/asset selection. Do not add per-user selection, session/cookie/query overrides, a theme picker or route-based switching. Keep business logic shared and create separate presentation templates where needed. Enable joyful in the intended app configuration and document how the same setting restores default.

Use the packaged institutional Tailwind preset and reproducible build with a separate Joyful output, exact footer, approved header gradient, responsive shell/breadcrumbs, table styling, narrow shared title/detail and title/form containers, and action SVG rules. In Joyful menus, omit Home/Avaleht while retaining logo and breadcrumb home links. Keep default presentation unchanged. Apply conditional components only where the app has that functionality.

Preserve backend architecture, URLs, authorization, data, escaping, form/CSRF contracts, pagination/sorting, AJAX, dialogs, uploads and existing rich-text editors in both themes. Do not install Yii or migrate editors. Before optional mobile text fading, ask which blocks should collapse and how many lines remain visible; wait for confirmation before clipping text.

Verify default → joyful → default through application configuration only. Compare restored default screenshots with the original and check theme asset isolation. Verify representative public/admin table, detail, form and dialog pages at phone/tablet/desktop widths; compare Joyful with the supplied reference, rebuild its CSS, and run appropriate application checks. Keep print/export output suitable for its purpose. Report the setting, switch-back procedure, changes, checks and unverified behavior. Do not finish with sample links/data, incomplete theme coverage or unpopulated navigation.
```

For the motivating target, use `/Users/erikuus/dev/php/nimeregister` and read the skill's Nimeregister integration notes before changing templates.
