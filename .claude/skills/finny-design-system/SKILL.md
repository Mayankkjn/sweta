---
name: finny-design-system
description: Finny (personal finance / FIRE app) design tokens and UI components. Use whenever building, reviewing or prototyping any Finny screen, page, mockup, artifact or component — login/OTP, account aggregator, net worth, assets, transactions, cashflow, FIRE age/goals, profile — or when asked for Finny colours, fonts, spacing, Figma variable names, or "make it look like Finny". Provides tokens.css (CSS variables + ready-made .fy-* component classes), tokens.json (W3C design tokens), an icon sprite, and markup recipes.
---

# Finny design system

Finny is an Indian personal-finance app (net worth, cashflow, FIRE age). Mobile-first, 360px frames, Poppins, deep-forest greens on a warm cream canvas.

Sources it was built from: `style_guide.pdf` and the Figma file `9glnVU9csArTpIg1EVRcRA` ("Finny-Dev") — pages Login flows, Home, Assets individual pages, Transaction, Cashflow, FIRE Goals, Fire age, Overrides, All Launch Requirement. Living style guide in the repo: `finny-design-system/style-guide.html`.

## How to use

1. **Load the files, don't retype values.** Link or inline `assets/tokens.css` (it holds every token and every `.fy-*` component class). Add Poppins:
   `<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">`
   For an Artifact, inline the CSS or publish it alongside via `files`.
2. **Icons:** paste `assets/icons.svg.html` (a hidden `<svg><defs>` sprite) once at the top of `<body>`, then use `<svg><use href="#i-NAME"/></svg>`. Available: back close chev-down chev-right chev-left check check-circle sms phone chat mobile shield lock share eye-off bank sprout chart rupee alert flag doc play question in-flag home wallet fire user info calendar refresh pencil sliders selector tag sort split candles coins building gem house-loan heart rocket cap palm.
3. **Build from components** in `references/components.md` (markup recipes). Only write new CSS for something genuinely new, and build it from `--fy-*` tokens.
4. In repo work, the source of truth is `finny-design-system/` (tokens.css, tokens.json, style-guide.html). Keep `assets/` here in sync when those change.

## Token rules (the short version)

Colour primitives use the **Figma variable names and numbers** — `--fy-primary-400` is Figma "Primary 400".

| Ramp | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|
| primary | #9AAFAC | #678782 | #4E736E | #03685A | #1B4B44 | #02372F |
| neutral | #F5F7F7 | #E6EBEA | #CCD7D5 | #909D9B | #576361 | #01231E |

- success: 50 #EEF7F1 · 100 #CCE6D4 · 600 #4C9B66 · 700 #236B42 (text/links). error: 50 #F9ECEE · 600 #C85267 · 700 #B4475B (text). warning: 50 #F9F2EC · 600 #C88A52 · 700 #9A6531 (text). white #FFFFFF. cream-50 #F5F6F0 (screen canvas).
- Prefer **semantic** tokens in components: `--fy-bg-canvas|surface|subtle|muted|inverse`, `--fy-text-display` (hero/sheet titles, primary-400), `--fy-text-heading` (primary-500), `--fy-text-primary` (neutral-600), `--fy-text-secondary` (neutral-500), `--fy-text-muted` (primary-300), `--fy-text-placeholder`, `--fy-text-disabled`, `--fy-text-link` (success-700), `--fy-border-default|subtle|strong|focus`, `--fy-success|error|warning(-text|-subtle)`, `--fy-gain` / `--fy-loss` for amounts and returns.
- Category tints (breakdown bars): `--fy-tint-spends|investment|loans|untagged|surplus|shortfall`. FIRE dark theme: `--fy-fire-bg` #1C2518, `--fy-fire-accent`.
- Gradients: `--fy-gradient-green` (primary button, 94°, #1F673F→#57A870), `--fy-gradient-teal` (active toggle).
- Type: Poppins only. Scale `.fy-heading-1` 32/700 · `-2` 28/600 · `-3` 24/600 lh28 · `.fy-subheading-1` 20/600 · `.fy-subtitle-1` 16/600 lh22 · `-2` 16/500 lh22 · `.fy-body-1` 14/500 lh22 · `-2` 14/400 lh22 · `.fy-subtitle-3` 12/500 (field labels) · `.fy-caption` 10/400. Display titles on hero/sheets: 32/39 Bold (or 24/29) in `--fy-text-display`.
- Space: 4px grid `--fy-space-1..12` (4,8,12,16,20,24,32,40,48). Screen gutter 16px, stacked cards 12px apart.
- Radius: `--fy-radius-xs` 4 · `sm` 8 (buttons, inputs, chips) · `md` 12 (cards, rows) · `lg` 16 (sheets, panels) · `pill`. Section cards on Home use 24.
- Shadows: `--fy-shadow-card` (Figma "Card Shadow light"), `--fy-shadow-card-strong` ("Card shadow"), `--fy-shadow-row`, `--fy-shadow-panel` (upward, for sheets/panels), `--fy-scrim` behind sheets.
- Sizes: button 48px tall, inputs 40px (outlined) / 48px (filled phone input), option rows 54px, bottom nav 69px, period chips 28px.

## Do / don't

- Use `.fy-btn--primary` for one main action per screen, pinned to the bottom; pair with `.fy-btn--secondary` for the lesser action.
- Money: `₹ 1.16 L`, `₹ 1.31 Cr`, Indian grouping `₹ 1,02,209`; positive with `+` and `.is-gain`, negative with `−` and `.is-loss`. Use `font-variant-numeric: tabular-nums` for amounts (already set on amount classes).
- Accessibility (WCAG AA): never put text on success-600 #4C9B66 or use warning-600 / #678782 / #909D9B for readable text — use the `-700` text variants and `--fy-text-secondary`. White on the green gradient is fine only centred.
- Illustrations are 3D renders in Figma; in code use an `.fy-art` slot (tinted disc + icon) unless real assets are provided.
- Don't introduce off-palette greys/greens seen in older Figma frames (#EDEDED, #8B8B8B, #4A4A4A, #2F8F0D, #D19405, #546881, #09A98B) — map them to tokens. Don't use "Cina GEO Test", "Inria Sans" or serif faces.
- Open design question: Figma "Body 2" is Medium 14/22, PDF says Regular 14. Tokens keep Regular; flag if it matters.

See `references/components.md` for every component's markup.
