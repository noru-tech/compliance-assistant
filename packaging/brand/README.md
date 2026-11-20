# Plugin icon source

`signum-dark.svg` is the source for the plugin icons in `plugins/compliance-assistant/assets/`:
the Noru signum in white at 70% of the canvas, on the brand dark `#111B1C`, full-bleed so the
directories can apply their own rounded or circular mask without clipping it.

It lives here, outside the plugin folder, because Anthropic's plugin directory accepts no `.svg`
files in the plugin from unverified organizations. To regenerate the PNGs:

```bash
bunx --bun @resvg/resvg-js-cli --fit-width 1024 packaging/brand/signum-dark.svg plugins/compliance-assistant/assets/logo.png
bunx --bun @resvg/resvg-js-cli --fit-width 256 packaging/brand/signum-dark.svg plugins/compliance-assistant/assets/composer-icon.png
```

`docs/icon-preview.png` shows the icon at directory sizes on light and dark backgrounds.
