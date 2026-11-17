"""Draws the home-screen icons (two beamed eighth notes on a marigold staff) as PNGs.

Run with: python3 make_icons.py
Pure standard library, so it works without any image packages.
"""
import math
import struct
import zlib
from pathlib import Path

BG = (0xF5, 0xA6, 0x23)    # marigold, the jacket colour
INK = (0x1A, 0x22, 0x42)   # navy ink
LINE_ALPHA = 0.28          # staff lines are faint ink


def inside(x, y):
    """Shape test in a 100x100 design space. Returns 'ink', 'line' or None."""
    # note heads: tilted ellipses
    for cx, cy in ((38, 66), (62, 59)):
        a = -0.35
        dx, dy = x - cx, y - cy
        rx = dx * math.cos(a) + dy * math.sin(a)
        ry = -dx * math.sin(a) + dy * math.cos(a)
        if (rx / 7.2) ** 2 + (ry / 5.0) ** 2 <= 1:
            return 'ink'
    # stems
    if 43.6 <= x <= 46.2 and 30 <= y <= 66:
        return 'ink'
    if 67.6 <= x <= 70.2 and 24 <= y <= 59:
        return 'ink'
    # slanted beam from (43.6, 30) to (70.2, 24), 7 units thick
    if 43.6 <= x <= 70.2:
        top = 30 + (24 - 30) * (x - 43.6) / (70.2 - 43.6)
        if top <= y <= top + 7:
            return 'ink'
    # staff lines
    if 14 <= x <= 86:
        for i in range(5):
            if 38 + i * 7 <= y <= 38 + i * 7 + 1.4:
                return 'line'
    return None


def render(size, samples=4):
    rows = []
    for py in range(size):
        row = bytearray([0])  # PNG filter type 0
        for px in range(size):
            r, g, b = 0.0, 0.0, 0.0
            for sy in range(samples):
                for sx in range(samples):
                    x = (px + (sx + 0.5) / samples) * 100 / size
                    y = (py + (sy + 0.5) / samples) * 100 / size
                    hit = inside(x, y)
                    if hit == 'ink':
                        c = INK
                    elif hit == 'line':
                        c = tuple(BG[i] * (1 - LINE_ALPHA) + INK[i] * LINE_ALPHA for i in range(3))
                    else:
                        c = BG
                    r += c[0]; g += c[1]; b += c[2]
            n = samples * samples
            row += bytes((round(r / n), round(g / n), round(b / n)))
        rows.append(bytes(row))
    raw = b''.join(rows)

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')


if __name__ == '__main__':
    here = Path(__file__).parent
    for size in (180, 192, 512):
        (here / f'icon-{size}.png').write_bytes(render(size))
        print(f'icon-{size}.png')
