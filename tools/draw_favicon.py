#!/usr/bin/env python3
"""Draw the site's icon: a smoothly shaded torus in a soft teal.

    ~/venvs/math/bin/python tools/draw_favicon.py

Writes
  favicon.ico                  browser-tab icon, 16, 32 and 48 pixels
  images/favicon-192.png       large icon (Android, and browsers that prefer a big PNG)
  images/apple-touch-icon.png  180 pixels on the page colour, for phone home screens
  source/motifs/torus-shaded.png   512 pixels, for reference

The torus (R = 1, r = 0.5) is seen from above at an angle, lit from the upper left. Each
pixel is computed from the torus's equation: a ray from the pixel is followed until it
meets the surface (sphere tracing with the torus's distance function), and the colour comes
from the surface normal there (diffuse light plus a soft highlight). The picture is drawn at
1024 pixels and then reduced, which smooths the edges. The teal is a mid tone, so the icon
shows on light and on dark tab bars alike.

Needs numpy and Pillow, which plain Python does not have.
"""
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
R, r = 1.0, 0.5                           # torus radii
DARK, LIGHT = (0x1f, 0x5a, 0x66), (0x9f, 0xd4, 0xd6)   # soft teal, shadow to light
PAGE = (0xfc, 0xfb, 0xf8)                 # page background, for the phone icon
SIZE = 1024                               # drawing size before reduction


def rotation(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


ROT = rotation(-0.95, 0.0, 0.30)          # view = ROT @ model; the viewer looks along -z


def distance(p):
    """Signed distance from the points p (model coordinates) to the torus."""
    q = np.sqrt(p[..., 0] ** 2 + p[..., 1] ** 2) - R
    return np.sqrt(q ** 2 + p[..., 2] ** 2) - r


def normal(p):
    rho = np.sqrt(p[..., 0] ** 2 + p[..., 1] ** 2)
    q = rho - R
    n = np.stack([p[..., 0] * q / rho, p[..., 1] * q / rho, p[..., 2]], axis=-1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def render(size=SIZE, margin=0.02):
    # the torus's outline in the view plane, to frame the picture
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 400), np.linspace(0, 2 * np.pi, 200), indexing="ij")
    pts = np.stack([(R + r * np.cos(v)) * np.cos(u), (R + r * np.cos(v)) * np.sin(u), r * np.sin(v)], -1)
    view = pts.reshape(-1, 3) @ ROT.T
    lo, hi = view[:, :2].min(0), view[:, :2].max(0)
    span = (hi - lo).max() * (1 + 2 * margin)
    centre = (lo + hi) / 2
    xs = centre[0] + (np.arange(size) + 0.5 - size / 2) / size * span
    ys = centre[1] - (np.arange(size) + 0.5 - size / 2) / size * span
    X, Y = np.meshgrid(xs, ys)
    origin = np.stack([X, Y, np.full_like(X, 3.0)], -1) @ ROT        # view -> model (ROT is orthogonal)
    direction = np.array([0.0, 0.0, -1.0]) @ ROT
    t = np.zeros(X.shape)
    hit = np.zeros(X.shape, bool)
    alive = np.ones(X.shape, bool)
    for _ in range(160):                   # sphere tracing
        p = origin[alive] + t[alive][:, None] * direction
        dist = distance(p)
        t[alive] += dist
        done = dist < 1e-4
        idx = np.flatnonzero(alive)
        hit.flat[idx[done]] = True
        far = t.flat[idx] > 6.0
        alive.flat[idx[done | far]] = False
        if not alive.any():
            break
    p = origin + t[..., None] * direction
    n_view = normal(p) @ ROT.T
    light = np.array([-0.45, 0.65, 0.62]); light /= np.linalg.norm(light)
    half = light + np.array([0, 0, 1.0]); half /= np.linalg.norm(half)
    diffuse = np.clip(n_view @ light, 0, None)
    spec = np.clip(n_view @ half, 0, None) ** 40
    k = (0.18 + 0.82 * diffuse)[..., None]
    rgb = np.array(DARK) * (1 - k) + np.array(LIGHT) * k
    rgb = rgb + (255 - rgb) * (0.55 * spec)[..., None]
    img = np.zeros((size, size, 4))
    img[..., :3] = rgb
    img[..., 3] = np.where(hit, 255, 0)
    img[~hit, :3] = 0
    return Image.fromarray(np.round(img).astype(np.uint8), "RGBA")


def reduce(img, size, sharpen=False):
    small = img.convert("RGBa").resize((size, size), Image.LANCZOS).convert("RGBA")
    if sharpen:
        small = small.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=0))
    return small


def png_bytes(img):
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def ico(images):
    """An .ico file holding PNG images (supported by every browser since 2009)."""
    header = struct.pack("<HHH", 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries, blobs = b"", b""
    for size, data in images:
        entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)
    return header + entries + blobs


def main():
    big = render()
    (ROOT / "favicon.ico").write_bytes(ico([(s, png_bytes(reduce(big, s, sharpen=s <= 32))) for s in (16, 32, 48)]))
    reduce(big, 192).save(ROOT / "images" / "favicon-192.png", optimize=True)
    touch = Image.new("RGBA", (180, 180), PAGE + (255,))
    icon = reduce(big, 140)
    touch.alpha_composite(icon, (20, 20))
    touch.convert("RGB").save(ROOT / "images" / "apple-touch-icon.png", optimize=True)
    reduce(big, 512).save(ROOT / "source" / "motifs" / "torus-shaded.png", optimize=True)
    for f in ("favicon.ico", "images/favicon-192.png", "images/apple-touch-icon.png", "source/motifs/torus-shaded.png"):
        print(f"{f}: {(ROOT / f).stat().st_size // 1024 + 1} KB")


if __name__ == "__main__":
    main()
