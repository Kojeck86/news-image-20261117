#!/usr/bin/env python3
"""news-image-20261117: one-page newspaper front page summing up the world
news of Tuesday 17 November 2026.

Pure Python 3.13 standard library (zlib, struct, os). No network, no
system fonts: text is rendered with an embedded 5x7 bitmap font and every
picture is drawn procedurally. Deterministic: the same bytes every run.

Writes entry.png (1024x1024, PNG) to $MAKEFUN_OUTPUT_DIR or /output.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
CREAM = (246, 241, 227)
BLUE = (46, 90, 136)
WATER = (62, 110, 158)
SKY = (220, 231, 240)
PANEL = (234, 240, 246)
GREY = (138, 138, 138)
DARKGREY = (90, 96, 104)
ORANGE = (230, 120, 40)
SMOKE = (154, 160, 166)
TEAL = (47, 111, 106)
WHITE = (255, 255, 255)

# ------------------------------------------------------- 5x7 bitmap font
# Each glyph: 7 rows of 5 cells, '#' = on, '.' = off.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '•': ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}
# Map look-alikes onto glyphs we have.
ALIASES = {'—': '-', '–': '-', '’': "'", '‘': "'", '“': '"', '”': '"'}
FONT['"'] = ("01010", "01010", "01010", "00000", "00000", "00000", "00000")


def glyph(ch):
    ch = ch.upper()
    if ch in ALIASES:
        ch = ALIASES[ch]
    return FONT.get(ch, FONT[' '])


def text_width(text, scale):
    return len(text) * 6 * scale - scale if text else 0


def wrap_text(text, max_chars):
    """Word-wrap to lines of at most max_chars characters."""
    words = text.split(' ')
    lines = []
    cur = ''
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += ' ' + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def hline(self, x0, x1, y, c, t=1):
        if x0 > x1:
            x0, x1 = x1, x0
        self.fill_rect(x0, y, x1 - x0 + 1, t, c)

    def vline(self, x, y0, y1, c, t=1):
        if y0 > y1:
            y0, y1 = y1, y0
        self.fill_rect(x, y0, t, y1 - y0 + 1, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if t <= 1:
                self.set(x0, y0, c)
            else:
                self.fill_rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        if fill:
            for dy in range(-r, r + 1):
                dx = int((r * r - dy * dy) ** 0.5)
                self.hline(cx - dx, cx + dx, cy + dy, c)
        else:
            steps = max(24, r * 4)
            for i in range(steps):
                import math
                a = 2 * math.pi * i / steps
                self.set(cx + int(r * math.cos(a)), cy + int(r * math.sin(a)), c)

    def ellipse(self, cx, cy, rx, ry, c):
        for dy in range(-ry, ry + 1):
            dx = int(rx * (1 - (dy * dy) / (ry * ry)) ** 0.5) if ry else 0
            self.hline(cx - dx, cx + dx, cy + dy, c)

    def polygon(self, pts, c):
        """Scanline fill of a simple polygon (list of (x, y))."""
        if not pts:
            return
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.hline(int(xs[j]), int(xs[j + 1]), y, c)

    def text(self, x, y, s, scale, c):
        for ch in s:
            g = glyph(ch)
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '1':
                        self.fill_rect(x + col * scale, y + r * scale,
                                       scale, scale, c)
            x += 6 * scale

    def text_block(self, x, y, s, scale, c, max_w, leading=None):
        """Wrapped text; returns y after the last line."""
        if leading is None:
            leading = 7 * scale + 4
        max_chars = max(1, max_w // (6 * scale))
        for line in wrap_text(s, max_chars):
            self.text(x, y, line, scale, c)
            y += leading
        return y


# ------------------------------------------------------------ illustrations
def draw_bridge_panel(cv, x, y, w, h):
    """Kerch bridge over the sea, middle span collapsed, smoke rising."""
    cv.fill_rect(x, y, w, h, SKY)
    # sun haze
    cv.circle(x + w - 70, y + 34, 22, (240, 225, 170))
    # water
    cv.fill_rect(x, y + h - 58, w, 58, WATER)
    for wy in (y + h - 44, y + h - 28, y + h - 12):
        for wx in range(x + 8, x + w - 8, 46):
            cv.hline(wx, wx + 22, wy, (120, 165, 205), 2)
    deck_y = y + h - 92
    # towers
    for tx in (x + 150, x + w - 170):
        cv.fill_rect(tx, deck_y - 62, 10, 62, INK)
        cv.fill_rect(tx - 14, deck_y - 68, 38, 6, INK)
    # cables from towers to deck
    for tx in (x + 155, x + w - 165):
        for ddx in (-120, -60, 60, 120):
            cv.line(tx, deck_y - 62, tx + ddx, deck_y, INK, 1)
    # deck, left and right of the collapsed gap
    gap0, gap1 = x + w // 2 - 52, x + w // 2 + 52
    cv.fill_rect(x + 16, deck_y, gap0 - x - 16, 7, INK)
    cv.fill_rect(gap1, deck_y, x + w - 16 - gap1, 7, INK)
    # collapsed stubs angled into the water
    cv.line(gap0, deck_y + 3, gap0 + 26, deck_y + 62, INK, 5)
    cv.line(gap1, deck_y + 3, gap1 - 26, deck_y + 62, INK, 5)
    # pillars
    for px in (x + 60, x + 260, x + w - 260, x + w - 60):
        cv.fill_rect(px, deck_y + 7, 8, h - 92 - 7 - 58 + 14, DARKGREY)
    # explosion star at the gap
    cx, cy = x + w // 2, deck_y + 26
    for ang in range(0, 360, 30):
        import math
        r = 26
        cv.line(cx, cy, cx + int(r * math.cos(math.radians(ang))),
                cy + int(r * math.sin(math.radians(ang))), ORANGE, 3)
    cv.circle(cx, cy, 12, RED)
    cv.circle(cx - 4, cy - 3, 5, ORANGE)
    # smoke rising
    cv.circle(cx - 26, deck_y - 22, 16, SMOKE)
    cv.circle(cx + 6, deck_y - 44, 20, SMOKE)
    cv.circle(cx + 30, deck_y - 66, 14, SMOKE)
    # label
    cv.fill_rect(x + 10, y + 10, 196, 26, NAVY)
    cv.text(x + 18, y + 16, "KERCH BRIDGE", 2, CREAM)
    # Kyiv inset box
    bx, by, bw, bh = x + w - 372, y + h - 52, 360, 44
    cv.fill_rect(bx, by, bw, bh, NAVY)
    cv.text(bx + 10, by + 6, "KYIV: MISSILES HIT NORTH", 2, CREAM)
    cv.text(bx + 10, by + 24, "AND SOUTH BRIDGES", 2, CREAM)


def draw_radar(cv, x, y, w, h):
    """Radar dish with a drone above it."""
    cv.fill_rect(x, y, w, h, PANEL)
    # ground
    cv.fill_rect(x, y + h - 18, w, 18, (200, 210, 200))
    # mast
    mx = x + w // 2 - 30
    cv.vline(mx, y + 78, y + h - 18, INK, 4)
    # dish: arc with a chord and one support spoke
    import math
    hx, hy = mx, y + 78
    pts = []
    for a in range(-75, 15, 5):
        r = 52
        pts.append((hx + int(r * math.cos(math.radians(a))),
                    hy + int(r * math.sin(math.radians(a))) - 8))
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], BLUE, 2)
    cv.line(pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], BLUE, 2)
    cv.line(hx, hy, pts[len(pts) // 2][0], pts[len(pts) // 2][1], BLUE, 2)
    # sweep line
    cv.line(hx, hy, hx + 58, hy - 44, TEAL, 2)
    # drone top-right
    dx, dy = x + w - 42, y + 30
    cv.fill_rect(dx - 10, dy - 3, 20, 6, INK)
    cv.circle(dx - 12, dy - 6, 5, INK)
    cv.circle(dx + 12, dy - 6, 5, INK)
    cv.hline(dx - 20, dx - 4, dy - 8, INK, 2)
    cv.hline(dx + 4, dx + 20, dy - 8, INK, 2)
    cv.line(dx - 34, dy + 14, dx - 14, dy + 4, RED, 2)
    cv.line(dx - 34, dy + 22, dx - 14, dy + 12, RED, 2)


def draw_plane(cv, x, y, w, h):
    """Airliner in flight, three flag bars below (US / China / Russia)."""
    cv.fill_rect(x, y, w, h, PANEL)
    # clouds
    cv.ellipse(x + 30, y + 26, 26, 9, WHITE)
    cv.ellipse(x + w - 34, y + 96, 30, 10, WHITE)
    # fuselage
    fy = y + 62
    cv.line(x + 14, fy, x + w - 30, fy, BLUE, 7)
    cv.polygon([(x + w - 30, fy - 4), (x + w - 8, fy), (x + w - 30, fy + 4)],
               BLUE)
    # tail fin
    cv.polygon([(x + 22, fy - 3), (x + 34, fy - 26), (x + 46, fy - 3)], BLUE)
    # wing
    cv.polygon([(x + w // 2 - 6, fy), (x + w // 2 + 22, fy + 26),
                (x + w // 2 + 34, fy + 26), (x + w // 2 + 10, fy)], TEAL)
    # windows
    for wx in range(x + 34, x + w - 44, 12):
        cv.set(wx, fy - 1, WHITE)
        cv.set(wx, fy, WHITE)
    # contrail
    cv.hline(x + 8, x + 26, fy + 12, WHITE, 2)
    cv.hline(x + 8, x + 20, fy + 18, WHITE, 2)
    # three flag bars
    fy2 = y + h - 30
    bw = (w - 24) // 3
    # US: red/white stripes
    for i in range(4):
        cv.fill_rect(x + 8, fy2 + i * 6, bw - 6, 3,
                     RED if i % 2 == 0 else WHITE)
    # China: red field, gold star dot
    cv.fill_rect(x + 8 + bw, fy2, bw - 6, 24, RED)
    cv.circle(x + 8 + bw + 10, fy2 + 7, 3, GOLD)
    # Russia: white / blue / red bars
    cv.fill_rect(x + 8 + 2 * bw, fy2, bw - 6, 8, WHITE)
    cv.fill_rect(x + 8 + 2 * bw, fy2 + 8, bw - 6, 8, BLUE)
    cv.fill_rect(x + 8 + 2 * bw, fy2 + 16, bw - 6, 8, RED)


def draw_jet(cv, x, y, w, h):
    """Delta jet climbing, red sun (Japan) and contrails."""
    cv.fill_rect(x, y, w, h, PANEL)
    # rising sun
    cv.circle(x + w - 30, y + 28, 18, RED)
    # contrails
    cv.line(x + 10, y + h - 30, x + w // 2, y + 78, WHITE, 3)
    cv.line(x + 10, y + h - 18, x + w // 2 - 8, y + 92, WHITE, 3)
    # jet: delta wings + fuselage
    nx, ny = x + w - 34, y + 44  # nose
    cv.polygon([(nx, ny), (nx - 58, ny + 26), (nx - 34, ny + 30),
                (nx - 30, ny + 44), (nx - 52, ny + 52), (nx - 18, ny + 34)],
               NAVY)
    cv.line(nx, ny, nx - 34, ny + 30, NAVY, 5)
    cv.circle(nx - 12, ny + 10, 3, GOLD)


def draw_scales(cv, x, y, w, h):
    """Scales of justice on a plinth."""
    cv.fill_rect(x, y, w, h, PANEL)
    cx = x + w // 2
    # plinth
    cv.fill_rect(cx - 34, y + h - 26, 68, 10, INK)
    # post
    cv.vline(cx, y + 34, y + h - 26, INK, 4)
    # crossbar
    cv.hline(cx - 46, cx + 46, y + 40, INK, 4)
    # chains + pans
    for sx in (cx - 46, cx + 46):
        cv.line(sx, y + 42, sx - 16, y + 78, INK, 2)
        cv.line(sx, y + 42, sx + 16, y + 78, INK, 2)
        cv.polygon([(sx - 18, y + 78), (sx + 18, y + 78), (sx, y + 96)],
                   GOLD)
    # top finial
    cv.circle(cx, y + 28, 5, GOLD)


# -------------------------------------------------------------------- page
def build():
    cv = Canvas(W, H, PAPER)
    mx = 24
    cw = W - 2 * mx  # 976

    # ---- masthead
    cv.fill_rect(0, 0, W, 96, NAVY)
    cv.text(mx, 20, "THE WORLD", 6, CREAM)
    cv.text(mx, 70, "TUESDAY, 17 NOVEMBER 2026", 2, GOLD)
    # small globe, top right: outline, equator, meridian arc
    import math
    gx, gy = W - 66, 48
    cv.circle(gx, gy, 28, CREAM, fill=False)
    cv.vline(gx, gy - 28, gy + 28, CREAM, 1)
    cv.hline(gx - 28, gx + 28, gy, CREAM, 1)
    for a in range(0, 360, 5):
        cv.set(gx + int(13 * math.cos(math.radians(a))),
               gy + int(28 * math.sin(math.radians(a))), CREAM)
    cv.fill_rect(0, 96, W, 4, RED)

    # ---- lead story
    y = 116
    cv.text(mx, y, "UKRAINE WAR - BRIDGES UNDER FIRE", 2, RED)
    y = 140
    cv.text(mx, y, "BRIDGES UNDER FIRE", 6, INK)
    y = 196
    y = cv.text_block(
        mx, y,
        "Kerch road span collapses into the sea as Russian missiles hit "
        "Kyiv's North and South bridges over the Dnipro - heat, water and "
        "power cut.", 2, INK, cw)
    draw_bridge_panel(cv, mx, 252, cw, 188)
    cv.hline(mx, mx + cw - 1, 456, INK, 2)

    # ---- secondary stories, 2 x 2 grid
    cells = [
        (mx, 472, draw_radar,
         "IRAN DRONE HITS US RADAR IN BAHRAIN",
         "US carrier arrives; tanker struck near Hormuz"),
        (mx + 508, 472, draw_plane,
         "TRUMP FLIES TO ASIA FOR APEC TALKS",
         "Trilateral with Xi and Putin set for 19 Nov"),
        (mx, 662, draw_jet,
         "JAPAN SCRAMBLES JETS",
         "Russian planes 'violate airspace', Tokyo protests"),
        (mx + 508, 662, draw_scales,
         "UK SANCTIONS SETTLEMENT BUILDERS",
         "Eight Israeli firms blacklisted; settler kills woman, 72, in Jericho"),
    ]
    for cx, cy, draw, head, cap in cells:
        cv.rect(cx, cy, 468, 170, GREY, 1)
        draw(cv, cx + 8, cy + 8, 140, 154)
        tx = cx + 160
        ty = cy + 14
        ty = cv.text_block(tx, ty, head, 3, INK, 296)
        cv.text_block(tx, ty + 6, cap, 2, DARKGREY, 296)

    # ---- also today
    y = 852
    cv.text(mx, y, "ALSO TODAY", 2, RED)
    y = 878
    for line in (
        "• US LOSES MEASLES-FREE STATUS AFTER NEARLY 30 YEARS",
        "• DEPARDIEU PLEADS GUILTY TO SEXUAL ASSAULT CHARGES",
        "• HOUTHIS ADVANCE IN YEMEN; EU STATES PLAN RWANDA DEPORTATION HUB",
    ):
        cv.text(mx, y, line, 2, INK)
        y += 22

    # ---- footer
    cv.hline(mx, mx + cw - 1, 952, GREY, 1)
    foot = "THE WORLD IN ONE PAGE - TUESDAY 17 NOVEMBER 2026"
    cv.text((W - text_width(foot, 1)) // 2, 966, foot, 1, DARKGREY)
    return cv


# --------------------------------------------------------------------- png
def write_png(path, cv):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        return (struct.pack('>I', len(data)) + typ + data +
                struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF))

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) +
           chunk(b'IDAT', comp) + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    write_png(os.path.join(out_dir, 'entry.png'), cv)


if __name__ == '__main__':
    main()
