#!/usr/bin/env python3
"""Static accessibility checks for HTML: web pages, HTML email, exported slide decks.

Usage
-----
    python3 html_audit.py page.html
    python3 html_audit.py page.html --json

Reads one HTML file and reports, with element locations (line numbers):

    S1   heading structure: missing/multiple H1, skipped levels, empty headings
    T5   missing lang attribute
    S3   missing or generic <title>
    I1   images with no alt attribute; alt that looks like a file name or "image of ..."
    I2   images with empty alt (reported for confirmation they are decorative)
    L1   vague link text, raw URL as link text, empty links
    L2   same link text pointing to different destinations
    L4   links to PDF/Word/Excel files that do not name the file type in the text
    S4   layout tables (no header cells) in pages that look like email
    S5   no main landmark / skip link (pages longer than 3 headings)

It does NOT render the page, so it cannot measure colour contrast, check whether links are
underlined, or judge alt text quality. Use contrast.py and look at the page for those.

No third-party dependencies.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

VAGUE = {"click here", "here", "read more", "more", "more information", "learn more",
         "more info", "link", "this link", "click", "details", "info", "continue", "go"}
FILE_EXT = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|csv|zip)(?:[?#].*)?$", re.I)
TYPE_IN_TEXT = re.compile(r"\b(pdf|docx?|word|xlsx?|excel|pptx?|powerpoint|csv|zip)\b", re.I)
BAD_ALT = re.compile(r"^(image|photo|picture|graphic|img|logo)?[\s_-]*\d*\.(jpe?g|png|gif|svg|webp)$"
                     r"|^(img|dsc|image|photo|screenshot)[-_ ]?\d+$", re.I)
GENERIC_TITLES = {"untitled", "document", "home", "index", "new page", "page"}


class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.findings = []        # (check, severity, line, message)
        self.headings = []        # (level, line, text)
        self.links = []           # (text, href, line)
        self.lang = None
        self.title = None
        self.has_main = False
        self.has_skip = False
        self.tables = []          # stack of dicts
        self.table_log = []
        self._stack = []          # open tags of interest
        self._buf = None          # text buffer for headings/links/title
        self._link_alt = ""

    def add(self, check, severity, msg):
        self.findings.append((check, severity, self.getpos()[0], msg))

    # ---- parsing ----
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = (a.get("lang") or a.get("xml:lang") or "").strip()
        elif tag == "title":
            self._buf = ["title", self.getpos()[0], ""]
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._buf = [tag, self.getpos()[0], ""]
        elif tag == "a":
            href = a.get("href", "")
            if href.startswith("#") and "skip" in (a.get("class", "") + href + (a.get("id") or "")).lower():
                self.has_skip = True
            self._buf = ["a", self.getpos()[0], "", href, a.get("aria-label", "")]
            self._link_alt = ""
        elif tag == "img":
            self._check_img(a)
            if self._buf and self._buf[0] == "a":
                self._link_alt += " " + (a.get("alt") or "")
        elif tag in ("main",) or a.get("role") == "main":
            self.has_main = True
        elif tag == "table":
            self.tables.append({"line": self.getpos()[0], "th": False,
                                "role": a.get("role", ""), "rows": 0})
        elif tag == "th" and self.tables:
            self.tables[-1]["th"] = True
        elif tag == "tr" and self.tables:
            self.tables[-1]["rows"] += 1

    def handle_data(self, data):
        if self._buf is not None:
            self._buf[2] += data

    def handle_endtag(self, tag):
        b = self._buf
        if tag == "table" and self.tables:
            self.table_log.append(self.tables.pop())
        if b is None or b[0] != tag:
            return
        text = re.sub(r"\s+", " ", b[2]).strip()
        if tag == "title":
            self.title = text
        elif tag == "a":
            label = text or self._link_alt.strip() or b[4]
            self.links.append((re.sub(r"\s+", " ", label).strip(), b[3], b[1]))
        else:
            self.headings.append((int(tag[1]), b[1], text))
        self._buf = None

    def _check_img(self, a):
        src = a.get("src", "")[:60]
        if "alt" not in a:
            self.add("I1", "Must fix", f"<img src=\"{src}\"> has no alt attribute")
            return
        alt = (a["alt"] or "").strip()
        if alt == "":
            self.add("I2", "Confirm", f"<img src=\"{src}\"> has empty alt; fine only if purely decorative")
        elif BAD_ALT.search(alt):
            self.add("I1", "Must fix", f"alt \"{alt}\" looks like a file name")
        elif re.match(r"^(image|photo|picture|graphic) of\b", alt, re.I):
            self.add("I1", "Should fix", f"alt \"{alt[:40]}\" starts with a redundant phrase (\"image of\")")
        elif len(alt) > 150:
            self.add("I3", "Consider", f"alt is {len(alt)} chars; consider a short alt plus a long description on the page")


def analyse(html):
    p = Audit()
    p.feed(html)
    p.close()
    f = p.findings

    # language and title
    if not p.lang:
        f.append(("T5", "Must fix", 1, "<html> has no lang attribute (WCAG 3.1.1)"))
    if not p.title:
        f.append(("S3", "Must fix", 1, "no <title>, or it is empty (WCAG 2.4.2)"))
    elif p.title.lower() in GENERIC_TITLES:
        f.append(("S3", "Should fix", 1, f"<title> is generic: \"{p.title}\""))

    # headings
    h1s = [h for h in p.headings if h[0] == 1]
    if not p.headings:
        f.append(("S1", "Should fix", 1, "no headings found"))
    else:
        if not h1s:
            f.append(("S1", "Must fix", p.headings[0][1], "no H1 (GW Standards: one H1 per page)"))
        elif len(h1s) > 1:
            f.append(("S1", "Must fix", h1s[1][1], f"{len(h1s)} H1s (GW Standards: only one H1 per page)"))
        prev = 0
        for lvl, line, text in p.headings:
            if prev and lvl > prev + 1:
                f.append(("S1", "Must fix", line, f"heading jumps H{prev} to H{lvl}: \"{text[:50]}\""))
            if not text:
                f.append(("S1", "Must fix", line, f"empty H{lvl}"))
            prev = lvl

    # landmarks
    if len(p.headings) > 3 and not (p.has_main or p.has_skip):
        f.append(("S5", "Should fix", 1, "no <main> landmark or skip link on a longer page (WCAG 2.4.1)"))

    # links
    by_text = {}
    for text, href, line in p.links:
        low = text.lower().strip(" .:>»›")
        if not href or href == "#":
            if href == "":
                f.append(("L1", "Should fix", line, f"link \"{text[:40]}\" has no href"))
        if not text:
            f.append(("L1", "Must fix", line, f"empty link (no text, aria-label, or image alt) to {href[:50]}"))
            continue
        if low in VAGUE:
            f.append(("L1", "Must fix", line, f"vague link text \"{text}\" to {href[:50]}"))
        elif re.match(r"^(https?://|www\.)\S+$", text):
            f.append(("L1", "Must fix", line, f"raw URL as link text: {text[:60]}"))
        if FILE_EXT.search(href) and not TYPE_IN_TEXT.search(text):
            f.append(("L4", "Must fix", line, f"link to a document does not name the file type: \"{text[:40]}\" ({href[-20:]})"))
        by_text.setdefault(low, set()).add(href)
    for text, hrefs in by_text.items():
        if len(hrefs) > 1 and text:
            f.append(("L2", "Must fix", 1, f"link text \"{text}\" is used for {len(hrefs)} different destinations"))

    # layout tables
    for t in p.table_log:
        if not t["th"] and t["role"] not in ("presentation", "none"):
            f.append(("S4", "Should fix", t["line"],
                      "table with no <th> cells and no role=\"presentation\"; if used for layout, mark it so; "
                      "if it holds data, add header cells"))

    f.sort(key=lambda x: (x[2], x[0]))
    return f, p


def main(argv):
    ap = argparse.ArgumentParser(description="Static accessibility checks for an HTML file.")
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv[1:])
    try:
        with open(args.file, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    findings, p = analyse(html)
    if args.json:
        print(json.dumps([{"check": c, "severity": s, "line": l, "message": m}
                          for c, s, l, m in findings], indent=2))
        return 0
    print(f"{args.file}: {len(p.headings)} headings, {len(p.links)} links")
    print(f"lang={p.lang or '(none)'}  title={p.title!r}")
    if not findings:
        print("\nNo issues found by the static checks. This does not cover contrast, "
              "underlined links, or alt text quality.")
        return 0
    print()
    for c, s, l, m in findings:
        print(f"  line {l:<5} {c:<3} {s:<11} {m}")
    print("\nSeverity here is the check's ceiling; apply SKILL.md's rules when writing the report.")
    print("Not covered: colour contrast, link underlines, alt text quality, reading order.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
