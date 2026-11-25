#!/usr/bin/env python3
"""Draw the v2 news-image-20261124 poster: a newspaper front page summing up
Tuesday 24 November 2026 in one image — 36 dated stories (3 illustrated
heroes, 12 grid briefs, 21 one-line ticker stories), a numbered world map,
a numbers strip, a UTC timeline, a region count bar and a DATE CHECK strip.

Local build tool (Pillow). The competition program (main.py) is stdlib-only
and copies the rendered entry.png byte-for-byte, per the kit's simplest
valid route. Deterministic: fixed canvas, fixed fonts, no randomness,
no network. Story selection, figures, sources and certainty tags follow
V2_BATTLE_PACK.md exactly.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 14                      # page margin
PAPER = (246, 241, 229)     # newsprint cream
PAPER2 = (255, 253, 246)
INK = (22, 20, 18)
SOFT = (74, 68, 58)
RED = (178, 30, 40)
DARKRED = (140, 22, 32)
BLUE = (30, 74, 128)
NAVY = (15, 38, 68)
GOLD = (188, 138, 20)
GREEN = (18, 122, 62)
TEAL = (14, 110, 110)
PURPLE = (96, 52, 140)
BROWN = (146, 84, 20)
GREY = (110, 104, 94)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def block(x, y, text, font, fill, max_w, leading, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y

def fit_size(text, path, start, max_w, min_size=9):
    s = start
    while s > min_size and d.textlength(text, font=F(path, s)) > max_w:
        s -= 1
    return s

def vgrad(x, y, w, h, top, bot):
    for j in range(h):
        t = j / max(h - 1, 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.line([x, y + j, x + w, y + j], fill=col)

def tag_chip(x, y, tag, color):
    """Small certainty tag, right-aligned ending at x. Returns left edge."""
    f = F(SANS_B, 9)
    tw = d.textlength(tag, font=f)
    d.rectangle([x - tw - 10, y, x, y + 13], fill=color)
    d.text((x - tw - 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return x - tw - 10

TAG_COLORS = {
    "CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": BROWN,
    "CLAIM": RED, "ONGOING": PURPLE,
}
REGION_COLORS = {
    "ASIA": TEAL, "EUROPE": BLUE, "MIDDLE EAST": BROWN,
    "AMERICAS": RED, "AFRICA": GREEN, "GLOBAL": GREY,
}

# ================================================================ masthead
d.rectangle([0, 0, W, 20], fill=INK)
d.text((M, 4), "THE WORLD IN ONE PAGE", font=F(SANS_B, 12), fill=(240, 234, 218))
right = "EVERY STORY DATED TUESDAY 24 NOV"
rw = d.textlength(right, font=F(SANS_B, 12))
d.text((W - M - rw, 4), right, font=F(SANS_B, 12), fill=(240, 234, 218))
mid = "38 STORIES - 6 REGIONS"
mw = d.textlength(mid, font=F(SANS_B, 12))
d.text(((W - mw) / 2, 4), mid, font=F(SANS_B, 12), fill=(250, 214, 120))

title = "TUESDAY 24 NOVEMBER 2026"
ts = fit_size(title, SERIF_B, 57, W - 2 * M)
tf = F(SERIF_B, ts)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
d.line([M, 86, W - M, 86], fill=INK, width=3)
d.line([M, 90, W - M, 90], fill=INK, width=1)

sub = "Sanofi buys Insmed for $41bn  -  Asia's chip rally: TAIEX +9.0%  -  Iran says 3 more tankers hit mines in Hormuz"
ss = fit_size(sub, SERIF_I, 18, W - 2 * M)
sf = F(SERIF_I, ss)
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, 94), sub, font=sf, fill=DARKRED)

# ================================================================ region bar
REGIONS = [("ASIA", 14), ("EUROPE", 7), ("MIDDLE EAST", 6),
           ("AMERICAS", 5), ("AFRICA", 3), ("GLOBAL", 3)]
RY, RH = 118, 19
total = sum(c for _, c in REGIONS)
x = M
for name, count in REGIONS:
    seg = int((W - 2 * M) * count / total)
    d.rectangle([x, RY, x + seg - 2, RY + RH], fill=REGION_COLORS[name])
    label = "%s %d" % (name, count)
    lf = F(SANS_B, 11)
    lw = d.textlength(label, font=lf)
    d.text((x + (seg - 2 - lw) / 2, RY + 4), label, font=lf, fill=(255, 255, 255))
    x += seg

# ================================================================ timeline UTC
TY = 141
d.rectangle([M, TY, W - M, TY + 21], fill=(238, 231, 214), outline=INK, width=1)
d.rectangle([M, TY, M + 108, TY + 21], fill=NAVY)
d.text((M + 7, TY + 5), "THE DAY IN UTC", font=F(SANS_B, 10), fill=(255, 255, 255))
timeline = ("01:32 Nepal M5.6 quake  -  04:34 Zaporizhzhia strike  -  "
            "05:30 Sanofi announces $41bn deal, Paris  -  +/-08:00 Cartagena siege begins  -  "
            "Asia close: TAIEX +9.0%  -  Tue PM, Lausanne: CAS restores Senegal's title")
tls = fit_size(timeline, SANS_R, 12, W - 2 * M - 118, min_size=8)
d.text((M + 116, TY + 5), timeline, font=F(SANS_R, tls), fill=INK)

# ================================================================ numbers strip
NY, NH = 166, 42
NUMBERS = [
    ("$41.0bn", "SANOFI- INSMED DEAL"),
    ("+9.0%", "TAIEX, TAIWAN"),
    ("+31.5%", "NVIDIA MONDAY"),
    ("699", "DRONES RUSSIA SAYS DOWNED"),
    ("5,258", "UK SUMMER HEAT DEATHS"),
    ("40+", "WOUNDED, ZAPORIZHZHIA"),
    ("26", "DEAD, CIKANDE FIRE"),
    ("6,500", "ROHINGYA TO RETURN"),
]
nw = (W - 2 * M) // len(NUMBERS)
for i, (big, small) in enumerate(NUMBERS):
    x = M + i * nw
    if i:
        d.line([x, NY + 3, x, NY + NH - 3], fill=GREY, width=1)
    bs = fit_size(big, SERIF_B, 23, nw - 8)
    bf = F(SERIF_B, bs)
    bw = d.textlength(big, font=bf)
    d.text((x + (nw - bw) / 2, NY), big, font=bf, fill=DARKRED if i in (5, 6) else INK)
    for j, line in enumerate(wrap(small, F(SANS_B, 8), nw - 6)):
        lf = F(SANS_B, 8)
        lw = d.textlength(line, font=lf)
        d.text((x + (nw - lw) / 2, NY + 26 + j * 9), line, font=lf, fill=SOFT)
d.line([M, NY + NH + 3, W - M, NY + NH + 3], fill=INK, width=2)

# ================================================================ hero scenes
def burst(cx, cy, s, color=RED):
    pts = []
    for i in range(16):
        r = s if i % 2 == 0 else s * 0.45
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)

def scene_sanofi(x, y, w, h):
    vgrad(x, y, w, h, (186, 214, 238), (240, 243, 233))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 150, 110))
    # headquarters tower with a medical cross
    d.rectangle([x + 18, y + 18, x + 92, y + h - 16], fill=(238, 240, 244), outline=INK, width=2)
    for r in range(3):
        for c in range(3):
            d.rectangle([x + 27 + c * 21, y + 26 + r * 17, x + 40 + c * 21, y + 37 + r * 17], fill=(250, 220, 120))
    d.rectangle([x + 128, y + 14, x + 162, y + 48], fill=(255, 255, 255), outline=RED, width=2)
    d.rectangle([x + 141, y + 20, x + 149, y + 42], fill=RED)
    d.rectangle([x + 134, y + 27, x + 156, y + 35], fill=RED)
    d.text((x + 106, y + 56), "SANOFI", font=F(SANS_B, 17), fill=NAVY)
    # pill bottle being bought: bottle + big price
    d.rectangle([x + 188, y + 30, x + 216, y + 78], fill=(245, 180, 40), outline=INK, width=2)
    d.rectangle([x + 192, y + 20, x + 212, y + 30], fill=INK)
    d.ellipse([x + 194, y + 44, x + 206, y + 56], fill=(255, 255, 255))
    d.ellipse([x + 202, y + 58, x + 214, y + 70], fill=(255, 255, 255))
    d.text((x + 224, y + 20), "$41BN", font=F(SERIF_B, 25), fill=DARKRED)
    d.text((x + 224, y + 52), "$175/SHARE CASH", font=F(SANS_B, 10), fill=INK)
    d.text((x + 224, y + 66), "PREMIUM +46%", font=F(SANS_B, 10), fill=GREEN)

def scene_taiex(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for gx in range(x + 20, x + w, 34):
        d.line([gx, y + 6, gx, y + h - 18], fill=(38, 66, 108), width=1)
    for gy in range(y + 12, y + h - 14, 20):
        d.line([x + 8, gy, x + w - 8, gy], fill=(38, 66, 108), width=1)
    pts = [(x + 14, y + h - 26), (x + 70, y + h - 34), (x + 118, y + h - 52),
           (x + 168, y + h - 46), (x + 216, y + h - 68), (x + 268, y + 20)]
    d.line(pts, fill=(64, 224, 130), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(64, 224, 130))
    d.polygon([(x + 268, y + 8), (x + 282, y + 26), (x + 258, y + 28)], fill=(64, 224, 130))
    # chip
    d.rectangle([x + 16, y + 12, x + 62, y + 46], fill=(24, 24, 24), outline=(64, 224, 130), width=2)
    d.text((x + 27, y + 22), "AI", font=F(SANS_B, 16), fill=(255, 255, 255))
    for i in range(3):
        d.line([x + 22 + i * 14, y + 6, x + 22 + i * 14, y + 12], fill=GOLD, width=3)
        d.line([x + 22 + i * 14, y + 46, x + 22 + i * 14, y + 52], fill=GOLD, width=3)
    d.text((x + 178, y + h - 20), "TSMC + MEDIATEK LIMIT-UP", font=F(SANS_B, 9), fill=(200, 220, 245))

def scene_hormuz(x, y, w, h):
    vgrad(x, y, w, 44, (232, 168, 96), (250, 205, 130))
    d.rectangle([x, y + 44, x + w, y + h], fill=(52, 110, 160))
    for i in range(6):
        sx = x + 16 + i * 52
        d.arc([sx, y + h - 14, sx + 30, y + h - 2], 0, 180, fill=(160, 205, 235), width=2)
    # tanker hull + superstructure
    d.polygon([(x + 52, y + 62), (x + 252, y + 62), (x + 236, y + 82), (x + 70, y + 82)], fill=(30, 30, 34))
    d.rectangle([x + 66, y + 44, x + 148, y + 62], fill=(168, 44, 44))
    d.rectangle([x + 200, y + 34, x + 232, y + 62], fill=(238, 240, 244), outline=INK, width=1)
    d.rectangle([x + 210, y + 24, x + 222, y + 34], fill=INK)
    # flames and mine bursts
    for fx in (96, 128):
        d.polygon([(x + fx, y + 44), (x + fx + 9, y + 22), (x + fx + 15, y + 34),
                   (x + fx + 19, y + 44)], fill=(232, 110, 26))
    burst(x + 268, y + 58, 17, RED)
    burst(x + 34, y + 72, 12, (232, 110, 26))
    d.ellipse([x + 282, y + 70, x + 296, y + 84], outline=INK, width=2)
    d.text((x + 12, y + 6), "STRAIT OF HORMUZ", font=F(SANS_B, 13), fill=DARKRED)
    d.text((x + 190, y + 6), "3 MORE HIT", font=F(SERIF_B, 19), fill=INK)

# ================================================================ heroes
HEROES = [
    (1, "EUROPE - BUSINESS", "PARIS", "CONFIRMED", "Sanofi PR - Reuters", scene_sanofi,
     "SANOFI BUYS INSMED - $41BN",
     "Announced in Paris Tuesday: $175 a share cash, EUR37.6bn - biggest pharma "
     "takeover since Pfizer-SeaGen 2023, at a 46% premium."),
    (2, "ASIA - MARKETS", "TAIPEI - SEOUL - TOKYO", "CONFIRMED", "AP - Bloomberg", scene_taiex,
     "TAIEX +9.0% - ASIA'S CHIP RALLY",
     "Taiwan's biggest daily gain in over a year (+3,300 pts intraday, a record). "
     "KOSPI +6.5% to 5,014, Nikkei +3.9%; Nvidia +31.5% Monday."),
    (3, "MIDDLE EAST - SHIPPING", "STRAIT OF HORMUZ", "CLAIM", "IRGC via IRNA - Reuters", scene_hormuz,
     "HORMUZ: 3 MORE TANKERS HIT MINES, IRAN SAYS",
     "The IRGC says three more tankers struck mines and caught fire despite a US "
     "escort; Tehran warns ships to obey its traffic rules. Unverified claim."),
]
HY, HH, HGAP = 214, 200, 8
HW = (W - 2 * M - 2 * HGAP) // 3
for i, (num, kicker, place, tag, src, scene, head, body) in enumerate(HEROES):
    x = M + i * (HW + HGAP)
    d.rectangle([x + 3, HY + 4, x + HW + 3, HY + HH + 4], fill=(226, 218, 198))
    d.rectangle([x, HY, x + HW, HY + HH], fill=PAPER2, outline=INK, width=2)
    scene(x + 2, HY + 2, HW - 4, 80)
    ky = HY + 86
    d.rectangle([x, ky, x + HW, ky + 16], fill=REGION_COLORS[
        "EUROPE" if num == 1 else ("ASIA" if num == 2 else "MIDDLE EAST")])
    d.ellipse([x + 5, ky + 1, x + 19, ky + 15], fill=(255, 255, 255))
    nf = F(SANS_B, 10)
    nw_ = d.textlength(str(num), font=nf)
    d.text((x + 12 - nw_ / 2, ky + 2), str(num), font=nf, fill=INK)
    d.text((x + 24, ky + 3), kicker, font=F(SANS_B, 10), fill=(255, 255, 255))
    tag_chip(x + HW - 4, ky + 1, tag, TAG_COLORS[tag])
    hy = block(x + 8, ky + 19, head, F(SERIF_B, 18), INK, HW - 16, 20, max_lines=2)
    block(x + 8, hy + 1, body, F(SANS_R, 11), SOFT, HW - 16, 13, max_lines=3)
    d.text((x + 8, HY + HH - 13), place + "  -  " + src, font=F(SANS_B, 9), fill=GREY)

# ================================================================ grid of 12
# (num, region, place, tag, source, big stat, stat label, headline, body)
GRID = [
    (4, "ASIA", "SHANGHAI", "OFFICIAL", "Xinhua - Reuters", "4th", "POLITBURO FALL",
     "SHANGHAI PURGE: CHEN JINING PROBED",
     "Shanghai party boss and Politburo member investigated, Xinhua announced Tuesday."),
    (5, "EUROPE", "ZAPORIZHZHIA", "OFFICIAL", "Regional admin - Kyiv Ind.", "40+", "WOUNDED",
     "ZAPORIZHZHIA: 2 DEAD, 40+ WOUNDED",
     "Night strike about 04:00: 10+ guided bombs, a 5-storey block hit, 4 children hurt."),
    (6, "AFRICA", "LAUSANNE - DAKAR", "CONFIRMED", "CAS - AP", "1-0", "FINAL SCORE STANDS",
     "SENEGAL RECLAIM AFRICA CUP",
     "CAS ruled unanimously Tuesday: AFCON title restored; 1-0 win over Morocco stands."),
    (7, "AMERICAS", "CARTAGENA", "ONGOING", "Reuters", "+/-30", "SEIZED IN STORE",
     "CARTAGENA: +/-30 SEIZED IN SUPERMARKET",
     "Siege from about 08:00 after a failed cash-truck raid; 10 hostages freed in stages."),
    (8, "AMERICAS", "NEW YORK", "CONFIRMED", "DOJ - AFP", "10/12", "COUNTS GUILTY",
     "HUAWEI GUILTY ON 10 COUNTS",
     "Federal jury, Tuesday: bank fraud & trade-secret conspiracy; no racketeering."),
    (9, "EUROPE", "POLAND", "REPORTED", "Reuters roundup", "AWACS", "SENT TO POLAND",
     "NATO AWACS TO POLAND",
     "NATO sends AWACS as Russian drones reported in Polish airspace; Trump meets Rutte."),
    (10, "ASIA", "DHAKA", "REPORTED", "Reuters", "16 DEC", "PROMISED RETURN",
     "HASINA VOWS RETURN DEC 16",
     "The ex-PM, in exile and under a death sentence, promises to come home on 16 December."),
    (11, "ASIA", "CIKANDE, BANTEN", "OFFICIAL", "AP - Xinhua", "26", "DEAD, 8 MISSING",
     "CIKANDE FIRE TOLL RISES TO 26",
     "Police confirm 26 dead Tuesday in Saturday's candy-factory fire; criminal probe opened."),
    (12, "ASIA", "KOSHI, NEPAL", "REPORTED", "EMSC - Horizon", "M5.6", "QUAKE, 10 KM DEEP",
     "NEPAL: M5.6 QUAKE NEAR CHINA BORDER",
     "Morning quake at Taplejung, Koshi (EMSC logs 5.3); felt in India & China, no casualties."),
    (13, "AMERICAS", "MEXICO", "REPORTED", "Mexican officials - AP", "1", "CARTEL BOSS HELD",
     "MEXICO TO TRY 'EL CHAPO ISIDRO' AT HOME",
     "Captured boss Fausto Isidro Meza Flores will be tried in Mexico, not extradited to the US."),
    (14, "MIDDLE EAST", "GAZA", "REPORTED", "Reports", "7", "KILLED IN STRIKE",
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Naeem Abu Nahel, Hamas's internal security chief, killed with 6 others, reports say."),
    (15, "MIDDLE EAST", "RIYADH", "REPORTED", "Reports", "11+", "WOUNDED",
     "DRONE HITS RIYADH TOWER",
     "A drone hits the tower housing the PIF headquarters in Riyadh; at least 11 wounded."),
]
GY, GH, GGAP = 422, 90, 6
GW = (W - 2 * M - 3 * GGAP) // 4
for i, (num, region, place, tag, src, stat, statlab, head, body) in enumerate(GRID):
    col, row = i % 4, i // 4
    x, y = M + col * (GW + GGAP), GY + row * (GH + GGAP)
    d.rectangle([x + 2, y + 3, x + GW + 2, y + GH + 3], fill=(228, 220, 200))
    d.rectangle([x, y, x + GW, y + GH], fill=PAPER2, outline=INK, width=1)
    d.rectangle([x, y, x + GW, y + 4], fill=REGION_COLORS[region])
    # stat block
    d.rectangle([x + 5, y + 10, x + 55, y + 52], fill=(238, 231, 214), outline=GREY, width=1)
    ssf = fit_size(stat, SERIF_B, 17, 46)
    sff = F(SERIF_B, ssf)
    sw_ = d.textlength(stat, font=sff)
    d.text((x + 30 - sw_ / 2, y + 15), stat, font=sff, fill=DARKRED)
    for j, line in enumerate(wrap(statlab, F(SANS_B, 7), 48)):
        lf = F(SANS_B, 7)
        lw = d.textlength(line, font=lf)
        d.text((x + 30 - lw / 2, y + 36 + j * 8), line, font=lf, fill=SOFT)
    # number badge + place + tag
    d.ellipse([x + 60, y + 9, x + 74, y + 23], fill=INK)
    nf = F(SANS_B, 9)
    nw_ = d.textlength(str(num), font=nf)
    d.text((x + 67 - nw_ / 2, y + 11), str(num), font=nf, fill=(255, 255, 255))
    d.text((x + 78, y + 11), place, font=F(SANS_B, 9), fill=BLUE)
    tag_chip(x + GW - 4, y + 8, tag, TAG_COLORS[tag])
    hy = block(x + 60, y + 25, head, F(SERIF_B, 13), INK, GW - 66, 14, max_lines=2)
    block(x + 6, y + 54, body, F(SANS_R, 10), SOFT, GW - 12, 11, max_lines=2)
    d.text((x + 6, y + GH - 10), src, font=F(SANS_B, 8), fill=GREY)

# ================================================================ world map
LAND = (214, 203, 168)
SEA = (172, 198, 220)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 62),
     (-76, 58), (-65, 50), (-70, 44), (-74, 40), (-76, 35), (-80, 32), (-80, 26),
     (-84, 30), (-89, 29), (-97, 26), (-97, 22), (-94, 17), (-87, 13), (-83, 9),
     (-90, 14), (-105, 20), (-110, 23), (-114, 29), (-117, 33), (-122, 37),
     (-124, 46), (-130, 55), (-152, 60), (-165, 60)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-70, -18), (-70, -23),
     (-70, -30), (-71, -38), (-73, -44), (-74, -50), (-69, -54), (-66, -55),
     (-68, -50), (-65, -45), (-62, -41), (-58, -34), (-48, -28), (-41, -23),
     (-39, -17), (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-53, 4), (-60, 8),
     (-68, 10), (-72, 12), (-77, 7)],
    [(-9, 43), (-9, 37), (-6, 36), (0, 39), (3, 42), (7, 44), (10, 44), (12, 42),
     (15, 44), (19, 45), (23, 40), (26, 38), (23, 36), (28, 45), (30, 46),
     (28, 54), (24, 58), (18, 56), (12, 58), (8, 55), (3, 53), (-2, 50), (-5, 48), (-2, 44)],
    [(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-6, 58), (-8, 55), (-6, 52)],
    [(5, 58), (5, 60), (10, 62), (14, 65), (20, 69), (28, 71), (31, 70), (30, 65),
     (25, 60), (21, 60), (18, 59), (12, 56), (8, 57)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
     (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2), (40, -10),
     (40, -18), (37, -22), (35, -27), (32, -29), (26, -34), (20, -35), (17, -32),
     (15, -27), (13, -18), (12, -15), (9, -5), (9, 0), (8, 4), (-8, 4), (-13, 8),
     (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-10, 31)],
    [(26, 41), (40, 43), (50, 40), (55, 45), (62, 50), (72, 54), (85, 58), (100, 60),
     (115, 60), (130, 60), (145, 58), (160, 58), (175, 64), (178, 62), (170, 59),
     (162, 57), (158, 52), (150, 50), (142, 48), (140, 42), (135, 35), (129, 33),
     (126, 38), (122, 37), (120, 30), (121, 25), (115, 22), (108, 18), (109, 12),
     (106, 8), (104, 2), (100, 6), (98, 10), (97, 15), (93, 17), (91, 22), (88, 21),
     (85, 19), (80, 13), (77, 8), (76, 10), (73, 16), (70, 21), (67, 24), (61, 25),
     (57, 26), (53, 27), (50, 26), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (30, 36), (27, 37)],
    [(43, 12), (45, 12), (50, 15), (55, 17), (58, 20), (59, 22), (56, 26), (52, 25),
     (50, 29), (48, 30), (47, 29), (43, 28), (42, 32), (39, 35), (36, 36),
     (35, 33), (34, 31), (36, 29), (39, 21), (40, 15)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44), (140, 45),
     (138, 38), (135, 34), (131, 32)],
    [(95, 5), (100, 2), (105, -2), (102, -4), (97, -3), (94, 2)],
    [(106, -1), (113, -3), (119, -2), (114, -5), (107, -5)],
    [(120, -1), (126, -2), (131, -3), (128, -5), (121, -4)],
    [(131, -2), (138, -3), (145, -5), (141, -7), (133, -5)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32),
     (135, -35), (138, -36), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (151, -24), (146, -19), (143, -15), (142, -11), (137, -12),
     (135, -15), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (172, -41), (174, -39), (176, -38), (174, -41), (169, -46), (166, -46)],
]
PINS = [  # story number, pin lon, pin lat, true lon, true lat (dot, if pin is offset)
    (1, 2.3, 48.9, None, None), (2, 129.0, 19.0, 121.0, 24.5),
    (3, 60.0, 20.0, 56.3, 26.5), (4, 121.5, 31.2, None, None),
    (5, 35.2, 47.8, None, None), (6, -17.4, 14.7, None, None),
    (7, -75.5, 10.4, None, None), (8, -74.0, 40.7, None, None),
    (9, 19.0, 52.0, None, None), (10, 95.0, 18.5, 90.4, 23.8),
    (11, 106.3, -6.3, None, None), (12, 86.5, 28.5, None, None),
    (13, -107.5, 24.8, None, None), (14, 34.3, 31.5, None, None),
    (15, 46.7, 24.6, None, None),
]
BY, MAPW = 712, 330
MX, MY, MW, MH = M + 4, BY + 22, MAPW - 8, 128
d.text((M, BY), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
d.text((M + 168, BY + 2), "pins carry story numbers 1-15", font=F(SANS_R, 10), fill=SOFT)
d.rectangle([M, BY + 18, M + MAPW, BY + 18 + 136], fill=SEA, outline=INK, width=1)
def to_xy(lon, lat):
    return (MX + (lon + 180) / 360.0 * MW, MY + (75 - lat) / 135.0 * MH)
for poly in CONTINENTS:
    d.polygon([to_xy(lon, lat) for lon, lat in poly], fill=LAND, outline=(150, 138, 105))
for lon, lat, name in [(-102, 57, "NORTH AMERICA"), (-60, -20, "SOUTH AMERICA"),
                       (20, 6, "AFRICA"), (88, 52, "ASIA"), (140, -29, "OCEANIA")]:
    lx, ly = to_xy(lon, lat)
    lf = F(SANS_B, 7)
    d.text((lx - d.textlength(name, font=lf) / 2, ly), name, font=lf, fill=(133, 118, 84))
for lon in (-120, -60, 0, 60, 120):
    gx, _ = to_xy(lon, 0)
    d.line([gx, MY, gx, MY + MH], fill=(190, 212, 228), width=1)
for num, lon, lat, tlon, tlat in PINS:
    px, py = to_xy(lon, lat)
    if tlon is not None:
        tx_, ty_ = to_xy(tlon, tlat)
        d.line([px, py, tx_, ty_], fill=RED, width=1)
        d.ellipse([tx_ - 2.5, ty_ - 2.5, tx_ + 2.5, ty_ + 2.5], fill=RED)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    nf = F(SANS_B, 8 if num < 10 else 7)
    nw_ = d.textlength(str(num), font=nf)
    d.text((px - nw_ / 2, py - 4), str(num), font=nf, fill=(255, 255, 255))
d.text((M, BY + 160), "1 Paris - 2 Taipei - 3 Hormuz - 4 Shanghai - 5 Zaporizhzhia - 6 Dakar", font=F(SANS_R, 9), fill=SOFT)
d.text((M, BY + 172), "7 Cartagena - 8 New York - 9 Poland - 10 Dhaka - 11 Cikande - 12 Nepal", font=F(SANS_R, 9), fill=SOFT)
d.text((M, BY + 184), "13 Mexico - 14 Gaza - 15 Riyadh", font=F(SANS_R, 9), fill=SOFT)

# ================================================================ ticker 21
TICKER = [
    (16, "Zelensky: US envoys push for peace deal by January", "Kyiv"),
    (17, "Bangladesh garment workers clash with police", "Reuters"),
    (18, "175 migrants missing from a Senegal boat", "Reuters"),
    (19, "Israel: Eisenkot signs first coalition deal", "Reuters"),
    (20, "Iraq orders control of Kurdish oilfields", "Reuters"),
    (21, "UK sanctions Houthis & 4 senior officials", "Reports"),
    (22, "Houthis 60 km from Aden; Yemen warns city won't fall", "Reports"),
    (23, "Colombia car bomb injures 23 in Villavicencio", "Reports"),
    (24, "China sentences official Ma to death for spying", "Reports"),
    (25, "Indonesia names Amran & Sugiono as VP candidates", "Reports"),
    (26, "Malaysia to return 6,500 Rohingya to Myanmar", "Reports"),
    (27, "14 nations back ICJ Rohingya ruling; UK sanctions Myanmar officers", "Reuters"),
    (28, "Tripoli demands Kyiv explain Benghazi strike on Russian vessels", "Reports"),
    (29, "Hanoi restaurant blast kills 6; suspected gas leak", "Reports"),
    (30, "Helicopter crash kills 5 crew on training flight, Turkiye", "Reports"),
    (31, "Russian jets enter Korea air zone; fighters scrambled", "AP"),
    (32, "Rescuers search for dozens trapped in flooded Pongkor mine", "Reports"),
    (33, "UN: 47,000 women killed by partners or kin in 2025, five an hour", "UNODC"),
    (34, "Pakistan's Zeeshan Ali joins Shenzhou-24 crew to Tiangong", "Reuters"),
    (35, "FT: 60 Patriot interceptors for Ukraine await US sign-off", "FT"),
    (36, "Germany first to tap Ukraine's Delta battlefield system", "Reuters"),
    (37, "Landmine casualties hit 5-year high: 6,929 in 2025", "Monitor"),
    (38, "US consumer confidence jumps to 103.3 in November", "Conf. Board"),
]
TX = M + MAPW + 14
d.rectangle([TX, BY, W - M, BY + 18], fill=INK)
d.text((TX + 8, BY + 3), "ALSO ON TUESDAY - 23 MORE STORIES", font=F(SANS_B, 12), fill=(250, 214, 120))
tr = "one line each, with its source"
trw = d.textlength(tr, font=F(SANS_R, 10))
d.text((W - M - trw - 8, BY + 4), tr, font=F(SANS_R, 10), fill=(220, 214, 198))
colw = (W - M - TX - 10) // 2
for i, (num, line, src) in enumerate(TICKER):
    col, row = i // 12, i % 12
    x = TX + col * (colw + 10)
    y = BY + 24 + row * 14
    d.ellipse([x, y + 1, x + 14, y + 14], fill=NAVY)
    nf = F(SANS_B, 8)
    nw_ = d.textlength(str(num), font=nf)
    d.text((x + 7 - nw_ / 2, y + 3), str(num), font=nf, fill=(255, 255, 255))
    text = line + " (" + src + ")"
    fs = fit_size(text, SANS_R, 11, colw - 20)
    d.text((x + 19, y + 2), text, font=F(SANS_R, fs), fill=INK)

# ================================================================ date check + footer
DY = 906
d.rectangle([M, DY, W - M, DY + 62], fill=(250, 246, 234), outline=RED, width=2)
d.rectangle([M, DY, M + 92, DY + 62], fill=RED)
d.text((M + 10, DY + 12), "DATE", font=F(SERIF_B, 17), fill=(255, 255, 255))
d.text((M + 10, DY + 32), "CHECK", font=F(SERIF_B, 17), fill=(255, 255, 255))
d.text((M + 102, DY + 5), "Stories left out because they happened on other days - checked, not counted:", font=F(SANS_B, 11), fill=DARKRED)
checks = [
    "Mon 23 Nov: Nvidia board reinstates Huang as CEO (Tuesday's story is Asia's rally, #2) - Pentagon rebukes Canada.",
    "Sun 22 Nov: COP31 collapses in Antalya - Mon 23 Nov: Kilauea's 57th lava fountain, Hawaii.",
    "Sat-Sun 22-23 Nov: Ukraine's Libya strike on Russian vessels (claimed 23 Nov).",
    "Mon 23 Nov night: Pongkor mine floods (the search continues today, #32).",
]
for j, line in enumerate(checks):
    d.text((M + 102, DY + 21 + j * 10), line, font=F(SANS_R, 10), fill=INK)

FY = 974
d.line([M, FY - 4, W - M, FY - 4], fill=INK, width=1)
legend = ("CONFIRMED = named source / official release   OFFICIAL = government or agency statement   "
          "REPORTED = reported, single-outlet or roundup   CLAIM = one side's account   ONGOING = still unfolding")
ls = fit_size(legend, SANS_B, 10, W - 2 * M)
d.text((M, FY + 2), legend, font=F(SANS_B, ls), fill=INK)
foot = ("Every story here happened, or was first reported, on Tuesday 24 November 2026, as the named outlets reported it. "
        "Map pins 1-15 match the hero and grid stories. All drawings are original programmatic art, drawn in code for this entry.")
fs2 = fit_size(foot, SANS_R, 10, W - 2 * M)
d.text((M, FY + 18), foot, font=F(SANS_R, fs2), fill=SOFT)
d.text((M, FY + 34), "THE WORLD IN ONE PAGE - Tuesday 24 November 2026 - 38 stories", font=F(SANS_B, 10), fill=DARKRED)

img.save("entry.png", optimize=True)
print("saved entry.png")
