# Hongyu Liu — Academic Homepage Design

Status: Apple-inspired revision approved for publication by the user, 2026-10-16.

## Direction
Apple-inspired academic portfolio: strong typographic hierarchy, white and pearl-gray surfaces, generous space, and research imagery as the visual focus. Keep the approved academic layout and content. Avoid decorative chrome or marketing slogans.

Reference (third-party design analysis, not an official Apple specification):
- https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/apple/DESIGN.md

Apply its restrained blue interactions, system typography, pill actions and imagery-first presentation. Do not copy Apple branding or download proprietary fonts.

## Tokens
| Role | Light | Dark |
| --- | --- | --- |
| Canvas | `#ffffff` | `#000000` |
| Section surface | `#f5f5f7` | `#161617` |
| Card surface | `#ffffff` | `#1d1d1f` |
| Primary text | `#1d1d1f` | `#f5f5f7` |
| Secondary text | `#6e6e73` | `#a1a1a6` |
| Fine borders | `#e0e0e0` | `#424245` |
| Interaction blue | `#0066cc` | `#2997ff` |

Use native system sans-serif fonts. Name: responsive 44–64px; section headings 29–40px; biography 17px with 1.65 line height. Avoid overly tracked labels. Use blue only for interactions, with a solid primary Publications pill and quiet secondary profile links. Keyboard focus uses `#0071e3`.

Spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 px. Major research sections have 64px separation on desktop. White introduction transitions into a pearl-gray video stage. Portrait and cards have 18px corners, stage 24px, actions pill corners. Keep affiliation logos unboxed. Reserve shadows for the selected video and subtle card hover feedback. Existing amber biography underlines remain a small personal detail; publication author styling stays unchanged.

## Page structure and invariants
1. Name and HKUST affiliation; portrait; compact Publications / Google Scholar / GitHub links; three Current Focus icons.
2. Three short biography paragraphs, preserving identity/advisor, research interests and fishing. Current emphasis: post-training world models and embodied intelligence.
3. Eight affiliations, with transparent NVIDIA logo and no individual logo boxes.
4. News: readable dates and complete announcements. Do not fabricate acceptance details.
5. Recent Highlights: plain heading, 3D carousel, original complete videos represented by lightweight previews. Initial center OPSD-V, left DyaPlex, right HelixWorld. Keep WorldSonus and LongCat accessible. Project Page / Code / Paper links appear only when available.
6. Research topics: World Models left, Human-Centered Spatial Intelligence middle, Image Generation & Editing right. Three desktop columns, stacked on smaller screens.
7. Compact contact links.

Publications retain complete author lists, a teal highlight for Hongyu Liu, and deduplicated contribution superscripts. BibTeX shown to visitors must exclude presentation fields.

## Interaction and performance requirements
- Initial HTML contains carousel positions. Never show a grid that later rearranges when JavaScript loads.
- CSS grid reserves the stage height; controls reserve their space before initialization.
- Preserve `data-position` selectors in PurgeCSS. Test the purged stylesheet, not only development CSS.
- Keep keyboard controls, arrows, dots, touch swipe, pause and audio toggle. Inactive hidden cards are inert.
- Videos use data-src, attach only near the viewport and only for the selected card, and detach inactive videos. Preserve full duration and audio; retain originals on project/publication pages.
- MP4 previews use faststart. Respect reduced motion. Avoid added decorative animation.
- Portrait is a committed 800px WebP, eagerly loaded with high priority. No dependency on build-generated thumbnails for the portrait. Image fallback must not depend on jQuery or affect unrelated pictures.
- Clear focus indication; do not communicate research categories by color alone.

## Implementation
- `_sass/_home_refresh.scss`: approved functional carousel/responsive foundation.
- `_sass/_home_editorial.scss`: scoped visual refinement, imported last.
- `_layouts/about.liquid`: homepage identity and section hooks.
- `_includes/recent_highlights.liquid` and `assets/js/highlights-carousel.js`: initial and interactive carousel state.
- Keep this document out of the public build via Jekyll excludes.

## Verification before publishing
Build Jekyll; run the deployment CSS cleanup; inspect desktop and 390px/320px mobile, plus dark mode. Check all initial carousel positions before JavaScript is released, no height jump, switching, video pause/sound and reduced-motion behavior. Check the portrait in a fresh session. Check no media 404s and no horizontal overflow. Never equate a successful local build with a verified live deployment.

The user approved publishing this revision on 2026-10-16. Future design revisions should be previewed locally before publication.

## Collection pages
Projects, Publications and Memories share the homepage’s Apple-inspired typography, neutral surfaces and blue actions through `_sass/_apple_collections.scss`. Headers are open and unboxed. Projects use image-led gray cards; Publications use quiet separated rows with blue category pills and a neutral search panel; Memories prioritize photographs with unboxed album statistics and legible image captions. Preserve all paper authors, contribution marks, search/category state, project destinations and external album links. Scope these styles to the collection pages so project microsites remain unchanged.

## October 17 refinement
Keep the cover compact without a separate research-focus headline; the biography retains the current research focus. Use two desktop columns for larger project imagery. Remove repeated research tags from the publication header and shorten its search panel so papers appear earlier. Keep search, all five categories, full author lists and contribution notes intact; expose category selection with aria-pressed. Memories uses a clear page title and an image-led gallery. Main navigation uses a restrained translucent neutral surface. This refinement and the October 27 content update were approved for publication on October 27, 2026.

## October 27 content and navigation update
SMD metadata is verified against its official repository and arXiv:2610.18472. The highlight and 4d publication use the full official teaser from https://zjwfufu.github.io/SMD-Page/assets/teaser/SMD_r69_1080p_x264.mp4, re-encoded for delivery without trimming or dropping audio. Poster source: assets/teaser/SMD_r69_first_frame.jpg on the same official project.
Publication category is resolved in the document head before paint; category buttons initialize before the bibliography and synchronize with browser history. Publication videos use data-src and only attach in the visible viewport, releasing sources outside it or on hidden pages. Preserve these behaviors when changing publication markup.
