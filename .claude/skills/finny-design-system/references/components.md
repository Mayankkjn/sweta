# Finny component recipes

All classes live in `assets/tokens.css`. Icons: `<svg><use href="#i-NAME"/></svg>` with the sprite from `assets/icons.svg.html`. Interactive state is expressed with ARIA attributes (`aria-pressed`, `aria-selected`, `aria-checked`, `aria-current`, `aria-busy`, `:checked`, `disabled`) — toggle those, not extra classes.

## Foundations

```html
<button class="fy-btn fy-btn--primary">Continue</button>          <!-- also: --secondary --danger --danger-outline --text; disabled; aria-busy="true" with <span class="fy-spinner"></span> -->
<div class="fy-card">…</div>  <div class="fy-card fy-card--dashed">…</div>
<p class="fy-heading-3">…</p>  <!-- type classes: fy-heading-1..3 fy-subheading-1 fy-subtitle-1..3 fy-body-1..2 fy-caption -->
```

Outlined form field:
```html
<label class="fy-field [fy-field--error]"><span class="fy-field__label">PAN</span>
  <span class="fy-input"><span class="fy-input__prefix">₹</span><input placeholder="Eg. Text here"></span>
  <span class="fy-field__helper">Required</span></label>
```
Choice chips `.fy-choices > .fy-choice[role=radio][aria-checked]`; segmented toggle `.fy-segmented > button[aria-pressed]`; filter chips `.fy-filter > .fy-filter__chip[aria-pressed]`.

## Screen scaffolding

```html
<div class="fy-screen [fy-screen--main]">                  <!-- #F5F7F7 by default; --main = cream, landing/main pages only -->
  <div class="fy-appbar"><button class="fy-icon-btn" aria-label="Back"><svg><use href="#i-back"/></svg></button></div>
  <div class="fy-hero"><h1 class="fy-hero__title">Verify your number</h1><span class="fy-art fy-art--sm"><svg><use href="#i-mobile"/></svg></span></div>
  <!-- fy-hero--stacked | fy-hero--center ; .fy-hero__lede for a sub line -->
  <div class="fy-panel">                                  <!-- white, 16px top corners, rises over hero -->
    <div><p class="fy-panel__title">Enter your number</p><p class="fy-panel__sub">Use your phone number registered with PAN</p></div>
    …
    <div class="fy-actions"><button class="fy-btn fy-btn--primary">Continue</button></div>
  </div>
  <nav class="fy-bnb">…</nav>
</div>
```

Bottom sheet:
```html
<div class="fy-scrim"><div class="fy-sheet" role="dialog" aria-label="…">
  <div class="fy-sheet__head [fy-sheet__head--center] [fy-sheet__head--plain]">
    <button class="fy-icon-btn fy-sheet__close" aria-label="Close"><svg><use href="#i-close"/></svg></button>
    <span class="fy-art fy-art--sm">…</span>
    <p class="fy-sheet__title">Choose a phone number</p><p class="fy-sheet__sub">…</p>
  </div>
  <div class="fy-sheet__body">…</div>
  <div class="fy-sheet__foot"><button class="fy-btn fy-btn--primary">I allow</button></div>
</div></div>
```
Status block (error/info/wait/update): `.fy-status [--start] [--display]` > `.fy-art [--error|--success]`, `.fy-status__title`, `.fy-status__body`.

## Login, OTP, account aggregator

```html
<div class="fy-phone">
  <button class="fy-phone__country" aria-label="Country: India"><svg class="fy-flag"><use href="#i-in-flag"/></svg><svg width="16" height="16"><use href="#i-chev-down"/></svg></button>
  <label class="fy-phone__field"><span class="fy-phone__code">+91</span><input inputmode="numeric" placeholder="Enter 10 digit phone number"></label>
</div>
<div class="fy-recipient">+91 8876273731 <button class="fy-tag">edit</button></div>
<div class="fy-otp [fy-otp--error]" data-otp>  <!-- 6 × <input class="fy-otp__cell" maxlength="1" placeholder=" "> -->
<p class="fy-field-error">Entered OTP is incorrect, please retry.</p>
<p class="fy-timer">Didn’t receive it? Retry in <b>00:12</b></p>
<span class="fy-status-pill"><span class="fy-spinner"></span>Auto fetching OTP</span>   <!-- or <svg><use href="#i-check-circle"/></svg>OTP sent via SMS -->
<p class="fy-label">Resend OTP via</p>
<div class="fy-channels"><button class="fy-channel"><svg><use href="#i-sms"/></svg>SMS</button>…Call…WhatsApp</div>
<button class="fy-option"><svg class="fy-flag"><use href="#i-in-flag"/></svg><span class="fy-option__label">8876273731</span><span class="fy-option__trail"><svg><use href="#i-chev-right"/></svg></span></button>
<!-- fy-option--plain for category rows; trail may hold .fy-logo-stack > .fy-logo.fy-logo--sm, or .fy-check -->
<details class="fy-group" open>
  <summary><span class="fy-group__icon"><svg><use href="#i-bank"/></svg></span>Bank accounts<svg class="fy-chevron"><use href="#i-chev-down"/></svg></summary>
  <div class="fy-group__body">
    <div class="fy-account"><span class="fy-logo">IC</span><span class="fy-account__text"><span class="fy-account__name">ICICI bank</span><span class="fy-account__meta">Savings ••••734</span></span><span class="fy-check [fy-check--off]"><svg><use href="#i-check"/></svg></span></div>
    <button class="fy-group__more">View all</button>
  </div>
</details>
<ul class="fy-features"><li><span class="fy-features__icon"><svg><use href="#i-shield"/></svg></span>RBI Authorised Account Aggregator</li>…</ul>
<div class="fy-faq"><details open><summary>What is account aggregator?<svg class="fy-chevron"><use href="#i-chev-down"/></svg></summary>
  <div class="fy-faq__answer"><p>…</p>
    <a class="fy-video" href="#"><span class="fy-video__thumb"><svg><use href="#i-play"/></svg></span><span class="fy-video__text"><span class="fy-video__title">…</span><span class="fy-video__time">1m : 20s</span></span></a>
  </div></details></div>
<div class="fy-stats"><div class="fy-stat"><span class="fy-stat__label">Valid till</span><span class="fy-stat__value">Feb 2028</span></div>×3</div>
<span class="fy-id-chip"><span class="fy-logo fy-logo--sm">IC</span>XX1231</span> <span class="fy-step">1 of 3</span>
<p class="fy-legal">By clicking on continue you agree to our <a href="#">T&amp;C</a> …</p>
<p class="fy-powered">Powered by RBI regulated account aggregator <span class="fy-powered__brand">onemoney</span></p>
```

## Home, net worth, assets

```html
<div class="fy-members"><button aria-pressed="true">You</button><button aria-pressed="false">Spouse</button><button aria-pressed="false">Family</button></div>
<div class="fy-metric"><span class="fy-metric__label">Networth <svg><use href="#i-info"/></svg></span>
  <span class="fy-metric__value">₹ 50.5 L <svg><use href="#i-eye-off"/></svg></span>
  <span class="fy-updated"><svg><use href="#i-calendar"/></svg>Last updated 15th Sep</span></div>
<div class="fy-section-card">
  <div class="fy-section-card__head"><div><p class="fy-section-card__title">Assets</p><p class="fy-section-card__sub">Your investments &amp; savings</p></div><span class="fy-total-pill">₹ 70.5 L</span></div>
  <!-- or <button class="fy-retry"><svg><use href="#i-refresh"/></svg>retry</button> instead of the pill -->
  <button class="fy-asset-row" style="--row-tint:var(--fy-tint-surplus)"><span class="fy-asset-row__icon"><svg><use href="#i-sprout"/></svg></span>
    <span class="fy-asset-row__name">Mutual Funds<small>you own 50%</small></span>
    <span class="fy-asset-row__value">₹ 5.31 L<small [class="is-stale"]>Today</small></span><svg class="fy-chevron"><use href="#i-chev-right"/></svg></button>
  <button class="fy-add-link">Add more assets</button>
</div>
<span class="fy-amount-pill">₹ 12.3 L</span>
<div class="fy-kpis [fy-kpis--sm]"><div class="fy-kpi"><span class="fy-kpi__label">Returns % <button class="fy-sort" aria-label="Sort"><svg><use href="#i-selector"/></svg></button></span><span class="fy-kpi__value is-gain">+21.1%</span></div>×3</div>
<article class="fy-holding">
  <div class="fy-holding__head"><span class="fy-holding__logo">AX</span><span class="fy-holding__name">Axis bank<span class="fy-holding__meta">Qty. 20 • Avg. ₹1.2k • LTP ₹1.2k</span></span><span class="fy-holding__value">₹ 32.3 cr<small>Current value</small></span></div>
  <hr><div class="fy-kpis fy-kpis--sm">…</div>
</article>
<p class="fy-subhead">All stocks <span class="fy-count">11</span></p>
<div class="fy-cat-tabs"><button aria-pressed="true"><svg><use href="#i-candles"/></svg>Stocks</button>…</div>
<nav class="fy-bnb" aria-label="Main"><a aria-current="page" href="#"><svg><use href="#i-home"/></svg>Home</a><a href="#"><svg><use href="#i-wallet"/></svg>Cashflow</a><a href="#"><svg><use href="#i-fire"/></svg>Fire Age</a><a href="#"><svg><use href="#i-user"/></svg>Profile</a></nav>
<label class="fy-select-row"><svg>…</svg><span>Mutual funds</span><input class="fy-radio" type="checkbox"></label>   <!-- asset picker -->
```

## Transactions

```html
<div class="fy-filterbar"><button class="fy-icon-chip" aria-label="All filters"><svg><use href="#i-sliders"/></svg></button><button class="fy-dropdown-chip" [aria-pressed="true"]>Month<svg><use href="#i-chev-down"/></svg></button>…</div>
<div class="fy-group-head">Sep’25 <b class="is-gain">+ ₹ 1,02,209</b></div>
<div class="fy-txn"><span class="fy-avatar">JD<span class="fy-avatar__badge">A</span></span>
  <span class="fy-txn__body"><span class="fy-txn__name">John Doe</span><span class="fy-txn__tags"><button class="fy-tag-chip">People</button><button class="fy-tag-chip fy-tag-chip--add">+ Tag</button></span></span>
  <span class="fy-txn__amount"><span class="is-gain">+ ₹ 3,504</span><small>29 Sep’25</small></span></div>
<div class="fy-filters">
  <div class="fy-filters__rail" role="tablist" aria-orientation="vertical"><button role="tab" aria-selected="true"><span class="fy-badge">4</span><svg><use href="#i-tag"/></svg>Tags</button>…</div>
  <div class="fy-filters__panel" role="radiogroup"><label class="fy-radio-card">Date : Newest first<input class="fy-radio" type="radio" name="sort" checked></label>…</div>
</div>
<label class="fy-check-row">Salary<input class="fy-checkbox" type="checkbox"></label>
<div class="fy-btn-row"><button class="fy-btn fy-btn--secondary">Clear All</button><button class="fy-btn fy-btn--primary" disabled>Apply</button></div>
```

## Cashflow

```html
<button class="fy-title-toggle"><svg><use href="#i-info"/></svg>Total<svg><use href="#i-selector"/></svg></button>
<div class="fy-stepper"><button aria-label="Previous month"><svg><use href="#i-chev-left"/></svg></button>October’25<button aria-label="Next month"><svg><use href="#i-chev-right"/></svg></button></div>
<div class="fy-periods"><button aria-pressed="true">1M</button><button aria-pressed="false">3M</button>…6M 1Y</div>
<div class="fy-amount-card"><span class="fy-amount-card__label">Incoming</span><span class="fy-amount-card__value">₹ 4.10 L</span></div>
<p class="fy-subhead">Outgoing <span>₹ 3.90 L</span></p>
<button class="fy-breakdown fy-breakdown--spends" style="--share:28%"><span class="fy-breakdown__icon"><svg><use href="#i-wallet"/></svg></span><span class="fy-breakdown__label">Spends</span><span class="fy-breakdown__value">₹ 1.16 L</span><svg class="fy-chevron"><use href="#i-chev-right"/></svg></button>
<!-- variants: --spends --investment --loans --untagged --surplus (green value) --shortfall (red value); --share = category share of total -->
<div class="fy-gauge" style="--value:88"><span class="fy-gauge__label">Cashflow Health</span><span class="fy-gauge__arc"></span><span class="fy-gauge__value">Excellent</span></div>  <!-- --value 0–100 -->
<label class="fy-switch-row">Monthly <input class="fy-switch" type="checkbox"> Yearly</label>
<p class="fy-note"><svg><use href="#i-info"/></svg>All values have been averaged out based on yearly spends</p>
```

## FIRE

```html
<div class="fy-timeline">
  <div class="fy-timeline__now">Today<small>32 years</small></div>
  <button class="fy-fire-card"><span class="fy-fire-card__icon"><svg><use href="#i-heart"/></svg></span><span class="fy-fire-card__text"><span class="fy-fire-card__title">Survive FIRE</span><span class="fy-fire-card__sub">₹ 10.5 cr</span></span><span class="fy-fire-card__stat">50<small>years</small></span></button>
  <button class="fy-fire-card fy-fire-card--locked">…<span class="fy-fire-card__add">+</span></button>
</div>
<div class="fy-ornament">✦</div>
<div class="fy-screen fy-fire-dark">  <!-- dark result screens -->
  <span class="fy-alert-pill"><svg><use href="#i-alert"/></svg>Not on track for early retirement</span>
  <h1 class="fy-hero__title">Early retirement isn’t possible at your pace. <span class="fy-accent">But Finny can get you there.</span></h1>
  <div class="fy-compare"><div><div class="fy-compare__card"><small>FIRE Age</small><b>77</b><small>years</small></div><div class="fy-compare__legend">Your pace</div></div>
    <div>…<div class="fy-compare__legend" style="--dot:var(--fy-success-600)">With Finny</div></div></div>
</div>
<div class="fy-tier-tabs"><button aria-pressed="true" style="--tier:#B85A47"><i></i>Basic</button>…Secure…Aspire</div>
<div class="fy-value-row"><span class="fy-value-row__label">Increase in income<small>Per year</small></span><span class="fy-value-row__value">10%</span><button class="fy-edit" aria-label="Edit"><svg><use href="#i-pencil"/></svg></button></div>
<div class="fy-slider">
  <div class="fy-slider__head"><span class="fy-slider__title">Down payment<small>At current value</small></span>
    <span class="fy-slider__value"><span class="fy-value-box">₹ 2.5 <small>cr</small></span><span class="fy-slider__hint">₹ 3.5 cr at redemption</span></span></div>
  <input class="fy-range" type="range" min="0" max="100" value="14" style="--pct:14%">   <!-- update --pct on input -->
  <div class="fy-slider__scale"><span>Lower</span><span>Same as today</span><span>Higher</span></div>
</div>
<div class="fy-wheel" role="listbox"><button role="option" aria-selected="false">2025</button><button role="option" aria-selected="true">2026</button>…</div>
<div class="fy-goal-card"><span class="fy-art">…</span><p class="fy-goal-card__title">Buying a house</p></div>
<div class="fy-goal-icons"><button aria-pressed="true"><svg><use href="#i-house-loan"/></svg></button>…</div>
```

## Profile and loading

```html
<span class="fy-avatar fy-avatar--lg">JD</span>
<div class="fy-list-group"><p class="fy-list-group__title">Account</p><a href="#">Logout<svg class="fy-chevron"><use href="#i-chev-right"/></svg></a><a href="#">Delete Account…</a></div>
<span class="fy-skeleton" style="width:60%"></span>
```

## Small JS the components expect

```js
// single-select groups (members, periods, chips, tabs)
document.querySelectorAll('[data-group]').forEach(g => g.addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  const attr = b.hasAttribute('aria-checked') ? 'aria-checked' : 'aria-pressed';
  g.querySelectorAll('button').forEach(x => x.setAttribute(attr, String(x === b)));
}));
// sliders
document.querySelectorAll('.fy-range').forEach(r => { const p = () => r.style.setProperty('--pct', (r.value - r.min) / (r.max - r.min) * 100 + '%'); r.oninput = p; p(); });
// OTP auto-advance
document.querySelectorAll('[data-otp]').forEach(row => { const c = [...row.querySelectorAll('input')];
  c.forEach((el, i) => { el.oninput = () => { el.value = el.value.replace(/\D/g, '').slice(-1); if (el.value) c[i + 1]?.focus(); };
    el.onkeydown = e => { if (e.key === 'Backspace' && !el.value) c[i - 1]?.focus(); }; }); });
```
