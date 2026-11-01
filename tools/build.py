#!/usr/bin/env python3
"""Builds the ANC Painting website into ../public.

Edit the SETTINGS block, then run:  python3 tools/build.py
Everything in public/ is what Netlify publishes.
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")

# ───────────────────────── SETTINGS ─────────────────────────
SITE = "https://ancpaintingct.com"
NAME = "ANC Painting"
LEGAL = "ANC Painting LLC"
PHONE = "+14016606025"
PHONE_DISPLAY = "(401) 660-6025"
EMAIL = ""                       # e.g. "nick@ancpaintingct.com" once email is set up
HIC = ""                         # e.g. "HIC.0712345" — REQUIRED before going live
GOOGLE_ADS_ID = ""               # e.g. "AW-123456789"
GOOGLE_ADS_CONVERSION = ""       # e.g. "AW-123456789/AbCdEfGh" (quote form conversion)
CLARITY_ID = ""                  # e.g. "abc123xyz"
GBP_URL = ""                     # Google Business Profile link, e.g. "https://maps.google.com/?cid=..."
HOME_TOWN = "Coventry"
HOME_ZIP = "06238"
# ─────────────────────────────────────────────────────────────

HIC_TEXT = HIC if HIC else "[PENDING]"

TOWNS = [
  # (name, slug, county, local line)
  ("West Hartford", "west-hartford", "Hartford County", "From the colonials and Tudors around Blue Back Square to the capes off Farmington Avenue, West Hartford homes deserve sharp trim lines and paint that lasts."),
  ("Glastonbury", "glastonbury", "Hartford County", "Glastonbury has everything from historic South Glastonbury homes near the river to newer colonials, and older wood siding needs careful prep before it sees a brush."),
  ("Wethersfield", "wethersfield", "Hartford County", "Old Wethersfield is one of the oldest historic districts in Connecticut, and homes here reward painters who take their time on prep, caulk and trim."),
  ("Newington", "newington", "Hartford County", "Newington is full of well-kept capes, ranches and split-levels where a fresh interior or a clean exterior repaint makes a big difference."),
  ("Rocky Hill", "rocky-hill", "Hartford County", "From neighborhoods near the river and the old ferry landing to newer developments, Rocky Hill homeowners want painters who show up on time and leave the place spotless."),
  ("Manchester", "manchester", "Hartford County", "Manchester's older mill-era homes and its newer neighborhoods both need the right primer and prep, especially on weathered wood siding and trim."),
  ("South Windsor", "south-windsor", "Hartford County", "South Windsor's colonials and farmhouse-style homes see plenty of sun and New England winters, so exterior prep and quality paint really matter here."),
  ("New Britain", "new-britain", "Hartford County", "The Hardware City has beautiful older homes, from multi-families to the larger houses near Walnut Hill Park, and many are ready for careful interior and exterior work."),
  ("Berlin", "berlin", "Hartford County", "In Berlin and Kensington we paint everything from classic capes to newer colonials, inside and out."),
  ("Plainville", "plainville", "Hartford County", "Plainville homeowners get the same careful prep, clean lines and Benjamin Moore paint we bring to every job."),
  ("Southington", "southington", "Hartford County", "Southington has a big mix of older homes downtown and newer neighborhoods on the hills, and we handle both interior and exterior work."),
  ("Farmington", "farmington", "Hartford County", "Farmington's historic village homes and Unionville neighborhoods call for painters who respect the details, especially on older trim and siding."),
  ("Avon", "avon", "Hartford County", "Avon homes, from the valley up toward Avon Mountain, are often larger with lots of trim, which is exactly where careful cutting-in shows."),
  ("Cromwell", "cromwell", "Middlesex County", "Cromwell sits right on the Connecticut River, and river-town humidity is hard on exterior paint, so good prep and the right product are key."),
  ("Coventry", "coventry", "Tolland County", "Coventry is home base for ANC Painting. We live here, so painting for our neighbors around Coventry Lake is personal."),
  ("Mansfield", "mansfield", "Tolland County", "From Storrs and the UConn area to Mansfield Center, we paint homes, rentals and condos with the same care we'd give our own."),
  ("Tolland", "tolland", "Tolland County", "Tolland's colonials and older homes around the historic Tolland Green are a short drive from home base, so scheduling is easy."),
  ("Vernon", "vernon", "Tolland County", "Vernon and Rockville have plenty of older homes with detailed trim, plus newer neighborhoods, and we paint both inside and out."),
  ("Bolton", "bolton", "Tolland County", "Bolton is right next door to our home base, and its homes near Bolton Lake and along the notch see a lot of weather, so exterior prep matters."),
  ("Hebron", "hebron", "Tolland County", "Hebron is where we repainted the clubhouse at Blackledge Country Club, and we'd love to do your home next."),
]

SERVICES = [
  ("interior-painting", "Interior Painting", "Walls, ceilings, trim and doors with crisp lines and a spotless cleanup.",
   ["Walls, ceilings, trim, doors and closets", "Patching nail holes and small drywall repairs before painting", "Furniture moved and floors covered before we start", "Benjamin Moore paint, with color help if you want it", "A full clean-up and walk-through when we finish"]),
  ("exterior-painting", "Exterior Painting", "Scraping, priming and painting built to hold up through New England winters.",
   ["Siding, trim, doors, shutters and porches", "Washing, scraping and sanding loose paint", "Caulking gaps and priming bare wood", "Benjamin Moore exterior paint", "Landscaping and walkways protected while we work"]),
  ("cabinet-refinishing", "Cabinet Refinishing", "A kitchen that looks brand new for a fraction of the cost of new cabinets.",
   ["Kitchen and bathroom cabinets, vanities and built-ins", "Cleaning and degreasing so the finish actually sticks", "Sanding and priming for a smooth, durable base", "A hard-wearing cabinet finish in the color you choose", "Your kitchen protected and kept usable as much as possible"]),
]

esc = html.escape

def tracking_head():
    out = []
    if CLARITY_ID:
        out.append('<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");</script>' % CLARITY_ID)
    if GOOGLE_ADS_ID:
        out.append('<!-- Google tag (gtag.js) -->\n<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag(\'js\', new Date());\n  gtag(\'config\', \'%s\');\n</script>' % (GOOGLE_ADS_ID, GOOGLE_ADS_ID))
    return "\n".join(out)

def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "HousePainter",
        "@id": SITE + "/#business",
        "name": NAME,
        "legalName": LEGAL,
        "description": "Family-owned interior, exterior and cabinet painting company based in Coventry, CT, serving the greater Hartford and New Britain areas. Benjamin Moore paints. Free, no-pressure quotes.",
        "url": SITE + "/",
        "logo": SITE + "/assets/logo.svg",
        "image": SITE + "/assets/blackledge-after.jpg",
        "telephone": PHONE,
        "address": {"@type": "PostalAddress", "addressLocality": HOME_TOWN, "addressRegion": "CT", "postalCode": HOME_ZIP, "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": t[0] + ", CT"} for t in TOWNS],
        "knowsAbout": ["Interior painting", "Exterior painting", "Cabinet refinishing", "Benjamin Moore paint"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    }
    if EMAIL: data["email"] = EMAIL
    if GBP_URL:
        data["hasMap"] = GBP_URL
        data["sameAs"] = [GBP_URL]
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2) + '\n</script>'

def head(title, desc, path, noindex=False, extra=""):
    canon = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
{tracking_head()}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{canon}">
  {'<meta name="robots" content="noindex">' if (noindex or not HIC) else ''}
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/assets/blackledge-after.jpg">
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <script defer src="/script.js"></script>
{schema()}
{extra}
</head>
<body>
"""

def header():
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="/" aria-label="{NAME} home">
        <span class="brand-mark" aria-hidden="true"><span>A</span><span class="brand-dot"></span><span>N</span><span class="brand-dot"></span><span>C</span></span>
        <span class="brand-sub" aria-hidden="true">PAINTING</span>
      </a>
      <nav class="nav" aria-label="Main">
        <a class="nav-link" href="/interior-painting/">Interior</a>
        <a class="nav-link" href="/exterior-painting/">Exterior</a>
        <a class="nav-link" href="/cabinet-refinishing/">Cabinets</a>
        <a class="nav-link" href="/about/">About</a>
        <a class="nav-link" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
        <a class="btn btn-sm" href="#quoteFormWrap">Free Quote</a>
      </nav>
    </div>
  </header>
"""

def footer():
    towns = "\n".join(f'          <a href="/{t[1]}-ct-painters/">{t[0]}</a>' for t in TOWNS)
    email = f' &bull; <a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL else ""
    reviews = f'<a href="{GBP_URL}" target="_blank" rel="noopener">Google reviews</a>' if GBP_URL else ""
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div>
          <div class="footer-brand">A·N·C PAINTING</div>
          <p style="margin:6px 0 10px">Family-owned painting company · {HOME_TOWN}, CT</p>
          <a href="tel:{PHONE}">{PHONE_DISPLAY}</a>{email}
          <p style="margin:10px 0 0">CT HIC # {HIC_TEXT}</p>
        </div>
        <div>
          <p style="margin:0 0 8px;color:#fff;font-weight:600">Services</p>
          <div class="foot-nav" style="flex-direction:column;gap:6px">
            <a href="/interior-painting/">Interior painting</a>
            <a href="/exterior-painting/">Exterior painting</a>
            <a href="/cabinet-refinishing/">Cabinet refinishing</a>
            <a href="/about/">About us</a>
            {reviews}
          </div>
        </div>
        <div>
          <p style="margin:0 0 8px;color:#fff;font-weight:600">Towns we serve</p>
          <div class="foot-nav">
{towns}
          </div>
        </div>
      </div>
      <p class="foot-legal">© {LEGAL} · CT HIC # {HIC_TEXT} · By submitting a quote request you agree to be contacted about your project. We never sell your info.</p>
    </div>
  </footer>
</body>
</html>
"""

def town_options(selected=""):
    opts = ['<option value="">Choose your town</option>']
    for t in TOWNS:
        sel = ' selected' if t[0] == selected else ''
        opts.append(f'<option{sel}>{t[0]}</option>')
    opts.append('<option>Other town</option>')
    return "".join(opts)

def quote_form(page_label, town="", service=""):
    svc_opts = "".join(f'<option{" selected" if s[1]==service else ""}>{s[1]}</option>' for s in SERVICES)
    return f"""        <div class="hero-card" id="quoteFormWrap">
          <h2 class="form-title">Get a free quote</h2>
          <p class="muted" style="font-size:15px;margin:0">No pressure. We'll text you two times that work for a quick look at the job.</p>
          <form id="quoteForm" name="anc-quote" method="POST" action="/success/" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data" novalidate>
            <input type="hidden" name="form-name" value="anc-quote">
            <input type="hidden" name="Page" value="{esc(page_label)}">
            <p class="hidden"><label>Do not fill this out: <input name="bot-field"></label></p>
            <div class="simple-form">
              <label>Your name *
                <input name="Full name" id="name" required placeholder="Jane Doe" autocomplete="name">
              </label>
              <div class="contact-or">
                <label>Phone
                  <input name="Phone" id="phone" type="tel" placeholder="(555) 555-5555" autocomplete="tel">
                </label>
                <div class="or-divider">or</div>
                <label>Email
                  <input name="Email" id="email" type="email" placeholder="jane@example.com" autocomplete="email">
                </label>
              </div>
              <p class="contact-hint">We just need one way to reach you. Texts are easiest.</p>
              <label>What needs painting?
                <select name="Service" id="service"><option value="">Choose one</option>{svc_opts}<option>More than one / not sure</option></select>
              </label>
              <label>Your town
                <select name="Town" id="town">{town_options(town)}</select>
              </label>
              <details class="more">
                <summary>Add details or photos <span>(optional, speeds up your quote)</span></summary>
                <div class="more-fields">
                  <label>Tell us about the job
                    <textarea name="Details" id="details" placeholder="Example: living room and hallway, walls and trim, light gray"></textarea>
                  </label>
                  <label>Photos of the area
                    <input type="file" name="Photo" id="photo" accept="image/*">
                  </label>
                </div>
              </details>
              <label class="consent-row">
                <input type="checkbox" id="consent" name="Consent to contact" value="Yes" required>
                I agree to be contacted by text, call or email about my painting quote.
              </label>
            </div>
            <div id="formError" class="form-error hidden" role="alert"></div>
            <button type="submit" class="btn btn-lg btn-full" id="submitQuote">Get My Free Quote</button>
            <p class="form-note">Free, written quote. No payment, no obligation.</p>
          </form>
        </div>
"""

def trust_bar():
    return """    <div class="trust-bar">
      <div class="container trust-bar-inner">
        <div class="trust-item"><strong>Family-owned</strong><span>Arella, Nick, Callie &amp; Carson</span></div>
        <div class="trust-item"><strong>Benjamin Moore</strong><span>Quality paint on every job</span></div>
        <div class="trust-item"><strong>Free quotes</strong><span>Written, no pressure</span></div>
        <div class="trust-item"><strong>On time</strong><span>We show up when we say</span></div>
      </div>
    </div>
"""

def before_after(caption=True):
    cap = '<p class="ba-caption">Clubhouse exterior at Blackledge Country Club, Hebron CT, before and after repainting.</p>' if caption else ""
    return f"""        <div class="ba">
          <figure><img src="/assets/blackledge-before.jpg" alt="Blackledge Country Club clubhouse in Hebron CT before repainting, faded siding" loading="lazy" width="1400" height="1050"><figcaption>Before</figcaption></figure>
          <figure class="after"><img src="/assets/blackledge-after.jpg" alt="Blackledge Country Club clubhouse in Hebron CT after exterior repainting by ANC Painting" loading="lazy" width="1400" height="1050"><figcaption>After</figcaption></figure>
        </div>
        {cap}
"""


def interior_ba():
    items = [("living-room-before.jpg","Before","Living room before painting, with orange and cream walls and stained wood trim"),
             ("living-room-prep.jpg","Prep","Same living room during prep: floors covered, walls patched and sanded smooth"),
             ("living-room-after.jpg","After","Same living room after painting: soft blue walls and crisp white trim")]
    figs = "\n".join(f'          <figure class="{"after" if l=="After" else ""}"><img src="/assets/{f}" alt="{esc(a)}" loading="lazy" width="1400" height="1050"><figcaption>{l}</figcaption></figure>' for f, l, a in items)
    return f"""        <div class="ba ba-3">
{figs}
        </div>
        <p class="ba-caption">Living room: dated orange walls and stained trim, patched and smoothed, then finished in a soft blue with the trim painted white.</p>
"""

GALLERY = [
  ("blackledge-golf-shop.jpg", "Golf shop at Blackledge Country Club in Hebron CT after exterior painting"),
  ("blackledge-gable.jpg", "Tall gable wall and window trim repainted at Blackledge Country Club, Hebron CT"),
  ("blackledge-tavern.jpg", "Blackledge River Tavern exterior after painting, Hebron CT"),
  ("blackledge-patio.jpg", "Clubhouse patio side after exterior painting at Blackledge Country Club"),
  ("blackledge-deck.jpg", "Clubhouse siding and trim after painting, Blackledge Country Club"),
  ("blackledge-side.jpg", "Vertical wood siding repainted on the clubhouse at Blackledge Country Club"),
]
def gallery():
    figs = "\n".join(f'          <figure><img src="/assets/{f}" alt="{esc(a)}" loading="lazy" width="1400" height="1050"></figure>' for f, a in GALLERY)
    return f"""        <h3 style="margin-top:36px">More from the Blackledge project</h3>
        <div class="gallery">
{figs}
        </div>
"""

def nick_photo(cls="nick-photo"):
    return '<figure class="%s"><img src="/assets/nick-on-the-job.jpg" alt="Nick, owner of ANC Painting, on a job with a respirator and spray gun" loading="lazy" width="1050" height="1400"><figcaption>Nick on the job</figcaption></figure>' % cls

def steps():
    return """        <div class="steps">
          <div class="step"><span class="badge">1</span><h3>Send your info</h3><p>Name, number and what needs painting. Photos help but aren't required.</p></div>
          <div class="step"><span class="badge">2</span><h3>We text you two times</h3><p>Pick whichever works for a quick look at the job. We'll give you a clear, written quote.</p></div>
          <div class="step"><span class="badge">3</span><h3>We paint, you relax</h3><p>We show up when we say, protect your home, do it right, and clean up like we were never there.</p></div>
        </div>
"""

def services_cards():
    cards = []
    for slug, title, blurb, _ in SERVICES:
        cards.append(f'          <div class="card"><h3>{title}</h3><p>{blurb}</p><a class="link" href="/{slug}/">{title} →</a></div>')
    return '        <div class="grid-3">\n' + "\n".join(cards) + "\n        </div>\n"

def areas_list():
    items = "\n".join(f'          <li><a href="/{t[1]}-ct-painters/">{t[0]}</a></li>' for t in TOWNS)
    return f'        <ul class="areas">\n{items}\n        </ul>\n'

def reviews_block():
    if GBP_URL:
        btn = f'<a class="btn" href="{GBP_URL}" target="_blank" rel="noopener">Read all on Google</a>'
    else:
        btn = '<a class="btn" href="#quoteFormWrap">Get a free quote</a>'
    return f"""    <section class="section">
      <div class="container">
        <p class="eyebrow">Reviews</p>
        <h2>What our customers say</h2>
        <div class="review-cta">
          <p>We're new to the area and building our Google reviews one happy customer at a time. Ask us for references from recent jobs any time.</p>
          {btn}
        </div>
      </div>
    </section>
"""

def faq(items):
    rows = "\n".join(f"        <details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f"""    <section class="faq section bg-paper">
      <div class="container">
        <h2>Common questions</h2>
{rows}
      </div>
      <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    </section>
"""

def cta_band(text="Ready for a fresh coat?"):
    return f"""    <section class="section bg-navy">
      <div class="container cta-inner">
        <div>
          <h2>{text}</h2>
          <p>Takes 30 seconds. We'll text you two times that work, then give you a clear written quote.</p>
        </div>
        <a href="#quoteFormWrap" class="btn btn-light btn-lg">Get a Free Quote</a>
      </div>
    </section>
"""

BASE_FAQ = [
    ("How much does painting cost?", "Every job is different, so we give you a free written quote after a quick look. The price depends on the size of the space, how much prep is needed and how many coats it takes. No surprises later."),
    ("What paint do you use?", "We use Benjamin Moore paint. If you have a color in mind, great. If not, we're happy to help you pick."),
    ("How long will my job take?", "It depends on the size of the job. We'll give you a realistic timeline with your quote, and then we stick to it."),
    ("Do I have to be home?", "For the quote visit, it helps if you're there so we can talk through what you want. During the work, you don't need to be home."),
    ("Where do you work?", "We're based in Coventry and paint across the greater Hartford and New Britain areas, from Mansfield and Tolland to West Hartford, Southington and Cromwell."),
    ("Are you registered with the state?", f"Yes. ANC Painting is a registered Connecticut Home Improvement Contractor, CT HIC # {HIC_TEXT}."),
]

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/"): full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f: f.write(content)

# ── Home ──
def build_home():
    h = head("House Painters in Hartford & New Britain Area CT | ANC Painting",
             "Family-owned interior, exterior and cabinet painting from Coventry, CT. Serving West Hartford, Glastonbury, New Britain, Southington, Manchester and nearby towns. Free, no-pressure quotes.", "/")
    body = header() + f"""  <main>
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">House painters · Hartford &amp; New Britain area, CT</p>
          <h1>Clean lines.<br>On time. Every time.</h1>
          <p class="tagline">Interior, exterior and cabinet painting by a local, family-owned crew. We show up when we say, protect your home, do it right, and leave it spotless.</p>
          <div class="hero-actions">
            <a href="#quoteFormWrap" class="btn btn-lg">Get My Free Quote</a>
            <a href="sms:{PHONE}" class="btn btn-lg btn-ghost">Text {PHONE_DISPLAY}</a>
          </div>
          <ul class="trust">
            <li>Free, no-pressure quotes</li>
            <li>Benjamin Moore paint</li>
            <li>CT HIC # {HIC_TEXT}</li>
          </ul>
        </div>
{quote_form("Homepage")}
      </div>
    </section>
{trust_bar()}
    <section class="section">
      <div class="container">
        <p class="eyebrow">What we paint</p>
        <h2>Inside, outside, and the kitchen</h2>
{services_cards()}
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container">
        <p class="eyebrow">Real work</p>
        <h2>Before &amp; after</h2>
{interior_ba()}
        <h3 style="margin-top:36px">Exterior: Blackledge Country Club, Hebron</h3>
{before_after()}
{gallery()}
      </div>
    </section>
    <section class="section">
      <div class="container">
        <p class="eyebrow">How it works</p>
        <h2>Three simple steps</h2>
{steps()}
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container story">
        {nick_photo()}
        <div class="story-copy">
          <p class="eyebrow">Why "ANC"?</p>
          <h2>It's our family's name on every wall</h2>
          <ul class="initials">
            <li><b>A</b><span>is for Arella</span></li>
            <li><b>N</b><span>is for Nick</span></li>
            <li><b>C</b><span>is for Callie &amp; Carson</span></li>
          </ul>
          <p class="muted">ANC Painting is a family business based in Coventry. We treat every home like it's our own, because our name is on every job. No pushy sales, no surprise charges, just careful work and a clean finish.</p>
          <a href="/about/" class="btn btn-ghost">Meet the family</a>
        </div>
      </div>
    </section>
{reviews_block()}
    <section class="section bg-paper" id="areas">
      <div class="container">
        <p class="eyebrow">Service area</p>
        <h2>Towns we paint in</h2>
        <p class="muted">Based in Coventry, painting across the greater Hartford and New Britain areas.</p>
{areas_list()}
        <p class="muted">Don't see your town? Send a quote request anyway. If it's within about 45 minutes, we can probably get to you.</p>
      </div>
    </section>
{faq(BASE_FAQ)}
{cta_band()}
  </main>
""" + footer()
    write("/", h + body)

# ── Services ──
SERVICE_FAQ = {
  "interior-painting": [("Do you move furniture?", "Yes. We move furniture to the middle of the room and cover it, and we cover floors before we start. Small, fragile or valuable items are best put away ahead of time."),
                        ("Do you fix nail holes and dings?", "Yes. Filling nail holes, small dings and minor drywall cracks is part of our prep. Bigger drywall repairs we'll price separately in your quote.")],
  "exterior-painting": [("When is exterior painting season in CT?", "Usually late spring through fall, when temperatures stay high enough for paint to cure. Spring fills up fast, so it's smart to get your quote over the winter and reserve a spot."),
                        ("Do you scrape and prime?", "Yes. Washing, scraping loose paint, sanding, caulking and priming bare wood are the steps that make an exterior paint job last.")],
  "cabinet-refinishing": [("Is painting cabinets cheaper than replacing them?", "Usually by a wide margin. If your cabinet boxes are in good shape, refinishing gives you a new look without the cost and mess of a remodel."),
                          ("Can I still use my kitchen?", "Mostly, yes. We'll walk you through the schedule so you know which days the kitchen will be busy.")],
}
def build_service(slug, title, blurb, bullets):
    h = head(f"{title} in the Hartford & New Britain Area CT | ANC Painting",
             f"{title} by ANC Painting, a family-owned painter based in Coventry, CT. {blurb} Free, no-pressure quotes across the greater Hartford area.", f"/{slug}/")
    lis = "\n".join(f"            <li>{b}</li>" for b in bullets)
    body = header() + f"""  <main>
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="breadcrumb"><a href="/">Home</a> › {title}</p>
          <p class="eyebrow">{title} · Hartford &amp; New Britain area, CT</p>
          <h1>{title}</h1>
          <p class="tagline">{blurb}</p>
          <ul class="checks">
{lis}
          </ul>
          <ul class="trust">
            <li>Free, no-pressure quotes</li>
            <li>Family-owned</li>
            <li>CT HIC # {HIC_TEXT}</li>
          </ul>
        </div>
{quote_form(title, service=title)}
      </div>
    </section>
{trust_bar()}
    <section class="section">
      <div class="container">
        <p class="eyebrow">How it works</p>
        <h2>Simple, no-pressure process</h2>
{steps()}
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container">
        <p class="eyebrow">Real work</p>
        <h2>Before &amp; after</h2>
{interior_ba()}
        <h3 style="margin-top:36px">Exterior: Blackledge Country Club, Hebron</h3>
{before_after()}
{gallery() if slug == "exterior-painting" else ""}
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h2>Where we do {title.lower()}</h2>
{areas_list()}
      </div>
    </section>
{faq(SERVICE_FAQ[slug] + BASE_FAQ[:3])}
{cta_band()}
  </main>
""" + footer()
    write(f"/{slug}/", h + body)

# ── Towns ──
def build_town(name, slug, county, line):
    others = [t for t in TOWNS if t[0] != name][:8]
    near = ", ".join(t[0] for t in others[:-1]) + " and " + others[-1][0]
    h = head(f"House Painters in {name}, CT | Interior, Exterior & Cabinets | ANC Painting",
             f"Looking for painters in {name}, CT? ANC Painting is a family-owned painting company offering interior, exterior and cabinet painting with Benjamin Moore paint. Free, no-pressure quotes.", f"/{slug}-ct-painters/")
    body = header() + f"""  <main>
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="breadcrumb"><a href="/">Home</a> › <a href="/#areas">Towns</a> › {name}</p>
          <p class="eyebrow">{county}, Connecticut</p>
          <h1>House Painters in {name}, CT</h1>
          <p class="tagline">{line}</p>
          <ul class="checks">
            <li><a href="/interior-painting/">Interior painting</a>: walls, ceilings, trim and doors</li>
            <li><a href="/exterior-painting/">Exterior painting</a>: siding, trim, doors and porches</li>
            <li><a href="/cabinet-refinishing/">Cabinet refinishing</a>: kitchens, vanities and built-ins</li>
          </ul>
          <ul class="trust">
            <li>Free, no-pressure quotes</li>
            <li>Benjamin Moore paint</li>
            <li>CT HIC # {HIC_TEXT}</li>
          </ul>
        </div>
{quote_form(name + " town page", town=name)}
      </div>
    </section>
{trust_bar()}
    <section class="section">
      <div class="container prose">
        <h2>Painting in {name}, the way it should be done</h2>
        <p>ANC Painting is a family-owned painting company based in Coventry. We paint homes in {name} and nearby towns like {near}.</p>
        <p>Every job starts the same way: a quick visit, a clear written quote, and a start date we stick to. We cover floors and furniture, do the prep that most painters skip, use Benjamin Moore paint, and clean up like we were never there.</p>
        <p>Want a quote for your {name} home? Fill out the form or text us at <a href="sms:{PHONE}">{PHONE_DISPLAY}</a>. We'll text you two times that work for a quick look.</p>
      </div>
    </section>
    <section class="section bg-paper">
      <div class="container">
        <p class="eyebrow">Real work</p>
        <h2>Before &amp; after</h2>
{interior_ba()}
        <h3 style="margin-top:36px">Exterior: Blackledge Country Club, Hebron</h3>
{before_after()}
      </div>
    </section>
    <section class="section">
      <div class="container">
        <p class="eyebrow">How it works</p>
        <h2>Three simple steps</h2>
{steps()}
      </div>
    </section>
{faq(BASE_FAQ[:4])}
{cta_band(f"Painting in {name}? Let's talk.")}
  </main>
""" + footer()
    write(f"/{slug}-ct-painters/", h + body)

# ── About ──
def build_about():
    h = head("About ANC Painting | Family-Owned Painters in Coventry, CT",
             "ANC Painting is a family business: Arella, Nick, Callie and Carson. Based in Coventry, CT, painting homes across the greater Hartford and New Britain areas.", "/about/")
    body = header() + f"""  <main>
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="breadcrumb"><a href="/">Home</a> › About</p>
          <p class="eyebrow">About us</p>
          <h1>A family name on every job</h1>
          {nick_photo("nick-photo nick-photo-inline")}
          <ul class="initials">
            <li><b>A</b><span>is for Arella</span></li>
            <li><b>N</b><span>is for Nick</span></li>
            <li><b>C</b><span>is for Callie &amp; Carson</span></li>
          </ul>
          <div class="prose">
            <p>ANC Painting is a small, family-owned painting company based in Coventry, Connecticut. Nick runs the jobs himself with a small crew, so the person who gives you the quote is the person who makes sure it's done right.</p>
            <p>We don't do high-pressure sales. We come out, look at the job, give you a clear written price, and let you decide. If you hire us, we show up when we say, protect your home, use Benjamin Moore paint, and leave the place cleaner than we found it.</p>
            <p>Nick also runs <a href="https://oilmeupct.com" rel="noopener">Oil Me Up!</a>, a mobile oil change service around Hartford, so a lot of our neighbors already know us.</p>
          </div>
          <ul class="trust">
            <li>Family-owned in Coventry</li>
            <li>Benjamin Moore paint</li>
            <li>CT HIC # {HIC_TEXT}</li>
          </ul>
        </div>
{quote_form("About page")}
      </div>
    </section>
{trust_bar()}
    <section class="section bg-paper">
      <div class="container">
        <p class="eyebrow">Real work</p>
        <h2>Before &amp; after</h2>
{interior_ba()}
        <h3 style="margin-top:36px">Exterior: Blackledge Country Club, Hebron</h3>
{before_after()}
{gallery()}
      </div>
    </section>
{cta_band()}
  </main>
""" + footer()
    write("/about/", h + body)

# ── Success ──
def build_success():
    conv = ""
    if GOOGLE_ADS_CONVERSION:
        conv = f"<script>if(typeof gtag==='function'){{gtag('event','conversion',{{'send_to':'{GOOGLE_ADS_CONVERSION}'}});}}</script>"
    h = head("Thanks, we got your request | ANC Painting", "Your painting quote request was received. We'll text you shortly.", "/success/", noindex=True, extra=conv)
    body = header() + f"""  <main>
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">Request received</p>
          <h1>Thanks! We'll be in touch soon.</h1>
          <p class="tagline">We got your request. Nick will text you shortly with two times that work for a quick look at the job. No payment, no obligation.</p>
          <p style="padding:14px 16px;border:1px solid var(--line);border-radius:12px;background:var(--paper)">We'll text you from <strong>{PHONE_DISPLAY}</strong>. Tap <strong>Save our number</strong> so our text doesn't look like spam.</p>
          <div class="hero-actions">
            <a href="/assets/anc-painting.vcf" class="btn btn-lg">Save our number</a>
            <a href="tel:{PHONE}" class="btn btn-lg btn-ghost">Call {PHONE_DISPLAY}</a>
            <a href="/" class="btn btn-lg btn-ghost">Back to home</a>
          </div>
        </div>
        <div class="hero-card" id="quoteFormWrap">
          <h2 class="form-title">What happens next?</h2>
          <ul class="checks">
            <li>We text you two times for a quick look</li>
            <li>You get a clear, written quote</li>
            <li>You decide. No pressure, ever.</li>
          </ul>
        </div>
      </div>
    </section>
  </main>
""" + footer()
    write("/success/", h + body)

def build_misc():
    urls = ["/", "/interior-painting/", "/exterior-painting/", "/cabinet-refinishing/", "/about/"] + [f"/{t[1]}-ct-painters/" for t in TOWNS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls) + "\n</urlset>\n"
    write("/sitemap.xml", sm)
    if HIC:
        write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /success/\n\nSitemap: {SITE}/sitemap.xml\n")
    else:  # keep the site out of Google until the CT HIC number is on it
        write("/robots.txt", "User-agent: *\nDisallow: /\n")
    write("/_redirects", "/success /success/ 301\n/thank-you /success/ 301\n/thank-you/ /success/ 301\n/thank-you.html /success/ 301\n")
    write("/_headers", '/assets/anc-painting.vcf\n  Content-Type: text/vcard; charset=utf-8\n  Content-Disposition: inline; filename="Nick - ANC Painting.vcf"\n')
    vcf = ["BEGIN:VCARD", "VERSION:3.0", "N:;Nick;;;", "FN:Nick - ANC Painting", f"ORG:{NAME}", f"TEL;TYPE=CELL,VOICE:{PHONE}"]
    if EMAIL: vcf.append(f"EMAIL;TYPE=INTERNET:{EMAIL}")
    vcf += [f"URL:{SITE}", "NOTE:Interior, exterior & cabinet painting.", "END:VCARD"]
    write("/assets/anc-painting.vcf", "\r\n".join(vcf) + "\r\n")
    write("/assets/logo.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="#0E2A47"/><circle cx="32" cy="32" r="27" fill="none" stroke="#F6F4EF" stroke-width="1"/><text x="32" y="38.5" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-size="19" font-weight="700" letter-spacing="1" fill="#F6F4EF">ANC</text></svg>\n')

if __name__ == "__main__":
    build_home()
    for s in SERVICES: build_service(*s)
    for t in TOWNS: build_town(*t)
    build_about()
    build_success()
    build_misc()
    print("Built", sum(len(f) for _, _, f in os.walk(OUT)), "files into", OUT)
