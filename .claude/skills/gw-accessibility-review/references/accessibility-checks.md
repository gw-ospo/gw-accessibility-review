# Accessibility checks

Testable checks for GW OSPO and OSCON marketing and communication output. Derived from the
GW Digital Content Accessibility Policy (WCAG 2.1 AA) and GW Standards and Best Practices;
see `gw-standards.md` for the sources.

Every check is tagged with where it comes from, and the tag caps the severity:

| Tag | Meaning | Highest severity |
|---|---|---|
| `[WCAG x.x.x]` | A WCAG 2.1 A/AA criterion. GW Policy adopts WCAG 2.1 AA, so failing it is a policy failure | Must fix |
| `[GW Standards]` | A rule GW Standards states as a requirement ("required", "must", "don't") | Must fix |
| `[GW Standards, advisory]` | GW Standards recommends it ("avoid", "consider", "recommended") | Should fix |
| `[House practice]` | This skill's judgment; not in GW sources or WCAG AA | Should fix |

Cite the tag in the finding's *Rule:* line. For house practice, say plainly that it is not
a GW rule.

**Applicability.** Run only the checks for the content types present (see the map in
`SKILL.md`). Mark the others "not applicable", not "passed". A check you cannot verify
from what you were given (for example a PDF's tag tree from a screenshot) is **Not verified**,
never a pass. Say what the author should check and how.

**Print-only pieces.** WCAG and GW Policy cover digital content. A print-only piece is out
of formal scope, but flyers and posters are nearly always also posted or emailed as PDFs
or images. Treat a print piece as digital if it will circulate that way; otherwise apply the
contrast, type, and colour checks as house practice and say so.

---

## 1. Colour and contrast

**V1 — Text contrast.** `[WCAG 1.4.3]` `[GW Standards]`
Pass: text and images of text are at least 4.5:1 against their background, or 3:1 if large
(18 pt+, or 14 pt+ bold). Measure with `scripts/contrast.py`; for a text colour over a
photo or gradient, sample the worst-case region and measure it.
Common failure: gold, green, or orchid text on white; white text over a photograph's bright
area; light-blue captions on a pastel panel.

**V2 — Non-text contrast.** `[WCAG 1.4.11]`
Pass: icons that carry meaning, button and form-field borders, and chart marks are at least
3:1 against their neighbours.
Common failure: pale pastel chart bars on white; a thin Blue Fog outline on a Parchment button.

**V3 — Colour is not the only signal.** `[WCAG 1.4.1]` `[GW Standards]`
Pass: nothing is conveyed only by colour — required fields, status, chart series, links,
"click the green button". A second cue is present: label, shape, pattern, underline.
Common failure: a schedule where track names are distinguished only by tile colour; a
legend that is colour swatches only.

**V4 — Approved colour combinations.** `[GW Standards]`
Pass: text and images of text use GW palette colours in combinations that pass AA. Check with
`contrast.py --palette`. Note that the OSCON Gold, Green, and Orchid accents fail as text on
white (see `DESIGN.md` §1.5) and so belong in shapes and fills.
Common failure: a "brand-colour" heading that is on palette and still fails contrast.
This is the main way on-brand and accessible diverge.

**V5 — Reads in greyscale.** `[GW Standards]` (charts) `[House practice]` (everything else)
Pass: convert the page to greyscale; hierarchy, chart series, and key states are still
distinguishable. Charts must pass; for other pieces it is a useful stress test.
Common failure: Potomac and Row House bars that come out as the same grey.

---

## 2. Text and type

**T1 — Live text over text-in-image.** `[GW Standards]` `[WCAG 1.4.5]`
Pass: text is live (selectable, resizable, readable by assistive tech) wherever possible.
Where it must be in a graphic (logo), alt text carries it.
Common failure: a PDF or web banner exported as one flat image with all text baked in; a
flyer posted as a JPG with the event details only in pixels.

**T2 — Legible size.** `[House practice]`
Pass: nothing meant to be read is below roughly 9 pt in print, 24 pt on a 1920×1080 slide,
or 16 px on a web page (these are the brand floors in `DESIGN.md` §2 plus a web norm; WCAG
sets no minimum size). Legal lines may go smaller if they are not the only place a fact lives.
Common failure: dates, times, and URLs set as small caption text.

**T3 — Reflow and resize (web and email).** `[WCAG 1.4.4]` `[WCAG 1.4.10]`
Pass: text can be enlarged to 200% and the layout reflows at 320 px width without
horizontal scrolling or clipped content.
Common failure: fixed-width email layouts; text boxes with a fixed height that clips.

**T4 — Plain language.** `[GW Standards]` (link text) `[House practice]` (body copy)
Pass: sentences are short and direct; acronyms are spelled out on first use; the call to
action says what will happen. Aim for a grade 8–9 reading level for general audiences.
Common failure: "Leverage cross-institutional OSS synergies" where "Work with other
universities on open source" would do.

**T5 — Language is identified.** `[WCAG 3.1.1]`
Pass: web pages and PDFs declare their language (`lang="en"`); a passage in another
language is marked. `scripts/html_audit.py` and `scripts/pdf_audit.py` check this.

**T6 — Moving and blinking content.** `[GW Standards]` (signage) `[WCAG 2.3.1]` `[WCAG 2.2.2]`
Pass: nothing flashes more than three times a second; auto-playing motion longer than five
seconds can be paused. For signage: no rapidly blinking content.

---

## 3. Images and graphics

**I1 — Informative images have alt text.** `[GW Standards]` `[WCAG 1.1.1]`
Pass: every informative image — web, email, Office, PDF, social — has alt text that
describes the content and includes any text in the image. Headshots give name and role.
No file names ("photo1821.jpg"), no "image of". Be descriptive, not verbose.
Where alt text lives is medium-specific: the `alt` attribute (web, email); Format Picture →
Alt Text (Office); the Alt Text field on each platform (see §7).
Common failure: missing alt; alt that repeats the file name; alt of "logo" for a logo that
contains the conference name and year.
*Verification:* you can see an image but cannot see its alt text. Use `html_audit.py` for
HTML and email source; for PDFs, `pdf_audit.py` reports whether figures have alt. For
anything else, mark **Not verified** and tell the author where to check.

**I2 — Decorative images are marked decorative.** `[WCAG 1.1.1]` `[House practice]`
Pass: purely decorative art (the OSCON pattern, divider flourishes) has empty alt
(`alt=""`) or is marked decorative, so screen readers skip it.
Common failure: the pattern strip announced as "image" or read out via a long filename.

**I3 — Complex images get a long description.** `[GW Standards]`
Pass: charts, infographics, maps, and diagrams have a text description on the same page,
and the short alt text says where it is.
Common failure: an infographic whose whole message lives only in the picture.

**I4 — No poster-as-page.** `[GW Standards]`
Pass: critical information (dates, location, how to register, who to contact) is also
available as real text, not only inside a poster image. A PDF that is a single graphic does
not pass.
Common failure: an event announced by posting the poster JPG with "see image for details".

**I5 — Text in image meets contrast.** `[GW Standards]` `[WCAG 1.4.3]`
Pass: text baked into graphics meets V1.

---

## 4. Structure and navigation

**S1 — Real headings, in order.** `[GW Standards]` `[WCAG 1.3.1]`
Pass: headings use heading styles or heading tags; one H1; no skipped levels (H2 → H4).
Not bold or large body text posing as headings. Applies to web, email, Word, PDF.
Common failure: a "heading" that is a bold 18 pt paragraph, invisible to a screen reader's
heading navigation.

**S2 — Logical reading order.** `[GW Standards]` `[WCAG 1.3.2]`
Pass: reading order (top-to-bottom, left-to-right, columns in sequence) matches the visual
order. Sidebars and callouts don't interrupt the middle of a sentence.
Common failure: a Canva/InDesign export whose tag order follows the order objects were
created, not the page.

**S3 — Page and document titles.** `[WCAG 2.4.2]`
Pass: web `<title>` and PDF Title metadata describe the piece. PDF viewers show Title, not
the file name, when "DisplayDocTitle" is set.
Common failure: title "Untitled-1" or "Microsoft Word - flyer_v7_FINAL".

**S4 — Lists and tables are real.** `[WCAG 1.3.1]`
Pass: lists use list markup; data tables have header cells and no merged-cell layout tricks;
tables are not used for layout.
Common failure: a schedule laid out as tab-aligned text; bullets typed as "•" characters.

**S5 — Bypass blocks and landmarks (web).** `[WCAG 2.4.1]`
Pass: a long page has landmarks (`main`, `nav`, `header`) or a skip link.

---

## 5. Links

**L1 — Descriptive link text.** `[GW Standards]` `[WCAG 2.4.4]`
Pass: link text describes the destination or action on its own. No "click here", "read
more", "more information", "learn more", "here". No raw URLs as text.
Common failure: "Register here", "Read more" repeated six times in a list of events.
Printed URLs are the exception: a human-readable short URL on a poster is fine.

**L2 — Unique link text for unique destinations.** `[GW Standards]`
Pass: two links with the same text go to the same place.

**L3 — Links are not identified by colour alone.** `[GW Standards]` `[WCAG 1.4.1]`
Pass: links carry at least two visual cues — colour plus underline, bold, or italics.
Common failure: Potomac-blue text with no underline in a paragraph of GW Blue text.

**L4 — Document type in link text.** `[GW Standards]`
Pass: links to downloads state the file type: "Sponsorship Prospectus (PDF)".

**L5 — Target size.** `[House practice]` (WCAG 2.2 criterion 2.5.8; not in GW Policy)
Pass: tap targets in email and mobile are at least 24×24 CSS px, ideally 44×44.

---

## 6. Charts and graphs

Apply to any chart, graph, or data-driven infographic.

**C1 — Data repeated as a table or text.** `[GW Standards]`
Pass: the underlying data is available as a table or list on the same page, and a text
summary of the point of the chart appears in the body, not only as alt text.

**C2 — More than colour.** `[GW Standards]` `[WCAG 1.4.1]`
Pass: series are told apart by texture, line style, shape, or direct labels as well as
colour.

**C3 — Chart-type rules.** `[GW Standards]`
- *Bar:* sufficient light/dark contrast between bars; each bar labelled with its value.
- *Line:* different line style per line; label lines directly; label visible data points.
- *Pie:* leader lines from label to slice; white space between slices.
Pass: the rules for the chart type present are met.

**C4 — Chart contrast.** `[WCAG 1.4.11]` `[WCAG 1.4.3]`
Pass: marks are ≥3:1 against the ground and neighbours; axis and label text ≥4.5:1.

**C5 — Built with an accessible tool.** `[GW Standards, advisory]`
Pass: GW staff build charts with Everviz, which exports accessible output. Not required if
C1–C4 are met by other means.

---

## 7. Media and platforms

**M1 — Video is captioned.** `[GW Standards]` `[WCAG 1.2.2]`
Pass: pre-recorded video has accurate captions, human-reviewed even when auto-generated.
Music with no dialogue is captioned ("(Music playing)").
*Verification:* you rarely see the caption file. If you cannot, mark **Not verified**.

**M2 — Transcript for visual-heavy video and audio.** `[GW Standards]` `[WCAG 1.2.1]` `[WCAG 1.2.3]`
Pass: audio-only content has a transcript; video whose meaning is mostly visual has a
screen-reader-readable transcript or audio description.

**M3 — Live streams.** `[GW Standards]` `[WCAG 1.2.4]`
Pass: scheduled streams have live captioning booked at least 72 hours ahead; spontaneous
streams are captioned within 48 hours.

**M4 — Auto-play and controls.** `[WCAG 1.4.2]` `[WCAG 2.2.2]`
Pass: audio does not auto-play for more than three seconds without a way to stop it; video
has operable controls.

**P1 — Social posts.** `[GW Standards]`
Pass: image posts carry alt text in the platform's field (X "add description"; Facebook
alt text; Instagram "Advanced settings"; LinkedIn "image description"). Text inside an image
is repeated in the post text. Videos are captioned. Text overlays on images are minimal and
meet contrast; Instagram Stories text has enough contrast against its background.
*Verification:* you rarely see alt fields. A graphic with a lot of baked-in text and a
post caption that doesn't repeat it is a visible failure. Otherwise **Not verified**.

**P2 — Mass email.** `[GW Standards]`
Pass: images have alt text; body text and graphics meet contrast; headings are real
headings; the email makes sense with images off; the message isn't a single image.
Check the HTML source with `html_audit.py`.

**P3 — Digital signage.** `[GW Standards]`
Pass: all text meets contrast; video is captioned; nothing blinks rapidly; text is readable
at viewing distance (house practice).

---

## 8. Documents and PDFs

For Word, PowerPoint, Google Docs, and the PDFs exported from them or from Canva/InDesign.
`scripts/pdf_audit.py` checks the structural items below that it can.

**D1 — The PDF is tagged.** `[WCAG 1.3.1]` `[GW Standards]`
Pass: the PDF has a structure tree and is marked as tagged (MarkInfo /Marked true).
Common failure: "Print to PDF", a screenshot-to-PDF, or a Canva export without the
"accessible" option. These produce untagged PDFs that screen readers cannot navigate.

**D2 — Not a flattened image.** `[GW Standards]`
Pass: the PDF contains real text. A PDF that is one picture per page fails, as does a
scanned document without OCR.

**D3 — Title and language metadata.** `[WCAG 2.4.2]` `[WCAG 3.1.1]`
Pass: Title is meaningful and language is set (see S3, T5).

**D4 — Figures have alt text; decorative content is artifacted.** `[GW Standards]` `[WCAG 1.1.1]`
Pass: every figure in the tag tree has alt text. Backgrounds and the OSCON pattern are
artifacted, not tagged as figures.

**D5 — Headings, lists, tables tagged.** `[GW Standards]` `[WCAG 1.3.1]`
Pass: see S1, S4, in the tag tree.

**D6 — Should this be a webpage?** `[GW Standards, advisory]`
Pass: a document that is mainly content to be read, with no print or signature need, is
better as a web page. Mention it as *Consider* when the piece is long text with few design
requirements.

**D7 — Office documents.** `[GW Standards]`
Pass: run Check Accessibility in Word/PowerPoint/Excel (GW provides Microsoft 365) and clear
errors. PowerPoint: every slide has a unique title, reading order is set in the Selection
Pane, and slides use layout placeholders instead of loose text boxes.
*Verification:* you will not see this from an exported image. Mark **Not verified** unless
you were given the source file.

---

## 9. Process and procurement

Only when the request involves a tool, vendor, or platform rather than a piece of content.

**Q1 — Third-party tools meet WCAG AA.** `[GW Policy]` `[GW Standards]`
Pass: a form, scheduler, survey, or registration tool used for GW business has a VPAT/ACR
reviewed before purchase, and any configured colour themes and templates meet contrast.
Common failure: a free form-builder with the conference's brand theme applied, whose
button colour fails contrast.

**Q2 — A way to report and be helped.** `[GW Policy]`
Pass: public pages, events, and emails give a contact for access requests ("To request an
accommodation, contact …"). Events: the registration form asks about accommodations.
Reports of barriers go to accessibility.gwu.edu/report-barrier-accessibility.
Rated `[House practice]` for the wording; the 30-day remediation duty is GW Policy.
