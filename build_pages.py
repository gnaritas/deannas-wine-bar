#!/usr/bin/env python3
"""Deanna's Wine Bar & Bert's Pig Shop — generator (single source for all pages).
websites lane, card t_5c0aaeee. Built 2026-11-25. Demo host pinned from first byte.
Design: wine-label typography — bordeaux/cream/blush + a kept-green hairline homage to
the old 7-Eleven walkway. No photos, no third-party JS, no webfonts.
Facts ONLY from press-verified card: P&C 2026-10-28 + hoodline + WhatNow + citypaper +
manytown + HCS + patch.com + SC DOR notice (NoticeRegistry). Unknown (phone, hours,
prices, opening day) = omitted, never guessed."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://deannas-wine-bar-demo.up.railway.app"

BRAND = "Deanna's Wine Bar &amp; Bert's Pig Shop"
BRAND_PLAIN = "Deanna's Wine Bar & Bert's Pig Shop"
ADDR = "521 Wappoo Road, Charleston, SC 29407"
GEO = (32.7864194, -80.0205329)  # exact house match, OpenStreetMap way 190346708 (ODbL)
MAP_Q = "https://www.google.com/maps?q=521%20Wappoo%20Road%2C%20Charleston%2C%20SC%2029407&output=embed"
DIRS = "https://www.google.com/maps/dir/?api=1&destination=521%20Wappoo%20Road%2C%20Charleston%2C%20SC%2029407"

def meta(desc, path, og_desc=None, img=True):
    u = ORIGIN + path
    d = desc.replace('"', "'")
    od = (og_desc or desc).replace('"', "'")
    tags = [
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="description" content="%s">' % d,
        '<link rel="canonical" href="%s">' % u,
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="/style.css">',
        '<meta property="og:title" content="%s">' % ("%s — Deanna's Wine Bar & Bert's Pig Shop" % BRAND_PLAIN if path == "/" else "Deanna's Wine Bar & Bert's Pig Shop"),
    ]
    return tags

def head(title, desc, path, ld=None, utility=False, og_desc=None):
    u = ORIGIN + path
    d = desc.replace('"', "'")
    parts = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
             '<meta name="robots" content="noindex, nofollow">',
             '<!-- BUILT-2026-11-25 -->',
             '<title>%s</title>' % title,
             '<meta name="description" content="%s">' % d,
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<link rel="canonical" href="%s">' % u,
             '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
             '<link rel="stylesheet" href="/style.css">']
    if not utility:
        t = title.replace('"', "'")
        od = (og_desc or desc).replace('"', "'")
        parts += [
            '<meta property="og:type" content="website">',
            '<meta property="og:title" content="%s">' % t,
            '<meta property="og:description" content="%s">' % od,
            '<meta property="og:image" content="%s/og.png">' % ORIGIN,
            '<meta property="og:url" content="%s">' % u,
            '<meta name="twitter:card" content="summary_large_image">']
    for blk in (ld or []):
        parts.append('<script type="application/ld+json">%s</script>' % json.dumps(blk, ensure_ascii=False))
    parts.append('</head>')
    return "\n".join(parts)

NAV_LINKS = [
    ("The concept", "/the-concept"),
    ("Wine", "/wine-list-west-ashley"),
    ("Pig Shop", "/charcuterie-and-fresh-pork"),
    ("Our story", "/our-story"),
    ("Visit", "/visit"),
]

def nav(active):
    items = []
    for label, href in NAV_LINKS:
        cur = ' aria-current="page"' if href == active else ""
        items.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    items.append('<a class="btn sm" href="/contact">Opening-day list</a>')
    return ('<body>\n<div class="topline" aria-hidden="true"></div>\n'
            '<a class="skip" href="#main">Skip to content</a>\n'
            '<header class="site">\n'
            '<p class="brand mono"><a href="/">Deanna&#8217;s Wine Bar <em>&amp; Bert&#8217;s Pig Shop</em></a></p>\n'
            '<nav aria-label="Site"><p>%s</p></nav>\n'
            '</header>\n<main id="main">' % " ".join(items))

FOOTER = ('</main>\n<footer>\n'
          '<p class="footline">%s</p>\n'
          '<p class="footline">%s</p>\n'
          '<p class="footline fine">&copy; 2026 &middot; <a href="/the-concept">Concept</a> &middot; <a href="/visit">Visit</a> &middot; <a href="/contact">Contact</a> &middot; <a href="/privacy">Privacy</a></p>\n'
          '</footer>\n</body>\n</html>\n') % (BRAND_PLAIN, "Opening late 2026 &middot; 521 Wappoo Road, Charleston, SC 29407 &middot; West Ashley")

def restaurant_node(path="/"):
    return {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": BRAND_PLAIN,
        "url": ORIGIN + path,
        "image": ORIGIN + "/og.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "521 Wappoo Road",
            "addressLocality": "Charleston",
            "addressRegion": "SC",
            "postalCode": "29407",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": "https://www.google.com/maps?q=521%20Wappoo%20Road%2C%20Charleston%2C%20SC%2029407",
    }

def breadcrumb(label, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": ORIGIN + path},
        ],
    }

def service_node(name, stype, desc, path):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": stype,
        "description": desc,
        "url": ORIGIN + path,
        "areaServed": [
            {"@type": "Place", "name": "West Ashley, Charleston"},
            {"@type": "City", "name": "Charleston", "containedInPlace": {"@type": "State", "name": "South Carolina"}},
        ],
        "provider": {k: v for k, v in restaurant_node(path).items() if k != "@context"},
    }

pages = {}

# ---------------- HOME ----------------
home_ld = [restaurant_node("/")]
pages["index.html"] = (
    head("Deanna's Wine Bar &amp; Bert's Pig Shop — Pig-to-Table, West Ashley, Charleston SC",
         "A wine bar and a working pig shop opening late 2026 at 521 Wappoo Road in West Ashley, Charleston SC. Small-producer wines, charcuterie made on site, pork raised on our own family farm.",
         "/", home_ld)
    + nav("/")
    + '''<section class="hero">
  <p class="lab mono">Pig-to-table &middot; West Ashley &middot; Charleston, SC</p>
  <h1>Deanna&#8217;s Wine Bar <span class="amp">&amp;</span> Bert&#8217;s Pig Shop</h1>
  <p class="sub">A wine bar and a working pig shop in the same room — opening by the end of 2026 at 521 Wappoo Road, in the building that used to hold a 7&#8209;Eleven.</p>
  <p class="hero-cta"><a class="btn" href="/contact">Leave your email for opening day</a> <a class="ghost" href="/the-concept">Read the concept</a></p>
</section>
<section class="panels">
  <article class="frame">
    <p class="lab mono">The wine</p>
    <h2>Small producers, generous pours</h2>
    <p>Little-known bottles and revived classics from small European and domestic makers — at prices that turn a glass into a habit. The list is built by sommelier Andres Contreras, the man behind Rue de Jean&#8217;s 300&#8209;bottle carte.</p>
    <p><a href="/wine-list-west-ashley">Explore the wine list &rarr;</a></p>
  </article>
  <article class="frame">
    <p class="lab mono">The pig shop</p>
    <h2>Charcuterie<br>made in this room</h2>
    <p>Bert&#8217;s Pig Shop works whole hogs from Peculiar Pig, a fifth-generation family farm in Dorchester County. Fresh pork, sausages and house-made charcuterie — rendered on site, under our state agriculture license.</p>
    <p><a href="/charcuterie-and-fresh-pork">Meet Bert&#8217;s Pig Shop &rarr;</a></p>
  </article>
  <article class="frame">
    <p class="lab mono">The room</p>
    <h2>Cozy. Neighborhood. Dinner-party.</h2>
    <p>Two counters, one table. Order at the counter, get a seat, watch the boards come out of the same kitchen that breaks down the hogs. Sandwiches and boards on the menu from day one.</p>
    <p><a href="/our-story">Read our story &rarr;</a></p>
  </article>
</section>
<section class="band">
  <div class="band-copy">
    <p class="lab mono">Opening late 2026</p>
    <h2>First word goes to the list</h2>
    <p>The exact opening day, the hours and the full board list land right here — and in the opening-day email, which people on the list get first.</p>
    <p><a class="btn" href="/contact">Join the opening-day list</a></p>
  </div>
  <div class="band-map"><iframe src="''' + MAP_Q + '''" loading="lazy" title="Map: Deanna's Wine Bar and Bert's Pig Shop, 521 Wappoo Road, Charleston SC" allow="management:coordinate"></iframe><p class="mapcap">521 Wappoo Road &middot; Charleston SC 29407 &middot; <a href="''' + DIRS + '''">Get directions &nearr;</a></p></div>
</section>''')

# ---------------- THE CONCEPT (hub + FAQ) ----------------
faq_items = [
    ("When do you open?",
     "By the end of 2026. The exact day, the hours and the full list of boards go up on this site first — and people on the opening-day list get the email before anyone else."),
    ("Is it a restaurant, a bar, or a butcher shop?",
     "All three, in one room. Deanna&#8217;s Wine Bar is the bar and dining room; Bert&#8217;s Pig Shop is the counter — one kitchen, one whole-hog program, one storefront on Wappoo Road."),
    ("Where does the meat come from?",
     "Peculiar Pig, a fifth-generation family farm on 12 acres of ancestral land in upper Dorchester County. The hogs graze and forage on wooded lots and get supplemented with heritage grains."),
    ("Do you have a menu?",
     "Sandwiches, charcuterie boards and wine from day one. Prices and the full list post here the same week we open."),
]
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a.replace("&#8217;", "'").replace("&#8209;", "-")}}
                         for q, a in faq_items]}
pages["the-concept.html"] = (
    head("Two Counters, One Room — Deanna's Wine Bar & Bert's Pig Shop, Charleston SC",
         "The pig-to-table concept behind Deanna's Wine Bar and Bert's Pig Shop: whole hogs from a fifth-generation Dorchester farm, charcuterie rendered on site under a state license, wine from small makers.",
         "/the-concept", [breadcrumb("The concept", "/the-concept"), faq_ld])
    + nav("/the-concept")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; The concept</p>
  <h1>Two counters, one room</h1>
  <p class="lede">Deanna&#8217;s Wine Bar and Bert&#8217;s Pig Shop share one storefront, one kitchen and one idea: the pig arrives whole, everything gets used, and the wine is chosen to drink with it.</p>
  <h2>One farm, start to finish</h2>
  <p>The pork program is not a supplier arrangement — it is a family farm. Bert&#8217;s Pig Shop works hogs from Peculiar Pig, a fifth-generation farm on ancestral land near the Edisto River in upper Dorchester County, where the herd grazes and forages across wooded lots and the diet is finished on heritage grains. Whole hogs come in; fresh cuts, sausages and charcuterie go out to the counter the same week.</p>
  <h2>Licensed to do it on the premises</h2>
  <p>Making charcuterie where you serve it takes a South Carolina Department of Agriculture license — and a hazard plan thick enough to stand up on its own. We hold one. That license is what lets the case in front of you come out of the same building the hogs did.</p>
  <h2>The wine, priced like a neighborhood should drink it</h2>
  <p>Sommelier Andres Contreras built the list from tastings and a deep dive through wine archives: small European and domestic makers, reviving bottlings that fell off the shelves, poured at prices that invite a second glass. Boards and sandwiches are built to match it.</p>
  <dl class="faq">''' + "".join('<dt>%s</dt><dd>%s</dd>' % (q, a) for q, a in faq_items) + '''</dl>
  <p class="lab mono">Keep going</p>
  <p class="cta-row"><a class="btn" href="/contact">Join the opening-day list</a> <a href="/wine-list-west-ashley">The wine list</a> &middot; <a href="/charcuterie-and-fresh-pork">The pig shop</a> &middot; <a href="/our-story">Our story</a></p>
</article>''')

# ---------------- WINE DETAIL ----------------
pages["wine-list-west-ashley.html"] = (
    head("Wine List by Andres Contreras — Deanna's Wine Bar, West Ashley, Charleston SC",
         "Deanna's Wine Bar pours small-producer European and domestic wines, revived bottles and old favorites at neighborhood prices. The list is curated by sommelier Andres Contreras.",
         "/wine-list-west-ashley",
         [breadcrumb("Wine list", "/wine-list-west-ashley"),
          service_node("Wine list curated by sommelier Andres Contreras", "Wine bar",
                       "Small European and domestic producers, revived and lesser-known bottles, affordable pours and boards, at 521 Wappoo Road in West Ashley, Charleston SC.",
                       "/wine-list-west-ashley")])
    + nav("/wine-list-west-ashley")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; <a href="/the-concept">The concept</a> &middot; Wine</p>
  <p class="lab mono">Deanna&#8217;s Wine Bar &middot; the list</p>
  <h1>Wine chosen the hard way</h1>
  <p class="lede">Nearly three dozen tastings, a long dive through wine archives, and one rule: small makers at prices people around here will actually drink every week.</p>
  <p>The list belongs to sommelier <strong>Andres Contreras</strong>, a West Ashley neighborhood wine program built on a résumé that starts with Rue de Jean — where he helped curate a 300&#8209;bottle carte — and runs through Coast Bar &amp; Grill and Costa. Charleston&#8217;s Zagat 30 Under 30 list says what the industry already knew; in 2017 he was the Charleston-based voice of the Wines of Chile campaign.</p>
  <h2>What to expect on it</h2>
  <ul class="board">
    <li><span>Small European producers</span> bottlings you will not find on the shelf at the big-box store two miles away</li>
    <li><span>Small domestic makers</span> the winemakers, not the wine brands</li>
    <li><span>Revived and lesser-known bottles</span> old favorites brought back, and new ones given their first Charleston pour</li>
    <li><span>Affordable by design</span> the whole point: a wine bar for Tuesday, not only for anniversaries</li>
  </ul>
  <p>Order a glass or a bottle; it comes with sandwiches and house-made boards from the counter behind you. The full list posts here the week we open.</p>
  <p class="cta-row"><a class="btn" href="/contact">Join the opening-day list</a> <a href="/charcuterie-and-fresh-pork">See the pig shop &rarr;</a></p>
</article>''')

# ---------------- PIG SHOP DETAIL ----------------
pages["charcuterie-and-fresh-pork.html"] = (
    head("Charcuterie Made On Site & Fresh Pork — Bert's Pig Shop, Charleston SC",
         "Bert's Pig Shop works whole hogs from Peculiar Pig, a fifth-generation family farm in Dorchester County: fresh pork, sausages and charcuterie rendered on site under a SCDA license.",
         "/charcuterie-and-fresh-pork",
         [breadcrumb("Pig shop", "/charcuterie-and-fresh-pork"),
          service_node("Fresh pork and house-made charcuterie", "Butcher counter and charcuterie",
                       "Whole-hog butchery, fresh pork, sausages and house-made charcuterie made on site from Peculiar Pig farm hogs, at 521 Wappoo Road in West Ashley, Charleston SC.",
                       "/charcuterie-and-fresh-pork")])
    + nav("/charcuterie-and-fresh-pork")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; <a href="/the-concept">The concept</a> &middot; Pig shop</p>
  <p class="lab mono">Bert&#8217;s Pig Shop &middot; the counter</p>
  <h1>Whole hog. Same building. No shortcuts.</h1>
  <p class="lede">Chef Bert Sheffield spent years in Asheville breaking down whole animals and fermenting what came off them. Bert&#8217;s Pig Shop is that craft pointed at one farm: Peculiar Pig, in Dorchester County.</p>
  <h2>The farm up the road</h2>
  <p>Peculiar Pig is a fifth-generation family farm on 12 acres of ancestral land near the Edisto River. Hogs graze and forage on wooded lots, moving paddock to paddock, finished on heritage grains. The farm raises whole hogs, primal cuts and sausages — and Bert&#8217;s Pig Shop exists to bring that meat home to West Ashley, fresh, with nothing wrapped in plastic from a warehouse three states away.</p>
  <h2>What the counter does</h2>
  <ul class="board">
    <li><span>Fresh pork, by the cut</span> the week&#8217;s breakdown, straight from the farm</li>
    <li><span>House-made charcuterie</span> rendered, cured and hung on site under our S.C. Department of Agriculture license</li>
    <li><span>Boards</span> the case, built to order for the table you are sitting at</li>
    <li><span>Sandwiches</span> what came off the hog, on bread, while you wait</li>
  </ul>
  <p>Restaurant accounts around Charleston are next on the list — the shop was always meant to feed more than the dining room.</p>
  <p class="cta-row"><a class="btn" href="/contact">Join the opening-day list</a> <a href="/wine-list-west-ashley">See the wine list &rarr;</a></p>
</article>''')

# ---------------- OUR STORY ----------------
pages["our-story.html"] = (
    head("Our Story — Deanna's Wine Bar & Bert's Pig Shop, Charleston SC",
         "Bert Sheffield and Douglas Hickerson are opening Deanna's Wine Bar and Bert's Pig Shop at the old 7-Eleven on Wappoo Road — named for Douglas's mother, fed by his partner's family farm.",
         "/our-story",
         [breadcrumb("Our story", "/our-story"),
          {"@context": "https://schema.org", "@type": "AboutPage", "name": "Our story — %s" % BRAND_PLAIN,
           "url": ORIGIN + "/our-story", "about": {"@type": "Restaurant", "name": BRAND_PLAIN,
           "address": {"@type": "PostalAddress", "streetAddress": "521 Wappoo Road", "addressLocality": "Charleston", "addressRegion": "SC", "postalCode": "29407", "addressCountry": "US"}}}])
    + nav("/our-story")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Our story</p>
  <h1>A wine bar named for somebody&#8217;s mother</h1>
  <p class="lede">Deanna&#8217;s is named for Deanna Hickerson — the mother of Douglas Hickerson, one half of the pair behind this place. The other half is chef Bert Sheffield, and his family&#8217;s farm puts the pigs on the counter.</p>
  <h2>The two of them</h2>
  <p><strong>Bert Sheffield</strong> was born in south Louisiana, cooked his way through Atlanta, then ran a kitchen in Asheville where he built a name for whole-animal butchery and fermentation. <strong>Douglas Hickerson</strong> is a Charleston real estate agent by day and a restaurateur by night — the pair kept circling each other&#8217;s plans until this corner lined up.</p>
  <h2>The room they chose</h2>
  <p>The building is the old 7&#8209;Eleven on Wappoo Road, and they did not sandblast that fact away. The original floor stays. The painted green walkway stays — it is now the thin green line across the top of every page of this site. Before the deal was even signed, Bert put up a sign out front: <em>hello, neighbors — something good is coming.</em> If you have photos of the old store, they genuinely want to see them.</p>
  <h2>The bet</h2>
  <p>A wine bar that renders its own charcuterie, licensed to do it on the premises, stocked with wines from makers you can count on one hand, in a room built to feel like a dinner party instead of a tasting event. The owners figure it will be the only restaurant of its kind in South Carolina. We intend to be right.</p>
  <h2>In the news</h2>
  <ul class="press">
    <li><a href="https://www.postandcourier.com/food/deannas-wine-bar-restaurant-charleston-sc/article_877cc05b-5550-4f2a-a15d-e10c32a71dc6.html">Post &amp; Courier — New wine, whole-hog charcuterie bar coming to old 7-Eleven in West Ashley</a></li>
    <li><a href="https://whatnow.com/charleston/restaurants/deannas-wine-bar-and-berts-pig-shop-bringing-wine-and-house-made-charcuterie-to-west-ashley/">WhatNow Charleston — Bringing Wine and House-Made Charcuterie to West Ashley</a></li>
    <li><a href="https://hoodline.com/2026/10/old-west-ashley-7-eleven-reborn-as-whole-hog-wine-bar-named-for-someone-s-mom/">Hoodline — Old West Ashley 7-Eleven reborn as whole-hog wine bar named for someone&#8217;s mom</a></li>
  </ul>
  <p class="cta-row"><a class="btn" href="/contact">Join the opening-day list</a> <a href="/visit">Find us on Wappoo Road &rarr;</a></p>
</article>''')

# ---------------- VISIT ----------------
pages["visit.html"] = (
    head("Visit — 521 Wappoo Road, West Ashley, Charleston SC 29407",
         "Deanna's Wine Bar and Bert's Pig Shop open late 2026 at 521 Wappoo Road in West Ashley — the corner of Wappoo and Pebble Street, a block off Savannah Highway, Charleston SC.",
         "/visit",
         [breadcrumb("Visit", "/visit"),
          service_node("Visit Deanna's Wine Bar & Bert's Pig Shop", "Dining and retail counter",
                       "Wine bar and pig shop opening late 2026 at 521 Wappoo Road, corner of Wappoo Road and Pebble Street, West Ashley, Charleston SC 29407.",
                       "/visit")])
    + nav("/visit")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Visit</p>
  <h1>521 Wappoo Road</h1>
  <p class="lede">Where Wappoo Road bends out toward the Wappoo Cut, at the corner of Pebble Street — a block off Savannah Highway, in the old 7&#8209;Eleven.</p>
  <div class="visit-grid">
    <div class="frame">
      <p class="lab mono">Address</p>
      <p class="addr">%s</p>
      <p><a href="%s">Get directions &nearr;</a></p>
      <p class="lab mono">Opening</p>
      <p>Late 2026. The opening day and the hours will be posted on this page first — people on the <a href="/contact">opening-day list</a> get an email the day it is set.</p>
    </div>
    <div class="map-tall"><iframe src="%s" loading="lazy" title="Map of Deanna's Wine Bar and Bert's Pig Shop at 521 Wappoo Road, Charleston SC" allow="management:coordinate"></iframe><p class="mapcap">Wappoo Road at Pebble Street &middot; a block off Savannah Highway</p></div>
  </div>
</article>''' % (ADDR, DIRS, MAP_Q))

# ---------------- CONTACT ----------------
pages["contact.html"] = (
    head("Contact — Deanna's Wine Bar & Bert's Pig Shop, Charleston SC",
         "Join Deanna's Wine Bar and Bert's Pig Shop's opening-day list: leave your email and the first word about opening day, hours and the wine list comes to you. 521 Wappoo Road, Charleston SC.",
         "/contact",
         [breadcrumb("Contact", "/contact"),
          service_node("Opening-day list and contact", "Customer contact",
                       "Leave your email to hear first about the late-2026 opening of Deanna's Wine Bar and Bert's Pig Shop at 521 Wappoo Road, Charleston SC 29407.",
                       "/contact")])
    + nav("/contact")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Contact</p>
  <p class="lab mono">Opening-day list</p>
  <h1>Be first through the door</h1>
  <p class="lede">Leave your email. When the opening day is set — late 2026 — the first word goes to this list: the day, the hours, the wine list, the boards.</p>
  <form class="cform" method="post" action="/contact">
    <p><label for="f-name">Name</label><input id="f-name" name="name" type="text" maxlength="120" required></p>
    <p><label for="f-email">Email <span class="fine">so we can tell you when we open</span></label><input id="f-email" name="email" type="email" maxlength="120" required></p>
    <p><label for="f-msg">Questions or something you&#8217;re hoping we&#8217;ll pour? <span class="fine">(optional)</span></label><textarea id="f-msg" name="message" rows="4" maxlength="4000"></textarea></p>
    <p><button class="btn" type="submit">Send it</button></p>
  </form>
  <div class="frame">
    <p class="lab mono">The storefront</p>
    <p class="addr">%s</p>
    <p><a href="%s">Get directions &nearr;</a></p>
  </div>
  <div class="map-tall"><iframe src="%s" loading="lazy" title="Map: 521 Wappoo Road, Charleston SC — Deanna's Wine Bar and Bert's Pig Shop" allow="management:coordinate"></iframe><p class="mapcap">521 Wappoo Road &middot; corner of Wappoo Road and Pebble Street &middot; <a href="%s">Get directions &nearr;</a></p></div>
</article>''' % (ADDR, DIRS, MAP_Q, DIRS))

# ---------------- PRIVACY ----------------
pages["privacy.html"] = (
    head("Privacy — Deanna's Wine Bar & Bert's Pig Shop",
         "How this site handles what you send it: contact-form messages go to the shop's inbox and are used only to answer you and the opening-day announcements. No cookies, no trackers.",
         "/privacy",
         [breadcrumb("Privacy", "/privacy"), restaurant_node("/privacy")])
    + nav("/privacy")
    + '''<article class="page">
  <p class="crumbs mono"><a href="/">Home</a> &middot; Privacy</p>
  <h1>What you send us</h1>
  <p>Messages from this site&#8217;s form go straight to the shop&#8217;s inbox — the name, email and note you type, nothing more. We use them to answer you and to send the opening-day announcement to people who asked for it. We do not sell, rent or trade your details.</p>
  <p>This site sets no cookies and runs no advertising or analytics trackers. Pages load from our own host with our own stylesheet; there is no third-party script on any page.</p>
  <p>Questions about this page? <a href="/contact">Use the form</a> and ask.</p>
</article>''')

# ---------------- 404 / THANKS (utility) ----------------
pages["404.html"] = (
    head("Page not found — Deanna's Wine Bar & Bert's Pig Shop",
         "That page is off the board. Deanna's Wine Bar and Bert's Pig Shop open late 2026 at 521 Wappoo Road in West Ashley, Charleston SC.",
         "/404", utility=True)
    + nav("")
    + '''<article class="page">
  <p class="lab mono">404</p>
  <h1>That page is off the board</h1>
  <p class="lede">The old 7&#8209;Eleven is gone and so is this page. The two that matter are below.</p>
  <p class="cta-row"><a class="btn" href="/">Back to the front</a> <a href="/contact">Join the opening-day list</a></p>
</article>''')

pages["thanks.html"] = (
    head("You're on the list — Deanna's Wine Bar & Bert's Pig Shop",
         "Thanks — Deanna's Wine Bar and Bert's Pig Shop will email you first when the doors open at 521 Wappoo Road, West Ashley, Charleston SC, late 2026.",
         "/thanks", utility=True)
    + nav("")
    + '''<article class="page">
  <p class="lab mono">Received</p>
  <h1>You&#8217;re on the list</h1>
  <p class="lede">When the opening day is set — late 2026, Wappoo Road — this list hears it first: the day, the hours, the wine list, the boards.</p>
  <p class="cta-row"><a class="btn" href="/">Back to the site</a></p>
</article>''')

# ---------------- CSS ----------------
CSS = """:root{
  --ink:#200a12; --wine:#7e2235; --wine-dk:#5c1626; --wine-deep:#3a0d18;
  --paper:#faf5e9; --cream:#f6efe1; --blush:#e2b7a6; --walk:#2f5a3f;
  --rule:#3a1d26; --dim:#8a6f72;
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{color-scheme:light}
body{background:var(--paper);color:var(--ink);font-family:var(--serif);font-size:17px;line-height:1.6}
.topline{height:4px;background:var(--walk)}
.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:var(--cream);padding:.5rem 1rem;z-index:9}
.skip:focus{left:1rem;top:1rem}
a{color:var(--wine)}
a:hover{color:var(--wine-deep)}
.mono{font-family:var(--mono)}
header.site{padding:1.1rem max(1.1rem, calc((100vw - 1012px)/2));border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:.6rem 1.5rem;align-items:center;justify-content:space-between}
.brand{font-size:13px;letter-spacing:.16em;text-transform:uppercase;margin:0}
.brand a{color:var(--ink);text-decoration:none}
.brand em{font-style:normal;color:var(--wine)}
header.site nav p{display:flex;flex-wrap:wrap;gap:.35rem 1.1rem;justify-content:flex-end;margin:0}
header.site nav a{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--rule)}
header.site nav a:hover{color:var(--wine);text-decoration:underline;text-underline-offset:4px}
header.site nav a[aria-current="page"]{color:var(--wine);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
main{max-width:1060px;margin:0 auto;padding:0 1.5rem 3.5rem}
.lab{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--wine);margin-bottom:.6rem}
.hero{background:var(--wine-deep);color:var(--cream);margin:1.5rem 0;border:1px solid var(--rule);outline:1px solid var(--wine);outline-offset:6px;padding:clamp(2rem,6vw,4.5rem) clamp(1.2rem,5vw,4rem);text-align:center}
.hero .lab{color:var(--blush)}
.hero h1{font-size:clamp(2.3rem,6vw,4rem);line-height:1.06;font-weight:700;letter-spacing:.01em;margin:.2rem 0 .4rem}
.hero .amp{color:var(--blush);font-size:.6em;vertical-align:.15em}
.hero .sub{max-width:38rem;margin:.8rem auto 1.4rem;color:var(--cream);font-size:1.05rem;line-height:1.55}
.hero-cta{display:flex;flex-wrap:wrap;gap:.8rem 1.2rem;justify-content:center;align-items:center}
.btn{display:inline-block;background:var(--wine);color:var(--cream);font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;padding:.8rem 1.3rem;border:1px solid var(--rule)}
.btn:hover{background:var(--wine-deep);color:#fff}
.btn.sm{padding:.45rem .8rem;font-size:11px}
a.ghost{color:var(--blush);font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;text-decoration:underline;text-underline-offset:5px}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.2rem;margin:1.6rem 0 2.2rem}
.panels>.frame{height:100%}
.frame{background:#fff;border:1px solid var(--rule);outline:1px solid var(--blush);outline-offset:-9px;padding:1.6rem 1.4rem 1.4rem;display:flex;flex-direction:column}
.frame h2{font-size:1.3rem;line-height:1.2;margin-bottom:.5rem}
.frame p{margin-bottom:.7rem}
.frame p:last-child{margin-bottom:0;margin-top:auto}
.band{display:grid;grid-template-columns:minmax(300px,1.25fr) minmax(260px,1fr);gap:1.4rem;align-items:center;background:var(--cream);border:1px solid var(--rule);padding:1.6rem}
.band h2{font-size:1.6rem;margin-bottom:.4rem}
.band-map iframe{width:100%;aspect-ratio:4/3;border:1px solid var(--rule);display:block;background:var(--paper)}
.mapcap{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);text-align:center;margin-top:.5rem}
.page{padding-top:1.8rem}
.crumbs{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-bottom:1rem}
h1{font-size:clamp(1.9rem,4.5vw,2.9rem);line-height:1.1;margin-bottom:.8rem}
.lede{font-size:1.15rem;line-height:1.55;max-width:44rem;margin-bottom:1.4rem;color:var(--rule)}
.page h2{font-size:1.35rem;margin:1.6rem 0 .5rem}
.page p{max-width:46rem;margin-bottom:1rem}
.board{list-style:none;margin:0 0 1.2rem;border-top:1px solid var(--rule)}
.board li{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:.5rem 1.4rem;padding:.65rem 0;border-bottom:1px solid var(--rule);font-size:.98rem}
.board li span{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--wine);padding-top:.15rem}
dl.faq{margin:1.6rem 0;border-top:1px solid var(--rule)}
dl.faq dt{font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--wine);padding:.9rem 0 .2rem}
dl.faq dd{padding:0 0 1rem;border-bottom:1px solid var(--rule);max-width:46rem}
ul.press{list-style:none;margin:0 0 1.2rem}
ul.press li{padding:.5rem 0;border-bottom:1px solid var(--rule)}
.cta-row{display:flex;flex-wrap:wrap;gap:.8rem 1.2rem;align-items:center;margin-top:1.4rem}
.addr{font-family:var(--mono);font-size:14px;letter-spacing:.04em;margin-bottom:.6rem}
.visit-grid{display:grid;grid-template-columns:minmax(280px,1fr) minmax(280px,1.2fr);gap:1.4rem;align-items:start}
.map-tall iframe{width:100%;aspect-ratio:4/3;border:1px solid var(--rule);display:block;background:var(--paper)}
.cform{max-width:34rem;margin:0 0 1.8rem}
.cform p{margin-bottom:1rem}
.cform label{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--rule);margin-bottom:.35rem}
.fine{color:var(--dim);text-transform:none;letter-spacing:.02em}
.cform input,.cform textarea{width:100%;font-family:var(--serif);font-size:16px;padding:.65rem .8rem;border:1px solid var(--rule);background:#fff;color:var(--ink)}
.cform input:focus,.cform textarea:focus{outline:2px solid var(--wine);outline-offset:1px}
footer{background:var(--ink);color:var(--cream);padding:1.8rem 1.5rem;text-align:center}
footer p.footline{font-family:var(--mono);font-size:12px;letter-spacing:.08em;line-height:1.9;max-width:none;margin:0 auto}
footer a{color:var(--blush)}
footer p.fine{color:#c9a79b;font-size:11px}
@media (max-width:640px){
  body{font-size:16px}
  header.site nav p{justify-content:flex-start}
  .band,.visit-grid{grid-template-columns:1fr}
  .board li{grid-template-columns:1fr;gap:.2rem}
  main{padding:0 1.1rem 3rem}
  .hero{padding:2rem 1.1rem}
}"""

def write(name, content):
    with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as f:
        f.write(content if content.endswith("\n") else content + "\n")

os.makedirs(PUBLIC, exist_ok=True)
for name, content in pages.items():
    write(name, content + FOOTER)
write("style.css", CSS)

core = ["index.html", "the-concept.html", "wine-list-west-ashley.html", "charcuterie-and-fresh-pork.html",
        "our-story.html", "visit.html", "contact.html", "privacy.html"]
today = "2026-11-25"
locs = "\n".join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' %
                 (ORIGIN, "/" if f == "index.html" else "/" + f[:-5], today) for f in core)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % locs)
write("robots.txt", "User-agent: *\nDisallow:\n\nSitemap: %s/sitemap.xml\n" % ORIGIN)
# static assets that live at repo root must ride into public/ (server serves public/ only)
import shutil
for asset in ("pixel.gif", "favicon.svg"):
    src = os.path.join(HERE, asset)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(PUBLIC, asset))
print("built %d pages + css + sitemap + robots" % len(pages))
