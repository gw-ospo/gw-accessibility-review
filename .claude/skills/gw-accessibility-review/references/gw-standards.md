# GW accessibility sources

What the review is measured against, and where each rule comes from. Cite these by their
short names in findings.

| Short name | Source | Weight |
|---|---|---|
| **GW Policy** | [Digital Content Accessibility Policy](https://compliance.gwu.edu/digital-content-accessibility-policy), Office of Ethics, Compliance, and Risk | The requirement |
| **GW Standards** | [Standards and Best Practices](https://accessibility.gwu.edu/standards-and-best-practices), GW Digital Accessibility | How GW says to meet it |
| **WCAG 2.1 AA** | W3C Web Content Accessibility Guidelines 2.1, Level AA | The measurable standard the policy adopts |

## What GW Policy requires

- **Standard:** WCAG 2.1, Conformance Level AA, for all digital content and functionality
  that is developed, purchased, or used, including university websites and social media.
- **Scope:** every GW community member — faculty, postdocs, staff, students, affiliates.
  Student workers producing OSPO material are in scope.
- **Existing and new content** must conform, unless an Undue Financial or Administrative
  Burden or Fundamental Alteration is demonstrated through the Accessibility Committee.
  Even then, an Equally Effective Alternative Access must be available on request.
- **30 days:** once a content owner receives a complaint, or content is found inaccessible,
  they have 30 days to fix it. After that the university may take the content offline.
  Barriers are reported at accessibility.gwu.edu/report-barrier-accessibility.
- **Procurement:** third-party tools used for GW business (Calendly, Salesforce, a survey or
  email platform) must meet WCAG AA. Ask the vendor for a VPAT or ACR before buying.
- Policy next scheduled review: 2027–2028 academic year.

WCAG 2.2 is **not** what the policy names. Where a 2.2 criterion is useful (target size,
focus not obscured), recommend it as *Consider*, never *Must fix*.

## What GW Standards add, by content type

Organised by POUR (Perceivable, Operable, Understandable, Robust), the principles GW cites.

**Web content**
- One H1 per page, then H2–H6 without skipping levels. Real heading styles, not bold or large text.
- Link text is a plain-language description of the destination. No raw URLs, no "click here",
  "read more", "more information". No identical link text going to different places.
- Links carry at least two visual cues (colour plus underline, bold, or italics) — colour alone is not enough.
- Document links name the file type in the text: "Brand Guidelines (PDF)".

**Documents (Office, PDF)**
- Alt text on every image, real heading styles, logical reading order.
- Ask whether it must be a document at all, or could be a web page.
- Never post a PDF that is a single graphic. See https://accessibility.gwu.edu/pdf-accessibility.

**Images**
- Alt text is required. Describe the content and include all text in the image. No file
  names, no "image of". Headshots: name and role.
- Avoid posters as images, especially for critical information.
- Long descriptions go on the same page, with the alt text pointing to them.
- Use live text where possible; if text must be in a graphic (a logo), alt text conveys it.

**Colour and contrast**
- 4.5:1 minimum for text and images of text (WCAG AA). 3:1 for large text and UI/graphics.
- Use only approved colours from the GW colour palette
  (https://communications.gwu.edu/brand-guidelines/color-palette); only some combinations pass AA/AAA.
- Do not use colour as the only means of conveying information (WCAG 1.4.1).
- Charts must read in black and white.

**Charts and graphs**
- Repeat chart data in a table; put a text summary in the body, not only in alt text.
- Use textures, line styles, or distinct shades in addition to colour.
- Bar: label each bar with its value. Line: different line style per line, label lines directly.
  Pie: leader lines from labels to slices, white space between slices.
- GW staff can use Everviz for accessible charts and maps.

**Social media**
- X, Facebook, Instagram, LinkedIn: alt text on every image (each platform has its own field).
  Text in an image is repeated in the post text. Caption all video. Keep text on images minimal.
  Instagram Stories text needs sufficient contrast against its background.

**Mass email**
- Alt text on images, contrast for body text and graphics, real text headings.

**Video**
- Captions, transcripts, or both; review auto-captions for accuracy.
- Visual-heavy video needs a screen-reader-readable transcript; visuals meet contrast rules.
- Caption music when no dialogue is present ("(Music playing)").
- Live: scheduled streams use live captioning booked 72 hours ahead; spontaneous streams
  captioned within 48 hours. Produced video: Rev is the recommended captioning vendor.
- Audio-only: no dedicated GW section; follow W3C WAI media guidance (https://www.w3.org/WAI/media/av/).
  A transcript is the usual need.

**Digital signage**
- Contrast guidelines for all content, captioned video, no rapidly blinking content.

## Where the sources stop

GW Standards does not give numeric minimum type sizes, a required document language, or
form/keyboard rules for print. When a check draws on WCAG 2.1 or common practice instead of
a GW statement, it is tagged accordingly in `accessibility-checks.md`. Do not present those
as GW rules.
