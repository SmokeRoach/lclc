#!/usr/bin/env python3
"""Build Low Cost Legends Club (LCLC) by SmokeRoach into static HTML (output lives in this folder, ready for GitHub Pages).

  python3 build.py

- Free guides: content/free/*.md  -> full pages in guides/
- Locked guides (Tier 1 / Tier 2): full text lives OUTSIDE this repo in
  ../smokeroach-savers-private/{tier1,tier2}/*.md . The public site only gets
  title / teaser / "what's inside" (cached in data/locked-guides.json so the
  site still builds without the private folder). Full text is exported to
  ../smokeroach-savers-private/whop-export/ for pasting into Whop.
"""
import html, json, re, sys, pathlib
import markdown

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = ROOT.parent / "smokeroach-savers-private"
SITE_URL = "https://smokeroach.github.io/lclc/"  # used for sitemap/canonical/404 only
UPDATED = "30 October 2026"
BRAND = "Low Cost Legends Club"
BRAND_FULL = "Low Cost Legends Club by SmokeRoach"
SHORT = "LCLC"
CHANNEL = "https://www.youtube.com/@smoke_roach"

cfg_txt = (ROOT / "assets/js/config.js").read_text()
CFG = json.loads(cfg_txt[cfg_txt.index("{", cfg_txt.index("SAVERS_CONFIG")):cfg_txt.rindex("}") + 1])
P = CFG["prices"]; CUR = CFG["currency"]

VIDEOS = {
    "6rVBsnNTFK4": ("£99 Amsterdam Day Trip: Price Challenge #1", "https://www.youtube.com/watch?v=6rVBsnNTFK4"),
    "kis9rcRZRwM": ("£249 All-Inclusive Mallorca: Price Challenge #2", "https://www.youtube.com/watch?v=kis9rcRZRwM"),
    "d8-CQOA8cyE": ("Amsterdam to Liverpool for £42 by coach + ferry", "https://www.youtube.com/watch?v=d8-CQOA8cyE"),
    "fPkkqX6zvn0": ("We stayed in the worst hotel in Amsterdam", "https://www.youtube.com/watch?v=fPkkqX6zvn0"),
    "7_8CuFV_sDA": ("The airport quiet-room tip (Short)", "https://www.youtube.com/shorts/7_8CuFV_sDA"),
    "yoJvbCu2F1I": ("Liverpool to Amsterdam and back for £50 (Short)", "https://www.youtube.com/shorts/yoJvbCu2F1I"),
}
TIER_LABEL = {"free": "Free", "tier1": "Tier 1", "tier2": "Tier 2"}
TIER_FULL = {"tier1": f"Tier 1 · {CUR}{P['tier1']}/month", "tier2": f"Tier 2 · {CUR}{P['tier2']}/month"}

def esc(s): return html.escape(str(s), quote=True)

def parse(path):
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    meta["order"] = int(meta.get("order", 99))
    meta["inside"] = [x.strip() for x in meta.get("inside", "").split("|") if x.strip()]
    meta["body"] = m.group(2)
    return meta

def md(text):
    out = markdown.markdown(text, extensions=["tables", "sane_lists"])
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)
    return out

# ---------- load guides ----------
free = sorted([parse(p) for p in (ROOT / "content/free").glob("*.md")], key=lambda g: g["order"])
locked_json = ROOT / "data/locked-guides.json"
if PRIVATE.exists():
    locked = []
    for t in ("tier1", "tier2"):
        locked += sorted([parse(p) for p in (PRIVATE / t).glob("*.md")], key=lambda g: g["order"])
    locked_json.parent.mkdir(exist_ok=True)
    locked_json.write_text(json.dumps([{k: v for k, v in g.items() if k != "body"} for g in locked], indent=2, ensure_ascii=False))
else:
    print("! private folder not found, using cached data/locked-guides.json (no Whop export)")
    locked = json.loads(locked_json.read_text())
t1 = [g for g in locked if g["tier"] == "tier1"]
t2 = [g for g in locked if g["tier"] == "tier2"]
ALL = free + t1 + t2

# ---------- shared bits ----------
NAV = [("index.html", "Home"), ("guides.html", "Guides"), ("pricing.html", "Pricing"), ("account.html", "Account")]

def honesty(r, compact=False, tag="h2"):
    t = "h3" if compact else tag
    return f"""<aside class="honesty{' compact' if compact else ''}" aria-label="Our honesty promise">
  <span class="badge">✋ Straight up</span>
  <{t}>You could do all of this <span class="hl-g">yourself</span></{t}>
  <p>Every saver on this site is something you could work out on your own with enough time and patience. We're Scott and Charlotte (plus Gunner) from Liverpool, and we've <strong>trial-and-errored it across loads of trips</strong> to find the best possible price. You're paying for our shortcuts, not secrets.</p>
  <p><span class="flag">🇬🇧 For British travellers only.</span> Everything is tested for getting the best price as a UK traveller, from UK airports, in pounds. <strong>We can't speak for other countries.</strong></p>
  {'' if compact else '<p class="muted">Prices are what we paid or found when we checked, and each guide says when. They change, so always check before you book.</p>'}
</aside>"""

def head(title, desc, r, path):
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE_URL}assets/img/crew.webp">
<meta property="og:type" content="website">
<meta name="theme-color" content="#05010c">
<meta property="og:site_name" content="{BRAND_FULL}">
<meta name="application-name" content="{SHORT}">
<link rel="icon" href="{r}favicon.ico" sizes="any">
<link rel="icon" href="{r}assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preload" href="{r}assets/fonts/anton.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/outfit.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="{BRAND_FULL}: home"><img src="{r}assets/img/lclc-mark.svg" alt="" width="36" height="36"><span><b class="b-full">Low Cost <em>Legends</em> Club</b><b class="b-short">LC<em>LC</em></b><small>BY SMOKEROACH</small></span></a>
    <nav class="nav" aria-label="Main">{''.join(f'<a href="{r}{h}"' + (' aria-current="page"' if path == h else '') + f'>{l}</a>' for h, l in NAV)}</nav>
    <a class="btn btn-green btn-sm" href="{r}pricing.html">Join from {CUR}{P['tier1']}</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="Menu">☰</button>
  </div>
  <nav id="mnav" class="mnav" aria-label="Mobile">{''.join(f'<a href="{r}{h}">{l}</a>' for h, l in NAV)}<a href="{CFG['hubUrl']}">← SmokeRoach hub</a></nav>
</header>
<main id="main">
"""

def foot(r):
    return f"""</main>
<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="{r}index.html"><img src="{r}assets/img/lclc-mark.svg" alt="" width="36" height="36" loading="lazy"><span><b>Low Cost <em>Legends</em> Club</b><small>BY SMOKEROACH</small></span></a>
      <p class="fine">Budget travel savers from Scott, Charlotte and Gunner, tested on our own trips, for UK travellers. Everything here is general info, not financial or legal advice. Prices change, so always check before you book. Follow local laws wherever you go.</p>
      <p class="fine">{BRAND_FULL} ({SHORT}) is the trading name of <span class="todo">[SCOTT: YOUR LEGAL NAME, AS A SOLE TRADER]</span>. Contact: <a href="mailto:{CFG['contactEmail']}">{CFG['contactEmail']}</a></p>
    </div>
    <nav aria-label="Footer">
      <a href="{r}guides.html">All guides</a><a href="{r}pricing.html">Pricing</a><a href="{r}account.html">Account</a>
      <a href="{r}terms.html">Terms</a><a href="{r}refunds.html">Refunds &amp; cancellation</a><a href="{r}privacy.html">Privacy</a>
      <a href="{CHANNEL}" target="_blank" rel="noopener">YouTube</a><a href="{CFG['hubUrl']}">SmokeRoach hub</a>
    </nav>
  </div>
</footer>
<script src="{r}assets/js/config.js"></script>
<script src="{r}assets/js/main.js" defer></script>
</body>
</html>
"""

def chip(t):
    lock = "" if t == "free" else "🔒 "
    return f'<span class="chip {t}">{lock}{TIER_LABEL[t]}</span>'

def gcard(g, r):
    lk = " locked" if g["tier"] != "free" else ""
    more = "Read free →" if g["tier"] == "free" else "See what's inside →"
    return f"""<a class="card gcard{lk}" href="{r}guides/{g['slug']}.html">
  <div class="gtop"><span class="gemo" aria-hidden="true">{g['emoji']}</span>{chip(g['tier'])}</div>
  <b>{esc(g['title'])}</b><p>{esc(g['teaser'])}</p><span class="more">{more}</span></a>"""

def tier_cards(r):
    return f"""<div class="tiers">
  <div class="card tier t1" id="tier1">
    <span class="tname">Tier 1 · Savers</span>
    <div class="price"><span data-price="tier1">{CUR}{P['tier1']}</span> <small>/ month</small></div>
    <p class="tag">Our travel tips, hacks and cheapest places.</p>
    <ul><li>Every Tier 1 travel tip and hack</li><li>Cheapest places to go from the UK, kept up to date</li><li>Where-to-go and what-to-do guides from our trips</li><li>Full write-ups of our Price Challenges, receipts and all</li><li>Cancel any time</li></ul>
    <div><a class="btn btn-ghost btn-block" data-checkout="tier1" href="{r}pricing.html#tier1">Get Tier 1 · {CUR}{P['tier1']}/mo</a><span class="btn-note"></span></div>
  </div>
  <div class="card tier t2" id="tier2">
    <span class="ribbon">Best value</span>
    <span class="tname">Tier 2 · Insiders</span>
    <div class="price"><span data-price="tier2">{CUR}{P['tier2']}</span> <small>/ month</small></div>
    <p class="tag">Everything in Tier 1, plus our hidden gems and codes.</p>
    <ul><li><strong>Everything in Tier 1</strong></li><li>Our hidden gems, and how to do them cheap</li><li>Coupon codes exclusive to SmokeRoach subscribers</li><li>The stacking playbook: codes + cashback + the right card</li><li>Cancel any time</li></ul>
    <div><a class="btn btn-green btn-block" data-checkout="tier2" href="{r}pricing.html#tier2">Get Tier 2 · {CUR}{P['tier2']}/mo</a><span class="btn-note"></span></div>
  </div>
  <div class="card tier t3" id="tier3">
    <span class="ribbon soon">Coming soon</span>
    <span class="tname">Tier 3 · Crew</span>
    <div class="price"><span data-price="tier3">{CUR}{P['tier3']}</span> <small>/ month</small></div>
    <p class="tag">Everything in Tier 2, plus us on speed dial.</p>
    <ul><li><strong>Everything in Tier 2</strong></li><li>Direct messages with us, with 1-hour responses*, when you're using one of our offers or want money-saving advice</li><li>A mention on this website</li><li>Entry into our monthly SmokeRoach merch giveaways**</li></ul>
    <div><a class="btn btn-pink btn-block" data-checkout="tier3" href="mailto:{CFG['contactEmail']}?subject=Tier%203%20waitlist&amp;body=Put%20me%20on%20the%20Low%20Cost%20Legends%20Club%20Tier%203%20waitlist%20please!">Join the waitlist</a><span class="btn-note">Not on sale yet. We'll email you when it opens.</span></div>
  </div>
</div>
<p class="muted" style="font-size:13px;margin-top:14px">*Response times and hours will be confirmed before Tier 3 launches. **Giveaway rules, including a free way to enter, will be published before launch. Prices include any VAT that applies. Subscriptions renew monthly until you cancel. See our <a href="{r}terms.html">terms</a> and <a href="{r}refunds.html">refunds &amp; cancellation</a>.</p>"""

def vcard(vid, r):
    t, u = VIDEOS[vid]
    return f'<a class="card vcard" href="{u}" target="_blank" rel="noopener"><img src="{r}assets/img/v/{vid}.webp" alt="" width="320" height="180" loading="lazy"><div><b>{esc(t)}</b><small>Watch on YouTube ↗</small></div></a>'

def write(rel, content):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)

# ---------- index ----------
r = ""
idx = head(f"{BRAND_FULL}: budget travel tips for UK travellers", "Low Cost Legends Club (LCLC): money-saving travel guides from SmokeRoach (Scott, Charlotte and Gunner). Free starter guides, plus members' guides from £4.99/month. Tested on our trips, for UK travellers.", r, "index.html")
idx += f"""<section class="hero"><div class="wrap">
  <div>
    <img class="brand-badge" src="assets/img/lclc-badge.svg" alt="LCLC: Low Cost Legends Club by SmokeRoach" width="200" height="200">
    <span class="kicker k-green">Low Cost Legends Club · by SmokeRoach</span>
    <h1>Travel <span class="hl">cheaper.</span><br>Properly cheaper.</h1>
    <p class="lede">Budget travel savers from a Liverpool couple and their dog who try to do Europe for less than everyone else. Real receipts from our videos, tested on our own trips, written for UK travellers.</p>
    <div class="cta-row"><a class="btn btn-green btn-big" href="guides.html#free">Read the free guides</a><a class="btn btn-ghost btn-big" href="#tiers">See membership</a></div>
    <ul class="pills"><li>🇬🇧 For UK travellers</li><li>🧾 Real receipts</li><li>💷 From {CUR}{P['tier1']}/month</li><li>✌️ Cancel any time</li></ul>
  </div>
  <div class="hero-art"><img src="assets/img/crew.webp" alt="Cartoon of Scott, Charlotte and Gunner the dog walking together: SmokeRoach Budget Travel Crew" width="552" height="516"><span class="sticker">Tested on our trips</span></div>
</div></section>
<section style="padding-top:10px"><div class="narrow">{honesty(r)}</div></section>
<section id="free"><div class="wrap">
  <span class="kicker k-green">Free for everyone</span><h2>Start <span class="hl">here</span></h2>
  <p class="lede">Our basic money savers, free. No sign-up, no catch.</p>
  <div class="ggrid">{''.join(gcard(g, r) for g in free)}</div>
</div></section>
<section id="tiers"><div class="wrap">
  <span class="kicker k-yellow">Membership</span><h2>Pick your <span class="hl">tier</span></h2>
  <p class="lede">About 80% of our guides are for members. That's where the full trip breakdowns, cheapest-places lists, hidden gems and exclusive codes live.</p>
  {tier_cards(r)}
</div></section>
<section><div class="wrap">
  <span class="kicker k-cyan">Inside the members' library</span><h2>{len(t1) + len(t2)} guides <span class="hl">and counting</span></h2>
  <div class="ggrid">{''.join(gcard(g, r) for g in (t1[:3] + t2[:3]))}</div>
  <p style="margin-top:18px"><a class="btn btn-ghost" href="guides.html">Browse every guide →</a></p>
</div></section>
<section><div class="wrap">
  <span class="kicker k-pink">Where the tips come from</span><h2>Watch the <span class="hl">challenges</span></h2>
  <div class="vgrid">{vcard('6rVBsnNTFK4', r)}{vcard('kis9rcRZRwM', r)}{vcard('d8-CQOA8cyE', r)}</div>
</div></section>
"""
idx += foot(r)
write("index.html", idx)

# ---------- guides library ----------
lib = head(f"All guides | {BRAND_FULL}", "Every Low Cost Legends Club guide: free starter guides plus Tier 1 and Tier 2 members' guides.", r, "guides.html")
lib += f"""<section><div class="wrap">
  <span class="kicker k-green">The library</span><h1>Every <span class="hl">guide</span></h1>
  <p class="lede">{len(free)} free, {len(t1)} for Tier 1, {len(t2)} for Tier 2. New ones land after every trip.</p>
  <div class="gfilter"><a href="#free">🟢 Free ({len(free)})</a><a href="#tier1">🔒 Tier 1 ({len(t1)})</a><a href="#tier2">🔒 Tier 2 ({len(t2)})</a></div>
  {honesty(r, compact=True)}
  <div class="lib-head" id="free"><div><h2>Free <span class="hl-g">savers</span></h2><p>Open to everyone.</p></div></div>
  <div class="ggrid">{''.join(gcard(g, r) for g in free)}</div>
  <div class="lib-head" id="tier1"><div><h2>Tier 1 <span class="hl">library</span></h2><p>Travel tips, hacks, cheapest places, and where to go and what to do. {CUR}{P['tier1']}/month.</p></div><a class="btn btn-ghost btn-sm" href="pricing.html#tier1">Unlock Tier 1</a></div>
  <div class="ggrid">{''.join(gcard(g, r) for g in t1)}</div>
  <div class="lib-head" id="tier2"><div><h2>Tier 2 <span class="hl">library</span></h2><p>Hidden gems, how to do them cheap, and exclusive codes. Includes all of Tier 1. {CUR}{P['tier2']}/month.</p></div><a class="btn btn-green btn-sm" href="pricing.html#tier2">Unlock Tier 2</a></div>
  <div class="ggrid">{''.join(gcard(g, r) for g in t2)}</div>
</div></section>
"""
lib += foot(r)
write("guides.html", lib)

# ---------- guide pages ----------
def related(g, r):
    pool = [x for x in ALL if x["slug"] != g["slug"]]
    pick = [x for x in pool if x["tier"] == g["tier"]][:2] + [x for x in pool if x["tier"] != g["tier"]][:1]
    return f'<div class="related"><h2>Keep <span class="hl">saving</span></h2><div class="ggrid">{"".join(gcard(x, r) for x in pick)}</div></div>'

def vid_block(g, r):
    v = g.get("video")
    if not v or v not in VIDEOS: return ""
    t, u = VIDEOS[v]
    return f'<div class="card vid-embed"><a href="{u}" target="_blank" rel="noopener"><img src="{r}assets/img/v/{v}.webp" alt="" width="140" height="79" loading="lazy"><span><small>▶ THE VIDEO THIS IS BASED ON</small><b>{esc(t)}</b></span></a></div>'

r = "../"
for g in ALL:
    tier = g["tier"]
    page = head(f"{g['title']} | {BRAND_FULL}", g["teaser"], r, f"guides/{g['slug']}.html")
    page += f"""<article class="narrow">
  <p class="crumbs"><a href="{r}guides.html">Guides</a> › <a href="{r}guides.html#{tier}">{TIER_LABEL[tier]}</a></p>
  <header class="ghead"><div class="meta">{chip(tier)}<span>Checked {UPDATED}</span></div><h1>{g['emoji']} {esc(g['title'])}</h1><p class="lede">{esc(g['teaser'])}</p></header>
  {honesty(r, compact=True)}
  <div style="height:22px"></div>
  {vid_block(g, r)}
"""
    if tier == "free":
        page += f'<div class="prose">{md(g["body"])}</div>'
        page += f"""<div class="card unlock-box" style="margin:34px auto 0"><div class="lock">🗝️</div><h2>Want the full <span class="hl">playbook?</span></h2><p>This is one of our free starters. Members get {len(t1) + len(t2)}+ full guides, including our Price Challenge breakdowns, the cheapest places from the UK, hidden gems and exclusive codes.</p><div class="btns"><a class="btn btn-green" href="{r}pricing.html">See membership from {CUR}{P['tier1']}/month</a></div></div>"""
    else:
        need = "Tier 1 or Tier 2" if tier == "tier1" else "Tier 2"
        btn_t = tier
        page += f"""<div class="card inside"><h2>What's <span class="hl">inside</span></h2><ul>{''.join(f'<li>{esc(i)}</li>' for i in g['inside'])}</ul></div>
  <div class="fog card">
    <div class="lines" aria-hidden="true">{''.join(f'<i style="width:{w}%"></i>' for w in (92, 85, 97, 60, 88, 94, 72, 90, 81, 55))}</div>
    <div class="unlock"><div class="card unlock-box"><div class="lock">🔒</div><h2>Members' <span class="hl">guide</span></h2>
      <p>The full guide is for {need} members ({TIER_FULL[tier]}{', includes all of Tier 1' if tier == 'tier2' else ''}).</p>
      <div class="btns"><a class="btn btn-green" data-checkout="{btn_t}" href="{r}pricing.html#{btn_t}">Unlock with {TIER_LABEL[tier]} · {CUR}{P[tier]}/mo</a><span class="btn-note"></span>
      <a class="btn btn-ghost btn-sm" data-member="{tier}" href="{r}account.html">Already a member? Read it in the members' area</a></div></div></div>
  </div>"""
    page += related(g, r) + "</article>"
    page += foot(r)
    write(f"guides/{g['slug']}.html", page)

# ---------- pricing ----------
r = ""
faq = [
    ("Couldn't I just do all this myself?", "Yes, honestly. Everything here is something you could work out yourself. We've just done the trial and error across loads of trips, so you get the shortcuts without the bedbugs (long story, it's in a video)."),
    ("I'm not from the UK. Will it work for me?", "Probably not as well. Everything is tested for British travellers: UK airports, UK cards, pounds and UK rules. We can't speak for other countries."),
    ("How do I pay, and who handles it?", f"Payments and member access are handled securely by {CFG['provider']}. We never see or store your card details."),
    ("Where do I read the members' guides?", f"After you subscribe you get access to the members' area on {CFG['provider']}, where the full guides and codes live. The guide pages on this site show what's inside each one."),
    ("Can I cancel?", f"Any time. Cancel from your {CFG['provider']} account (Profile → Orders) and you keep access until the end of the month you've paid for. Full details are in our refunds & cancellation policy."),
    ("Are the coupon codes guaranteed?", "Codes come from brands and have their own terms and expiry dates. We list the terms with each code and remove dead ones as soon as we know."),
    ("When is Tier 3 coming?", "Soon. Join the waitlist and we'll email you when it opens. It isn't on sale yet, so you can't be charged for it."),
]
pr = head(f"Pricing | {BRAND_FULL}", f"Low Cost Legends Club membership: Tier 1 {CUR}{P['tier1']}/month, Tier 2 {CUR}{P['tier2']}/month, Tier 3 coming soon.", r, "pricing.html")
pr += f"""<section><div class="wrap">
  <span class="kicker k-yellow">Membership</span><h1>Simple <span class="hl">pricing</span></h1>
  <p class="lede">Monthly, cancel any time. Start with the free guides if you want to see how we work first.</p>
  <div style="margin:0 0 30px">{honesty(r)}</div>
  {tier_cards(r)}
  <div class="card free-row"><p><strong>Not ready?</strong> <span class="muted">{len(free)} guides are free for everyone, no sign-up needed.</span></p><a class="btn btn-ghost btn-sm" href="guides.html#free">Read the free guides</a></div>
</div></section>
<section style="padding-top:10px"><div class="narrow faq"><h2>Questions</h2>{''.join(f'<details class="card"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)}</div></section>
"""
pr += foot(r)
write("pricing.html", pr)

# ---------- account ----------
ac = head(f"Account | {BRAND_FULL}", "Log in to the Low Cost Legends Club members' area.", r, "account.html")
ac += f"""<section><div class="narrow">
  <span class="kicker k-cyan">Members</span><h1>Your <span class="hl">account</span></h1>
  <p class="lede">Accounts, logins and payments are handled by {CFG['provider']}, so there are no passwords on this site.</p>
  <div class="card unlock-box" style="margin:0 auto 22px;max-width:none;text-align:left">
    <h2>Members' area</h2><p>Read the full Tier 1 and Tier 2 guides and the codes vault.</p>
    <div class="btns"><a class="btn btn-green" data-member="hub" href="#">Log in to the members' area</a>
    <a class="btn btn-ghost" data-member="manage" href="#">Manage or cancel my subscription</a></div>
  </div>
  <div class="card" style="padding:22px"><h3>Not a member yet?</h3><p class="muted">Start with the free guides, or join from {CUR}{P['tier1']}/month.</p><div class="cta-row"><a class="btn btn-ghost btn-sm" href="guides.html#free">Free guides</a><a class="btn btn-green btn-sm" href="pricing.html">See pricing</a></div></div>
  <p class="muted" style="margin-top:20px;font-size:15px">Can't get in? Email <a href="mailto:{CFG['contactEmail']}">{CFG['contactEmail']}</a> with the email address you subscribed with.</p>
</div></section>
"""
ac += foot(r)
write("account.html", ac)

# ---------- legal ----------
TODO = lambda s: f'<span class="todo">[{s}]</span>'
legal = {
"terms.html": ("Terms of service", f"""
<p>Last updated: {UPDATED}</p>
<p>These terms apply to {BRAND_FULL} ("{SHORT}", the "site") and our paid memberships. {BRAND_FULL} is the trading name of {TODO('SCOTT: YOUR LEGAL NAME, AS A SOLE TRADER')}, {TODO('BUSINESS ADDRESS')} ("we", "us"). Contact: <a href="mailto:{CFG['contactEmail']}">{CFG['contactEmail']}</a>.</p>
<h2>1. What we offer</h2>
<p>Free guides open to everyone, plus monthly memberships: Tier 1 ({CUR}{P['tier1']}/month) and Tier 2 ({CUR}{P['tier2']}/month). Tier 3 ({CUR}{P['tier3']}/month) is not on sale yet. Joining its waitlist is not a purchase and creates no contract.</p>
<h2>2. Our content is general information</h2>
<p>Our guides share what has worked for us as UK travellers. You could find all of it yourself. It is general information, not financial, legal, immigration or medical advice. Prices, rules and offers change, and each guide says when we checked it. Always check the current price and rules before you book. We're not responsible for bookings you make with third parties.</p>
<h2>3. UK travellers</h2>
<p>Our content is written for people travelling from the UK. We can't speak for other countries.</p>
<h2>4. Payments and renewal</h2>
<p>Memberships are sold and billed through {CFG['provider']}, which also handles your account and access. By subscribing you also agree to {CFG['provider']}'s buyer terms. Your membership renews automatically each month at the price shown when you joined until you cancel. If we change a price, we'll tell you at least 30 days before it affects your next payment, and you can cancel before then.</p>
<h2>5. Cancelling</h2>
<p>You can cancel at any time from your {CFG['provider']} account. Your access continues until the end of the period you've paid for. See our <a href="refunds.html">refunds &amp; cancellation policy</a> for your legal rights, including the 14-day cancellation period.</p>
<h2>6. Your membership is personal</h2>
<p>Please don't share your login, or copy or republish members' guides or subscriber codes. We may suspend memberships that do, after contacting you where reasonable.</p>
<h2>7. Coupon codes</h2>
<p>Codes are provided by third-party brands under their own terms, minimum spends and expiry dates. We can't guarantee a code will be accepted, but we'll remove codes we know have expired.</p>
<h2>8. Tier 3 extras (when launched)</h2>
<p>Response times, messaging hours and giveaway rules (including a free entry route) will be published before Tier 3 goes on sale.</p>
<h2>9. Our responsibility to you</h2>
<p>Nothing in these terms limits your rights under UK consumer law, including the Consumer Rights Act 2015. If digital content we supply is faulty, you have legal rights to a repair, replacement or refund. We aren't liable for losses that weren't foreseeable, or for business losses.</p>
<h2>10. Law</h2>
<p>These terms are governed by the law of England and Wales. If you live elsewhere in the UK, you can also bring claims in your local courts.</p>"""),
"refunds.html": ("Refunds & cancellation", f"""
<p>Last updated: {UPDATED}</p>
<h2>Cancel any time</h2>
<p>Log in to {CFG['provider']}, go to <strong>Profile → Orders</strong>, choose your Low Cost Legends Club membership and select <strong>Cancel membership</strong>. You'll get a confirmation email. You keep access until the end of the month you've already paid for, and you won't be charged again. Stuck? Email <a href="mailto:{CFG['contactEmail']}">{CFG['contactEmail']}</a> and we'll sort it.</p>
<h2>Your 14-day right to cancel</h2>
<p>Under the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013 you normally have 14 days after buying to cancel and get a refund. Because membership gives you <strong>instant access to digital content</strong>, at checkout we ask you to agree that access starts straight away and that you understand you lose the 14-day right to cancel once you start accessing the content. If you haven't accessed the members' area, you can still cancel within 14 days for a full refund.</p>
<h2>Our goodwill promise</h2>
<p>{TODO('SCOTT TO CONFIRM: e.g. "If you\'re not happy in the first 7 days of your first payment, email us and we\'ll refund that first month, no questions asked." Delete this section if you prefer not to offer it.')}</p>
<h2>Faulty content</h2>
<p>If something we supply is faulty or not as described, you have rights under the Consumer Rights Act 2015. Tell us and we'll fix it or refund you as the law requires.</p>
<h2>How refunds are paid</h2>
<p>Refunds go back to your original payment method through {CFG['provider']}. Your bank may take a few working days to show it.</p>"""),
"privacy.html": ("Privacy policy", f"""
<p>Last updated: {UPDATED}</p>
<p>This policy explains how {TODO('SCOTT: YOUR LEGAL NAME')}, trading as {BRAND_FULL} ("we"), handles personal data for {SHORT}, under UK GDPR and the Data Protection Act 2018. We are the controller. Contact: <a href="mailto:{CFG['contactEmail']}">{CFG['contactEmail']}</a>, {TODO('BUSINESS ADDRESS')}.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Browsing this site:</strong> the site doesn't use analytics, advertising or tracking cookies. Our host (GitHub Pages) may log basic technical data such as IP addresses for security.</li>
<li><strong>Members:</strong> when you subscribe, {CFG['provider']} collects your name, email and payment details. We receive your name, email, membership tier and status. We never see your full card number.</li>
<li><strong>Emails to us:</strong> if you email us (including the Tier 3 waitlist), we keep your email and message to reply to you.</li>
</ul>
<h2>Why we use it (lawful basis)</h2>
<ul><li>To provide your membership: <em>contract</em>.</li><li>To keep tax and accounting records: <em>legal obligation</em>.</li><li>To answer your messages and run the waitlist: <em>legitimate interests</em>.</li><li>Marketing emails only if you opt in: <em>consent</em>, which you can withdraw any time.</li></ul>
<h2>Who we share it with</h2>
<p>{CFG['provider']} (payments, accounts and member content), our email provider, and our accountant where needed. Some providers may process data outside the UK under appropriate safeguards. We never sell your data.</p>
<h2>How long we keep it</h2>
<p>Membership records are kept while you're a member and then for up to 6 years for tax purposes. Waitlist emails are deleted once Tier 3 launches or when you ask.</p>
<h2>Your rights</h2>
<p>You can ask to access, correct, delete, restrict or move your data, or object to how we use it. Email us. If you're unhappy, you can complain to the Information Commissioner's Office (<a href="https://ico.org.uk/make-a-complaint/" target="_blank" rel="noopener">ico.org.uk</a>).</p>
<h2>Links</h2>
<p>We link to YouTube and to booking sites. They have their own privacy policies.</p>"""),
}
for fn, (title, body) in legal.items():
    pg = head(f"{title} | {BRAND_FULL}", f"{BRAND_FULL} {title.lower()}.", r, fn)
    pg += f'<section><div class="narrow legal prose"><h1>{esc(title)}</h1>{body}</div></section>'
    pg += foot(r)
    write(fn, pg)

# ---------- 404 (absolute base so it works at any depth on GitHub Pages) ----------
base = SITE_URL.replace("https://smokeroach.github.io", "")
nf = head(f"Page not found | {BRAND_FULL}", "Page not found.", base, "404.html")
nf += f'<section><div class="narrow center"><h1>Lost? Happens to us <span class="hl">too</span></h1><p class="lede" style="margin-inline:auto">That page isn\'t here. Try the guides instead.</p><a class="btn btn-green" href="{base}guides.html">All guides</a></div></section>'
nf += foot(base)
write("404.html", nf)

# ---------- sitemap / robots ----------
pages = ["index.html", "guides.html", "pricing.html", "account.html", "terms.html", "refunds.html", "privacy.html"] + [f"guides/{g['slug']}.html" for g in ALL]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}{p}</loc></url>\n" for p in pages) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
write(".nojekyll", "")

# ---------- Whop export (private, never in this repo) ----------
if PRIVATE.exists():
    ex = PRIVATE / "whop-export"
    for g in locked:
        body = md(g["body"])
        doc = f"<!-- Paste into the Whop content/course lesson for {TIER_LABEL[g['tier']]}. -->\n<h1>{g['emoji']} {esc(g['title'])}</h1>\n<p><em>Straight up: you could do all of this yourself. We've trial-and-errored it so you don't have to. For British travellers only; we can't speak for other countries. Checked {UPDATED}; prices change, so always check before you book.</em></p>\n{body}\n"
        (ex / g["tier"]).mkdir(parents=True, exist_ok=True)
        (ex / g["tier"] / f"{g['order']:02d}-{g['slug']}.html").write_text(doc)
    print(f"whop export: {len(locked)} guides -> {ex}")

print(f"built: {len(free)} free, {len(t1)} tier1, {len(t2)} tier2, {len(pages)} pages in sitemap")
