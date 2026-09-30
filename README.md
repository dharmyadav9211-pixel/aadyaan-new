# Reliable Steel Weld — Website

Static, SEO-optimised website for **Reliable Steel Weld (RSW)** — CNC plasma cutting, profile cutting, plate cutting, CNC machining and fabrication, erection & civil work in Taloja MIDC, Panvel & Mumbai.

## Edit & rebuild
1. Put the real business details (owner name, phone, WhatsApp, email, address, domain) in `build/config.py` — every `TODO` there is a placeholder.
2. Page text lives in `build/pages.py`.
3. Run `python3 build/build.py` — it regenerates all HTML pages, `sitemap.xml` and `robots.txt`.

Do not hand-edit the generated `index.html` files; they are overwritten on every build.

## Keyword → page map
| Page | Target keywords |
|---|---|
| `/` | CNC plasma cutting job work, CNC plasma cutting services near me, CNC plasma profile cutting (all clusters linked) |
| `/cnc-plasma-cutting-job-work/` | CNC Plasma Cutting Job Work, CNC Plasma Cutting Services, Plasma Cutting Job Work, CNC Plasma Profile Cutting, Industrial Plasma Cutting Services, Plasma Cutting Services near me, CNC Plasma Cutting Service in Maharashtra, Fabrication Job Work CNC Plasma Cutting |
| `/cnc-profile-cutting-services/` | CNC Profile Cutting Job Work, CNC Profile Cutting Services, CNC profile cutting provider, Metal Profile Cutting Services, Custom Metal Profile Cutting |
| `/ms-plate-cutting-job-work/` | MS Plate Plasma Cutting Job Work, MS Plate Cutting Job Work near me, Steel Plate Cutting Job Work, CNC Plate Cutting Job Work, Heavy Plate Cutting Job Work, MS SS Plate Cutting Job Work, Structural Steel Cutting Job Work |
| `/cnc-machining-job-work/` | CNC machining service near me, CNC machining job work services, CNC turning and milling job work, 5-axis CNC machining job work, CNC lathe machine job work, CNC job works for aluminum components, Automotive CNC machine shop, Custom CNC manufacturing shop, CNC job work provider near me |
| `/cnc-laser-cutting-job-work/` | CNC laser cutting job work contract |
| `/cnc-cutting-job-work-for-fabricators/` | CNC Cutting Job Work for Fabricators, Engineering Job Work CNC Cutting |
| `/fabrication-erection-civil-work/` | Fabrication, erection & civil work (brand tagline) |
| `/cnc-plasma-cutting-taloja-midc/` | CNC Plasma profile Cutting Job Work provider in Taloja MIDC |
| `/cnc-plasma-cutting-panvel/` | CNC Plasma profile Cutting Job Work provider in Panvel |
| `/cnc-plasma-cutting-mumbai/` | CNC Plasma profile Cutting Job Work provider in Mumbai |

## On-page SEO included
Unique title + meta description per page, one keyword H1, keyword H2s, canonical URLs, Open Graph tags, LocalBusiness / Service / FAQPage / BreadcrumbList JSON-LD schema, geo meta tags, internal linking, breadcrumbs, `sitemap.xml`, `robots.txt`, image alt text, mobile-first responsive layout, and no heavy libraries.

## Hosting
Pure static files — works on GitHub Pages (Settings → Pages → deploy from this branch, root), Netlify, Vercel or any hosting. After going live, submit `sitemap.xml` in Google Search Console and create or verify the Google Business Profile with the **same** name, address and phone.
