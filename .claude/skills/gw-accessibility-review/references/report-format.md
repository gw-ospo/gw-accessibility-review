# Report format

The review is a teaching and clearance document, not a scorecard. The reader should finish
knowing whether the piece can go out, what to change, in what order, and why — well enough
to build it accessibly the next time without the reviewer.

## Severity levels

Use exactly these three, and label every finding with one.

| Level | Meaning |
|---|---|
| **Must fix** | Fails a WCAG 2.1 AA criterion, or a GW Standards requirement — a check tagged `[WCAG x.x.x]` or `[GW Standards]` in `accessibility-checks.md`. Under GW Policy the piece cannot be published this way. |
| **Should fix** | Fails a `[GW Standards, advisory]` or `[House practice]` check, or is a barrier GW's sources don't name but that measurably costs a reader. |
| **Consider** | An improvement beyond the required standard (including WCAG 2.2 items). Say plainly that it is optional. |

A house-practice check never makes a finding Must fix, however confident you are. If
something should be a rule and the sources are silent, say so in the finding; the fix is to
raise it with GW Digital Accessibility or the maintainers, not to stretch an existing rule.

## Verdict

Every report ends its header with one verdict, so the reader knows where they stand:

| Verdict | When |
|---|---|
| **Not ready to publish** | One or more Must fix findings |
| **Ready, with verification needed** | No Must fix findings, but one or more checks are **Not verified** and the author has to confirm them in the source |
| **Ready to publish** | No Must fix findings and nothing material left unverified |

Never write "WCAG compliant" or "accessible". A review of an exported file and a few
scripts cannot establish that. Say "no Must fix findings in what was checked".

## Structure

```markdown
# Accessibility review — <piece name>
<Content type and format> · Reviewed <date> · Against GW Digital Content Accessibility
Policy (WCAG 2.1 AA) and GW Standards and Best Practices
<Anything you inferred rather than were told — content type, where it will be published,
print vs digital — in one line. Omit if all stated.>
**Verdict: <Not ready to publish | Ready, with verification needed | Ready to publish>**

## The one-line read
<What the piece does well for accessibility, and the single biggest barrier. Two sentences.>

## What's working
<Two or three specific things, each with WHY it helps a reader. Name the element.>

## At a glance
| Principle | Result |
|---|---|
| Perceivable (contrast, alt text, captions, colour) | <Pass / n Must fix / Not verified> |
| Operable (links, headings, navigation, motion) | ... |
| Understandable (language, plain language, consistency) | ... |
| Robust (tagging, structure, real text) | ... |

## Findings

### Must fix
**1. <Short imperative title>**
*Where:* <page / element>
*Rule:* <WCAG 2.1 AA x.x.x, or GW Standards section, or house practice with check ID>
*Who it affects:* <e.g. screen-reader users, low-vision users, deaf and hard-of-hearing users>
*What's happening:* <one or two sentences of diagnosis, with the measured number if any>
*Fix:* <concrete, specific, actionable — a value or a step, not a direction>

### Should fix
...same shape, numbering continues...

### Consider
...same shape...

## Not verified
<Checks you could not run from what you were given, and exactly how the author can check
each one: "alt text on the three headshots — in Canva, select the image → Alt text".
Separate from findings. An unverified check is not a pass.>

## If you only do three things
<The three highest-leverage fixes, as a checklist. Many readers will act on this section
and nothing else.>

## Checks run
<Which objective checks were run and their results — contrast pairs tested (with ratios),
html_audit / pdf_audit output, greyscale check. Include the numbers so the reader can
re-run them. List any check that could not run, and why, so its absence is not read as a
pass.>

## What happens next
<One or two lines: GW Policy gives content owners 30 days to fix inaccessible content once
it is reported or found, and unresolved content may be taken offline. Barriers are reported
at accessibility.gwu.edu/report-barrier-accessibility. Include only when the verdict is Not
ready to publish or the content is already live.>
```

## Writing the findings

**Name the element and its location.** "Page 3, the 'Who Attends?' heading", "the second
slide's bar chart", "the three headshots on the speakers page".

**Give a value or a step, not a direction.** "Improve contrast" is not actionable. "Set it in
GW Blue #033C5A (11.68:1) instead of OSCON Gold (1.43:1)" is.

**Say who it affects.** A person who has never used a screen reader may not know why missing
alt text matters. One phrase — "a screen-reader user hears 'image' and nothing else" —
teaches more than the citation.

**Cite the rule.** WCAG 2.1 AA 1.4.3, GW Standards (Images), or the check ID with
"house practice". Quote the rule as written, not a stronger paraphrase.

**One finding per problem.** If link text is "click here" on six links, that's one finding
listing all six, not six findings.

**Rank across the whole piece.** Barriers that block access entirely (untagged PDF, missing
captions, image-only content) rank above barriers that make reading harder (borderline
contrast).

### Worked examples

> **1. Section headings are unreadable on white**
> *Where:* "Who Attends?" and "Why Sponsor?" headings, pages 3–4
> *Rule:* WCAG 2.1 AA 1.4.3 (contrast); GW Standards (Color and Contrast)
> *Who it affects:* low-vision users, anyone reading on a phone in daylight
> *What's happening:* both headings are OSCON Gold `#FFD34D` on white: 1.43:1. Even large
> text needs 3:1.
> *Fix:* set them in GW Blue `#033C5A` (11.68:1). Keep the gold as a small square next to
> the heading, where it is a shape and the contrast requirement is lower.

> **4. Event poster is the only place the details appear**
> *Where:* the Instagram post and the web page that embeds the same JPG
> *Rule:* GW Standards (Images: "avoid using posters as images, especially to convey
> critical information"); WCAG 2.1 AA 1.4.5 (images of text)
> *Who it affects:* screen-reader users, anyone who zooms or translates text
> *What's happening:* date, time, location and registration link are all baked into the
> image; the post caption says "Details in image".
> *Fix:* repeat date, time, location, and the registration link as text in the caption and
> on the page, and add alt text that gives the same details.

> **9. Link text is non-specific**
> *Where:* the three "Read more" links under Upcoming Events
> *Rule:* GW Standards (Links); WCAG 2.1 AA 2.4.4
> *What's happening:* a screen-reader user pulling up the links list hears "Read more"
> three times with no clue where each goes.
> *Fix:* name the destination: "OSCON 2027 call for papers", "Workshop schedule (PDF)",
> "Sponsor the conference".

## Length

- **What's working:** 2–3 items.
- **Findings:** 12 at the absolute maximum, fewer is better. Fold symptoms of one cause
  into one finding.
- **Whole report:** readable in under ten minutes.

## Tone

- Address the author, not the artefact: "your headings have good contrast on the cover".
- Describe the effect on the reader, not your feelings.
- No sarcasm, no "obviously". The person reading may be learning accessibility for the
  first time; many working practitioners are too.
- Name correct instincts so they get repeated, particularly the hard ones (real heading
  styles, alt text that is not a file name).
- Do not soften a Must fix. Kindness is in the tone and the explanation, not in hedging
  about whether a rule was broken.
- Do not claim certainty you do not have. Where you could not check something, say so in
  *Not verified*; never imply the piece passes.

## Delivery

Write the report as a Markdown file named `accessibility-review-<piece>-<YYYY-MM-DD>.md` —
in the working directory if you have one, otherwise as a downloadable file — and give it to
the user. If it is going to be shared with a team or discussed in a meeting and your client
can publish shareable pages, offer that, but ask first: a review names someone's work.
