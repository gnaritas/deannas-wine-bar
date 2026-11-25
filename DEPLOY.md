# DEPLOY — Deanna's Wine Bar & Bert's Pig Shop (deannas-wine-bar)

Built 2026-11-25 · t_5c0aaeee · 10-page T2 pre-opening vitrine, template v2 gates.

- Preview/origin: https://deannas-wine-bar-demo.up.railway.app (noindex demo host forever; indexing starts at delivery on owner domain)
- GH: github.com/gnaritas/deannas-wine-bar (public, no secrets)
- Railway: co-hosted service `deannas-wine-bar-demo` (14ef9b60-e47f-4f91-a0b7-2968378d7192) inside dead-shell host project `the-plain-bar` (604a72a9-09eb-4169-920d-e64619651640, env 693ac1d9-8b77-41d9-8735-67e7777cb9d0) — account project cap hit 11-23; teardown = GraphQL serviceDelete only, NEVER project delete (capitol-locksmith sibling service lives here).
- Domain id df543311-1440-476a-801b-38a434840183 pinned to -demo host (canonical/og/sitemap re-pinned; _verify sitemap-vs-origin tripwire PASS).
- Form relay: POST /contact → server.js → Brevo v3 HTTP API (443; htmlContent/textContent keys) → lane mailbox; 303→/thanks on success, 502 fallback renders shop identity only. BREVO_API_KEY set on service via --stdin, fingerprint cffe2fd40342…==local 89B match.
- Pixel: GET /open?t=<token> 200 image/gif 43B (+ /pixel.gif alias); t1 token deannas-wine-bar-t1 verified live.
- Deploys: build 6b91c9d1 → CSS round-1 fixes 98e3f0bf → /open route 2105beb8 (SUCCESS).
- Verification: _verify.py PASS (public + origin); 17-path 200-walk incl /open, /healthz, og.png sha==local, X-Robots noindex headers; render-sweep 10 pages × 2 viewports = 20/20 DOM gates, 0px overflow; vision battery 2 rounds — real defects fixed (masthead grid alignment 134/1146 parity, card link baselines flex/margin-top:auto, h2 orphan break, redundant breadcrumb labels, map captions); all round-2 claims adjudicated against Playwright DOM numbers (footer centering, caption centering centerDiff=0, hero CTA vcenter parity, clipping family = battery false positives).
- Facts discipline: press-only copy (P&C/Hoodline/WhatNow 2026-10; SC LLC notice charleston-639956 2026-08-19); no phone/hours/prices invented — unknowns omitted; ZIP 29407 (corrected from press 29414 via geocode+parcel).
- lane.db: deploys + services rows recorded via sites_agency_state.py; export+verify IDENTICAL 2026-11-25.
- Owner: pitch t1 sent 2026-11-25 13:53 PST (16:53 EST) → info@peculiarpigfarm.com; t2 seat t_eec9d21a parked to 2026-12-04T07:30:00-05:00; ladder 12-04/12-11/12-18; teardown recheck >=12-23 EST silent. bertspigshop.com = owner-grabbed parked domain (registered 2026-06-29 NetSolutions) — delivery path: connect in owner's name, no recovery needed.
