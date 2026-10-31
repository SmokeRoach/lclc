# Low Cost Legends Club (LCLC) by SmokeRoach

> **Suggested GitHub repo name: `lclc`** → the site will live at `https://smokeroach.github.io/lclc/` (already set as `SITE_URL` in `build.py`, and used by the hub card). This folder is still called `smokeroach-savers` locally; renaming it is optional.

## Brand marks (for designs and merch)
Outlined SVGs (no font needed, print-safe) plus PNG renders in `assets/img/`:
- `lclc-badge.svg` / `.png` (2000px, transparent): round club badge, "LOW COST LEGENDS CLUB · BY SMOKEROACH" around "LCLC"
- `lclc-mark.svg` / `.png` (512px): compact LCLC roundel (header/avatar/favicon use)
- `lclc-wordmark.svg` / `.png`: horizontal "LOW COST LEGENDS CLUB / BY SMOKEROACH"
Regenerate with `python3 tools/make_logo.py && python3 tools/render_png.py`. Always show "by SmokeRoach" with the name. Colours: yellow #ffd60a, green #7cff3a, pink #ff2bd6, ink #05010c.

(Previously "SmokeRoach Savers".)

A standalone money-saving travel site for SmokeRoach (Scott, Charlotte and Gunner). It's plain static HTML/CSS/JS with no runtime dependencies, so you can host it on GitHub Pages as its own repo. It's separate from the hub (`smokeroach-site`), which only has one removable link card pointing here.

## Edit payments / member links: ONE file
`assets/js/config.js`
- `checkout.tier1` / `checkout.tier2` hold the Whop checkout links. While empty, the buttons show "checkout opening soon".
- `tier3Live: false` keeps Tier 3 as "Coming soon" with a waitlist mailto. Set it to true and add `checkout.tier3` at launch.
- `memberHub`, `memberLibrary.tier1/tier2` hold the Whop members'-area links used by "Already a member?" buttons and the Account page.
- `prices` change the text. Run `python3 build.py` after changing them.

## Content
- Free guides (full text, public) go in `content/free/*.md`.
- Locked guides (Tier 1 / Tier 2) are deliberately **not in this repo**. They live in `../smokeroach-savers-private/tier1|tier2/*.md`. The public site only shows title, teaser and "what's inside" (cached in `data/locked-guides.json`). A static site can't really lock text, so anything you commit here is public.
- `python3 build.py` regenerates every page and writes paste-ready HTML for Whop to `../smokeroach-savers-private/whop-export/`.
- Requires `pip install markdown`.

Front matter: `title, slug, tier (free|tier1|tier2), emoji, order, teaser, inside (a | b | c), video (YouTube id, optional)`.

## Before going live (checklist)
1. Fill `[TRADING NAME]` / `[BUSINESS ADDRESS]` in `build.py` (footer and legal pages), and the goodwill-refund line in `refunds.html`.
2. Fill Tier 2 codes in the private `tier2/01-codes-vault.md` with real codes only.
3. Paste the Whop links into `config.js`. In Whop, add the 14-day-waiver consent and refund policy to checkout.
4. Set `SITE_URL` in `build.py` if the address isn't `https://smokeroach.github.io/lclc/`, and update the hub card href to match.

## Preview locally
`python3 -m http.server 8090` then open http://127.0.0.1:8090/

## Guide covers

The guide covers in `assets/img/covers/` are original illustrations made for LCLC, with the LCLC mark added on top. They are not stock photos, so no third-party credit is needed. There are no people and no cannabis imagery in them.
