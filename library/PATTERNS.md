# Patterns that recur

Fifteen moves that show up again and again across the library (see README.md for each site) and in the two
rival apps that beat us. Each one: what it is, where it is seen, how to apply it in a data or AI hackathon app,
the glass.css class that does it, and the trap. Order = order of impact on a judge in the first 5 seconds.

## 1. The first-screen story (3-second rule)
One hero number or visual, one sentence that says what it means, one action. Nothing else competes above the fold.
- Seen: BlueWatch ("Due next: 10 days" card + sonar + act-now list), Atlas dashboard (KPI row + donut), Apple (one product, one line).
- Apply: decide the sentence before building. "6 signals need action this week" beats "Dashboard". The visual proves it, the button acts on it.
- Kit: dashboard template header (`.g-h1` with `.g-hl`) + `.g-stage` + one `.g-btn--primary`.
- Trap: opening on a filter form, a search box alone, or a paragraph (our JunctionX entry did all three).

## 2. The number is the headline
Put the key number inside the headline and colour only the number.
- Seen: Atlas home ("28/28 ventures assessed"), Stripe (live GDP counter), Mercury, Tremor ($328,505.10 card).
- Apply: `<h1><span class="g-hl">6 signals</span> need action this week</h1>`. Dim denominators: `5<span class="g-dim">/6</span>`.
- Trap: animated counters (slop) and numbers without a source chip nearby.

## 3. One hero KPI, the rest in a strip
One huge number (64-116 px, tracking -0.055em) carries the screen; secondary numbers live in one card divided by hairlines.
- Seen: Atlas home KPI strip, shadcn dashboard cards (label, delta pill, number, one-line verdict), Tremor.
- Apply: `.g-kpi--hero` inside the stage; `.g-kpi-strip` with 3-4 cells below. Each cell: label, value, delta or rule.
- Kit: `.g-kpi`, `.g-kpi__value small` for units, `.g-delta--up/down` (arrow + colour, never colour alone).
- Trap: four identical KPI cards in a row with the same icon size and no hierarchy.

## 4. The stage: visual first, glass floats on it
A large solid panel holds the visual (chart, map, sonar); small glass elements (tooltip, legend, segmented control) float on top and show the visual through them. This is Liquid Glass used the Apple way: glass over content, never as the content.
- Seen: Apple Maps / iOS 26 controls over content, Framer hero (product shot with floating panels), BlueWatch sonar card.
- Apply: `.g-stage` (or `.g-stage--dark` for a dark island in a light page) + `.g-float.g-glass--thick` positioned over the data point that matters.
- Trap: glass cards on a plain background (looks like nothing), or glass on glass.

## 5. Floating glass capsule nav
A pill-shaped bar detached from the edges (14 px from the top), blurred, with the active item as a solid capsule.
- Seen: Apple sub-nav pills, BlueWatch pill tabs, Linear and Vercel blurred sticky headers.
- Apply: `.g-nav` with brand, 3-5 links, one action. On phones it collapses to brand + actions; the tab bar takes over.
- Trap: a full-width white header with 9 links and a hamburger on desktop.

## 6. Phone: floating tab bar + separate orb
A capsule tab bar 12-14 px above the bottom edge with 3-5 icon+label tabs, and the assistant as a separate round glass button beside it (the iOS 26 search-button position).
- Seen: BlueWatch phone (floating capsule tab bar), iOS 26 tab bars, Apple Music / Photos.
- Apply: `.g-tabbar.g-tabbar--with-orb` + `.g-orb-btn` (fixed). Content gets `padding-bottom: 112px` (done by `.g-main`).
- Trap: a desktop sidebar squashed into a hamburger; tap targets under 44 px.

## 7. The act-now list
A short list sorted by urgency: date block, two-line title, entity and source in the meta line, countdown chip.
- Seen: BlueWatch (dated actions with days left), Atlas (deadline cards in amber), Apple Reminders.
- Apply: `.g-list` with `.g-date` (`--urgent` for under 7 days) and `.g-chip--warn` "3 days". Five rows maximum, then "View all".
- Trap: a 50-row table as the first thing on screen.

## 8. Bento grid with unequal spans
A 12-column grid where neighbouring cells have different sizes and different content shapes (chart, list, number, text).
- Seen: Apple product pages, Supabase feature grid, Linear and Vercel feature sections, Tremor blocks.
- Apply: `.g-bento` + `.g-span-7` / `.g-span-5`, `.g-rows-2` for a tall cell. Collapses to 6 columns on tablets and 1 on phones.
- Trap: three or four equal cards with icon, title, paragraph (the most common AI-slop layout).

## 9. Icons in tinted squares
Line icons (1.8 px stroke) inside 28-48 px rounded squares tinted 12% of their colour. Gives rhythm and colour without decoration.
- Seen: Atlas KPI cards, Supabase product grid, iOS Settings.
- Apply: `.g-tile` (`--teal`, `--good`, `--warn`, `--bad`, `--neutral`). One icon per row or card label, never an icon alone without a word.
- Trap: emoji, mixed icon sets, filled and outlined icons together.

## 10. Pill tabs with counts and a segmented control
Pill tabs filter a list and show how many items each filter holds; a segmented control switches views of the same data.
- Seen: BlueWatch (All 10 · Act now 6 · Dive deeper 4), Apple sub-nav, shadcn Tabs.
- Apply: `.g-tabs` with `.g-count`; `.g-seg` (or `.g-seg--glass` over a visual) for Week / Month or Map / List.
- Trap: dropdowns for 3 options; tabs without counts in a data app.

## 11. Receipts: a source chip under every number
Each claim carries a small mono chip with where it came from and when. Missing data is shown as missing.
- Seen: BlueWatch sources panel and provenance line, Perplexity citations, our DESIGN.md "evidence first" rule.
- Apply: `.g-source` (mono, linkable) next to numbers and in table rows; `.g-chip--outline.g-chip--plain` "no public record".
- Trap: numbers with no source, or a placeholder that looks like real data.

## 12. Real product in a glass frame (landing hero)
The landing hero shows the actual product UI, framed in a thin glass bezel, with two floating callouts that overlap the frame edge and create depth.
- Seen: Framer, Attio, Dia (arc.net), Cal.com (live booking widget), Linear (app screenshot under the headline).
- Apply: `.g-frame.g-glass.g-glass--thin` around real components; `.g-float.g-glass--thick` callouts; a coloured glow behind so the glass bends something.
- Trap: abstract 3D blobs or stock illustrations instead of the product.

## 13. Tight display type, loose small type, one family + mono
Big type at -0.03 to -0.055em tracking and weight 600; body 15-17 px at 1.5; numbers tabular; mono only for data and sources.
- Seen: Vercel (Geist), Linear (Inter Display), Apple (SF Pro Display at -0.015em on 80 px), Stripe.
- Apply: the kit's type tokens (`--g-t-hero` ... `--g-t-micro`), Geist + Geist Mono. Headlines `text-wrap: balance`.
- Trap: three fonts, centred body paragraphs, default letter-spacing on 64 px type.

## 14. One accent, greys for everything else
A single accent for the primary action, links and the hero number; status colours only where they mean something.
- Seen: Linear, Vercel, Apple (#0071e3 only), Resend. Stripe's gradient is the famous exception, not the rule.
- Apply: `data-accent="blue|teal|green|orange|graphite"` on `<html>`. Status via `.g-chip--good/warn/bad` with words.
- Trap: purple-to-blue gradients, rainbow charts, colour as the only signal.

## 15. Ask bar + voice orb as the AI's presence
For AI apps, the question box is a first-class control: a glass capsule with a mic button and 3 real suggestion chips; the voice orb is the assistant's body, with visible states (listening, thinking, speaking).
- Seen: Dia ("what are my priorities this week"), Attio ("Good morning, Alex"), Atlas "Ask Atlas", Siri and ChatGPT voice orbs.
- Apply: `.g-ask` + `.g-ask__mic` + `.g-suggest`; `.g-orb-btn` with `data-state`; `.g-pilot-panel` for transcript + cited answer. Suggestions must be questions the demo answers well.
- Trap: a chat window as the whole product; suggestions the backend cannot answer live.

## Supporting rules seen everywhere
- Dark sections as punctuation in a light page (Stripe, Linear CTA bands): `.g-stage--dark` for one band, not the whole page.
- Calm motion: one live thing (a list that re-sorts, a bar that grows, the orb breathing). No parallax, no counters.
- Generous outer space, dense inner data: 96-120 px above the hero, 16 px gaps inside cards.
- Empty and loading states designed: one sentence + one action; skeletons in the final layout (`.g-empty`, `.g-skel`).
