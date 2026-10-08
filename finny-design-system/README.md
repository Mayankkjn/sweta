# Finny design system

Design tokens and a living style guide, built from the Finny `style_guide.pdf`.

| File | What it is |
| --- | --- |
| `tokens.json` | Source of truth, in [W3C Design Tokens](https://design-tokens.github.io/community-group/format/) format. Three tiers: `primitive` → `semantic` → `component`. Works with Style Dictionary, Tokens Studio and similar tools. |
| `tokens.css` | The same tokens as `--fy-*` CSS custom properties, plus ready-made classes: type styles (`.fy-heading-1`…`.fy-caption`), buttons, inputs, choice chips, segmented toggle, filter chips and cards. |
| `style-guide.html` | A living style guide that renders every token and component from `tokens.css`. Open it in a browser. |

## Usage

```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="finny-design-system/tokens.css">

<button class="fy-btn fy-btn--primary">Looks Good</button>
```

Components should use **semantic** tokens (`--fy-text-heading`, `--fy-border-default`), not primitives (`--fy-primary-800`).

## Where this differs from the PDF

- Both "BG" swatches are labelled `#02372F`. The tokens use what the artwork actually shows: `#4C9B66` (`bg-brand`) and `#F5F6F0` (`bg-canvas`).
- "Subtitle 2" appears twice. The Medium 12 style is renamed `subtitle-3`.
- The success tint is labelled `#CCE6D4` but renders as `#EEF7F1`. Both are kept (`green-200`, `green-50`).
- Three new text colours give each status an AA-compliant text variant: `green-600 #2E7A4A`, `red-600 #B4475B` and `amber-600 #9A6531`. The PDF's status colours measure 2.9–4.4:1 on white.
- The PDF doesn't specify line heights, spacing, radii, shadows, gradient angles or component heights. Those values are proposed or measured from the artwork, and are marked as such in `tokens.json`.
