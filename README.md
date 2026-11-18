# gw-accessibility-review

An accessibility reviewer for everything the George Washington University Open Source Program
Office (OSPO) and the GW Open Source Conference (OSCON) publish: posters, flyers, slide decks,
PDFs, reports, prospectuses, web pages, email, social posts, charts, video, and signage.

It checks the piece against the GW
[Digital Content Accessibility Policy](https://compliance.gwu.edu/digital-content-accessibility-policy)
(WCAG 2.1 Level AA) and the GW
[Standards and Best Practices](https://accessibility.gwu.edu/standards-and-best-practices),
and gives back a written report in the same style as the GW design review.

| What | It is |
|---|---|
| [`.claude/skills/gw-accessibility-review/`](.claude/skills/gw-accessibility-review/) | The reviewer. Run it before anything goes out. |
| [`references/gw-standards.md`](.claude/skills/gw-accessibility-review/references/gw-standards.md) | What GW requires, and where each rule comes from. |
| [`references/accessibility-checks.md`](.claude/skills/gw-accessibility-review/references/accessibility-checks.md) | The testable checks, each tagged with its source. |

It is the companion to `gw-design-review`: that skill asks "is it on brand and well composed?",
this one asks "can everyone use it?". Run both.

---

## Get your piece reviewed

Attach a PDF, image, HTML file, or a link, and say where it will be published:

> Check this poster for accessibility. It is a PDF and an Instagram post for the OSCON call for papers.

> Run the accessibility review on this sponsorship prospectus PDF.

> Review this email HTML before I send it.

**You get back a report with:**

- A **verdict**: Not ready to publish, Ready with verification needed, or Ready to publish
- Two or three things that work, and why
- A POUR summary (Perceivable, Operable, Understandable, Robust)
- Ranked findings, each saying where, which rule, **who it affects**, and exactly how to fix it
- A **Not verified** list: things the reviewer cannot see from a file, such as alt text in
  Canva or caption files, with how to check them yourself
- The three highest-leverage fixes
- The numbers behind the contrast and structure checks, so you can re-run them

| | |
|---|---|
| **Must fix** | Fails WCAG 2.1 AA or a GW Standards requirement. Under GW Policy, this blocks publishing. |
| **Should fix** | Advisory GW guidance or house practice. Makes the piece harder to use. |
| **Consider** | Beyond the requirement, including WCAG 2.2 items. Optional. |

**What it cannot do.** It works from what you give it. It cannot see alt text inside Canva,
Word, or social platforms, captions you did not attach, or how a page behaves with a keyboard,
and it says so rather than guessing. It does not claim a piece is "accessible", and it gives
no legal opinion. Questions about the policy go to the Office of Ethics, Compliance, and Risk
(202-994-3386). Barriers are reported at accessibility.gwu.edu/report-barrier-accessibility.
Under the policy, content owners have 30 days to fix reported barriers.

Giving it the source file (Word, PowerPoint, HTML) as well as the export makes the review
much more complete.

---

## Setting it up

This is an **Agent Skill**. Where it goes depends on your tool; the setup is the same as for
`gw-design-review`.

| If you use... | What to do |
|---|---|
| **claude.ai** in a browser | Build the upload package with `sh scripts/build-skill-zip.sh`, then upload `gw-accessibility-review.zip` under Settings, Capabilities, Skills. Do not upload the repository ZIP: it nests `SKILL.md` too deeply. |
| **Claude Cowork, Claude desktop, Claude Code** | Download or clone the repository and point the tool at the folder. The skill loads from `.claude/skills/`. |
| **Cursor, VS Code with Copilot** | Same as Claude. They also read `.claude/skills/`. |
| **ChatGPT / Codex** | Copy `.claude/skills/gw-accessibility-review` into `.agents/skills/`. |
| **Anything else** | Attach `references/gw-standards.md`, `references/accessibility-checks.md` and `references/report-format.md` to your conversation and ask for a review in that format. You lose the measured contrast and structure checks. |

### Helper scripts

Plain Python, run for you during a review. You only need these for a quick number.

```bash
cd .claude/skills/gw-accessibility-review

# Contrast for one pair, or the whole palette against the usual backgrounds
python3 scripts/contrast.py "#FFD34D" "#FFFFFF"
python3 scripts/contrast.py --palette

# Headings, lang, title, alt attributes, link text, document links, layout tables
python3 scripts/html_audit.py page.html

# Tagged? real text? title, language, figure alt text, headings in the tag tree
python3 scripts/pdf_audit.py document.pdf

# Render PDF pages to PNG; match flat colours in a graphic against the palette
python3 scripts/rasterize.py document.pdf --pages 2-4
python3 scripts/palette_audit.py poster.png
```

`contrast.py` and `html_audit.py` need nothing extra. `pdf_audit.py` is reliable with
`pip install pypdf`; without it, it scans raw bytes and reports "unknown" where compressed
objects could hide the answer. `palette_audit.py` needs Pillow. `rasterize.py` needs one of
pdftoppm, Ghostscript, pypdfium2, or PyMuPDF.

---

## For maintainers

| File | Role |
|---|---|
| `SKILL.md` | The workflow: what the review can and cannot establish, content-type map, steps |
| `references/gw-standards.md` | Summary of GW Policy and GW Standards with URLs. **Re-read the originals when either changes** (policy next review: 2027-2028) |
| `references/accessibility-checks.md` | The checks. A tag decides the maximum severity: `[WCAG]` and `[GW Standards]` can be Must fix; `[House practice]` cannot |
| `references/report-format.md` | Report structure, verdict rules, tone |
| `brand/palette.json`, `brand/DESIGN.md`, `brand/profile.md` | Palette values used for contrast, copied from `gw-design-review` |

When the palette changes in `gw-design-review`, copy `brand/DESIGN.md` and `brand/palette.json`
across; `scripts/build-skill-zip.sh` runs `scripts/check-palette.py` and refuses to build if
the two disagree.

`gw-accessibility-review.zip` is a committed build artifact. Rebuild it after any change:

```sh
sh scripts/build-skill-zip.sh
```

See [`HISTORY.md`](HISTORY.md) for how the skill was derived and the decisions behind it.
