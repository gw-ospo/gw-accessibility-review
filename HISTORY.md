# History

`gw-accessibility-review` was forked from `gw-design-review` in November 2026. The design
review asks whether a GW OSPO or OSCON piece is on brand and well composed; this one asks
whether people can use it, and whether it can be published under GW's accessibility rules.

## Sources

- GW [Digital Content Accessibility Policy](https://compliance.gwu.edu/digital-content-accessibility-policy):
  WCAG 2.1 Level AA for all digital content, including social media; a 30-day remediation
  window once content is reported or found inaccessible; VPAT or ACR for purchased tools.
- GW [Standards and Best Practices](https://accessibility.gwu.edu/standards-and-best-practices):
  rules by content type — web, documents, images, colour, charts, social, email, video,
  signage, procurement. Both pages were read on 4 November 2026. The policy's next review
  is scheduled for 2027–2028; re-read both sources when it happens.

## What was kept, changed, and added

- **Kept:** the skill layout, the report's shape and tone, the severity ladder, the
  `contrast.py`, `gw_palette.py`, `palette_audit.py`, and `rasterize.py` scripts, and the
  `brand/` folder (the palette is still needed to judge contrast).
- **Replaced:** the brand checks and design-principles reference became
  `accessibility-checks.md`, with every check tagged `[WCAG]`, `[GW Standards]`,
  `[GW Standards, advisory]` or `[House practice]` so that only requirements can be Must fix.
- **Added:** a publish **verdict**, a **Not verified** section (a reviewer rarely sees alt
  text or caption files, and silence must not read as a pass), a POUR summary table, and
  `html_audit.py` and `pdf_audit.py` for the mechanical checks.

## Decisions worth remembering

- WCAG 2.1 is the standard, not 2.2. WCAG 2.2 items are *Consider*.
- The review never says "accessible" or "WCAG compliant" — only "no Must fix findings in
  what was checked".
- The review gives no legal conclusions about the ADA or Section 504.
