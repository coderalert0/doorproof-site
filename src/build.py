#!/usr/bin/env python3
"""Builds Doorproof's site from src/pages into the repo root, which GitHub Pages serves from main.

    python3 -m venv .venv && .venv/bin/pip install markdown pillow
    .venv/bin/python src/build.py && python3 src/check.py

Pages: the home page (src/pages/home.html), the privacy policy (src/pages/privacy.body.html) and the guides
(src/pages/guides/*.md, each with a Markdown copy next to its page). Also written: 404.html, sitemap.xml, llms.txt and
llms-full.txt for AI tools, and the social card img/og.png. Change UPDATED when a page's facts are rechecked.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import markdown
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
BASE = "https://coderalert0.github.io/doorproof-site/"
APP_ID = "6832112189"
APP = f"https://apps.apple.com/us/app/id{APP_ID}"
APP_FR = f"https://apps.apple.com/ca/app/id{APP_ID}?l=fr-CA"   # the Canadian store, in French
NAME = "Doorproof"
APP_NAME = "ID Scanner & Age: Doorproof"
TERMS = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
UPDATED = "2026-11-07"
UPDATED_LONG = date.fromisoformat(UPDATED).strftime("%B %-d, %Y")
DISCLAIMER = "Doorproof helps staff check IDs. It isn't legal advice or a guarantee, and rules on checking and scanning IDs differ by state."
PUBLISHER = {"@type": "Organization", "name": NAME, "url": BASE, "logo": BASE + "img/icon-512.png"}
HOME_TITLE = "Doorproof: ID Scanner & Age Verification App for Bars, Clubs and Stores"
HOME_DESCRIPTION = ("Free, unlimited ID scanning on iPhone and iPad for bars, clubs and stores: age and expiry in a second, "
                    "altered-ID checks and Fake Watch. Pro adds pass-back alerts.")
SUMMARY = ("Doorproof is an ID scanner and age verification app for iPhone and iPad. Door staff at bars, clubs, liquor "
           "stores and events point the camera at the barcode on the back of a US or Canadian driver's license or ID "
           "card, a passport's machine-readable lines, or an Apple Wallet ID, and get the age, the expiry and any sign "
           "the card was altered, in a second.")
FACTS = [
    "Scanning is free and unlimited, with no account. Fake Watch is free.",
    "Doorproof Pro costs $9.99 a month or $49.99 a year in the US, with a one-week free trial for new subscribers. It adds pass-back alerts (the same card twice in one night), scan records with a one-tap nightly report, a door counter, ban and VIP lists matched to the person, wristband colors by age and iPad door mode.",
    "Doorproof Venue costs $29.99 a month or $249.99 a year in the US: everything in Pro on every device at a venue, sharing one pass-back list, tonight's counts and the ban and VIP lists through the owner's iCloud.",
    "Reads driver's licenses and ID cards from every US state, DC, the US territories and Canada's provinces (the AAMVA PDF417 barcode), passports and passport-style ID cards (the ICAO Doc 9303 machine-readable zone, check digits verified), and Apple Wallet IDs through Apple's ID Verifier.",
    "Checks: age and expiry in the venue's time zone; barcodes that disagree with themselves, such as an under-21 date that doesn't follow from the birth date; the same card scanned twice in one night (pass-back, with Pro); cards made like fakes other venues confirmed (Fake Watch); a question only the real holder would know.",
    "Limits: a phone can't check holograms, ultraviolet ink or card thickness, and a well-made fake carries a working barcode. Doorproof never calls a card genuine on its barcode alone. An unreadable barcode means check by hand, not fake.",
    "Privacy: IDs are read on the device and no image is saved. Records are off by default and stay on the device. Fake Watch shares only what staff mark as fake or real: how that card's barcode was made, the issuing state, the venue's city, an anonymous venue code and the time, never a name, ID number, birth date, address or photo. It can be turned off.",
    "Runs on iPhone and iPad with iOS 17 or later. On the App Store in the United States and Canada, in English, French (Canada) and Spanish (Mexico). The home page and privacy policy are also in French: " + BASE + "fr/",
]


def parse(path):
    _, head, body = path.read_text().split("---\n", 2)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    meta["slug"] = path.stem
    meta["related"] = [s.strip() for s in meta.get("related", "").split(",") if s.strip()]
    meta["body"] = body.strip()
    faq_block = re.search(r"## Frequently asked questions\n(.*?)(?=\n## |\Z)", body, re.S)
    meta["faqs"] = re.findall(r"### (.+?)\n\n(.+?)(?=\n\n###|\Z)", faq_block.group(1).strip(), re.S) if faq_block else []
    source_block = re.search(r"## Sources\n(.*)", body, re.S)
    meta["sources"] = re.findall(r"- \[(.+?)\]\((.+?)\)", source_block.group(1)) if source_block else []
    return meta


def render(text):
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"], extension_configs={"toc": {"toc_depth": "2"}})
    out = md.convert(text).replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out, [(t["id"], t["name"]) for t in md.toc_tokens]


def plain(text):
    return re.sub(r"<[^>]+>", "", re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)).replace("&gt;", ">").replace("&amp;", "&").strip()


def jsonld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


DISCLAIMER_FR = ("Doorproof aide le personnel à vérifier les pièces d'identité. Ce n'est ni un avis juridique ni une garantie, "
                 "et les règles sur la vérification et le scan des pièces d'identité varient selon la province ou l'État.")
CHROME = {
    "en": {"skip": "Skip to content", "how": "How it works", "guides": "Guides", "support": "Support", "privacy": "Privacy",
           "get": "Get the app", "tagline": "The ID scanner for the door, on iPhone and iPad.", "disclaimer": DISCLAIMER,
           "app": "App", "policy": "Privacy Policy", "terms": "Terms of Use", "other": ("fr", "Français"),
           "alt": "Doorproof, the ID scanner for the door, showing a green OK result"},
    "fr": {"skip": "Aller au contenu", "how": "Comment ça marche", "guides": "Guides", "support": "Soutien", "privacy": "Confidentialité",
           "get": "Obtenir l'app", "tagline": "Le scanner de pièces d'identité pour la porte, sur iPhone et iPad.", "disclaimer": DISCLAIMER_FR,
           "app": "Application", "policy": "Politique de confidentialité", "terms": "Conditions d'utilisation", "other": ("en", "English"),
           "alt": "Doorproof, le scanner de pièces d'identité pour la porte, affichant un résultat vert OK"},
}
# Pages that exist in both languages: (English path, French path) under BASE.
TWINS = {"index": ("", "fr/"), "privacy": ("privacy.html", "fr/privacy.html")}


def page(slug, title, description, body, *, schema=(), kind="article", current="", root="", markdown_twin=False,
         robots="index,follow,max-snippet:-1,max-image-preview:large", lang="en"):
    c = CHROME[lang]
    twin = TWINS.get(slug.removeprefix("fr/"))
    url = BASE + (twin[1] if lang == "fr" else twin[0]) if twin else (BASE if slug == "index" else f"{BASE}{slug}.html")
    hreflang = ""
    if twin:
        hreflang = (f'\n<link rel="alternate" hreflang="en" href="{BASE}{twin[0]}">'
                    f'\n<link rel="alternate" hreflang="fr-CA" href="{BASE}{twin[1]}">'
                    f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{twin[0]}">')
    # The other language: this page's twin, or the other language's home page.
    other = BASE + ((twin[0] if lang == "fr" else twin[1]) if twin else ("" if lang == "fr" else "fr/"))
    e = html.escape
    alternate = f'\n<link rel="alternate" type="text/markdown" href="{root}{slug}.md">' if markdown_twin else ""
    ld = "\n".join(jsonld(item) for item in schema)
    here = lambda name: ' aria-current="page"' if name == current else ""
    home = "./" if lang == "fr" else (root or "./")
    app = APP_FR if lang == "fr" else APP
    return f"""<!doctype html>
<html lang="{'fr-CA' if lang == 'fr' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">{alternate}{hreflang}
<meta name="theme-color" content="#f6f8f7">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(c["alt"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}icon.png">
<link rel="apple-touch-icon" href="{root}icon.png">
<link rel="stylesheet" href="{root}style.css">
<link rel="alternate" type="text/plain" title="llms.txt" href="{root}llms.txt">
{ld}
</head>
<body>
<a class="skip" href="#main">{c["skip"]}</a>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="{home}"><img src="{root}icon.png" alt="" width="34" height="34"><span>{NAME}</span></a>
    <nav class="nav" aria-label="Site">
      <a href="{home}#how"{here("home")}>{c["how"]}</a>
      <a href="{home}#guides"{here("guides")}>{c["guides"]}</a>
      <a href="{home}#support">{c["support"]}</a>
      <a href="{home if lang == "fr" else root}privacy.html"{here("privacy")}>{c["privacy"]}</a>
      <a href="{other}" hreflang="{"fr-CA" if c["other"][0] == "fr" else "en"}" lang="{"fr-CA" if c["other"][0] == "fr" else "en"}">{c["other"][1]}</a>
      <a class="nav-cta" href="{app}">{c["get"]}</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="in">
    <div class="foot-about">
      <a class="brand" href="{home}"><img src="{root}icon.png" alt="" width="28" height="28"><span>{NAME}</span></a>
      <p>{c["tagline"]}</p>
      <p>© 2026 {NAME}. {c["disclaimer"]}</p>
    </div>
    <nav aria-label="Guides"><p class="foot-title">{c["guides"]}</p>{FOOTER_GUIDES.replace('href="', f'href="{root}')}</nav>
    <nav aria-label="App"><p class="foot-title">{c["app"]}</p><a href="{app}">App Store</a><a href="{home}#support">{c["support"]}</a><a href="{home if lang == "fr" else root}privacy.html">{c["policy"]}</a><a href="{TERMS}">{c["terms"]}</a><a href="{root}llms.txt">llms.txt</a></nav>
  </div>
</footer>
<script src="{root}site.js"></script>
</body>
</html>
"""


def guide_page(g, by_slug):
    body_md = re.sub(r"\n## Sources\n.*", "", g["body"], flags=re.S)
    content, headings = render(body_md)
    url = f'{BASE}{g["slug"]}.html'
    e = html.escape
    sources = "".join(f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in g["sources"])
    related = "".join(f'<li><a href="{s}.html">{e(by_slug[s]["h1"])}</a></li>' for s in g["related"])
    toc = "".join(f'<li><a href="#{i}">{e(n)}</a></li>' for i, n in headings)
    body = f"""<div class="guide">
<nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">/</span> <a href="./#guides">Guides</a> <span aria-hidden="true">/</span> <span>{e(g["nav"])}</span></nav>
<article>
<h1>{e(g["h1"])}</h1>
<p class="updated">Checked against its sources on <time datetime="{UPDATED}">{UPDATED_LONG}</time></p>
<div class="answer"><h2>Short answer</h2><p>{e(g["answer"])}</p></div>
<nav class="toc" aria-label="On this page"><p class="foot-title">On this page</p><ul>{toc}</ul></nav>
{content}
<aside class="app-cta">
  <div><h2>Check IDs in a second</h2><p>Doorproof reads the barcode, counts the age and flags what doesn't add up. Free, unlimited scanning on iPhone and iPad.</p></div>
  <a class="badge" href="{APP}"><img src="img/app-store-badge.svg" alt="Download on the App Store" width="150" height="50"></a>
</aside>
<section class="sources"><h2>Sources</h2><ul>{sources}</ul><p class="muted">Guides summarize public sources and aren't legal advice. Rules differ by state: check with your state's alcohol regulator.</p></section>
<section class="related"><h2>Related guides</h2><ul>{related}</ul></section>
</article>
</div>"""
    crumbs = [("Home", BASE), ("Guides", BASE + "#guides"), (g["nav"], url)]
    schema = [
        {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["description"],
         "datePublished": UPDATED, "dateModified": UPDATED, "mainEntityOfPage": url, "image": BASE + "img/og.png",
         "author": PUBLISHER, "publisher": PUBLISHER, "inLanguage": "en-US", "citation": [u for _, u in g["sources"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    if g["faqs"]:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in g["faqs"]]})
    return page(g["slug"], g["title"], g["description"], body, schema=schema, current="guides", markdown_twin=True)


def guide_markdown(g):
    body = re.sub(r"\]\((?!https?:)([a-z0-9-]+)\.html\)", rf"]({BASE}\1.md)", g["body"])
    return f"""# {g["h1"]}

> {g["answer"]}

Source page: {BASE}{g["slug"]}.html
Checked against its sources on {UPDATED_LONG}. Published by {NAME}, an ID scanner app for iPhone and iPad. Not legal advice.

{body}
"""


def social_card():
    """img/og.png: 1200x630, light, the app's name and promise beside the first App Store screenshot."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), (246, 248, 247))
    d = ImageDraw.Draw(card)
    font = lambda size, bold=True: ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=1 if bold else 0)
    icon = Image.open(ROOT / "img" / "icon-512.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    mask = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 95, 95), 22, fill=255)
    card.paste(icon, (72, 76), mask)
    d.text((186, 96), NAME, font=font(56), fill=(12, 21, 32))
    y = 232
    for line in ["Check IDs at the door,", "in a second."]:
        d.text((72, y), line, font=font(62), fill=(8, 122, 73) if line == "in a second." else (12, 21, 32))
        y += 76
    d.text((72, y + 26), "Free ID scanner and age check for", font=font(30, False), fill=(91, 102, 112))
    d.text((72, y + 66), "bars, clubs and stores. iPhone and iPad.", font=font(30, False), fill=(91, 102, 112))
    shot = Image.open(ROOT / "img" / "1-demo.jpg").convert("RGB")
    sw = 300
    shot = shot.resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((W - sw - 90 + 6, 48 + 18, W - 90 + 6, 48 + shot.height + 18), 36, fill=70)
    from PIL import ImageFilter
    card.paste((200, 208, 204), (0, 0), shadow.filter(ImageFilter.GaussianBlur(22)))
    smask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(smask).rounded_rectangle((0, 0, shot.width - 1, shot.height - 1), 36, fill=255)
    card.paste(shot, (W - sw - 90, 48), smask)
    card.save(ROOT / "img" / "og.png", optimize=True)


# The icon at 512 for structured data and the card, from the app's 1024 artwork when it's beside this repo.
art = Path.home() / "doorproof-app" / "App" / "Assets.xcassets" / "AppIcon.appiconset" / "icon-1024.png"
if art.exists():
    Image.open(art).convert("RGB").resize((512, 512), Image.LANCZOS).save(ROOT / "img" / "icon-512.png", optimize=True)
    Image.open(art).convert("RGB").resize((180, 180), Image.LANCZOS).save(ROOT / "icon.png", optimize=True)   # favicon and touch icon
social_card()

guides = [parse(p) for p in sorted((PAGES / "guides").glob("*.md"))]
order = ["do-id-scanners-detect-fake-ids", "how-to-check-an-id", "drivers-license-barcode", "passed-back-id", "checking-passports"]
guides.sort(key=lambda g: order.index(g["slug"]) if g["slug"] in order else len(order))
by_slug = {g["slug"]: g for g in guides}
FOOTER_GUIDES = "".join(f'<a href="{g["slug"]}.html">{html.escape(g["nav"])}</a>' for g in guides)

for g in guides:
    (ROOT / f'{g["slug"]}.html').write_text(guide_page(g, by_slug))
    (ROOT / f'{g["slug"]}.md').write_text(guide_markdown(g))

# Home
cards = "".join(f'<li><a href="{g["slug"]}.html"><strong>{html.escape(g["h1"])}</strong><span>{html.escape(g["description"])}</span></a></li>' for g in guides)
home = (PAGES / "home.html").read_text().replace("{APP}", APP).replace("{GUIDES}", f'<ul class="guides">{cards}</ul>')
faqs = re.findall(r"<details><summary>(.+?)</summary><p>(.+?)</p></details>", home)
home_schema = [
    {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE, "description": HOME_DESCRIPTION, "publisher": PUBLISHER, "inLanguage": "en-US"},
    {"@context": "https://schema.org", "@type": "MobileApplication", "name": APP_NAME, "alternateName": NAME, "url": BASE,
     "installUrl": APP, "downloadUrl": APP, "operatingSystem": "iOS 17.0 or later", "applicationCategory": "BusinessApplication",
     "description": SUMMARY, "image": BASE + "img/icon-512.png", "screenshot": [BASE + f"img/{n}.jpg" for n in ("1-demo", "2-mismatch", "3-fakewatch", "4-passback")],
     "featureList": ["Age and expiry check", "Altered ID check", "Pass-back alerts (Pro)", "Fake Watch", "Passport MRZ reading", "Apple Wallet ID verification", "Scan records (Pro)", "Door counter (Pro)", "Shared pass-backs and lists across devices (Venue)", "Ban and VIP lists (Pro)", "Wristbands by age (Pro)", "iPad door mode (Pro)"],
     "inLanguage": ["en", "fr-CA", "es-MX"], "publisher": PUBLISHER,
     "offers": [{"@type": "Offer", "name": "Doorproof", "price": "0", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Doorproof Pro, monthly", "price": "9.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Doorproof Pro, yearly", "price": "49.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Doorproof Venue, monthly", "price": "29.99", "priceCurrency": "USD"},
                {"@type": "Offer", "name": "Doorproof Venue, yearly", "price": "249.99", "priceCurrency": "USD"}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]},
]
(ROOT / "index.html").write_text(page("index", HOME_TITLE, HOME_DESCRIPTION, home, schema=home_schema, kind="website", current="home"))

# Privacy keeps its URL: the app and App Store Connect link to it.
privacy = (PAGES / "privacy.body.html").read_text()
(ROOT / "privacy.html").write_text(page("privacy", f"Privacy Policy · {NAME}", "What the Doorproof ID scanner app reads, what it keeps on the device, and the little it shares.",
                                        f'<div class="doc">\n{privacy}</div>', current="privacy", schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"{NAME} privacy policy", "url": f"{BASE}privacy.html",
     "dateModified": "2026-11-07", "publisher": PUBLISHER, "inLanguage": "en-US",
     "about": {"@type": "MobileApplication", "name": APP_NAME, "url": BASE}}]))

# French (for Quebec venues): the home page and the privacy policy, under fr/. The guides stay in English.
FR = ROOT / "fr"
FR.mkdir(exist_ok=True)
cards_fr = "".join(f'<li><a href="../{g["slug"]}.html" hreflang="en"><strong>{html.escape(g["h1"])}</strong><span>{html.escape(g["description"])}</span></a></li>' for g in guides)
home_fr = (PAGES / "home.fr.html").read_text().replace("{APP}", APP_FR).replace("{GUIDES}", f'<ul class="guides">{cards_fr}</ul>')
faqs_fr = re.findall(r"<details><summary>(.+?)</summary><p>(.+?)</p></details>", home_fr)
HOME_TITLE_FR = "Doorproof\u00a0: scanner d'identité et vérification de l'âge"
HOME_DESCRIPTION_FR = ("Scan de pièces d'identité gratuit et illimité sur iPhone et iPad\u00a0: l'âge et l'expiration en une seconde, "
                       "les cartes modifiées et Fake Watch.")
(FR / "index.html").write_text(page("fr/index", HOME_TITLE_FR, HOME_DESCRIPTION_FR, home_fr, kind="website", current="home", root="../", lang="fr", schema=[
    {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + "fr/", "description": HOME_DESCRIPTION_FR, "publisher": PUBLISHER, "inLanguage": "fr-CA"},
    {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "fr-CA", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs_fr]}]))
privacy_fr = (PAGES / "privacy.body.fr.html").read_text()
(FR / "privacy.html").write_text(page("fr/privacy", f"Politique de confidentialité · {NAME}",
                                      "Ce que l'application Doorproof lit, ce qu'elle conserve sur l'appareil et le peu qu'elle partage.",
                                      f'<div class="doc">\n{privacy_fr}</div>', current="privacy", root="../", lang="fr", schema=[
    {"@context": "https://schema.org", "@type": "WebPage", "name": f"Politique de confidentialité de {NAME}", "url": f"{BASE}fr/privacy.html",
     "dateModified": "2026-11-07", "publisher": PUBLISHER, "inLanguage": "fr-CA", "about": {"@type": "MobileApplication", "name": APP_NAME, "url": BASE}}]))

# 404 is served at any depth, so its links are absolute.
missing = '<div class="doc"><h1>Page not found</h1><p>That page has moved or never existed.</p><p><a href="/doorproof-site/">Go to Doorproof\'s home page</a> or read <a href="/doorproof-site/how-to-check-an-id.html">how to check an ID at the door</a>.</p></div>'
(ROOT / "404.html").write_text(page("404", f"Page not found · {NAME}", "This page could not be found.", missing, robots="noindex", root="/doorproof-site/"))

# Sitemap
urls = ([(BASE, "1.0"), (f"{BASE}fr/", "0.9")] + [(f'{BASE}{g["slug"]}.html', "0.8") for g in guides]
        + [(f"{BASE}privacy.html", "0.3"), (f"{BASE}fr/privacy.html", "0.3")])
entries = "".join(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n')

# llms.txt and the full text for AI tools
facts = "\n".join(f"- {f}" for f in FACTS)
links = "\n".join(f'- [{g["h1"]}]({BASE}{g["slug"]}.md): {g["description"]}' for g in guides)
(ROOT / "llms.txt").write_text(f"""# {NAME}

> {SUMMARY}

{DISCLAIMER} Facts on this site were checked on {UPDATED_LONG}. When citing a guide, link its page.

## Key facts

{facts}

## Guides

{links}

## App

- [App Store listing]({APP}): {APP_NAME}, for iPhone and iPad, iOS 17 or later
- [Home page]({BASE}): What Doorproof checks, Doorproof Pro, questions and support
- [Privacy Policy]({BASE}privacy.html): What the app reads, keeps and shares
- [Terms of Use]({TERMS}): Apple's standard license agreement

## Optional

- [Full text]({BASE}llms-full.txt): The facts, the questions and answers, every guide and the privacy policy in one Markdown file
""")
qa = "\n\n".join(f"### {plain(q)}\n\n{plain(a)}" for q, a in faqs)
privacy_md = re.sub(r"<li>", "- ", privacy)
privacy_md = re.sub(r"<h2>(.+?)</h2>", r"## \1", privacy_md)
privacy_md = re.sub(r"<h1>(.+?)</h1>", r"", privacy_md)
privacy_md = "\n".join(l.strip() for l in plain(privacy_md.replace("laddothis at gmail dot com", "laddothis@gmail.com")).splitlines() if l.strip())
privacy_md = re.sub(r"\n(## )", r"\n\n\1", privacy_md).replace("\n- ", "\n\n- ", 1)
full = [f"# {NAME}\n\n> {SUMMARY}\n\n{DISCLAIMER} Checked on {UPDATED_LONG}. Source: {BASE}\n\n## Key facts\n\n{facts}\n\n## Questions and answers\n\n{qa}"]
full += [guide_markdown(g) for g in guides]
full.append(f"# Doorproof privacy policy\n\nSource page: {BASE}privacy.html\n\n{privacy_md}\n")
(ROOT / "llms-full.txt").write_text("\n\n---\n\n".join(full))
(ROOT / ".nojekyll").write_text("")
print(f"built home, privacy, their French pages, 404 and {len(guides)} guides")
