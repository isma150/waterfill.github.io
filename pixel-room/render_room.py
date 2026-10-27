#!/usr/bin/env python3
"""Render a pixel-art room: structure from one image, skin from another.

The structure image fixes the geometry: the room faces, the openings (the
transparent holes), and the candle positions. The theme image supplies the
look: stone, hieroglyphs, torches, the lion emblem and the palette. Each room
face is mapped from the structure to the theme with a homography, sampled, and
snapped to a grid of CELL x CELL output pixels, so every block is one flat colour.

A reskin is a new theme image with its THEME_FACES quads measured on it.

Usage:
    python3 render_room.py [structure.webp] [theme.webp] [out.png]
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

CELL = 3  # output pixels per art pixel: 1368 = 456 * 3, and 769 = 255 * 3 + 4
PALETTE_SIZE = 32
LUMA = np.array([0.299, 0.587, 0.114])

# Room faces as quads, in the same semantic corner order in both images.
STRUCTURE_FACES = {
    'ceiling': [(0, 0), (1368, 0), (1063, 150), (305, 150)],
    'left': [(0, 0), (305, 150), (305, 620), (0, 769)],
    'back': [(305, 150), (1063, 150), (1063, 620), (305, 620)],
    'floor': [(305, 620), (1063, 620), (1368, 769), (0, 769)],
    'right': [(1063, 150), (1368, 0), (1368, 769), (1063, 620)],
}
THEME_FACES = {
    'ceiling': [(0, 0), (1672, 0), (1362, 175), (310, 175)],
    'left': [(0, 0), (310, 175), (310, 745), (0, 941)],
    'back': [(310, 175), (1362, 175), (1362, 745), (310, 745)],
    'floor': [(310, 745), (1362, 745), (1672, 941), (0, 941)],
    'right': [(1362, 175), (1672, 0), (1672, 941), (1362, 745)],
}
# Dark slots of the theme image (x0, y0, x1, y1). Their pure-black pixels are
# replaced by the surrounding stone, because the structure decides where holes are.
THEME_HOLES = [
    (411, 140, 571, 181), (754, 140, 916, 175), (1098, 140, 1260, 178),
    (409, 750, 571, 786), (753, 752, 917, 787), (1098, 750, 1261, 786),
    (264, 378, 317, 561), (1355, 378, 1407, 561),
]
# Candle flame centres in the structure image (x, y).
CANDLES = [(452, 596), (683, 597), (914, 596)]


def homography(src, dst):
    """Return the 3x3 matrix that maps the four src points onto the four dst points."""
    rows, rhs = [], []
    for (x, y), (u, v) in zip(src, dst):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        rhs.extend([u, v])
    h = np.linalg.solve(np.array(rows, float), np.array(rhs, float))
    return np.append(h, 1).reshape(3, 3)


def fill_theme_holes(theme):
    """Replace the pure-black pixels inside THEME_HOLES by diffusing the stone around them."""
    img = theme.astype(float)
    dark = np.zeros(img.shape[:2], bool)
    for x0, y0, x1, y1 in THEME_HOLES:
        dark[y0:y1, x0:x1] = img[y0:y1, x0:x1].max(axis=2) < 12
    known = ~dark
    while not known.all():
        acc = np.zeros_like(img)
        cnt = np.zeros(known.shape)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            k = np.roll(known, (dy, dx), axis=(0, 1))
            acc += np.roll(img, (dy, dx), axis=(0, 1)) * k[..., None]
            cnt += k
        fill = ~known & (cnt > 0)
        if not fill.any():
            break
        img[fill] = acc[fill] / cnt[fill][:, None]
        known |= fill
    return img


def face_labels(size, faces):
    """Label every pixel of the canvas with the index of the face it lies on."""
    label = Image.new('I', size, -1)
    draw = ImageDraw.Draw(label)
    for i, quad in enumerate(faces.values()):
        draw.polygon(quad, fill=i)
    labels = np.array(label)
    assert (labels >= 0).all(), 'faces do not tile the canvas'
    return labels


def cell_edges(size):
    """Pixel edges of the logical grid. A remainder shorter than CELL joins the last cell."""
    n = size // CELL
    return [i * CELL for i in range(n)] + [size]


def block_sum(arr, ey, ex):
    rows = np.add.reduceat(arr, ey[:-1], axis=0)
    return np.add.reduceat(rows, ex[:-1], axis=1)


def snap_to_palette(colours, keep):
    """Quantise the kept cell colours to at most PALETTE_SIZE colours."""
    pix = np.clip(np.round(colours[keep]), 0, 255).astype(np.uint8)
    img = Image.fromarray(pix[None, :, :]).quantize(
        colors=PALETTE_SIZE, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    table = np.array(img.getpalette()[:256 * 3], np.uint8).reshape(-1, 3)
    palette = table[np.unique(np.array(img)[0])]
    return palette


def nearest(palette, colour):
    d = ((palette - np.asarray(colour, float)) ** 2).sum(axis=1)
    return palette[d.argmin()]


def render(structure, theme):
    sh, sw = structure.shape[:2]
    th, tw = theme.shape[:2]
    alpha = structure[..., 3]
    theme = fill_theme_holes(theme)

    labels = face_labels((sw, sh), STRUCTURE_FACES)
    colour = np.zeros((sh, sw, 3))
    ys, xs = np.mgrid[0:sh, 0:sw]
    for i, (name, quad) in enumerate(STRUCTURE_FACES.items()):
        m = labels == i
        h = homography(quad, THEME_FACES[name])
        p = np.stack([xs[m] + 0.5, ys[m] + 0.5, np.ones(m.sum())])
        q = h @ p
        u = np.clip(np.floor(q[0] / q[2]).astype(int), 0, tw - 1)
        v = np.clip(np.floor(q[1] / q[2]).astype(int), 0, th - 1)
        colour[m] = theme[v, u]

    ey = np.array(cell_edges(sh))
    ex = np.array(cell_edges(sw))
    counts = np.outer(np.diff(ey), np.diff(ex))
    cell_colour = block_sum(colour, ey, ex) / counts[..., None]
    cell_hole = block_sum((alpha < 128).astype(float), ey, ex) / counts > 0.5

    keep = ~cell_hole
    palette = snap_to_palette(cell_colour, keep)
    cells = np.zeros(cell_colour.shape[:2] + (4,), np.uint8)
    cells[keep, :3] = [nearest(palette, c) for c in cell_colour[keep]]
    cells[keep, 3] = 255

    ranked = palette[np.argsort(-(palette.astype(float) @ LUMA))]
    for cx, cy in CANDLES:
        gx, gy = int(cx) // CELL, int(cy) // CELL
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                d2 = dx * dx + dy * dy
                if d2 > 5 or cell_hole[gy + dy, gx + dx]:
                    continue
                # Bright flame core, then a dark rounded outline so it reads on the lit wall.
                rank = 0 if d2 == 0 else 1 if d2 == 1 else 3 if d2 == 2 else -1
                cells[gy + dy, gx + dx, :3] = ranked[rank]

    out = np.repeat(np.repeat(cells, np.diff(ey), axis=0), np.diff(ex), axis=1)
    return out, palette


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('structure', nargs='?', default=os.path.join(here, 'source', 'structure.webp'))
    parser.add_argument('theme', nargs='?', default=os.path.join(here, 'source', 'theme.webp'))
    parser.add_argument('out', nargs='?', default=os.path.join(here, 'room_pixel_art.png'))
    args = parser.parse_args()

    structure = np.array(Image.open(args.structure).convert('RGBA'))
    theme = np.array(Image.open(args.theme).convert('RGB')).astype(float)
    out, palette = render(structure, theme)

    Image.fromarray(out, 'RGBA').save(args.out, optimize=True)
    hole_pixels = out[..., 3] == 0
    reference = structure[..., 3] < 128
    print(f'wrote {args.out}: {out.shape[1]}x{out.shape[0]}, palette {len(palette)} colours')
    print(f'opening pixels that differ from the structure: {int((hole_pixels != reference).sum())}')


if __name__ == '__main__':
    main()
