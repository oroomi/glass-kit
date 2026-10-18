# Before and after

## Before: our JunctionX Turku entry (18 Oct 2026)
`library/shots/ours_home_desk.png`, `library/shots/ours_home_phone.png`. Judges' verdict in the owner's words: "didn't stand out,
was clunky and not easy on the eye". What the screenshot shows:
- The first screen is a 266 px filter column (radio buttons, 12 checkboxes) beside a prompt box. The largest number on
  screen is "59 of 59" at about 14 px. Nothing says what matters this week.
- A serif display headline ("Ask Aava") that names the assistant instead of telling the story.
- Navy page, hairline rules, no cards, no depth; the eye has nowhere to land.
- Phone: a paragraph and chips push the results below the fold; MENU button instead of a tab bar.

The two rivals that beat it (`bluewatch_home_*`, `atlas_*`) open on big numbers, a visual (sonar, donut, bars) and an
act-now list with deadlines, in white rounded cards with tinted icon squares, pill tabs, and (BlueWatch) a floating
glass tab bar on the phone.

## After: the kit's dashboard template
`docs/shots/dashboard_desk_light.png` (and `_dark`, `_phone_*`), side by side with the above in a private comparison image
(the comparison images include third-party apps and are kept private).
- Sentence with the number in it: "6 signals need action this week", one primary action, a mono provenance line.
- A dark stage island holds the hero number (116 px) and the 12-week chart, with a glass tooltip floating on the bars.
- Act-now list with date blocks and countdown chips next to it; secondary numbers in one KPI strip; ask panel and
  source health in a side column; voice orb bottom-right (phone: beside the floating tab bar).
- WCAG AA on all text including text on glass against worst-case backdrops (`tools/contrast_check.py`: 0 failures).

## Iteration log (what the screenshot loop caught)
1. Dashboard v1: units ("of 31 signals") rendered at hero size and wrapped; act-now titles truncated to one word;
   chart axis labels came out at about 7 px because SVG text scaled with the viewBox; a decorative orb in the side
   card looked like a stray marble; the stage left an empty gap on phones. Fixed: unit size token, two-line clamped
   titles, axis labels moved to HTML (`.g-chart__x`), orb removed from the card, stage min-height only on desktop.
2. Glass looked unblurred in phone screenshots. Cause: headless Chromium at device scale 2 samples the backdrop from
   the wrong place in the lower half of the viewport. Fixed in the tools (`--use-gl=angle --use-angle=swiftshader`);
   real browsers were never affected. Without this the review loop would have "fixed" a non-bug.
3. Landing v1 on phones scrolled sideways (a 120vw decorative glow). Fixed with `overflow-x: clip` on `body.g` by
   default, so no page built on the kit can hit it. A floating callout covered the hero number; moved down.
4. Contrast pass 1: 30 failures, all on glass (nav links on dark glass 4.38:1, the SAMPLE badge 2.95:1, accent text
   on glass 2.9 to 3.9:1, a warn chip on tinted glass 3.06:1, decorative clear glass carrying text). Fixed with
   on-glass tokens (`--g-glass-text-2`, `--g-glass-accent-text`) that glass components switch to automatically,
   opaque chips (`color-mix` with the surface), solid active capsules in tab bar and segmented control, dark glass
   alpha 0.78 to 0.82, thin glass forced to one text colour. Pass 2: 0 failures. The checker itself had a bug
   (it ignored `color(srgb ...)` backgrounds from `color-mix`), found and fixed on the way.
5. A glass label inside the dark stage was white on white: the dark island overrode regular glass but not thick.
   Fixed by giving `.g-stage--dark` the complete dark token set.
6. Refraction: `backdrop-filter: url(#lens) blur() saturate()` bent the backdrop but Chromium dropped the blur, so
   text behind the glass became readable. Fixed by doing blur, displacement and saturation inside one SVG filter.
7. Dashboard v3 still felt paler than BlueWatch: its dark "due next" card anchors the eye. Switched the hero stage
   to a dark island in the light theme (`.g-stage--dark`) and added the provenance line. This is the version shown.
