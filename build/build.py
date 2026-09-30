#!/usr/bin/env python3
"""
Static site generator for the Reliable Steel Weld website.

Usage:  python3 build/build.py
Writes HTML pages, sitemap.xml and robots.txt into the repository root,
ready to host on GitHub Pages, Netlify, Vercel or any static host.
"""
import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import config as C  # noqa: E402
import pages as P  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
ASSET_VERSION = "3"

ICONS = {
    "plasma": '<path d="M12 2v6M9 5l3 3 3-3"/><path d="M4 21h16"/><path d="M6 21l3-9h6l3 9"/><path d="M12 12v3"/>',
    "profile": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 4v2M12 18v2M4 12h2M18 12h2"/>',
    "plate": '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M3 10h18M8 6v12"/>',
    "machining": '<path d="M4 20h16"/><rect x="6" y="14" width="12" height="4"/><path d="M12 14V8M9 4h6l-1 4h-4z"/>',
    "laser": '<path d="M12 2v10"/><path d="M8 2h8"/><path d="M4 20l8-8 8 8"/><path d="M4 20h16"/>',
    "fabricator": '<path d="M3 21l7-7M14 4l6 6-8 8-6-6z"/><path d="M17 7l-3-3"/>',
    "structure": '<path d="M3 21V9l9-6 9 6v12"/><path d="M3 21h18M9 21v-6h6v6M3 9h18"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0114 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONS[name]}</svg>')


WA_SVG = ('<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 001.8-1.2 2.2 2.2 0 00.1-1.2c0-.1-.2-.2-.5-.3z"/></svg>')


def url(path):
    return f"{C.SITE_URL}/{path}"


def wa_link(text="Hello Reliable Steel Weld, I need a quote for CNC cutting job work."):
    from urllib.parse import quote
    return f"https://wa.me/{C.WHATSAPP_E164}?text={quote(text)}"


# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
def business_schema():
    data = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": url("#business"),
        "name": C.BUSINESS_NAME,
        "alternateName": C.SHORT_NAME,
        "slogan": C.TAGLINE,
        "url": url(""),
        "logo": url("assets/img/rsw-logo.png"),
        "image": url("assets/img/rsw-logo-full.jpg"),
        "telephone": C.PHONE_E164,
        "email": C.EMAIL,
        "founder": {"@type": "Person", "name": C.OWNER_NAME},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": C.STREET,
            "addressLocality": C.LOCALITY,
            "addressRegion": C.REGION,
            "postalCode": C.POSTAL_CODE,
            "addressCountry": C.COUNTRY,
        },
        "geo": {"@type": "GeoCoordinates", "latitude": C.GEO_LAT, "longitude": C.GEO_LNG},
        "openingHours": C.HOURS_SCHEMA,
        "areaServed": [{"@type": "Place", "name": a} for a in P.AREAS] + [{"@type": "State", "name": "Maharashtra"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "CNC Cutting, Machining & Fabrication Job Work",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["h1"], "url": url(s["slug"] + "/")}}
                for s in P.SERVICES
            ],
        },
    }
    if C.SOCIAL:
        data["sameAs"] = list(C.SOCIAL.values())
    return data


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url(path)}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def service_schema(name, description, path, area=None):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "url": url(path),
        "serviceType": name,
        "provider": {"@id": url("#business")},
        "areaServed": area or [{"@type": "Place", "name": a} for a in ("Taloja MIDC", "Panvel", "Navi Mumbai", "Mumbai", "Maharashtra")],
    }


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def head(title, description, path, rel, schemas):
    canonical = url(path)
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="IN-MH">
<meta name="geo.placename" content="Taloja MIDC, Navi Mumbai">
<meta name="geo.position" content="{C.GEO_LAT};{C.GEO_LNG}">
<meta name="ICBM" content="{C.GEO_LAT}, {C.GEO_LNG}">
<meta name="theme-color" content="#a3261f">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="{C.BUSINESS_NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url('assets/img/rsw-logo-full.jpg')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{rel}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{rel}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/style.css?v={ASSET_VERSION}">
{''.join(ld(s) for s in schemas)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>"""


def header(rel, active):
    svc_links = "".join(
        f'<li><a href="{rel}{s["slug"]}/"{" aria-current=page" if active == s["slug"] else ""}>{s["nav"]}</a></li>'
        for s in P.SERVICES
    )
    loc_links = "".join(
        f'<li><a href="{rel}{l["slug"]}/">{l["place"]}</a></li>' for l in P.LOCATIONS
    )

    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return f"""
<div class="topbar">
  <div class="wrap topbar-in">
    <span>{icon('pin')} Taloja MIDC, Navi Mumbai</span>
    <span class="tb-right"><a href="tel:{C.PHONE_E164}">{icon('phone')} {C.PHONE_DISPLAY}</a><a href="mailto:{C.EMAIL}">{icon('mail')} {C.EMAIL}</a></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap nav-in">
    <a class="brand" href="{rel}" aria-label="{C.BUSINESS_NAME} home">
      <img src="{rel}assets/img/rsw-logo.png" alt="Reliable Steel Weld RSW logo" width="52" height="52">
      <span class="brand-txt"><strong>Reliable Steel Weld</strong><small>Fabrication · Erection · Civil Work</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu">{icon('menu')}</button>
    <nav id="nav" class="nav" aria-label="Main">
      <ul>
        <li><a href="{rel}"{cur('home')}>Home</a></li>
        <li><a href="{rel}about/"{cur('about')}>About Us</a></li>
        <li class="has-sub"><button class="sub-btn" aria-expanded="false">Services</button><ul class="sub">{svc_links}</ul></li>
        <li class="has-sub"><button class="sub-btn" aria-expanded="false">Locations</button><ul class="sub">{loc_links}</ul></li>
        <li><a href="{rel}contact/"{cur('contact')}>Contact</a></li>
      </ul>
      <a class="btn btn-primary nav-cta" href="{rel}contact/">Get a Quote</a>
    </nav>
  </div>
</header>
<main id="main">"""


def footer(rel):
    svc = "".join(f'<li><a href="{rel}{s["slug"]}/">{s["h1"].split(" — ")[0].split(" & ")[0]}</a></li>' for s in P.SERVICES)
    loc = "".join(f'<li><a href="{rel}{l["slug"]}/">CNC Plasma Cutting {l["place"]}</a></li>' for l in P.LOCATIONS)
    gst = f"<p>GSTIN: {C.GSTIN}</p>" if C.GSTIN else ""
    social = "".join(f'<a href="{v}" rel="noopener" target="_blank">{k.title()}</a>' for k, v in C.SOCIAL.items())
    return f"""</main>
<section class="cta-band">
  <div class="wrap cta-in">
    <div>
      <h2>Have a drawing? Get a quote today.</h2>
      <p>Send your DXF, PDF or sketch with material, thickness and quantity.</p>
    </div>
    <div class="cta-btns">
      <a class="btn btn-wa" href="{wa_link()}" rel="noopener" target="_blank">{WA_SVG} WhatsApp Drawing</a>
      <a class="btn btn-light" href="tel:{C.PHONE_E164}">{icon('phone')} Call Now</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="{rel}assets/img/rsw-logo.png" alt="Reliable Steel Weld logo" width="64" height="64" loading="lazy">
      <p class="foot-name">Reliable Steel Weld</p>
      <p>{C.TAGLINE}.</p>
      {gst}
      <div class="social">{social}</div>
    </div>
    <div>
      <h3>Services</h3>
      <ul>{svc}</ul>
    </div>
    <div>
      <h3>Locations</h3>
      <ul>{loc}<li><a href="{rel}cnc-plasma-cutting-job-work/">CNC Plasma Cutting Maharashtra</a></li></ul>
    </div>
    <div>
      <h3>Contact</h3>
      <address>
        <p>{icon('pin')} <span>{C.STREET},<br>{C.LOCALITY}, {C.CITY},<br>{C.REGION} {C.POSTAL_CODE}</span></p>
        <p>{icon('phone')} <a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a></p>
        <p>{icon('mail')} <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
        <p>{icon('clock')} {C.HOURS}</p>
      </address>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <p>© <span data-year>{datetime.date.today().year}</span> Reliable Steel Weld. All rights reserved.</p>
    <p><a href="{rel}about/">About</a> · <a href="{rel}contact/">Contact</a> · <a href="{rel}sitemap.xml">Sitemap</a></p>
  </div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}</a>
<script src="{rel}assets/js/main.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
"""


def breadcrumbs_html(rel, crumbs):
    parts = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<li aria-current="page">{name}</li>')
        else:
            parts.append(f'<li><a href="{rel}{path}">{name}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def faq_html(faqs, heading="Frequently Asked Questions"):
    items = "".join(
        f'<details class="faq"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )
    return f'<section class="section"><div class="wrap narrow"><h2 class="sec-title">{heading}</h2>{items}</div></section>'


def service_cards(rel, exclude=None, heading_level="h3"):
    cards = []
    for s in P.SERVICES:
        if s["slug"] == exclude:
            continue
        cards.append(
            f'<a class="card svc" href="{rel}{s["slug"]}/">'
            f'<span class="svc-ic">{icon(s["icon"])}</span>'
            f'<{heading_level}>{s["nav"]}</{heading_level}>'
            f'<p>{s["card"]}</p>'
            f'<span class="more">Learn more {icon("arrow")}</span></a>'
        )
    return f'<div class="grid cards">{"".join(cards)}</div>'


def process_html():
    steps = "".join(
        f'<li><span class="n">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(P.PROCESS)
    )
    return f"""<section class="section alt"><div class="wrap">
<p class="eyebrow">How it works</p><h2 class="sec-title">From drawing to delivery in 4 steps</h2>
<ol class="process">{steps}</ol></div></section>"""


def why_html():
    items = "".join(
        f'<div class="why">{icon("check", "ic tick")}<div><h3>{t}</h3><p>{d}</p></div></div>'
        for t, d in P.WHY_US
    )
    return f"""<section class="section"><div class="wrap">
<p class="eyebrow">Why Reliable Steel Weld</p><h2 class="sec-title">Reliable is not just our name</h2>
<div class="grid why-grid">{items}</div></div></section>"""


def page_hero(rel, crumbs, h1, lead, kicker):
    return f"""<section class="page-hero"><div class="wrap">
{breadcrumbs_html(rel, crumbs)}
<p class="eyebrow">{kicker}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="hero-btns"><a class="btn btn-primary" href="{rel}contact/">Request a Quote {icon('arrow')}</a>
<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG} Send Drawing on WhatsApp</a></div>
</div></section>"""


def write(path, content):
    full = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_home():
    rel = ""
    schemas = [business_schema(), {
        "@context": "https://schema.org", "@type": "WebSite", "name": C.BUSINESS_NAME, "url": url(""),
    }, faq_schema(P.HOME_FAQS)]
    inds = "".join(f"<li>{i}</li>" for i in P.INDUSTRIES)
    areas = "".join(f"<li>{a}</li>" for a in P.AREAS)
    loc_cards = "".join(
        f'<a class="card loc" href="{l["slug"]}/">{icon("pin")}<h3>CNC Plasma Profile Cutting in {l["place"]}</h3><p>{l["intro"]}</p><span class="more">View {icon("arrow")}</span></a>'
        for l in P.LOCATIONS
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow light">Taloja MIDC · Panvel · Mumbai</p>
      <h1>CNC Plasma Cutting Job Work &amp; <span>Complete Fabrication Solutions</span></h1>
      <p class="lead">Reliable Steel Weld delivers precise <strong>CNC plasma cutting</strong>, <strong>CNC profile cutting</strong>, <strong>MS &amp; SS plate cutting</strong> and <strong>CNC machining job work</strong> — plus complete fabrication, erection &amp; civil work — for industries across Maharashtra.</p>
      <div class="hero-btns">
        <a class="btn btn-primary" href="contact/">Get a Free Quote {icon('arrow')}</a>
        <a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp Your Drawing</a>
      </div>
      <ul class="hero-points">
        <li>{icon('check','ic tick')} Cut to your DXF / drawing</li>
        <li>{icon('check','ic tick')} Single parts to bulk batches</li>
        <li>{icon('check','ic tick')} On-time delivery</li>
      </ul>
    </div>
    <div class="hero-art" aria-hidden="true">
      <svg viewBox="0 0 400 360" class="plate-svg">
        <defs>
          <linearGradient id="pl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5b5f66"/><stop offset="1" stop-color="#2f3237"/></linearGradient>
          <radialGradient id="spark" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#ffd24a"/><stop offset="1" stop-color="#ff5a1f" stop-opacity="0"/></radialGradient>
        </defs>
        <rect x="20" y="60" width="360" height="260" rx="6" fill="url(#pl)"/>
        <g fill="none" stroke="#1b1c1f" stroke-width="3">
          <circle cx="120" cy="150" r="54"/><circle cx="120" cy="150" r="20"/>
          <circle cx="120" cy="104" r="6"/><circle cx="120" cy="196" r="6"/><circle cx="74" cy="150" r="6"/><circle cx="166" cy="150" r="6"/>
          <path d="M220 100h120v60l-40 40h-80z"/><circle cx="250" cy="130" r="8"/>
          <path d="M60 240h110l30 50H60z"/>
        </g>
        <path class="cut-path" d="M230 250 h110 v50 h-110 z" fill="none" stroke="#ffb03a" stroke-width="3"/>
        <circle class="spark" cx="340" cy="250" r="22" fill="url(#spark)"/>
        <g class="torch"><rect x="332" y="170" width="16" height="60" rx="3" fill="#b5cf1e"/><rect x="336" y="228" width="8" height="14" fill="#ddd"/></g>
      </svg>
    </div>
  </div>
</section>

<section class="stats">
  <div class="wrap stats-in">
    <div><strong>CNC</strong><span>Plasma &amp; profile cutting</span></div>
    <div><strong>MS · SS</strong><span>Light to heavy plates</span></div>
    <div><strong>360°</strong><span>Cut · Machine · Fabricate · Erect</span></div>
    <div><strong>MMR</strong><span>Taloja, Panvel, Navi Mumbai, Mumbai</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Our services</p>
    <h2 class="sec-title">CNC Cutting, Machining &amp; Fabrication Job Work Services</h2>
    <p class="sec-lead">One reliable partner for every stage — from cutting your first plate to erecting the finished structure.</p>
    {service_cards(rel)}
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <div>
      <p class="eyebrow">About us</p>
      <h2 class="sec-title">Complete solution provider for fabrication, erection &amp; civil work</h2>
      <p>{C.ABOUT_PARAGRAPHS[0]}</p>
      <p>{C.ABOUT_PARAGRAPHS[1]}</p>
      <a class="btn btn-outline" href="about/">More about RSW {icon('arrow')}</a>
    </div>
    <div class="about-logo"><img src="assets/img/rsw-logo-full.jpg" alt="Reliable Steel Weld - Complete Solution Provider For Fabrication, Erection &amp; Civil Work" width="1200" height="638" loading="lazy"></div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow prose">
    <p class="eyebrow">CNC plasma cutting in Maharashtra</p>
    <h2 class="sec-title">Your CNC plasma cutting job work provider near Mumbai</h2>
    <p>If you are searching for <strong>CNC plasma cutting services near me</strong> or <strong>CNC plasma profile cutting job work in Mumbai, Taloja MIDC or Panvel</strong>, Reliable Steel Weld is right where you need us. Our Taloja MIDC workshop cuts <a href="ms-plate-cutting-job-work/">MS plates, SS plates and heavy structural plates</a> into flanges, base plates, gussets, brackets and any custom profile from your drawing.</p>
    <p>We are more than a cutting shop. As a <a href="cnc-cutting-job-work-for-fabricators/">CNC cutting job work partner for fabricators</a>, we also offer <a href="cnc-machining-job-work/">CNC turning and milling job work</a>, <a href="cnc-laser-cutting-job-work/">CNC laser cutting job work contracts</a> and full <a href="fabrication-erection-civil-work/">fabrication, erection and civil work</a> — so your parts arrive ready to use.</p>
  </div>
</section>

{why_html()}
{process_html()}

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Service areas</p>
    <h2 class="sec-title">CNC plasma profile cutting job work near you</h2>
    <div class="grid cards three">{loc_cards}</div>
    <ul class="chips">{areas}</ul>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="eyebrow">Industries</p>
    <h2 class="sec-title">Industries we serve</h2>
    <ul class="chips big">{inds}</ul>
  </div>
</section>

{faq_html(P.HOME_FAQS)}
"""
    write("", head(P.HOME["title"], P.HOME["description"], "", rel, schemas) + header(rel, "home") + body + footer(rel))


def build_service(s):
    rel = "../"
    path = s["slug"] + "/"
    crumbs_schema = [("Home", ""), (s["nav"], path)]
    schemas = [
        business_schema(),
        service_schema(s["h1"], s["description"], path),
        breadcrumb_schema(crumbs_schema),
        faq_schema(s["faqs"]),
    ]
    sections = "".join(
        f'<h2>{h}</h2>{b.replace("{rel}", rel)}' for h, b in s["sections"]
    )
    toc = "".join(f'<li><a href="#s{i}">{h}</a></li>' for i, (h, _) in enumerate(s["sections"]))
    # Add ids to h2s for the table of contents.
    for i, (h, _) in enumerate(s["sections"]):
        sections = sections.replace(f"<h2>{h}</h2>", f'<h2 id="s{i}">{h}</h2>', 1)
    body = f"""
{page_hero(rel, [("Home", ""), (s["nav"], path)], s["h1"], s["lead"], "Services")}
<section class="section">
  <div class="wrap with-aside">
    <article class="prose">{sections}</article>
    <aside class="aside">
      <div class="aside-box">
        <h2 class="aside-h">On this page</h2>
        <ul class="toc">{toc}</ul>
      </div>
      <div class="aside-box quote-box">
        <h2 class="aside-h">Get a quick quote</h2>
        <p>Send drawing, material, thickness &amp; quantity.</p>
        <a class="btn btn-wa block" href="{wa_link('Hello RSW, I need a quote for ' + s['nav'] + '.')}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>
        <a class="btn btn-primary block" href="tel:{C.PHONE_E164}">{icon('phone')} {C.PHONE_DISPLAY}</a>
      </div>
    </aside>
  </div>
</section>
{process_html()}
{faq_html(s["faqs"])}
<section class="section alt"><div class="wrap">
<h2 class="sec-title">Related services</h2>
{service_cards(rel, exclude=s["slug"])}
</div></section>
"""
    write(s["slug"], head(s["title"], s["description"], path, rel, schemas) + header(rel, s["slug"]) + body + footer(rel))


def build_location(l):
    rel = "../"
    path = l["slug"] + "/"
    crumbs = [("Home", ""), (f"CNC Plasma Cutting {l['place']}", path)]
    faqs = [
        (f"Do you provide CNC plasma profile cutting job work in {l['place']}?",
         f"Yes. Reliable Steel Weld is a CNC plasma profile cutting job work provider for {l['place']}, operating from our workshop in Taloja MIDC, Navi Mumbai."),
        (f"How fast can you deliver cut parts to {l['place']}?",
         "Delivery depends on quantity and complexity. Urgent breakdown jobs get priority. Share your drawing for a committed delivery date."),
        ("What materials do you cut?",
         "Mild steel (MS), stainless steel (SS) and other conductive metal plates, from thin sheet to heavy plate."),
    ]
    schemas = [
        business_schema(),
        service_schema(l["h1"], l["description"], path, area={"@type": "Place", "name": l["place"]}),
        breadcrumb_schema(crumbs),
        faq_schema(faqs),
    ]
    nearby = "".join(f"<li>{n}</li>" for n in l["nearby"])
    others = " · ".join(
        f'<a href="{rel}{o["slug"]}/">CNC plasma cutting in {o["place"]}</a>' for o in P.LOCATIONS if o is not l
    )
    body = f"""
{page_hero(rel, crumbs, l["h1"], l["intro"], "Service area · " + l["place"])}
<section class="section">
  <div class="wrap with-aside">
    <article class="prose">
      <h2>CNC Plasma Cutting Services in {l['place']}</h2>
      {l['body']}
      <h2>Job Work We Offer in {l['place']}</h2>
      <ul class="ticks">
        <li><a href="{rel}cnc-plasma-cutting-job-work/">CNC plasma cutting job work</a> &amp; industrial plasma cutting services</li>
        <li><a href="{rel}cnc-profile-cutting-services/">CNC profile cutting job work</a> &amp; custom metal profile cutting</li>
        <li><a href="{rel}ms-plate-cutting-job-work/">MS plate plasma cutting</a>, MS SS plate cutting &amp; heavy plate cutting job work</li>
        <li><a href="{rel}cnc-machining-job-work/">CNC machining job work</a> — turning, milling &amp; lathe work</li>
        <li><a href="{rel}cnc-cutting-job-work-for-fabricators/">CNC cutting job work for fabricators</a></li>
        <li><a href="{rel}fabrication-erection-civil-work/">Fabrication, erection &amp; civil work</a></li>
      </ul>
      <h2>Areas Covered Around {l['place']}</h2>
      <ul class="chips">{nearby}</ul>
      <p>Also see: {others}</p>
    </article>
    <aside class="aside">
      <div class="aside-box quote-box">
        <h2 class="aside-h">Job work in {l['place']}?</h2>
        <p>Send your drawing and get a quote.</p>
        <a class="btn btn-wa block" href="{wa_link('Hello RSW, I need CNC plasma cutting job work in ' + l['place'] + '.')}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>
        <a class="btn btn-primary block" href="tel:{C.PHONE_E164}">{icon('phone')} {C.PHONE_DISPLAY}</a>
      </div>
      <div class="map-box"><iframe title="Reliable Steel Weld location map" src="{C.MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </aside>
  </div>
</section>
{why_html()}
{faq_html(faqs)}
"""
    write(l["slug"], head(l["title"], l["description"], path, rel, schemas) + header(rel, l["slug"]) + body + footer(rel))


def build_about():
    rel = "../"
    path = "about/"
    crumbs = [("Home", ""), ("About Us", path)]
    schemas = [business_schema(), breadcrumb_schema(crumbs), {
        "@context": "https://schema.org", "@type": "AboutPage", "name": P.ABOUT["title"], "url": url(path),
        "about": {"@id": url("#business")},
    }]
    paras = "".join(f"<p>{p}</p>" for p in C.ABOUT_PARAGRAPHS)
    initials = "".join(w[0] for w in C.OWNER_NAME.split()[:2]).upper()
    body = f"""
{page_hero(rel, crumbs, "About Reliable Steel Weld", C.TAGLINE + ".", "About us")}
<section class="section">
  <div class="wrap split">
    <div class="prose">
      <h2>Who We Are</h2>
      {paras}
    </div>
    <div class="about-logo"><img src="{rel}assets/img/rsw-logo-full.jpg" alt="Reliable Steel Weld logo and tagline" width="1200" height="638" loading="lazy"></div>
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow">
    <div class="owner">
      <div class="owner-avatar" aria-hidden="true">{initials}</div>
      <div>
        <p class="eyebrow">Leadership</p>
        <h2 class="owner-name">{C.OWNER_NAME}</h2>
        <p class="owner-title">{C.OWNER_TITLE}, Reliable Steel Weld</p>
        <blockquote>“{C.OWNER_MESSAGE}”</blockquote>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 class="sec-title">What We Do</h2>
    {service_cards(rel)}
  </div>
</section>
{why_html()}
"""
    write("about", head(P.ABOUT["title"], P.ABOUT["description"], path, rel, schemas) + header(rel, "about") + body + footer(rel))


def build_contact():
    rel = "../"
    path = "contact/"
    crumbs = [("Home", ""), ("Contact", path)]
    schemas = [business_schema(), breadcrumb_schema(crumbs), {
        "@context": "https://schema.org", "@type": "ContactPage", "name": P.CONTACT["title"], "url": url(path),
    }]
    options = "".join(f"<option>{s['nav']}</option>" for s in P.SERVICES)
    body = f"""
{page_hero(rel, crumbs, "Contact Reliable Steel Weld", "Send your drawing and requirement — we will reply with a quotation quickly.", "Get a quote")}
<section class="section">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <h2>Reach us</h2>
      <ul class="c-list">
        <li>{icon('pin')}<div><strong>Workshop</strong><span>{C.STREET}, {C.LOCALITY}, {C.CITY}, {C.REGION} {C.POSTAL_CODE}</span></div></li>
        <li>{icon('phone')}<div><strong>Phone</strong><a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a></div></li>
        <li>{WA_SVG}<div><strong>WhatsApp</strong><a href="{wa_link()}" target="_blank" rel="noopener">Chat &amp; send drawings</a></div></li>
        <li>{icon('mail')}<div><strong>Email</strong><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></div></li>
        <li>{icon('clock')}<div><strong>Working hours</strong><span>{C.HOURS}</span></div></li>
      </ul>
      <div class="map-box tall"><iframe title="Reliable Steel Weld on Google Maps" src="{C.MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
    <form class="quote-form" id="quote-form" data-wa="{C.WHATSAPP_E164}" data-email="{C.EMAIL}" novalidate>
      <h2>Request a quote</h2>
      <p class="form-note">Fill the form and send it to us on WhatsApp or email. Attach your drawing in the chat.</p>
      <label>Your name<input name="name" required autocomplete="name"></label>
      <label>Company<input name="company" autocomplete="organization"></label>
      <label>Phone<input name="phone" type="tel" required autocomplete="tel"></label>
      <label>Service<select name="service">{options}</select></label>
      <div class="row2">
        <label>Material<select name="material"><option>MS (Mild Steel)</option><option>SS (Stainless Steel)</option><option>Aluminium</option><option>Other</option></select></label>
        <label>Thickness / size<input name="thickness" placeholder="e.g. 12 mm"></label>
      </div>
      <label>Quantity<input name="qty" placeholder="e.g. 50 pcs"></label>
      <label>Requirement details<textarea name="msg" rows="4" placeholder="Describe the parts, delivery location and timeline"></textarea></label>
      <p class="form-error" role="alert" hidden>Please enter your name and phone number.</p>
      <div class="form-btns">
        <button class="btn btn-wa" type="submit" name="via" value="wa">{WA_SVG} Send on WhatsApp</button>
        <button class="btn btn-outline" type="submit" name="via" value="email">{icon('mail')} Send by Email</button>
      </div>
    </form>
  </div>
</section>
"""
    write("contact", head(P.CONTACT["title"], P.CONTACT["description"], path, rel, schemas) + header(rel, "contact") + body + footer(rel))


def build_404():
    rel = "/"  # 404 is served from any path, so use root-relative links
    body = f"""
<section class="page-hero"><div class="wrap narrow center">
<p class="eyebrow">Error 404</p><h1>Page not found</h1>
<p class="lead">The page you are looking for has moved. Try our services below.</p>
<a class="btn btn-primary" href="/">Go to Home</a></div></section>
<section class="section"><div class="wrap">{service_cards(rel)}</div></section>
"""
    html_doc = head("Page Not Found | Reliable Steel Weld", "Page not found.", "404.html", rel, []).replace(
        'content="index, follow, max-image-preview:large"', 'content="noindex"') + header(rel, "") + body + footer(rel)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)


def build_sitemap():
    paths = [("", "1.0")] + [(s["slug"] + "/", "0.9") for s in P.SERVICES] + \
            [(l["slug"] + "/", "0.8") for l in P.LOCATIONS] + [("about/", "0.6"), ("contact/", "0.7")]
    urls = "".join(
        f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in paths
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /build/\n\nSitemap: {url('sitemap.xml')}\n")


def main():
    build_home()
    for s in P.SERVICES:
        build_service(s)
    for l in P.LOCATIONS:
        build_location(l)
    build_about()
    build_contact()
    build_404()
    build_sitemap()
    print(f"Built {1 + len(P.SERVICES) + len(P.LOCATIONS) + 3} pages into {ROOT}")


if __name__ == "__main__":
    main()
