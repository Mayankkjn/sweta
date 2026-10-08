# Finny design system

Design tokens and a living style guide, built from the Finny `style_guide.pdf`.

| File | What it is |
| --- | --- |
| `tokens.json` | Source of truth, in [W3C Design Tokens](https://design-tokens.github.io/community-group/format/) format. Three tiers: `primitive` → `semantic` → `component`. Works with Style Dictionary, Tokens Studio and similar tools. |
| `tokens.css` | The same tokens as `--fy-*` CSS custom properties, plus ready-made classes: type styles (`.fy-heading-1`…`.fy-caption`), buttons, inputs, choice chips, segmented toggle, filter chips and cards. |
| `style-guide.html` | A living style guide that renders every token and component from `tokens.css`, plus 8 Figma screens rebuilt from the components. Open it in a browser. |

## Usage

```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="finny-design-system/tokens.css">

<button class="fy-btn fy-btn--primary">Looks Good</button>
```

Components should use **semantic** tokens (`--fy-text-heading`, `--fy-border-default`), not primitives (`--fy-primary-500`).

## Where this differs from the PDF

- Both "BG" swatches are labelled `#02372F`. The tokens use what the artwork actually shows: `#4C9B66` (`bg-brand`) and `#F5F6F0` (`bg-canvas`).
- "Subtitle 2" appears twice. The Medium 12 style is renamed `subtitle-3`.
- The success tint is labelled `#CCE6D4` but renders as `#EEF7F1`. Both are kept (`success-100`, `success-50`).
- Three new text colours give each status an AA-compliant text variant: `success-700 #2E7A4A`, `error-700 #B4475B` and `warning-700 #9A6531`. The PDF's status colours measure 2.9–4.4:1 on white.
- The PDF doesn't specify line heights, spacing, radii, shadows, gradient angles or component heights. Those values are proposed or measured from the artwork, and are marked as such in `tokens.json`.

## App components (from Figma "Login flows")

The 50 screens on the Figma page (login, OTP, account aggregator, errors and app update) break down into these reusable components, all in `tokens.css`:

| Component | Class | Variants |
| --- | --- | --- |
| Hero header | `.fy-hero` | art right, stacked, centred |
| Content panel | `.fy-panel` | over hero, with or without keypad |
| Bottom sheet | `.fy-scrim` + `.fy-sheet` | cream or plain head, centred; list, form, status and consent bodies |
| Phone input | `.fy-phone` | empty, filled, focused |
| OTP input | `.fy-otp` | empty, typing, filled, error |
| Edit tag, retry timer | `.fy-tag`, `.fy-timer` | |
| Status pill | `.fy-status-pill` | progress (spinner), done (check) |
| Resend channels | `.fy-channel` | SMS, Call, WhatsApp |
| Option row | `.fy-option` | flag, icon, logo stack, chevron or check |
| Account group, account row | `.fy-group`, `.fy-account` | collapsed or expanded; selected or not |
| Feature list | `.fy-features` | |
| FAQ accordion, video card | `.fy-faq`, `.fy-video` | closed, text and video, video only |
| Stat tiles | `.fy-stats` | 3-up |
| Status block | `.fy-status` | error, info, waiting, update; centred or left |
| Small print | `.fy-legal`, `.fy-powered`, `.fy-id-chip`, `.fy-step` | |

### What Figma changed

- Radii are 8px (controls), 12px (cards, rows) and 16px (sheets). The PDF read as 6px.
- The primary gradient is `#1F673F → #57A870` at 94°.
- Links and secondary text use success-700 `#236B42`. This replaces the earlier proposed `#2E7A4A`.
- Off-palette values in Figma are mapped to tokens: `#EDEDED`, `#F4F5EF`, `#546881`, `#09A98B`, `#151A20` and `#4C9B67`. The file has no Figma variables, which is why they drift.
- Account meta text in Figma (`#678782` at 10px) is 3.9:1. The component uses neutral-500 instead.
- 3D illustrations stay in Figma. The guide shows them as tinted icon slots (`.fy-art`).

## Product components (Home, Assets, Transactions, Cashflow, FIRE)

From the Figma pages Home, Assets individual pages, Transaction, Cashflow, FIRE Goals, Fire age, Overrides and All Launch Requirement.

| Component | Class |
| --- | --- |
| Bottom navigation | `.fy-bnb` |
| Member switcher (You / Spouse / Family) | `.fy-members` |
| Headline metric, last-updated chip, Total/Average toggle | `.fy-metric`, `.fy-updated`, `.fy-title-toggle` |
| Section card, total pill, add link, retry | `.fy-section-card`, `.fy-total-pill`, `.fy-add-link`, `.fy-retry` |
| Asset row | `.fy-asset-row` |
| KPI strip, holding card, sort toggle, count | `.fy-kpis`, `.fy-holding`, `.fy-sort`, `.fy-count` |
| Category tabs | `.fy-cat-tabs` |
| Filter bar, transaction row, tag chip | `.fy-filterbar`, `.fy-txn`, `.fy-tag-chip` |
| Filter panel, radio card, checkbox, select row | `.fy-filters`, `.fy-radio-card`, `.fy-checkbox`, `.fy-select-row` |
| Period stepper and chips | `.fy-stepper`, `.fy-periods` |
| Amount card, breakdown row, health gauge | `.fy-amount-card`, `.fy-breakdown`, `.fy-gauge` |
| Switch | `.fy-switch` |
| FIRE timeline and card, comparison cards, alert pill | `.fy-timeline`, `.fy-fire-card`, `.fy-compare`, `.fy-alert-pill` |
| Tier tabs, value row, slider, wheel picker, goal picker | `.fy-tier-tabs`, `.fy-value-row`, `.fy-slider`, `.fy-wheel`, `.fy-goal-card` |
| Profile list, large avatar, skeleton | `.fy-list-group`, `.fy-avatar--lg`, `.fy-skeleton` |

### Token names follow Figma

The product pages use Figma variables. The colour tokens now use the same names and numbers:
`--fy-primary-100…600`, `--fy-neutral-100…600`, `--fy-success-50/100/600/700`, `--fy-error-50/600/700`, `--fy-warning-50/600/700` and `--fy-white`.
This renumbers the earlier tokens (for example, the old `primary-700` is now `primary-400`).
