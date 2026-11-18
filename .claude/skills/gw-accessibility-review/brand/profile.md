# Profile — GW OSPO and GW OSCON accessibility review

Who this review is for, and what it needs to know about the institution before it starts.

## Institution

The George Washington University (GW), Open Source Program Office (OSPO), including the GW
Open Source Conference (OSCON). Accessibility obligations come from the GW Digital Content
Accessibility Policy, which adopts WCAG 2.1 Level AA and applies to every GW community
member, student workers and volunteers included.

## What gets reviewed

All GW OSPO marketing and communication output: posters, flyers, slide decks, reports,
sponsorship prospectuses, web pages, mass email, social posts, charts and infographics,
video, signage, and any third-party tool used to collect registrations or send messages.

## Brand context and accessibility

The brand palette still matters here, but only for contrast. The OSCON extended accents
(Gold `#FFD34D`, Green `#33A56E`, Orchid `#B04A8F`) fail 4.5:1 as text on white, and Gold
fails even 3:1; they belong in shapes and fills, or as large text on dark grounds only
after measuring. Do not review whether an accent is *allowed* (that is `gw-design-review`);
review whether text set in it can be read.

## Who reads the review

Usually a student worker or staff member who makes the piece, often new to accessibility.
The report has to teach and say who is affected, not only grade. A second reader is whoever
approves publication, who needs the verdict and the *Not verified* list at the top and
bottom of the report.

## Brand files

| File | What it is |
|---|---|
| `brand/palette.json` | The GW / OSCON colours, for `contrast.py` and `palette_audit.py` |
| `brand/DESIGN.md` | The OSCON design specification this palette is read from. Copied from the `gw-design-review` skill; keep the two in sync. Its §1.5 summarises WCAG for the palette |
| `references/gw-standards.md` | Summary of GW Policy and GW Standards, with source URLs |
| `references/accessibility-checks.md` | The testable checks, each tagged with its source |

If the project being reviewed has its own `DESIGN.md` or `palette.json`, pass it to the
colour scripts with `--design`.

## Contacts to name in reports

- GW Digital Accessibility: accessibility.gwu.edu
- Report a barrier: accessibility.gwu.edu/report-barrier-accessibility
- Policy questions: Office of Ethics, Compliance, and Risk, 202-994-3386
- Colour palette and Everviz questions: Web Strategy and Support (go.gwu.edu/officehours)
