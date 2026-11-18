#!/usr/bin/env python3
"""Structural accessibility checks for a PDF.

Usage
-----
    python3 pdf_audit.py document.pdf

Reports whether the PDF:

    D1   is tagged (MarkInfo /Marked true, and has a StructTreeRoot)
    D2   has real text (not a flattened image or unOCR'd scan)
    D3   has a Title and a document language, and displays the title in the title bar
    D4   has Figure tags, and whether they carry /Alt text (needs pypdf)
    S1   has Heading tags (H1-H6) in the tag tree (needs pypdf)

With pypdf installed (pip install pypdf) it reads the document properly. Without it, it
falls back to scanning the raw bytes, which cannot see inside compressed object streams,
so it says "unknown" rather than guessing wherever the answer could be hidden there.

It cannot judge reading order, alt text quality, or contrast. Look at the pages for those.
"""

import re
import sys


def with_pypdf(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    root = r.trailer["/Root"]
    out = {"engine": "pypdf", "pages": len(r.pages)}
    mark = root.get("/MarkInfo")
    out["marked"] = bool(mark.get_object().get("/Marked")) if mark else False
    out["struct_tree"] = "/StructTreeRoot" in root
    out["lang"] = str(root.get("/Lang")) if root.get("/Lang") else None
    vp = root.get("/ViewerPreferences")
    out["display_title"] = bool(vp.get_object().get("/DisplayDocTitle")) if vp else False
    meta = r.metadata
    out["title"] = (meta.title if meta and meta.title else None)

    chars = 0
    for i, page in enumerate(r.pages):
        if i >= 15:
            break
        chars += len((page.extract_text() or "").strip())
    out["text_chars_sampled"] = chars
    out["pages_sampled"] = min(len(r.pages), 15)

    roles = {}
    figs = figs_alt = 0

    def walk(node, depth=0):
        nonlocal figs, figs_alt
        if depth > 60 or node is None:
            return
        node = node.get_object()
        if hasattr(node, "get"):
            s = node.get("/S")
            if s:
                roles[str(s)] = roles.get(str(s), 0) + 1
                if str(s) == "/Figure":
                    figs += 1
                    if node.get("/Alt") and str(node.get("/Alt")).strip():
                        figs_alt += 1
            k = node.get("/K")
            if k is None:
                return
            for kid in (k if isinstance(k, list) else [k]):
                try:
                    walk(kid, depth + 1)
                except Exception:
                    pass

    if out["struct_tree"]:
        walk(root["/StructTreeRoot"])
    out["roles"] = roles
    out["figures"] = figs
    out["figures_with_alt"] = figs_alt
    return out


def raw_scan(path):
    data = open(path, "rb").read()
    text = data.decode("latin-1")
    hidden = "/ObjStm" in text      # compressed objects can hide the markers below
    out = {"engine": "raw byte scan (install pypdf for a reliable check)", "pages": None}

    def found(flag):                # present -> True; absent -> False only if nothing is hidden
        return True if flag else (None if hidden else False)

    out["marked"] = found(re.search(r"/Marked\s+true", text))
    out["struct_tree"] = found("/StructTreeRoot" in text)
    m = re.search(r"/Lang\s*\(([^)]*)\)", text)
    out["lang"] = m.group(1) if m else None
    out["lang_unknown"] = hidden and not m
    out["display_title"] = found(re.search(r"/DisplayDocTitle\s+true", text))
    m = re.search(r"/Title\s*\(([^)]*)\)", text)
    t = m.group(1) if m else None
    if t and t.startswith("\xfe\xff"):
        t = t.encode("latin-1").decode("utf-16", errors="replace").lstrip("\ufeff")
    out["title"] = t
    out["text_chars_sampled"] = None
    out["roles"] = {}
    out["figures"] = out["figures_with_alt"] = None
    out["compressed_objects"] = hidden
    return out


def tri(v):
    return "unknown" if v is None else ("yes" if v else "NO")


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = argv[1]
    try:
        try:
            info = with_pypdf(path)
        except ImportError:
            info = raw_scan(path)
    except Exception as exc:
        print(f"error reading {path}: {exc}", file=sys.stderr)
        return 2

    print(f"{path}  [{info['engine']}]")
    if info.get("pages"):
        print(f"pages: {info['pages']}")
    print()
    print(f"D1  tagged (MarkInfo /Marked):      {tri(info['marked'])}")
    print(f"D1  has structure tree:             {tri(info['struct_tree'])}")
    if info["text_chars_sampled"] is not None:
        n = info["text_chars_sampled"]
        verdict = "yes" if n >= 20 * max(1, info["pages_sampled"]) else "VERY LITTLE — possibly an image or unOCR'd scan"
        print(f"D2  real text (sampled {info['pages_sampled']} pages): {verdict} ({n} chars)")
    else:
        print("D2  real text:                      unknown (needs pypdf; check by selecting text in a viewer)")
    print(f"D3  title:                          {info['title']!r}")
    print(f"D3  title shown in title bar:       {tri(info['display_title'])}")
    print(f"D3  language (/Lang):               {info['lang'] or ('unknown' if info.get('lang_unknown') else 'NOT SET')}")
    if info["figures"] is not None:
        r = info["roles"]
        heads = {k: v for k, v in r.items() if re.fullmatch(r"/H[1-6]?", k)}
        print(f"D4  figures: {info['figures']}, with /Alt: {info['figures_with_alt']}")
        print(f"S1  headings in tag tree:           {heads or 'NONE'}")
        if r:
            print("    tag roles: " + ", ".join(f"{k.lstrip('/')}×{v}" for k, v in sorted(r.items())))
    else:
        print("D4  figure alt text / headings:     unknown (needs pypdf)")
    if info.get("compressed_objects"):
        print("\nnote: this PDF uses compressed object streams; the raw scan can miss tags.")

    problems = []
    if info["marked"] is False or info["struct_tree"] is False:
        problems.append("D1: not tagged — screen readers cannot navigate it (Must fix)")
    if not info["lang"] and not info.get("lang_unknown"):
        problems.append("D3: no document language (Must fix, WCAG 3.1.1)")
    if not info["title"]:
        problems.append("D3: no Title metadata (Must fix, WCAG 2.4.2)")
    if info["figures"]:
        if info["figures_with_alt"] < info["figures"]:
            problems.append(f"D4: {info['figures'] - info['figures_with_alt']} of {info['figures']} figures lack alt text (Must fix)")
    if info["struct_tree"] and info["figures"] is not None and not any(
            re.fullmatch(r"/H[1-6]?", k) for k in info["roles"]):
        problems.append("S1: tag tree has no headings (Should fix; Must fix if the document has section headings)")
    print()
    if problems:
        print("Problems:")
        for p in problems:
            print("  - " + p)
    else:
        print("No structural problems found by this script. Reading order, alt text quality and "
              "contrast still need a human look.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
