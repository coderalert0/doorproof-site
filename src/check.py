#!/usr/bin/env python3
"""Fails if the built site has a broken page, broken internal link or invalid metadata.

    python3 src/check.py            checks the built files
    python3 src/check.py --external also checks every outside link
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://coderalert0.github.io/doorproof-site/"
errors = []


class Page(HTMLParser):
    void = {"meta", "link", "img", "br", "hr", "input"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.links, self.h1, self.ld, self.title, self.in_ld, self.in_title, self.in_h1 = [], [], 0, [], "", False, False, False
        self.desc = self.canonical = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in self.void:
            self.stack.append(tag)
        if tag in ("a", "link", "img", "script"):
            self.links.append(a.get("href") or a.get("src") or "")
        if tag == "img" and "alt" not in a:
            errors.append(f"{self.name}: image without alt")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.in_title = True
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")

    def handle_endtag(self, tag):
        self.in_title = self.in_ld = False if tag in ("title", "script") else self.in_title or self.in_ld
        if tag in self.void:
            return
        if not self.stack or self.stack.pop() != tag:
            errors.append(f"{self.name}: mismatched </{tag}>")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_ld:
            self.ld.append(data)


outside = set()
sitemap = {e.text for e in ET.parse(ROOT / "sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
# Search Console proves ownership with this file, so it stays in place and is not a page.
pages = sorted(p for p in ROOT.glob("*.html") if not p.name.startswith("google")) + sorted((ROOT / "fr").glob("*.html"))

for path in pages:
    text = path.read_text()
    p = Page()
    p.name = str(path.relative_to(ROOT))
    p.feed(text)
    if p.stack:
        errors.append(f"{p.name}: unclosed tags {p.stack[-3:]}")
    if p.h1 != 1:
        errors.append(f"{p.name}: {p.h1} h1 tags")
    if not 20 <= len(p.title) <= 75:
        errors.append(f"{p.name}: title is {len(p.title)} characters")
    if not p.desc or not 25 <= len(p.desc) <= 175:
        errors.append(f"{p.name}: description is {len(p.desc or '')} characters")
    if "stdeula" not in text or "privacy.html" not in text:
        errors.append(f"{p.name}: missing the Terms of Use or Privacy Policy link")
    for block in p.ld:
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{p.name}: bad JSON-LD: {e}")
    if p.name != "404.html" and p.canonical not in sitemap:
        errors.append(f"{p.name}: canonical {p.canonical} is not in the sitemap")
    if p.name != "404.html" and not p.ld:
        errors.append(f"{p.name}: no JSON-LD")
    for link in p.links:
        if link.startswith("http"):
            outside.add(link)
            continue
        target = link.split("#")[0]
        if link.startswith("/doorproof-site/"):
            resolved = ROOT / target.replace("/doorproof-site/", "")
        else:
            resolved = path.parent / target   # relative to the page (the French pages are under fr/)
        if target and target != "./" and not target.startswith("mailto:") and not resolved.exists():
            errors.append(f"{p.name}: broken link {link}")
    # Pages in two languages point at each other.
    for alt in re.findall(r'hreflang="[^"]+" href="([^"]+)"', text):
        if not (ROOT / alt.replace(BASE, "")).exists() and not (ROOT / alt.replace(BASE, "") / "index.html").exists():
            errors.append(f"{p.name}: hreflang points at a missing page {alt}")

# The app and App Store Connect link to these, so they must keep working.
for required in ("index.html", "privacy.html", "llms.txt", "llms-full.txt", "sitemap.xml", "img/og.png", "img/icon-512.png", ".nojekyll", "site.js"):
    if not (ROOT / required).exists():
        errors.append(f"missing {required}")
if '<span class="email">' not in (ROOT / "privacy.html").read_text() or 'id="support"' not in (ROOT / "index.html").read_text():
    errors.append("the support section or the privacy contact is gone")
for md in ROOT.glob("*.md"):
    if md.name != "README.md" and not (ROOT / md.with_suffix(".html").name).exists():
        errors.append(f"{md.name}: Markdown copy without a page")
for url in re.findall(r"\((https://coderalert0\.github\.io/doorproof-site/[^)]+)\)", (ROOT / "llms.txt").read_text()):
    if not (ROOT / url.replace("https://coderalert0.github.io/doorproof-site/", "")).exists():
        errors.append(f"llms.txt: broken link {url}")

if "--external" in sys.argv:
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
    for url in sorted(u for u in outside if "coderalert0.github.io" not in u and "schema.org" not in u):
        try:
            code = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": agent}), timeout=25).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = repr(e)[:60]
        if code != 200:
            print(f"  outside link {code}: {url}")

print(f"checked {len(pages)} pages, {len(sitemap)} sitemap URLs, {len(outside)} outside links")
for error in errors:
    print("ERROR", error)
sys.exit(1 if errors else 0)
