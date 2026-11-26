#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Global Edition — one day of world news on a single 1024x1024 poster.

Edition: Wednesday 25 November 2026. 56 verified stories in 7 regions,
each with its outlet tag; the full attribution list lives in SOURCES.md.
Security and diplomacy items were refreshed against the Just Security
Early Edition of 25 Nov 2026 itself; markets, culture, sport and weather
come from the wires and outlets listed per story.

Run:  python3 main.py   ->  writes entry.png next to this file.
Deterministic: no clock, no randomness, fixed fonts — two runs of this
file produce a byte-identical poster.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (250, 246, 239)
PAPER_DARK = (240, 233, 220)
INK = (26, 23, 18)
INK_SOFT = (74, 68, 58)
RED = (179, 64, 42)
GOLD = (176, 124, 32)
TEAL = (14, 110, 96)
BLUE = (38, 84, 138)
LINE = (203, 192, 172)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- the data
# (number, short poster headline, outlet tag) — full text + URLs in SOURCES.md
REGIONS = [
    ("NORTH AMERICA", RED, [
        (1, "Dow tops 50,000 for the first time", "Investopedia"),
        (2, "Nvidia -5.86% a day after +31% surge", "Reuters"),
        (3, "Consumer confidence jumps to 103.3", "Reuters"),
        (4, "USTR set to raise tariffs on 16 economies", "AP via JS"),
        (5, "Senate probes Vance role in Vitol oil deal", "Reuters via JS"),
        (6, "Huawei guilty of trade-secret conspiracy", "BBC via JS"),
        (7, "Rep. Gomez to resign after ethics finding", "NYT via JS"),
        (8, "Sullivan concedes Alaska race to Peltola", "NYT via JS"),
        (9, "Abrego Garcia leaves US for Spain", "NYT via JS"),
    ]),
    ("LATIN AMERICA & CARIBBEAN", TEAL, [
        (10, "Mexico to try 'El Chapo Isidro' itself", "Reuters"),
        (11, "Bolsonaro in ICU, bowel obstruction", "Al Jazeera"),
        (12, "Brazil lifts 2027 inflation view to 4.5%", "MercoPress"),
        (13, "Argentina economy shrank 1.2% y/y", "Rio Times"),
        (14, "WHO chief: lift US fuel blockade on Cuba", "Reuters via JS"),
        (15, "Drone hits Colombia police base, civilians hurt", "Al Jazeera"),
        (16, "Peru dengue: 45 dead, 20,000+ cases", "Rio Times"),
    ]),
    ("EUROPE", BLUE, [
        (17, "Lukashenko offers Zelenskiy Moscow flight", "Reuters"),
        (18, "Moscow: Estonia on 'verge of open war'", "Al Jazeera"),
        (19, "Russian strike on Odesa kills 2, hurts 3", "Reuters via JS"),
        (20, "Libya LNA vows payback for warship strike", "AP via JS"),
        (21, "Rutte: NATO will defend in space too", "BBC via JS"),
        (22, "Poland: deal won't end Russian sabotage", "Politico via JS"),
        (23, "Putin: refinery retaliation 'inevitable'", "Reuters via JS"),
        (24, "Europe launches 36 Kuiper satellites", "Bloomberg"),
        (25, "Merz: Russia escalating threats to Europe", "Reuters via JS"),
    ]),
    ("MIDDLE EAST & N. AFRICA", GOLD, [
        (26, "Israel kills Hamas security chief Abuelouf", "Reuters via JS"),
        (27, "Strike kills UNRWA worker at Jabalia well", "Reuters via JS"),
        (28, "Eisenkot clinches first coalition deal", "Reuters"),
        (29, "Iran: unconcerned by US naval blockade", "Reuters via JS"),
        (30, "Two tankers strike mines in Hormuz", "Reuters via JS"),
        (31, "Houthi strike on Riyadh tower injures 11", "NYT via JS"),
        (32, "Houthis claim Ras Tanura refinery attack", "Reuters via JS"),
        (33, "Vance, Rubio meet Qatari PM at White House", "AP via JS"),
    ]),
    ("SUB-SAHARAN AFRICA", (122, 74, 140), [
        (34, "Zambia opposition leader charged: treason", "Reuters"),
        (35, "Boat capsizes off Senegal, ~175 missing", "OkayAfrica"),
        (36, "Senegal reinstated as AFCON champions", "PANA"),
        (37, "Amnesty: Tigray shelling may be war crime", "Reuters via JS"),
        (38, "DRC hunts missing cargo plane", "OkayAfrica"),
        (39, "DRC to open miners' local units by Jan", "OkayAfrica"),
        (40, "Gavi to buy 1.5m Ebola vaccine doses", "OkayAfrica"),
        (41, "Sudan: RSF drones kill 19 civilians", "Reuters via JS"),
    ]),
    ("ASIA-PACIFIC", (178, 84, 32), [
        (42, "China probes Politburo member Chen Jining", "Reuters"),
        (43, "Japan to pay full 2027 ICC dues early", "Reuters via JS"),
        (44, "S. Korea: $375k to catch AI exam cheats", "WSJ via JS"),
        (45, "Russian jets enter S. Korea defence zone", "AP via JS"),
        (46, "Hasina plans Bangladesh return Dec 16", "Reuters via JS"),
        (47, "Solomon Is. signs Australia treaty", "NYT via JS"),
        (48, "Singapore probes Megaspeed after US ban", "Reuters"),
        (49, "China extends US minerals-curb pause", "SCMP"),
        (50, "Hanoi gas blast kills 6, injures 10", "World Now"),
    ]),
    ("GLOBAL: MARKETS, CULTURE, SPORT", (84, 110, 44), [
        (51, "UCL: Madrid 5-1 PSV, City 2-2 Napoli", "SuperSport"),
        (52, "Record quasar, 630m yrs after Big Bang", "Reuters/AP"),
        (53, "Titanium oxide found round a young star", "Phys.org"),
        (54, "Pope Leo: COP31 failure a climate warning", "AP via JS"),
        (55, "Anthropic shares slip below IPO price", "Investopedia"),
        (56, "Gold -2.7% to $3,552.80, oil up on Hormuz", "StockMarketWatch"),
    ]),
]

LEADS = [
    ("50,018.70", "THE DOW CLOSES ABOVE 50,000", "Story 1 — first close over the mark, +0.85%"),
    ("2 TANKERS", "MINES IN THE STRAIT OF HORMUZ", "Story 30 — IRGC says both struck mines, burned"),
    ("GAZA CITY", "HAMAS SECURITY CHIEF KILLED", "Story 26 — Abuelouf, wife and two children"),
]

BY_NUMBERS = [
    ("103.3", "US consumer confidence"),
    ("490,334", "Russian dead, leaked stats"),
    ("36", "Kuiper satellites launched"),
    ("~175", "missing off Senegal"),
    ("45", "Peru dengue deaths"),
    ("$375k", "S. Korea cheat rewards"),
]

WEATHER = [  # Open-Meteo, fetched 02:26 UTC 25 Nov 2026
    ("New York", "3C", "Clear"), ("Quito", "13C", "Overcast"),
    ("London", "5C", "Overcast"), ("Tokyo", "11C", "Clear"),
    ("Sydney", "21C", "Overcast"), ("Mumbai", "24C", "Clear"),
    ("Singapore", "29C", "Drizzle"), ("Sao Paulo", "23C", "Drizzle"),
]

# story number -> (lon, lat) for the map pins
PINS = {
    1: (-74, 41), 8: (-150, 64), 10: (-102, 23), 15: (-74, 4),
    19: (31, 46), 20: (22, 32), 24: (-52, 5), 26: (34, 31),
    30: (56, 26), 31: (47, 25), 35: (-17, 15), 41: (33, 12),
    42: (116, 40), 47: (160, -10), 50: (106, 21), 54: (12, 42),
}

# 16 illustration panels: (story number, glyph kind, caption)
PANELS = [
    (1, "chart", "Dow 50k"), (2, "chip", "Nvidia"),
    (6, "scales", "Huawei verdict"), (8, "ballot", "Alaska"),
    (19, "shield", "Odesa"), (20, "ship", "Benghazi"),
    (24, "satellite", "Kuiper x36"), (26, "cross", "Gaza"),
    (30, "flame", "Hormuz"), (31, "tower", "Riyadh"),
    (35, "boat", "Senegal"), (37, "gavel", "Tigray"),
    (42, "eye", "Beijing probe"), (47, "anchor", "Solomons"),
    (51, "trophy", "Champions Lg"), (52, "star", "Quasar"),
]

TIMELINE = [
    ("OVERNIGHT", "Russian strike hits Odesa (19)"),
    ("MORNING", "Two tankers strike mines in Hormuz (30)"),
    ("MIDDAY", "Houthis claim Ras Tanura refinery attack (32)"),
    ("AFTERNOON", "Merz warns Bundestag: Russia wants more (25)"),
    ("EVENING", "Dow closes over 50,000 for the first time (1)"),
]

LEFT_OUT = (
    "LEFT OUT & WHY — Held: claims carried by a single partisan feed with no "
    "credible outlet behind them. Superseded: the first Hormuz claim (three "
    "tankers) was replaced by the confirmed two-tanker mine report. Date "
    "check: every story was filed inside the 25 Nov 2026 cycle — 24 Nov UTC "
    "filings are 25 Nov across Asia. Security spine: Just Security Early "
    "Edition, 25 Nov 2026."
)

# coarse world landmass grid for the dot map (rows north -> south)
LAND = [
    "        oooo                                          o  ooooooo ooooooooooo                     ",
    "   oooooooooo        ooo        o              ooooo oooooooooooooooooooooooooooo  ooo           ",
    "  oooooooooooo     oooooo    ooooo           oooooooooooooooooooooooooooooooooooooooooooo        ",
    "   oooooooooo      ooooo    ooooooo         oooooooooooooooooooooooooooooooooooooooooooooo       ",
    "    ooooooo         ooo      oooooo          oooooooooooooooooooooooooooooooooooooooooooo        ",
    "     ooooo                    oooo            oooooooooooooooooooooooooooooooooooooooooo         ",
    "      oooo                     oo              oooooooooooooooooooooooooooooooooooooooo          ",
    "       ooo                                      ooooooooooooooooooooooooooooooooooooo            ",
    "       oooo       o                              ooooooooooooooooooooooooooooooooooo             ",
    "        oooo     oo                                ooooooooooooooooooooooooooooooooo             ",
    "        ooooo   oo                                  ooooooooooooooooooooooooooooooo              ",
    "         ooooo oo                                    ooooooooooooooooooooooooooooo               ",
    "         oooooo                                       ooooooooooooooooooooooooooo                ",
    "          ooooo                                        ooooooooooooooooooooooooo                 ",
    "          ooooo                                         oooooooooooooooooooooooo                 ",
    "           oooo                                          oooooooooooooooooooooo                  ",
    "           ooooo                                          oooooooooooooooooooo                   ",
    "           oooooo                                           oooooooooooooooooo                    ",
    "           oooooo                                            oooooooooooooooo                     ",
    "            ooooo                                             oooooooooooooo                      ",
    "            ooooo                                              oooooooooooo                       ",
    "            oooo                                                oooooooooo                        ",
    "            oooo                                                 oooooooo                         ",
    "           oooo                                                   oooooo         o                ",
    "           ooo                                                     oooo        ooooo               ",
    "          ooo                                                       oo        oooooooo             ",
    "          oo                                                                    ooooo              ",
]


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns the list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def lonlat_to_xy(lon, lat, box):
    """Equirectangular projection into box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
    return x, y


def draw_map(draw, box):
    """Dot-matrix world from the LAND grid, then numbered pins on top."""
    x0, y0, x1, y1 = box
    rows = len(LAND)
    cols = max(len(r) for r in LAND)
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    for ri, row in enumerate(LAND):
        for ci, cell in enumerate(row):
            if cell == "o":
                cx = x0 + (ci + 0.5) * cw
                cy = y0 + (ri + 0.5) * ch
                r = min(cw, ch) * 0.30
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 178, 146))
    f_pin = font(SANS_B, 10)
    for num, (lon, lat) in sorted(PINS.items()):
        px, py = lonlat_to_xy(lon, lat, box)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
        label = str(num)
        w = draw.textlength(label, font=f_pin)
        draw.text((px - w / 2, py - 6), label, font=f_pin, fill=WHITE)


def glyph(draw, kind, x, y, s, color):
    """Tiny geometric illustration, drawn inside an s-by-s box at (x, y)."""
    if kind == "chart":
        pts = [(x + 2, y + s - 4), (x + s * 0.35, y + s * 0.62),
               (x + s * 0.6, y + s * 0.72), (x + s - 3, y + 4)]
        draw.line(pts, fill=color, width=2)
        draw.line([(x + 2, y + s - 2), (x + s - 2, y + s - 2)], fill=color, width=1)
    elif kind == "chip":
        draw.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], outline=color, width=2)
        for i in range(3):
            p = x + 10 + i * (s - 20) / 2
            draw.line([(p, y + 1), (p, y + 6)], fill=color, width=2)
            draw.line([(p, y + s - 6), (p, y + s - 1)], fill=color, width=2)
    elif kind == "scales":
        cx = x + s / 2
        draw.line([(cx, y + 3), (cx, y + s - 6)], fill=color, width=2)
        draw.line([(x + 4, y + 7), (x + s - 4, y + 7)], fill=color, width=2)
        draw.arc([x + 1, y + 6, x + 13, y + 16], 0, 180, fill=color, width=2)
        draw.arc([x + s - 13, y + 6, x + s - 1, y + 16], 0, 180, fill=color, width=2)
        draw.line([(x + 4, y + s - 3), (x + s - 4, y + s - 3)], fill=color, width=2)
    elif kind == "ballot":
        draw.rectangle([x + 5, y + 8, x + s - 5, y + s - 4], outline=color, width=2)
        draw.rectangle([x + 10, y + 2, x + s - 10, y + 10], outline=color, width=2)
        draw.line([(x + 10, y + s / 2), (x + 15, y + s / 2 + 4), (x + s - 9, y + 8 + 4)],
                  fill=color, width=2)
    elif kind == "shield":
        draw.polygon([(x + s / 2, y + 2), (x + s - 4, y + 6), (x + s - 4, y + s * 0.55),
                      (x + s / 2, y + s - 2), (x + 4, y + s * 0.55), (x + 4, y + 6)],
                     outline=color, width=2)
    elif kind == "ship":
        draw.polygon([(x + 3, y + s * 0.62), (x + s - 3, y + s * 0.62),
                      (x + s - 8, y + s - 5), (x + 8, y + s - 5)], outline=color, width=2)
        draw.line([(x + s / 2, y + 6), (x + s / 2, y + s * 0.62)], fill=color, width=2)
        draw.polygon([(x + s / 2, y + 8), (x + s / 2, y + s * 0.5), (x + s - 10, y + s * 0.5)],
                     fill=color)
    elif kind == "satellite":
        draw.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                       outline=color, width=2)
        draw.rectangle([x + 2, y + s * 0.3, x + s * 0.34, y + s * 0.52], outline=color, width=1)
        draw.rectangle([x + s * 0.66, y + s * 0.48, x + s - 2, y + s * 0.7], outline=color, width=1)
        draw.arc([x + s * 0.55, y + 2, x + s - 2, y + s * 0.3], 200, 320, fill=color, width=2)
    elif kind == "cross":
        cx, cy = x + s / 2, y + s / 2
        draw.rectangle([cx - 2, y + 4, cx + 2, y + s - 4], fill=color)
        draw.rectangle([x + 6, cy - 2, x + s - 6, cy + 2], fill=color)
    elif kind == "flame":
        draw.polygon([(x + s / 2, y + 2), (x + s - 7, y + s * 0.6), (x + s * 0.68, y + s - 4),
                      (x + s * 0.32, y + s - 4), (x + 7, y + s * 0.6)], fill=color)
        draw.ellipse([x + s * 0.4, y + s * 0.55, x + s * 0.6, y + s - 6], fill=PAPER)
    elif kind == "tower":
        draw.rectangle([x + s * 0.36, y + 3, x + s * 0.64, y + s - 3], outline=color, width=2)
        for i in range(3):
            wy = y + 8 + i * (s - 16) / 3
            draw.line([(x + s * 0.42, wy), (x + s * 0.58, wy)], fill=color, width=1)
    elif kind == "boat":
        draw.polygon([(x + 3, y + s * 0.55), (x + s - 3, y + s * 0.55),
                      (x + s - 9, y + s - 6), (x + 9, y + s - 6)], outline=color, width=2)
        for i in range(3):
            wx = x + 4 + i * (s - 8) / 2
            draw.arc([wx, y + s - 6, wx + (s - 8) / 2, y + s + 2], 0, 180, fill=color, width=1)
    elif kind == "gavel":
        draw.line([(x + 6, y + s - 6), (x + s * 0.55, y + s * 0.45)], fill=color, width=3)
        draw.rectangle([x + s * 0.52, y + 4, x + s - 4, y + 12], outline=color, width=2)
        draw.line([(x + 4, y + s - 3), (x + s - 6, y + s - 3)], fill=color, width=2)
    elif kind == "eye":
        draw.ellipse([x + 3, y + s * 0.28, x + s - 3, y + s * 0.72], outline=color, width=2)
        draw.ellipse([x + s * 0.42, y + s * 0.4, x + s * 0.58, y + s * 0.6], fill=color)
    elif kind == "anchor":
        cx = x + s / 2
        draw.line([(cx, y + 6), (cx, y + s - 6)], fill=color, width=2)
        draw.line([(x + 8, y + 10), (x + s - 8, y + 10)], fill=color, width=2)
        draw.arc([x + 6, y + s * 0.45, x + s - 6, y + s - 2], 0, 180, fill=color, width=2)
        draw.ellipse([cx - 3, y + 1, cx + 3, y + 7], outline=color, width=2)
    elif kind == "trophy":
        draw.arc([x + s * 0.3, y + 3, x + s * 0.7, y + s * 0.62], 0, 180, fill=color, width=2)
        draw.line([(x + s * 0.3, y + s * 0.32), (x + s * 0.7, y + s * 0.32)], fill=color, width=2)
        draw.arc([x + 4, y + 6, x + s * 0.34, y + s * 0.4], 90, 270, fill=color, width=2)
        draw.arc([x + s * 0.66, y + 6, x + s - 4, y + s * 0.4], 270, 90, fill=color, width=2)
        draw.line([(x + s / 2, y + s * 0.6), (x + s / 2, y + s - 8)], fill=color, width=2)
        draw.line([(x + s * 0.32, y + s - 4), (x + s * 0.68, y + s - 4)], fill=color, width=2)
    elif kind == "star":
        cx, cy = x + s / 2, y + s / 2
        pts = []
        import math
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = (s * 0.44) if i % 2 == 0 else (s * 0.19)
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=color)


# ---------------------------------------------------------------- layout
W = 1024
MARGIN = 24


def section_label(draw, x, y, text, color=INK):
    draw.text((x, y), text, font=font(SANS_B, 10), fill=color)


def region_block(draw, x, y, w, name, color, stories):
    draw.rectangle([x, y, x + w, y + 17], fill=color)
    draw.text((x + 6, y + 3), name, font=font(SANS_B, 9), fill=WHITE)
    count = "%d stories" % len(stories)
    cw = draw.textlength(count, font=font(SANS, 8))
    draw.text((x + w - cw - 6, y + 4), count, font=font(SANS, 8), fill=WHITE)
    f_num = font(SANS_B, 8)
    f_txt = font(SANS, 8)
    cy = y + 22
    for num, headline, tag in stories:
        label = "%d." % num
        draw.text((x + 1, cy), label, font=f_num, fill=color)
        body = "%s (%s)" % (headline, tag)
        lines = wrap(draw, body, f_txt, w - 22)
        for li, line in enumerate(lines[:2]):
            draw.text((x + 22, cy + li * 10), line, font=f_txt, fill=INK)
        cy += max(1, min(2, len(lines))) * 10 + 1
    return cy


def build(path):
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header
    d.text((MARGIN, 14), "GLOBAL EDITION  ·  ONE POSTER, ONE DAY, EVERY STORY SOURCED",
           font=font(SANS_B, 10), fill=RED)
    d.text((MARGIN, 30), "The World in One Day", font=font(SERIF, 38), fill=INK)
    d.text((MARGIN, 76),
           "Wednesday 25 November 2026  ·  56 verified stories  ·  7 regions  ·  all times UTC",
           font=font(SANS, 11), fill=INK_SOFT)
    d.line([(MARGIN, 94), (W - MARGIN, 94)], fill=INK, width=2)

    # ---- leads
    lw = (W - 2 * MARGIN - 16) / 3
    for i, (big, label, note) in enumerate(LEADS):
        x = MARGIN + i * (lw + 8)
        d.rectangle([x, 102, x + lw, 184], fill=PAPER_DARK, outline=LINE)
        d.rectangle([x, 102, x + lw, 107], fill=RED)
        d.text((x + 10, 112), big, font=font(SERIF, 24), fill=INK)
        d.text((x + 10, 146), label, font=font(SANS_B, 10), fill=RED)
        text_block(d, (x + 10, 162), note, font(SANS, 9), INK_SOFT, lw - 20, 11)

    # ---- map + right rail
    section_label(d, MARGIN, 194, "WHERE IT HAPPENED — numbered pins match the index")
    draw_map(d, (MARGIN, 212, 648, 396))
    d.text((MARGIN, 400),
           "Pins: 1 New York · 8 Alaska · 10 Mexico · 15 Colombia · 19 Odesa · 20 Libya · 24 Guiana · 26 Gaza",
           font=font(SANS, 8), fill=INK_SOFT)
    d.text((MARGIN, 411),
           "30 Hormuz · 31 Riyadh · 35 Senegal · 41 Sudan · 42 Beijing · 47 Solomons · 50 Hanoi · 54 Vatican",
           font=font(SANS, 8), fill=INK_SOFT)
    rx = 664
    rw = W - MARGIN - rx
    d.rectangle([rx, 194, rx + rw, 300], outline=LINE)
    section_label(d, rx + 10, 200, "BY THE NUMBERS", RED)
    ny = 222
    for value, label in BY_NUMBERS:
        d.text((rx + 10, ny), value, font=font(SERIF, 14), fill=INK)
        vw = d.textlength(value, font=font(SERIF, 14))
        d.text((rx + 16 + vw, ny + 4), label, font=font(SANS, 9), fill=INK_SOFT)
        ny += 13
    d.rectangle([rx, 308, rx + rw, 440], outline=LINE)
    section_label(d, rx + 10, 314, "WEATHER — OPEN-METEO, 02:26 UTC", TEAL)
    wy = 334
    for i in range(0, 8, 2):
        for j in range(2):
            city, temp, cond = WEATHER[i + j]
            cx = rx + 10 + j * (rw / 2)
            d.text((cx, wy), city, font=font(SANS_B, 9), fill=INK)
            d.text((cx, wy + 11), "%s %s" % (temp, cond), font=font(SANS, 8), fill=INK_SOFT)
        wy += 25

    # ---- panels
    section_label(d, MARGIN, 424, "SIXTEEN PANELS — the day in pictures, drawn in code")
    tw = (W - 2 * MARGIN) / 16
    for i, (num, kind, caption) in enumerate(PANELS):
        x = MARGIN + i * tw
        d.rectangle([x + 1, 442, x + tw - 1, 496], fill=WHITE, outline=LINE)
        d.text((x + 4, 444), str(num), font=font(SANS_B, 8), fill=RED)
        glyph(d, kind, x + tw / 2 - 13, 446, 26, INK)
        lines = wrap(d, caption, font(SANS, 7), tw - 6)
        for li, line in enumerate(lines[:2]):
            lw2 = d.textlength(line, font=font(SANS, 7))
            d.text((x + (tw - lw2) / 2, 474 + li * 8), line, font=font(SANS, 7), fill=INK_SOFT)

    # ---- story index, row A: four regions
    colw = (W - 2 * MARGIN - 24) / 4
    for i, (name, color, stories) in enumerate(REGIONS[:4]):
        region_block(d, MARGIN + i * (colw + 8), 506, colw, name, color, stories)
    # ---- story index, row B: three regions, wider columns
    colw_b = (W - 2 * MARGIN - 16) / 3
    for i, (name, color, stories) in enumerate(REGIONS[4:]):
        region_block(d, MARGIN + i * (colw_b + 8), 716, colw_b, name, color, stories)

    # ---- timeline
    d.line([(MARGIN, 880), (W - MARGIN, 880)], fill=LINE, width=1)
    section_label(d, MARGIN, 886, "THE DAY IN UTC")
    cellw = (W - 2 * MARGIN - 32) / 5
    for i, (part, what) in enumerate(TIMELINE):
        x = MARGIN + i * (cellw + 8)
        d.text((x, 902), part, font=font(SANS_B, 9), fill=RED)
        text_block(d, (x, 915), what, font(SANS, 8), INK_SOFT, cellw, 10)

    # ---- left out + footer
    d.line([(MARGIN, 950), (W - MARGIN, 950)], fill=LINE, width=1)
    text_block(d, (MARGIN, 956), LEFT_OUT, font(SANS, 8), INK_SOFT, W - 2 * MARGIN, 10)
    d.text((MARGIN, 1002),
           "Full text and a source link for every story: SOURCES.md in this repository · Poster generated by main.py",
           font=font(SANS, 8), fill=INK_SOFT)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(out)
    print("wrote", out)
