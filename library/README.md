# Reference library

Above-the-fold screenshots of 18 reference sites, plus the two rival apps that beat us at JunctionX Turku 2026 ("the bar to beat") and our own losing entry (the anti-reference). Captured 18 Oct 2026. Desktop is 1440x900 at 1x, phone is 390x844 at 2x (780x1688 files), both above the fold only: no scroll, no hover, and CSS animations are frozen, so motion is not visible in any still.
Re-capture from the repo root with `python3 tools/capture_library.py [--only key1,key2]`; it rewrites `shots/<key>_desk.png`, `shots/<key>_phone.png` and `shots/facts.json` (computed font family, size, weight, tracking, line height, colours, button style, count of elements using backdrop-filter, fonts loaded).
Numbers: values from facts.json are given plain; values marked `~` are read off the screenshot (the four rival and anti-reference shots have no facts.json entry, so all their numbers are `~`). `px` means CSS px. Tracking is given in px as measured plus em in brackets.
Caveats:
- The capturing server is in Europe: apple.com shows a German region banner ("Deutschland / Weiter") above the nav, stripe shows a cookie panel and a "Vereinigte Staaten" region toast, attio shows a cookie card over its product shot.
- arc.net now shows the Dia product page, not Arc. WebGL and video heroes (lusion, vercel, resend, mercury, raycast) may render differently headless.
- raycast: the desktop capture failed (screenshot timed out after 60 s), so the desktop capture does not exist, and facts.json has no raycast entry. Its section is written from the phone shot only.
- stripe: facts.json still holds the earlier German capture (44px, hero colour rgb(129,184,26) which is not what is on screen). The re-captured English shot is what the section describes.
- The facts picker takes the largest visible text node and the first coloured button, so it sometimes picks the wrong element (nav buttons, hidden links, off-screen slides). Each wrong pick is flagged in its section.

## Apple iOS - https://www.apple.com/os/ios/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** SF Pro Display 48px, weight 600, tracking -0.144px (-0.003em), leading 52px, off-white rgb(245,245,247); two centred sentences ("Introducing Siri AI. / Truly helpful. Truly yours."), three lines on the phone. Eyebrow "iOS 27" ~22px, grey subline ~17px. The facts button ("Weiter") is the region banner, not a page button.
- **Spacing:** one centred column with no body copy; pill row ~16px under the nav, headline ~50px under the pills, product row ~50px under the subline. The devices bleed off the left, right and bottom edges instead of sitting in a frame.
- **Colour:** pure black page, off-white text, one grey; no accent colour above the fold, all colour comes from the product images.
- **Depth:** flat. The sub-nav is a row of seven ~35px pills with 1px borders, the active one ("iOS") filled white with black text, "Apple Intelligence" has a glowing gradient border. 4 backdrop-filter elements per facts.json (not identified; likely nav, sub-nav and banner).
- **Motion:** not visible in a still.
- **Hero move:** Mac, iPad, iPhone, Watch and Vision shown as one cropped composition under a two-sentence headline, so the whole product range reads in one image.

Steal for a hackathon app: a pill tab row (35px high, 1px border, active pill filled white on black) as the top-level view switcher.

## Apple iPhone - https://www.apple.com/iphone/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** SF Pro Display 80px, weight 600, tracking -1.2px (-0.015em), leading 84px, rgb(29,29,31); the headline is one word, "iPhone", left aligned. Card title "iPhone Duo" ~56px, subtitle ~28px regular. Body is SF Pro Text 14px/20px, tracking -0.224px.
- **Spacing:** everything hangs on one left edge at x=90 (headline, first icon, card). Icon row is ten items at ~127px pitch (~70px icons, 14px bold labels), the hero card starts ~80px below it. Generous: ~70px of white above the headline.
- **Colour:** white page, #f5f5f7 grey card, near-black text, one blue (#0071e3 "Learn more" pill and text link); the only other colour is the orange "New" tag under two items.
- **Depth:** flat, no shadows; the card is a grey panel with ~28px radius that bleeds off the right edge into the next (black) card. 3 backdrop-filter elements per facts.json (likely nav and banner layers).
- **Motion:** not visible in a still.
- **Hero move:** a one-word headline above a strip of product icons with names and "New" tags; the first screen is a picker, not a pitch.

Steal for a hackathon app: an icon-plus-label picker strip with an accent-coloured "New" tag as the app's entry menu.

## Linear - https://linear.app/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Inter Variable 64px, weight 510, tracking -1.408px (-0.022em), leading 64px (1.0), rgb(247,248,248); two lines, ~4 lines (~42px) on the phone. Body 15px/24px, grey rgb(138,143,152). Berkeley Mono is loaded and used for inline code. facts.json hero text is only the first line.
- **Spacing:** 80px left margin, 72px nav with a 1px hairline, ~200px of empty black above the headline, subline ~40px under it; the app panel starts at y=527 and is cut by the fold. Product UI text inside the panel is ~12-13px.
- **Colour:** near-black rgb(8,9,10), panels #151618, three greys, white-ish text; no accent colour is visible. The facts button (indigo rgb(94,106,210), "Skip to content") is a hidden accessibility link; the only filled button on screen is a light "Sign up" pill.
- **Depth:** 3 backdrop-filter elements per facts.json. Panels use a slightly lighter fill, a 1px low-contrast border and ~12px radius with no visible shadow; a floating agent-chat window overlaps the issue view, which is the only layering cue.
- **Motion:** not visible in a still.
- **Hero move:** the real product UI (sidebar, issue, activity log, an agent chat) at true density, cropped by the fold, under a two-line headline.

Steal for a hackathon app: render your own app screen with real data as a dark panel (#151618, 1px border, 12px radius) cropped at the fold.

## Vercel - https://vercel.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Geist Sans 64px, weight 400 (regular, not bold), tracking -3.84px (-0.06em), leading 64px, rgb(23,23,23); left aligned, two lines. Geist Mono is used for the small-caps "READ THE RECAP" pill and the phone subline "Automated by agents". On the phone the headline drops to ~24px and sits under the artwork.
- **Spacing:** 24px side margins, 64px nav, headline vertically centred left, a three-link list (Backends, Agents, Enterprise) at right, a 7-logo row pinned to the bottom. Lots of empty space around the centred object.
- **Colour:** #fafafa page, rgb(23,23,23) text, no accent. Primary button is a black pill ("Deploy now", ~124x40), secondary is a white pill with a 1px border. The facts button ("Get a Demo", 6px radius) is a nav item.
- **Depth:** flat, 0 backdrop-filter elements, no shadows; 1px borders only. All depth is in the rendered container hanging on a cable.
- **Motion:** the crane cable entering at the top edge implies an animated drop or sway; not visible in a still.
- **Hero move:** one rendered object (a shipping container reading "Ship SF") hanging from the top edge carries the event and the verb without any text.

Steal for a hackathon app: one centred hero object on #fafafa, a mono small-caps pill under it, and a black pill plus outline pill CTA pair.

## Stripe - https://stripe.com/en-us

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** sohne-var, weight 300; headline ~48px (line pitch ~55px; the stale German entry says 44px, tracking -0.88px = -0.02em, leading 50.6px). One four-line paragraph: first sentence in navy (#020826), the rest in slate blue, so hierarchy comes from tone, not size. Phone shows only the first sentence at ~34px. Body 32px/300 in facts.json is also from the German capture.
- **Spacing:** content framed by 1px vertical hairlines at x=88 and x=1352; text starts 120px inside the frame; ~64px from headline to the two buttons; a logo strip between 1px rules (72px row). Nav 76px.
- **Colour:** white, navy, slate, one violet (#533afd) on the primary button, the "Contact sales" button and the "Sign up with Google" text; the orange, pink and violet ribbon is the only multi-colour element.
- **Depth:** the ribbon fills the top right ~40% of the screen and the headline text turns violet where it crosses it. Buttons are flat, 4px radius, 40-48px high (~44px and full width on the phone). 2 backdrop-filter elements per facts.json (stale). The cookie and region cards floating bottom right have soft shadows.
- **Motion:** the ribbon and the counter are likely animated; not visible in a still.
- **Hero move:** a one-line live number above the headline ("Global GDP running on Stripe: 1.73448808%", nine digits) plus the ribbon: scale shown as a figure, then a promise.

Steal for a hackathon app: a one-line KPI eyebrow (label plus a long tabular-figure number, updated live) above the headline.

## Raycast - https://www.raycast.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`. Written from the phone shot only; no facts.json entry.

- **Type:** a grotesk that looks like Inter, ~36px (line pitch ~39px), weight ~600, white with a soft text shadow, centred on two lines ("Your shortcut to / everything."). Subline ~15px on three centred lines with slightly open tracking.
- **Spacing:** nav is a floating capsule (~358x58px, ~20px radius) inset 16px from the screen edges; headline sits in the middle of the beams; one outlined pill CTA ("The Raycast Keyboard ->", ~212x32px) below, then ~200px of empty black.
- **Colour:** near-black #07080a page, one hue (red, ~#c10f24 in the beams), white text. Nothing else.
- **Depth:** diagonal red beams with grainy, dithered edges over black are the whole background; the nav capsule is dark and translucent with a 1px border; the CTA pill has a thin red outline and a lit patch on its lower edge. Backdrop-filter count unknown.
- **Motion:** not visible in a still.
- **Hero move:** one saturated colour as light beams across the entire first screen, with centred white text on top.

Steal for a hackathon app: rotated, blurred red gradient bands plus an SVG noise overlay behind centred text, and a floating dark capsule nav inset 16px.

## Arc - https://arc.net/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`. The page is now the Dia page, not Arc.

- **Type:** headline ~40px bold serif, centred, black ("Meet Dia, the next evolution of Arc"); subline ABC Oracle 20px/24px, rgba(0,0,0,.65). The facts hero (Marlin Soft SQ 45.51px, weight 700, tracking -1.82px, cream rgb(255,252,236)) is the pull quote at the bottom edge ("Arc is the Chrome replacement..."), which is partly visible on the blue band.
- **Spacing:** centred column: 96px blue nav band with a scalloped lower edge, headline ~80px under it, ~216x76px CTA ~40px under the subline, 1100px-wide product window ~55px under the CTA, cut by the next scalloped band at y=705.
- **Colour:** ultramarine #333bfb with a grain texture for the bands, cream #f5f4ec centre with pastel pink and peach glows in the top corners, black CTA; about four colours.
- **Depth:** 1 backdrop-filter element per facts.json. The CTA is a dark rounded rectangle (~18px radius) with a drop shadow; the product window has a 1px border and fades into the band at the bottom. The scalloped (wavy) section edge is the signature shape.
- **Motion:** not visible in a still.
- **Hero move:** the CTA button contains the product icon (~58px rounded square) next to "Try Dia ->", so the button is also the logo.

Steal for a hackathon app: a large CTA with the app icon inside it, over a cream page with a grain-textured saturated band behind the nav.

## Framer - https://www.framer.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** GT Walsheim Medium 54px, weight 500, tracking -2.16px (-0.04em), leading 54px (1.0), white; left aligned, two lines about 670px wide, three lines (~36px) on the phone. The facts button ("Sign up", 12px, link colour rgb(0,0,238)) is the nav button and the colour is a default-link artefact; on screen it is black on white.
- **Spacing:** 120px left margin on a 1200px container, nav 64px, headline ~100px under it, buttons ~24px under the headline (white ~161x34px with ~8px radius, dark grey "Download app"), "New: Skills ->" right aligned on the same line, product frame from y=372 cut by the fold.
- **Colour:** pure black, white text, grey secondary; saturated electric blue appears only inside the product frame (neon edge lines, blue image). One white filled button.
- **Depth:** 5 backdrop-filter elements per facts.json. Product frame has a 1px border, ~24px radius; inside it a translucent glass sphere sits over a blurred blue image, next to an agent side panel.
- **Motion:** the phone shot shows a "0:36" timer on the frame, so it is a video or a replay; otherwise not visible in a still.
- **Hero move:** the product mid-task: a prompt ("Create a sleek black homepage...") and a thinking log beside the generated result, input and output in one frame.

Steal for a hackathon app: a left-aligned two-line headline at -0.04em, a white button plus dark button pair, then a framed "prompt in, result out" panel.

## Family - https://family.co/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** custom "Family" face, 68px, weight 500, tracking -1.36px (-0.02em), leading 74.8px (1.1), warm near-black (display-p3 ~#343433); centred "Your favorite crypto wallet." (facts.json catches only the span "Your"). Subline Inter 17px/26px, weight 500, rgb(71,70,69). Next heading ~44px. The facts button ("Developers") is a nav item.
- **Spacing:** 1024px nav container (x=208..1232); a ~400px centred text column between two ~450px illustration clusters that bleed off both edges; CTAs ~28px under the subline (two 48px pills); three cards start at y=830 with ~32px gutters. On the phone four small illustrations sit above the headline and both buttons stack at ~210px wide.
- **Colour:** white page, warm near-black text; interface chrome is only a black pill and a beige pill. The colour (cyan #00b2ff, red-orange, green, yellow, beige) is all in the illustrations.
- **Depth:** flat, 0 backdrop-filter elements, no shadows; depth only from overlapping flat vector characters.
- **Motion:** the characters are probably animated; not visible in a still.
- **Hero move:** two clusters of mascot-style illustrations frame the headline, so the brand's tone (friendly, low-stakes) lands before the copy is read.

Steal for a hackathon app: a flat-vector cluster of 8-10 simple SVG shapes bleeding off each side of a 400px centred text column; black primary pill with an icon, beige secondary pill.

## Rauno Freiberg - https://rauno.me/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** custom face "X" (a Helvetica-like grotesk in the still), regular weight, ~64px with a ~90px line pitch, tight tracking by eye, near-black. facts.json hero ("Craft", 720px) and body (75px) are off-screen slides, not the visible sentence; the black bar at the right edge is the first letter of that slide.
- **Spacing:** a horizontal slide deck: first slide 1058x635px (x=191..1249) on the grey page, next slide peeking at x=1285 with a 12px grey label ("Devouring Details"); alternate text lines are indented ~57px, which gives a stepped rhythm. On the phone the slide is 360x216px with ~60% of the screen empty grey.
- **Colour:** #ededed page, white slide, black text, one acid yellow (#ffff02) circle; two colours plus neutrals.
- **Depth:** flat, 0 backdrop-filter elements, no shadows. The yellow circle is the full height of the slide and the black text runs over it without blending.
- **Motion:** a pager of a small rectangle plus 17 tick marks at the top and a crosshair cursor in the circle suggest scroll-driven and cursor-driven interaction; not visible in a still.
- **Hero move:** a staggered statement of who he is over one flat yellow circle; the shape does all the visual work.

Steal for a hackathon app: one flat saturated circle (`border-radius:50%`) behind an oversized left-aligned statement with alternate lines indented.

## Resend - https://resend.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Domaine (serif display) 96px, weight 400, tracking -0.96px (-0.01em), leading 96px (1.0), rgb(240,240,240) fading to grey down the second line; ~60px on the phone, centred. Body Inter 18px/27px, rgb(161,164,165). Nav 14px.
- **Spacing:** 168px left margin, headline ~40px under a 32px badge, body ~25px under the headline, buttons ~30px under the body (the dark "Get started" ~133x46px, "Documentation" text only); text takes the left 45%, the 3D object the right half; ~200px of black at the bottom.
- **Colour:** black and greys only; the one colour is a 1px teal-to-purple-to-orange gradient border on the "Join us at Resend Forward" badge. Buttons are dark grey (#141414) with a lighter 1px border and ~12px radius.
- **Depth:** 4 backdrop-filter elements per facts.json. The hero is a dark-on-dark 3D cube lit by one spot, plus a diagonal light streak crossing the lower left; buttons have a lit top edge.
- **Motion:** not visible in a still.
- **Hero move:** a high-contrast serif headline fading to grey over a monochrome 3D object; the type is the only thing that changes weight on screen.

Steal for a hackathon app: gradient-filled headline text (white to grey via `background-clip:text`) in a serif display face, with a 1px gradient-border pill badge above it.

## Cal.com - https://cal.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Cal Sans 64px, weight 600, tracking normal, leading 70.4px (1.1), rgb(36,36,36); three lines in a ~500px column. Body Cal Sans UI Variable Light 16px/24px, weight 300, grey rgb(137,137,137). Mock-up UI text ~13px.
- **Spacing:** the hero is one white card (~1174x698px, ~16px radius) on a #f4f4f4 page, ~100px inner padding; the page is framed by two vertical hairlines (x=121, x=1319) with "+" marks at the lower corners; CTAs are full column width and ~36px high, stacked; a logo row with a 14px caption sits under the card.
- **Colour:** grey #f4f4f4, white card, near-black buttons (#242424); colour only in the review badges (green, orange, red) and the Google icon. The booking mock-up is monochrome with the selected date as a dark chip.
- **Depth:** flat with 1px borders and a soft shadow on the card; 0 backdrop-filter elements; the secondary button has a faint vertical gradient.
- **Motion:** not visible in a still.
- **Hero move:** a working-looking booking widget (month calendar, 15m/30m/45m/1h segmented control, timezone) beside the headline, cropped at the card edge.

Steal for a hackathon app: put one real component (calendar, KPI card) in a bordered white card beside the headline, on a #f4f4f4 page.

## Supabase - https://supabase.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Manrope 46px, weight 500, tracking normal, leading 46px (1.0), near-black; second line "Scale to millions" in green. Body Inter 16px/24px, weight 450, mid-grey, set in a right column. Card titles ~17px Manrope; card body 14px grey with the key phrase in black.
- **Spacing:** 1088px container (176px side margins), 64px nav with hairline, ~160px empty above the headline; headline left and body right share a baseline; buttons ~32px under; a bento grid of cards starts at y=452 with ~12px gaps (one ~538px card, two ~263px cards, then a row of four) and ~24px card padding. On the phone the cards stack full width.
- **Colour:** #fcfcfc page, near-black text, one green (oklch(0.525 0.12 157.5), a dark emerald) on the primary button, the second headline line and the `supabase functions serve` command text; the logo bolt is a lighter mint.
- **Depth:** flat; cards have a 1px border, ~14px radius and a barely visible shadow; 1 backdrop-filter element (likely the nav). Card art is light-grey line drawing (elephant, wire globe).
- **Motion:** not visible in a still.
- **Hero move:** a two-line headline whose second line is the accent colour, then a card grid where each card is an outline icon, a title and one grey sentence with the key phrase in black.

Steal for a hackathon app: grey body sentences with the one key phrase in black inside 1px-border cards, each led by a 16px outline icon.

## Mercury - https://mercury.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** arcadiaDisplay 49.3px, weight 480, tracking normal, leading 54.3px, rgb(237,237,243), one centred line ("Radically different banking"), ~32px on the phone. The subline is ~20px (not in facts.json: its "body" is the 12px legal consent line, tracking 0.24px, which is a wrong pick). Disclaimer text at the bottom is 12px.
- **Spacing:** nav 72px; headline ~100px under it; the form row (email field, "Open account", "Launch demo" all ~40px high) sits ~55px under the subline; the photograph is the full-bleed background and the desk sits in its lower half; a dark disclaimer panel pinned ~32px above the bottom edge. On the phone the field is full width and the two buttons sit side by side.
- **Colour:** desaturated lavender, peach and green-teal photograph; text off-white; one indigo (rgb(82,102,235)) on both "Open account" buttons.
- **Depth:** 4 backdrop-filter elements per facts.json, which fits the frosted email pill, the translucent "Launch demo" pill, the nav and the disclaimer panel over the photo. This is the nearest reference to the kit's glass: small controls only, a 1px lighter edge, text kept at full white.
- **Motion:** the background may be a video; not visible in a still.
- **Hero move:** a photograph of a lone desk and chair on a misty hilltop under a three-word promise, with the sign-up form already in the first screen.

Steal for a hackathon app: a frosted pill input (backdrop blur, ~12% white fill, 1px light border) with an indigo button inside it, over a full-bleed photo.

## Attio - https://attio.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Inter Display 64px, weight 600, tracking -1.28px (-0.02em), leading 60.8px (0.95), near-black; centred, one line at 1440, two on the phone. Body Inter 18px/23.4px, weight 500, tracking -0.18px, grey-blue. A serif (Tiempos Text) is loaded but not visible. The facts button ("Sign in", 10px radius) is a nav item.
- **Spacing:** 48px black announcement bar, 68px nav, ~96px to the badge, then ~36-40px steps (badge, headline, body, buttons); the 1080px product window starts at y=580 and is cut by the fold. Two ~36px buttons ("Talk to sales" outline, "Start for free" dark).
- **Colour:** white with a faint lavender wash behind the product (#fbfcfe to pale blue), near-black buttons, grey-blue text; the only accent is the small blue send button in the AI input.
- **Depth:** 9 backdrop-filter elements per facts.json (not identified; likely cookie card, nav and popovers). The product window is a frame in a frame: grey outer chrome with traffic lights, white inner panel, ~16px radius, 1px borders. The cookie card (white, ~16px radius, soft shadow) covers the lower left of the product shot.
- **Motion:** the typed prompt "How do I win my deal" with a visible caret implies a typing loop; not visible in a still.
- **Hero move:** an AI prompt box with a caret ("Good morning, Alex / How do I win my deal") and two suggestion chips, shown inside the app window.

Steal for a hackathon app: a gradient-hairline pill badge above a centred headline, then a prompt input with a blinking caret and two suggestion chips.

## Tremor - https://www.tremor.so/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Geist Sans 60px, weight 700, tracking -2.1px (-0.035em), leading 60px (1.0), navy-black oklch(0.21 0.034 264.7); body 18px/32px, weight 400, slate. A 12px small-caps eyebrow ("BUILT FOR REACT TAILWIND CSS") has wide tracking. The facts button is the black announcement bar ("Tremor is joining Vercel", radius 0, 48px), not the page CTA.
- **Spacing:** centred stack: eyebrow (y=204), headline (y=250-370), body (400-440), CTA (498-542), then two chart cards from y=625; announcement bar 48px plus nav 64px with hairline. The cards are 690px wide.
- **Colour:** white, navy-black, slate and one blue (~#1f6eff primary button); the chart series add cyan and magenta, and stacked bars add purple.
- **Depth:** cards are a ring in a ring: a pale outer 1px frame around an inner 1px card with ~12px radius and a faint shadow. 1 backdrop-filter element per facts.json. The announcement bar carries a dithered triangle texture.
- **Motion:** not visible in a still.
- **Hero move:** the real chart components under the headline: a KPI card ("Portfolio Value $328,505.10") over a three-series line chart with a legend, and a stacked bar chart with "Europe / North America" tabs.

Steal for a hackathon app: the KPI card anatomy: 14px grey label, ~32px semibold tight number, then the chart with a one-row legend, inside a nested 1px card.

## shadcn/ui dashboard - https://ui.shadcn.com/examples/dashboard

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** Geist 48px, weight 600, tracking -2.4px (-0.05em), leading 52.8px, black; one centred line on desktop. Body Geist 18px/28px, black. KPI numbers ~28px semibold, labels 14px grey. The facts button ("Search documentation...") is the search field, not a CTA.
- **Spacing:** nav 64px; badge at y=154, headline y=209, body two lines, buttons at y=349 ("Get Started" black pill ~105x34, "View Components" #f5f5f5 pill); the demo starts with a tab row at y=478 and its frame at y=512. Inside: 256px sidebar with 36px item pitch, four KPI cards (~246x200px, ~16px gutters, ~24px padding), then a full-width chart card. Dense but calm.
- **Colour:** white, black, three greys; no accent in the chrome. Status uses a blue dot after "RTL" and green dots in the table.
- **Depth:** flat, 0 backdrop-filter elements; 1px borders, 12-14px card radius, almost no shadow.
- **Motion:** not visible in a still.
- **Hero move:** the finished dashboard is the demo, and its first row is four KPI cards each with a label, an outlined delta pill (+12.5%), the number, a bold one-line verdict with an arrow ("Trending up this month") and a grey context line. The phone shot is the same desktop dashboard scaled down to illegibility, not a phone layout; do not copy that.

Steal for a hackathon app: the KPI card anatomy: label plus delta pill on the top row, 28px number, bold one-line verdict with an arrow, grey context line.

## Lusion - https://lusion.co/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** the only visible text is the "LUSION" wordmark at top left, ~28px uppercase, Aeonik by the fonts list. facts.json hero ("Subscribe to", 38px) is a hidden or off-screen newsletter element and the button ("LET'S TALK", pill, rgb(43,46,58)) is not visible, so ignore both.
- **Spacing:** a ~1295x650px panel with ~16px radius inset ~72px from the sides, starting at y=199 under the wordmark; nothing else on the screen. On the phone it is 360x650px with 16px margins.
- **Colour:** lavender-white (#f0f1fa) page (facts.json body is white, so the tint is a layer), dark panel (#14161a), three object colours: cobalt blue, glossy black, matte white.
- **Depth:** real 3D (specular highlights, soft shading), 0 backdrop-filter elements; depth comes from WebGL, not CSS.
- **Motion:** a WebGL scene, probably interactive; not visible in a still. The missing nav and headline may be an intro state in headless Chrome, unknown.
- **Hero move:** no copy at all: a cluster of 3D connector pieces in a rounded panel is the entire message. Least transferable of the set for a data app.

Steal for a hackathon app: an inset dark panel with a ~16px radius on a tinted page holding one generated image or short loop, with only the wordmark above it.

## The bar to beat

Two rival apps that beat us at JunctionX Turku 2026. No facts.json entries: every number is `~`, read off the stills.

### A'Pelago Atlas home - https://apelago-atlas.vercel.app/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** a tight grotesk, ~64px bold, ~80px line pitch, navy-black; "Find the next best [word pill] for every ocean startup." The word sits in a navy rounded pill that is empty in the desktop still (mid-rotation) and reads "grant" on the phone. Subline ~17px/28px slate with the first words ("Deep Panel") in dark; KPI numbers ~30px semibold, labels ~13px.
- **Spacing:** centred; 60px nav with hairline, a badge ~76px under it, then ~30px steps down to two buttons, then a 840x113px KPI strip ~46px below them; a hairline at y=725 starts the next section. A faint dot grid sits behind the hero.
- **Colour:** white, one deep navy (#002444, on the word pill and primary buttons), slate greys, a single amber dot on the badge.
- **Depth:** flat; 1px borders, ~20px radius on the strip, a faint shadow on the badge and strip. No glass.
- **Motion:** the empty word pill implies a rotating word; not visible in a still.
- **Hero move:** a four-cell KPI strip in one rounded container under the buttons: 28/28 ventures assessed, 116 investors, grants and partners, 52 warm intro paths, 3 deadlines in 60 days. It proves the system has already run, before any scroll. Judges got what it does ("find funding for ocean startups") and a number to remember in three seconds.

Steal for a hackathon app: a four-cell KPI strip with 1px dividers in one rounded card directly under the CTAs.

### A'Pelago Atlas dashboard - https://apelago-atlas.vercel.app/dashboard

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** "Welcome back" ~26px bold with a one-line slate status sentence ("Sunday 18 October - here's where the pipeline stands for Redstone Blue VC"); KPI numbers ~30px semibold; card titles ~14px semibold; table text ~13px; captions ~11px. One sans family throughout.
- **Spacing:** 224px white sidebar (workspace switcher, a navy "Assess a startup" button, icon nav with the active item in a grey pill) beside a #f3f5f8 canvas of white cards (~16px radius, 1px border, ~20px padding, ~16px gaps). Row 1: four KPI cards; row 2: donut, bar histogram, progress bars; row 3: table plus deadlines. Dense but calm.
- **Colour:** navy primary plus four semantic hues reused everywhere (teal, blue, green #047c58, gold); the KPI icons sit in tinted squares (slate, mint, cream, amber); red only on the bell badge (9).
- **Depth:** flat cards on a grey canvas; no glass, no heavy shadows.
- **Motion:** not visible in a still.
- **Hero move:** four icon-in-tinted-square KPI cards (28 ventures, 5 investment-ready, 43 average score, 2 calls closing in 30 days), then an act-now list: amber deadline cards with a date block ("4 NOV") and "16 days left - up to EUR 2.5M - 16 fit". The phone drops the sidebar to an icon, shows three round buttons (search, bell, Ask Atlas) and a 2x2 KPI grid; there is no bottom tab bar in the first screen.

Steal for a hackathon app: an icon-in-tinted-square KPI card (38px square, tint at ~10% of the semantic colour, 30px number, label, one-line caption).

### BlueWatch - https://bluewatch.demo.wicflow.com/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** "Now Surfacing" ~30px bold, tight; a mono meta line ~12px under it ("Week 42 - since 12 Oct 07:00 - 10 / 10 - Data as of Sun 18 Oct 09:40 - Sources 5/5 - rules-5e3d77763571"), which doubles as provenance. A sans for body ~13px, mono for numbers (two-decimal scores), dates and source tags.
- **Spacing:** a 56px top bar (logo square, workspace pill, centred pill tab bar with counts, Ctrl K search, EN/FI/SV segmented control, theme toggle, bell, avatar); then one 360px-tall row of three cards (dark "Due next", Sonar, Sources), then pill filters, then a dense table. Dense but calm: 1px row dividers, ~42px rows.
- **Colour:** warm off-white #f4f4f1, white cards, near-black text, one blue (#2446ff) for dots, bars and active states, green evidence bars, amber deadline chips; the one inverted element is a near-black (#0e0f12) "Due next" card with a blue glow in the corner.
- **Depth:** flat cards with 1px borders. On the phone the bottom tab bar is a floating capsule (5 tabs, active tab a black pill with icon and label, inset ~10px from the edges) with card text faintly visible through it, so it is translucent. It is the only translucent element visible in the rival shots.
- **Motion:** not visible in a still.
- **Hero move:** "Due next: 10 days" in a ~56px number on the dark card with three dated actions beneath it (date block, one-line action, "12 days" countdown), beside a radial Sonar plot of ten numbered blips and a sources list with feed names and update status. Why judges liked it: the first screen says what to do now, shows where the data came from, and has one picture to remember.

Steal for a hackathon app: a dark "Due next" card: mono caps label, ~56px number plus unit, one action line, then three rows of date block, action and countdown; add a floating capsule tab bar on the phone.

## Anti-reference

### Ocean Opportunity Radar (ours) - https://jx.hankintaviikko.fi/

Screenshots: not published (third-party site); recreate them locally with `python3 tools/capture_library.py`.

- **Type:** a serif display for the header and the "Ask Aava" headline (~60px, the name in italic cyan), italic serif country labels, and a plain sans body ~15px in blue-grey on navy, with no scale between the headline and 15px text. The largest figure on the screen is "59 of 59", at ~14px.
- **Spacing:** on desktop a 266px left column holds the first screen's biggest block: a "Filter" form with a three-option radio group (counts 59 / 149 / 1), ten checkboxes with counts, and a "What the judges score" group (Verdict filter) starting at y=809, still inside the first screen. The middle column stacks a headline, a two-line paragraph, a prompt box, five chips, a counts sentence, three tabs, seven country labels, a tag and a sort sentence before the first result ("Viva Jets Oy") appears at the bottom edge, as a text card. On the phone the paragraph, prompt, chips, counts sentence, tabs, country row, "Filter" button and sort sentence fill the screen and only one company name appears.
- **Colour:** navy #021b44, mid-blue fills (#023e8a) and one cyan accent used on the name, the send button, a heading and a link; low contrast between body grey-blue and background.
- **Depth:** flat, no cards, no shadows; surfaces are separated by 1px outlines in at least three shapes (pill chips, square tags, square buttons, radio, checkbox), so nothing says which control matters.
- **Motion:** not visible in a still.
- **Hero move:** none. The first screen asks the visitor to do the work (type a question, narrow a filter) and shows no number, no chart and no recommendation. "Aava" is a name that says nothing about what the product found, and a serif headline that reads as an instruction does not tell the story. The phone does have a bottom tab bar (Radar, Search, Lists, Match, Data), but it is a flat full-width strip, not a floating capsule.

Steal for a hackathon app: the inverse of this page: lead with a number and a "do this now" list, and move filters behind one button.

## What recurs

1. One idea per first screen: a headline of one or two lines, one subline, one primary action; everything else is product or image.
2. Display type at 48-96px with negative tracking (-0.02em to -0.06em), line height 0.95-1.1, weight 400-600 (Vercel 400, Linear 510, Stripe 300).
3. One accent colour on a near-neutral page (violet, green, blue, navy, red, indigo); the rest is greys and the product's own colours.
4. The product is the hero image: real UI, real numbers or live components, cropped at the fold (Linear, Framer, Attio, Cal, Tremor, shadcn, both rivals).
5. Pill or capsule controls: pill primary plus outline or tinted secondary, pill sub-nav tabs, a small pill badge above the headline.
6. Hairlines and 1px borders carry structure; surfaces are flat with 12-20px radii and little or no shadow.
7. Glass appears only on small floating controls over imagery (Mercury, Apple sub-nav, Raycast nav, BlueWatch tab bar); counts range 0-9 per facts.json and most sites use 0-4.
8. KPI cards: label, 28-32px tight number, delta pill or caption, one-line verdict (shadcn, Tremor, Atlas).
9. Marketing pages are generous with whitespace; density lives inside product panels at 12-14px, kept calm by hairlines and tinted status chips.
10. Phone: one column, nav reduced to logo plus menu, stacked full-width 40-48px pill buttons; the rivals add a floating capsule tab bar or icon-only header buttons.
