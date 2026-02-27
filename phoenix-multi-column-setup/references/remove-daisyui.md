# Remove Daisy UI

Steps to remove Daisy UI (Tailwind plugin based):

1. Delete plugin references from `assets/css/app.css`:

```
@plugin "../vendor/daisyui";
@plugin "../vendor/daisyui-theme";
```

2. Delete the plugin JS files from `assets/vendor/`:
- `daisyui.js`
- `daisyui-theme.js`

After removal, the app reverts to standard Tailwind configuration.
