"""
Business details for the Reliable Steel Weld website.

>>> EDIT THIS FILE, then run:  python3 build/build.py  <<<

Every value marked TODO is a placeholder. Replace it with the real detail
from the brochure / owner before the site goes live — Google uses the
name, address and phone (NAP) on every page for local SEO, so they must be
exact and identical to the Google Business Profile.
"""

# Live domain, no trailing slash. Used for canonical URLs, sitemap and schema.
SITE_URL = "https://www.reliablesteelweld.com"  # TODO: real domain

BUSINESS_NAME = "Reliable Steel Weld"
SHORT_NAME = "RSW"
TAGLINE = "Complete Solution Provider For Fabrication, Erection & Civil Work"

OWNER_NAME = "Owner Name"            # TODO: from brochure
OWNER_TITLE = "Founder & Proprietor"  # TODO: from brochure

PHONE_DISPLAY = "+91 98XXX XXXXX"   # TODO
PHONE_E164 = "+9198XXXXXXXX"         # TODO: digits only with country code, used in tel: links
WHATSAPP_E164 = "9198XXXXXXXX"       # TODO: digits only, no +, used in wa.me links
EMAIL = "info@reliablesteelweld.com" # TODO

STREET = "Plot No. XX, Taloja MIDC"  # TODO: exact plot / gala number
LOCALITY = "Taloja, Navi Mumbai"
CITY = "Panvel"
REGION = "Maharashtra"
POSTAL_CODE = "410208"
COUNTRY = "IN"
# Approximate centre of Taloja MIDC — replace with the exact pin of the workshop.
GEO_LAT = 19.0633
GEO_LNG = 73.1233
# Google Maps embed "src" URL (Maps > Share > Embed a map). Leave as is for a
# generic Taloja MIDC map.
MAP_EMBED = "https://www.google.com/maps?q=Taloja+MIDC,+Navi+Mumbai&output=embed"

HOURS = "Mon – Sat, 9:00 AM – 7:00 PM"
HOURS_SCHEMA = ["Mo-Sa 09:00-19:00"]

GSTIN = ""  # optional, shown in footer when filled

# About-us text from the brochure. Each string is one paragraph.
ABOUT_PARAGRAPHS = [
    "Reliable Steel Weld (RSW) is an engineering job-work company based in Taloja MIDC, "
    "Navi Mumbai, providing CNC plasma cutting, CNC profile cutting, CNC machining and "
    "complete fabrication, erection and civil work for industries across Mumbai, Panvel "
    "and Maharashtra.",
    "We started with one simple promise that is in our name — to be reliable. Accurate "
    "cutting to your drawing, honest pricing, and delivery on the date we commit. Today "
    "fabricators, OEMs, contractors and plant maintenance teams trust us for everything "
    "from a single custom profile to bulk production batches of MS and SS plate parts.",
    "Because cutting, machining, fabrication and site erection are handled by one team, "
    "our customers get a single point of responsibility — from the DXF file to the "
    "finished structure standing on site.",
]
OWNER_MESSAGE = (
    "Our customers run tight production schedules. When they send us a drawing, they "
    "need the parts right the first time and on time. That is the standard every person "
    "at Reliable Steel Weld works to."
)

SOCIAL = {
    # "facebook": "https://facebook.com/...",
    # "instagram": "https://instagram.com/...",
    # "linkedin": "https://linkedin.com/company/...",
    # "youtube": "https://youtube.com/@...",
}
