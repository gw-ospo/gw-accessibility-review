---
name: gw-accessibility-review
description: Review GW OSPO and OSCON marketing and communication output — posters, flyers, slide decks, PDFs, reports, prospectuses, web pages, HTML email, social posts, charts, video, signage — against the GW Digital Content Accessibility Policy (WCAG 2.1 AA) and the GW Standards and Best Practices, then issue a structured report with a publish verdict and prioritized fixes. Use whenever someone asks to check, audit, or review something for accessibility, WCAG, alt text, contrast, captions, or screen readers, or before anything from GW OSPO or GW OSCON is published or sent.
compatibility: Works in any Agent Skills client. The Python 3 helper scripts are optional — contrast.py and html_audit.py need nothing extra; pdf_audit.py is more reliable with pypdf; palette_audit.py needs Pillow; rendering PDFs needs one of pdftoppm, Ghostscript, pypdfium2, or PyMuPDF. The review still works without them.
metadata:
  author: GW Open Source Program Office
  version: "1.0"
---

# GW accessibility review

Produce a written review of a marketing or communication piece: can it be published under
GW's Digital Content Accessibility Policy, what stops it, and exactly what to change.

The sources are summarised in `references/gw-standards.md`; the testable checks are in
`references/accessibility-checks.md`. Read `brand/profile.md` first: it says who the reviews
are for and what the palette allows.

This is the companion to `gw-design-review`. That skill asks whether a piece is on brand and
well composed; this one asks whether people can use it. A piece can pass either and fail
the other, and the contrast rules are where they most often disagree. Do not review design
quality here, only note it when it bears on access.

## What this review can and cannot establish

You are usually given an exported file, an image, or a link — not the source. So:

- **You can measure:** colour contrast, text size (roughly), link wording, heading order
  and alt attributes in HTML, PDF tagging, whether text is real or an image, greyscale
  legibility, what a screenshot shows.
- **You cannot see:** alt text on images in Canva, Word, or social platforms; caption files;
  reading order in a tag tree you weren't given; whether a form works by keyboard.
- **Never present absence of evidence as a pass.** Anything you could not check goes under
  **Not verified** in the report, with how the author can check it.
- **Never say a piece "is accessible" or "WCAG compliant".** Say "no Must fix findings in
  what was checked".

## Before you start

Work out three things from the file and the request; ask only about what they leave open.
State what you inferred in the report header.

1. **Content type.** Decide which checks apply (map below). One piece can be several: a
   deck exported to PDF and posted on a web page is a document, a PDF, and web content.
2. **Where it will be published.** A web page, an email, a social post, a printed handout,
   signage. This decides who the audience is and whether GW Policy applies directly
   (anything digital) or by house practice (print only).
3. **Is the source available?** If the author can give you the Word/PowerPoint/Canva/HTML
   source, review that too: it is where alt text and structure live.

| Content type | Checks to run |
|---|---|
| Web page, landing page | §1 colour, §2 text, §3 images, §4 structure, §5 links, §6 charts if any |
| HTML email / newsletter | as web, plus P2; T3 matters most |
| PDF (report, prospectus, flyer, schedule) | §1, §2, §3, §6 if any, D1–D6; S1, S2, S4 in the tag tree |
| Word / PowerPoint / Google file | §1–§4, §5, D7 |
| Slide deck (as images or PDF) | §1, §2 (T2: 24 pt floor), §3, §6; D1–D5 if exported to PDF |
| Poster, flyer, banner (image or print) | §1, §2, §3 (I4 above all), V5; Q2 |
| Social graphic or post | §1, §2, §3, P1 |
| Chart / infographic | §1, §3 (I3), §6 |
| Video, livestream, audio | §7 M1–M4; §1 and T6 for what is on screen |
| Digital signage | §1, §2, T6, P3 |
| Third-party tool or vendor | §9 Q1 |

## Step 1 — Look at it properly

Review at a size where the smallest text is readable. Use whatever your client provides:

- **PDF** — render pages with `scripts/rasterize.py doc.pdf` (see Step 2). Re-render at
  `--dpi 300` for small print.
- **Image** — view it directly.
- **Web page or HTML** — open in a browser at about 1440 px and 390 px; also save the source
  and run `html_audit.py` on it.
- **Canva, Figma, Google Slides link** — open it, page through, and extract the text layer.
  Text that is missing from the text layer is probably text in an image (T1).
- **Video** — check whether captions are burned in, available as a track, or absent.

Then three quick looks:

1. **Greyscale.** Convert or imagine the page in black and white. Do charts, status, and
   hierarchy survive (V5)?
2. **Squint at the thumbnail.** Is the key fact (date, place, action) still findable?
3. **Text-only.** If the images vanished, what would a person get? That's roughly what a
   screen-reader user gets.

## Step 2 — Run the objective checks

Contrast ratios and structure checks are measurable, and estimates by eye are often wrong.
Report the numbers.

Find the skill's scripts directory (paths in the table are relative to the skill, not to the
user's folder):

```bash
SKILL=$(dirname "$(find . ~/.claude/skills ~/.agents/skills -maxdepth 6 -name SKILL.md -path '*gw-accessibility-review*' 2>/dev/null | head -1)")
```

| Command | What it does | Needs |
|---|---|---|
| `python3 "$SKILL/scripts/contrast.py" "#FFD34D" "#FFFFFF"` | WCAG contrast for one foreground/background pair | Nothing |
| `python3 "$SKILL/scripts/contrast.py" --palette` | The GW palette against the usual grounds, with what each may be used for | Nothing |
| `python3 "$SKILL/scripts/html_audit.py" page.html` | Headings, lang, title, alt attributes, link text, document-type links, layout tables, landmarks — with line numbers | Nothing |
| `python3 "$SKILL/scripts/pdf_audit.py" doc.pdf` | Tagged?, real text?, title, language, figures with alt, headings in the tag tree | pypdf (best) or nothing |
| `python3 "$SKILL/scripts/rasterize.py" doc.pdf [--pages 2-4] [--dpi 300]` | Renders PDF pages to PNGs | pdftoppm, Ghostscript, pypdfium2, or PyMuPDF |
| `python3 "$SKILL/scripts/palette_audit.py" image.png` | Dominant flat colours matched to the palette; use it to find text and background colours to feed to contrast.py | Pillow |

To measure a text colour in an image, sample it with `palette_audit.py` (or read it from
the design source), then run `contrast.py` on the pair. For text over a photograph, measure
the worst-case region, not the average.

Run `html_audit.py` and `pdf_audit.py` before you read the file in detail: they catch the
mechanical failures (skipped heading, "click here", untagged PDF) and let you spend your
attention on judgment. Their severities are ceilings, not verdicts — apply the rules in
`report-format.md`.

If a script is missing a dependency, its error message names what to install. If nothing
can be installed, continue without that check and list it under "Checks run" as not run.

## Step 3 — Work through the checks

Read `references/accessibility-checks.md` and run the checks for the content type(s) you
identified. Each check has a pass condition and a source tag; the tag caps the severity.

When a finding turns on the exact wording of a rule, read the relevant section of
`references/gw-standards.md` so you quote it as written. If you need something newer or
more specific than that summary, the originals are at
https://accessibility.gwu.edu/standards-and-best-practices and
https://compliance.gwu.edu/digital-content-accessibility-policy — fetch them if your
client can, since GW may have updated them.

## Step 4 — Write the report

Read `references/report-format.md` for the structure, the verdict, the severity levels, and
the tone. Deliver the report as a Markdown file unless the user asks for something else; if
your client can publish shareable pages, offer that when the report will be shared.

## Ground rules

- **Lead with what works, and mean it.** Name two or three specific things that help
  readers and say why.
- **Every finding names the element, the location, the rule, who it affects, and the fix.**
  "Poor contrast" is not a finding. "The 'Who Attends?' heading on page 3 is OSCON Gold on
  white, 1.43:1; set it in GW Blue (11.68:1)" is.
- **Separate what you checked from what you could not.** The *Not verified* section is part
  of the review, not an apology.
- **Keep GW requirements and your own judgment apart.** A WCAG criterion or a GW Standards
  requirement can be Must fix. House practice cannot. WCAG 2.2 items are Consider: GW's
  policy names 2.1.
- **Do not review taste.** Colour, type, and layout choices matter here only if they create
  a barrier. Leave brand and composition to `gw-design-review`.
- **Describe the change; leave the rebuilding to them.** Say what to change and why.
  Rebuilding the file is a separate request. For alt text, a *suggested* alt text in the
  finding is helpful — it shows what good looks like — but the author should check it
  against what the image is for.
- **No legal conclusions.** You can say a piece does not meet WCAG 2.1 AA, which GW Policy
  adopts. Do not say whether it violates the ADA or Section 504; send those questions to
  the Office of Ethics, Compliance, and Risk.
- **Point to help.** GW Digital Accessibility (accessibility.gwu.edu) and the Web Strategy
  and Support office hours (go.gwu.edu/officehours) can answer questions the review can't.
