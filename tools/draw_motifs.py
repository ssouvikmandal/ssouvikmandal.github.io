#!/usr/bin/env python3
"""Draw the topology motifs used for the favicon and the link preview (SVG line drawings).

Three variants, each computed from its mathematical description:

  torus  A torus R = 1, r = 0.42 seen from above at an angle: meridians, parallels and the
         outline, with hidden lines removed by casting a ray from each point to the viewer.
  hopf   Seven fibres of the Hopf fibration S^3 -> S^2 over the circle of latitude
         theta = pi/3, stereographically projected to R^3: linked (Villarceau) circles on a
         torus, with gaps at the under-crossings. The icon shows two fibres (a Hopf link).
  knot   A trefoil knot diagram with gaps at the under-crossings.

For each variant the script writes, into source/motifs/:
  <name>.svg          header version (thin lines)
  <name>-icon.svg     favicon version (fewer, thicker lines, readable at 16-32 px)

The chosen motif (the Hopf fibration, whose icon is a Hopf link) is installed as the
favicon and in the link-preview picture by tools/make_icons.py.

It also draws the very faint background drawings shown in the page margins on computer
screens (assets/site.css sets their position and faintness):

  images/bg-torus.svg   a large torus with more meridians and parallels (left margin and
                        behind the menu)
  images/bg-knot.svg    a cinquefoil, the (2, 5) torus knot (lower left margin)
  images/bg-hopf.svg    Hopf fibres over two circles of latitude, on two nested tori
                        (right margin)

Needs numpy, which plain Python does not have
(on the author's server: ~/venvs/math/bin/python tools/draw_motifs.py).
"""
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "source" / "motifs"
ACCENT = "#2e4a68"   # keep in step with --accent in assets/site.css


# --- geometry helpers -------------------------------------------------------------------

def rotation(ax, ay, az):
    """Rotation matrix: first about x by ax, then y by ay, then z by az (radians)."""
    cx, sx, cy, sy, cz, sz = (math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay),
                              math.cos(az), math.sin(az))
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


def project(points, rot):
    """Orthographic projection: returns screen (x, y) with y pointing down, and depth
    (larger = nearer to the viewer, who looks along -z after rotation)."""
    q = points @ rot.T
    return np.column_stack([q[:, 0], -q[:, 1]]), q[:, 2]


def crossings(curves2d, depths, closed, min_sep=6):
    """Find crossings between all strands. Returns, per curve, a list of arc positions
    (as fractional point indices) where the curve passes UNDER another strand."""
    under = [[] for _ in curves2d]
    segs = []
    for k, (c, d) in enumerate(zip(curves2d, depths)):
        n = len(c)
        idx = np.arange(n if closed[k] else n - 1)
        a, b = c[idx], c[(idx + 1) % n]
        segs.append((k, idx, a, b, d[idx], d[(idx + 1) % n], n))
    for i in range(len(segs)):
        for j in range(i, len(segs)):
            k1, i1, a1, b1, da1, db1, n1 = segs[i]
            k2, i2, a2, b2, da2, db2, n2 = segs[j]
            p, r = a1[:, None, :], (b1 - a1)[:, None, :]
            q, s = a2[None, :, :], (b2 - a2)[None, :, :]
            rxs = r[..., 0] * s[..., 1] - r[..., 1] * s[..., 0]
            qp = q - p
            with np.errstate(divide="ignore", invalid="ignore"):
                t = (qp[..., 0] * s[..., 1] - qp[..., 1] * s[..., 0]) / rxs
                u = (qp[..., 0] * r[..., 1] - qp[..., 1] * r[..., 0]) / rxs
            hit = (np.abs(rxs) > 1e-12) & (t >= 0) & (t < 1) & (u >= 0) & (u < 1)
            if k1 == k2:   # ignore neighbouring segments of the same strand
                ii, jj = np.meshgrid(i1, i2, indexing="ij")
                gap = np.abs(ii - jj)
                if closed[k1]:
                    gap = np.minimum(gap, n1 - gap)
                hit &= (gap > min_sep) & (ii < jj)
            for x, y in zip(*np.nonzero(hit)):
                z1 = da1[x] + t[x, y] * (db1[x] - da1[x])
                z2 = da2[y] + u[x, y] * (db2[y] - da2[y])
                if z1 < z2:
                    under[k1].append(i1[x] + t[x, y])
                else:
                    under[k2].append(i2[y] + u[x, y])
    return under


def cut(curve2d, closed, gaps, half_gap):
    """Split a polyline into visible pieces, leaving out a gap of the given half-length
    (in drawing units) around each arc position in `gaps`."""
    n = len(curve2d)
    pts = np.vstack([curve2d, curve2d[:1]]) if closed else curve2d
    seglen = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    arc = np.concatenate([[0], np.cumsum(seglen)])
    total = arc[-1]
    centres = [np.interp(g, np.arange(len(arc)), arc) for g in gaps]
    keep = np.ones(len(pts), bool)
    for c in centres:
        d = np.abs(arc - c)
        if closed:
            d = np.minimum(d, total - d)
        keep &= d > half_gap
    pieces, cur = [], []
    for i in range(len(pts)):
        if keep[i]:
            cur.append(pts[i])
        elif cur:
            pieces.append(np.array(cur)); cur = []
    if cur:
        if closed and pieces and keep[0] and len(pieces[0]) and keep[-1]:
            pieces[0] = np.vstack([np.array(cur), pieces[0][1:]])   # join across the seam
        else:
            pieces.append(np.array(cur))
    if closed and keep.all():
        return [pts]
    return [p for p in pieces if len(p) > 1]


def visible_pieces(points2d, mask):
    pieces, cur = [], []
    for p, m in zip(points2d, mask):
        if m:
            cur.append(p)
        elif cur:
            pieces.append(np.array(cur)); cur = []
    if cur:
        pieces.append(np.array(cur))
    return [p for p in pieces if len(p) > 1]


def simplify(p, tol):
    """Ramer-Douglas-Peucker: drop points closer than tol to the simplified line."""
    if len(p) < 3:
        return p
    a, b = p[0], p[-1]
    ab = b - a
    n = np.hypot(*ab)
    if n < 1e-12:
        dist = np.hypot(*(p - a).T)
    else:
        dist = np.abs(ab[0] * (p[:, 1] - a[1]) - ab[1] * (p[:, 0] - a[0])) / n
    i = int(np.argmax(dist))
    if dist[i] <= tol:
        return np.array([a, b])
    return np.vstack([simplify(p[:i + 1], tol)[:-1], simplify(p[i:], tol)])


def path_data(pieces, tol=0.04):
    out = []
    for p in pieces:
        p = simplify(p, tol)
        p = np.round(p, 2)
        d = [f"M{p[0, 0]:.2f} {p[0, 1]:.2f}"]
        prev = p[0]
        for q in p[1:]:
            dx, dy = q - prev
            if abs(dx) < 0.005 and abs(dy) < 0.005:
                continue
            d.append(f"l{dx:.2f} {dy:.2f}")
            prev = q
        out.append("".join(d))
    return "".join(out).replace("-0.00", "0.00").replace(".00", "")


def svg(groups, size, title, pad=0.06):
    """groups: list of (pieces, stroke_width, opacity). Pieces are scaled to fit a
    square of the given size."""
    allpts = np.vstack([p for g in groups for p in g[0]])
    lo, hi = allpts.min(axis=0), allpts.max(axis=0)
    span = (hi - lo).max()
    scale = size * (1 - 2 * pad) / span
    off = (np.array([size, size]) - (hi - lo) * scale) / 2
    body = []
    for pieces, width, opacity in groups:
        scaled = [(p - lo) * scale + off for p in pieces]
        op = "" if opacity == 1 else f' stroke-opacity="{opacity}"'
        body.append(f'<path d="{path_data(scaled)}" stroke-width="{width}"{op}/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}" role="img" aria-label="{title}">'
            f'<title>{title}</title>'
            f'<g fill="none" stroke="{ACCENT}" stroke-linecap="round" stroke-linejoin="round">'
            + "".join(body) + "</g></svg>\n")


# --- torus ------------------------------------------------------------------------------

def torus_surface(R, r):
    def f(p):
        return (np.sqrt(p[..., 0] ** 2 + p[..., 1] ** 2) - R) ** 2 + p[..., 2] ** 2 - r ** 2
    def point(u, v):
        return np.stack([(R + r * np.cos(v)) * np.cos(u), (R + r * np.cos(v)) * np.sin(u),
                         r * np.sin(v)], axis=-1)
    def normal(u, v):
        return np.stack([np.cos(v) * np.cos(u), np.cos(v) * np.sin(u), np.sin(v)], axis=-1)
    return f, point, normal


def visible_on_torus(points, normals, f, view, steps=400, reach=4.0):
    """A point of the surface is visible when the ray from it towards the viewer stays
    outside the solid torus."""
    start = points + 2e-3 * normals
    ts = np.linspace(1e-3, reach, steps)
    q = start[:, None, :] + ts[None, :, None] * view[None, None, :]
    return ~(f(q) < 0).any(axis=1)


def torus(icon=False):
    R, r = 1.0, 0.42
    f, point, normal = torus_surface(R, r)
    rot = rotation(-0.95 if icon else -1.08, 0.0, 0.32)
    view = rot.T @ np.array([0, 0, 1.0])        # direction towards the viewer, model coords
    groups = []
    n_mer, n_par = (0, 0) if icon else (20, 6)
    t = np.linspace(0, 2 * np.pi, 480)
    lines = []
    for k in range(n_mer):                          # meridians: u fixed
        u = np.full_like(t, 2 * np.pi * k / n_mer)
        lines.append((u, t))
    for k in range(n_par):                          # parallels: v fixed
        v = np.full_like(t, 2 * np.pi * k / n_par + np.pi / n_par)
        lines.append((t, v))
    wire = []
    for u, v in lines:
        P, N = point(u, v), normal(u, v)
        vis = visible_on_torus(P, N, f, view)
        xy, _ = project(P, rot)
        wire += visible_pieces(xy, vis)
    # outline: points where the normal is perpendicular to the view direction
    u = np.linspace(0, 2 * np.pi, 1440)
    a, b, c = view
    v0 = np.arctan2(-(a * np.cos(u) + b * np.sin(u)), c)
    outline = []
    for v in (v0, v0 + np.pi):
        P, N = point(u, v), normal(u, v)
        vis = visible_on_torus(P, N, f, view)
        xy, _ = project(P, rot)
        outline += visible_pieces(xy, vis)
    if icon:
        return svg([(outline, 3.2, 1)], 64, "Torus")
    return svg([(wire, 0.7, 0.7), (outline, 1.45, 1)], 120, "Torus")


# --- Hopf fibration ---------------------------------------------------------------------

def hopf_fibre(theta, phi, n=480):
    """Fibre over the point of S^2 with polar angle theta and azimuth phi, as a curve in R^3
    (stereographic projection of S^3 from (0, 0, 0, 1))."""
    psi = np.linspace(0, 2 * np.pi, n, endpoint=False)
    z1 = np.cos(theta / 2) * np.exp(1j * psi)
    z2 = np.sin(theta / 2) * np.exp(1j * (psi + phi))
    x = np.stack([z1.real, z1.imag, z2.real, z2.imag], axis=-1)
    return x[:, :3] / (1 - x[:, 3:4])


def hopf(icon=False):
    rot = rotation(-0.55, 0.0, 0.3)
    n = 2 if icon else 7       # the icon shows two fibres: a Hopf link
    fibres = [hopf_fibre(np.pi / 3, 2 * np.pi * k / n, 360) for k in range(n)]
    xy, dep = zip(*(project(c, rot) for c in fibres))
    closed = [True] * len(fibres)
    under = crossings(xy, dep, closed)
    span = np.ptp(np.vstack(xy), axis=0).max()
    half_gap = span * (0.06 if icon else 0.016)
    pieces = []
    for c, g in zip(xy, under):
        pieces += cut(c, True, g, half_gap)
    if icon:
        return svg([(pieces, 4.0, 1)], 64, "Hopf link")
    return svg([(pieces, 1.25, 1)], 120, "Hopf fibration")


# --- trefoil knot -----------------------------------------------------------------------

def knot(icon=False):
    t = np.linspace(0, 2 * np.pi, 900, endpoint=False)
    curve = np.stack([np.sin(t) + 2 * np.sin(2 * t), np.cos(t) - 2 * np.cos(2 * t),
                      -np.sin(3 * t)], axis=-1)
    rot = rotation(0.0, 0.0, np.pi)
    xy, dep = project(curve, rot)
    under = crossings([xy], [dep], [True], min_sep=20)
    span = np.ptp(xy, axis=0).max()
    pieces = cut(xy, True, under[0], span * (0.07 if icon else 0.045))
    if icon:
        return svg([(pieces, 4.2, 1)], 64, "Trefoil knot")
    return svg([(pieces, 1.9, 1)], 120, "Trefoil knot")


# --- background drawings ----------------------------------------------------------------

def svg_fit(groups, width, title, pad=4):
    """Like svg(), but the drawing area has the drawing's own proportions: `width` units
    wide (1 unit = 1 CSS pixel at the intended size). The drawing is decorative, so it
    carries no title for screen readers; `title` is only a comment."""
    allpts = np.vstack([p for g in groups for p in g[0]])
    lo, hi = allpts.min(axis=0), allpts.max(axis=0)
    scale = (width - 2 * pad) / (hi - lo)[0]
    height = int(np.ceil((hi - lo)[1] * scale + 2 * pad))
    body = []
    for pieces, stroke, opacity in groups:
        scaled = [(p - lo) * scale + pad for p in pieces]
        op = "" if opacity == 1 else f' stroke-opacity="{opacity}"'
        body.append(f'<path d="{path_data(scaled, tol=0.06)}" stroke-width="{stroke}"{op}/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" aria-hidden="true">'
            f'<!-- {title}, drawn by tools/draw_motifs.py -->'
            f'<g fill="none" stroke="{ACCENT}" stroke-linecap="round" stroke-linejoin="round">'
            + "".join(body) + "</g></svg>\n")


def bg_torus():
    R, r = 1.0, 0.45
    f, point, normal = torus_surface(R, r)
    rot = rotation(-1.2, 0.0, -0.42)
    view = rot.T @ np.array([0, 0, 1.0])
    t = np.linspace(0, 2 * np.pi, 720)
    lines = [(np.full_like(t, 2 * np.pi * k / 36), t) for k in range(36)]
    lines += [(t, np.full_like(t, 2 * np.pi * k / 12 + np.pi / 12)) for k in range(12)]
    wire = []
    for u, v in lines:
        P, N = point(u, v), normal(u, v)
        xy, _ = project(P, rot)
        wire += visible_pieces(xy, visible_on_torus(P, N, f, view))
    u = np.linspace(0, 2 * np.pi, 2000)
    a, b, c = view
    v0 = np.arctan2(-(a * np.cos(u) + b * np.sin(u)), c)
    outline = []
    for v in (v0, v0 + np.pi):
        P, N = point(u, v), normal(u, v)
        xy, _ = project(P, rot)
        outline += visible_pieces(xy, visible_on_torus(P, N, f, view))
    return svg_fit([(wire, 0.8, 0.6), (outline, 1.3, 1)], 480, "Torus")


def bg_knot():
    """Cinquefoil, the (2, 5) torus knot: ((3 + cos 5t) cos 2t, (3 + cos 5t) sin 2t, sin 5t)."""
    t = np.linspace(0, 2 * np.pi, 1500, endpoint=False)
    curve = np.stack([(3 + np.cos(5 * t)) * np.cos(2 * t), (3 + np.cos(5 * t)) * np.sin(2 * t),
                      np.sin(5 * t)], axis=-1)
    xy, dep = project(curve, rotation(0.0, 0.0, np.pi / 2))
    under = crossings([xy], [dep], [True], min_sep=20)
    span = np.ptp(xy, axis=0).max()
    return svg_fit([(cut(xy, True, under[0], span * 0.028), 1.3, 1)], 260, "Cinquefoil knot")


def bg_hopf():
    rot = rotation(-0.8, 0.0, 0.55)
    fibres = [hopf_fibre(np.pi / 2.4, 2 * np.pi * k / 10, 600) for k in range(10)]
    fibres += [hopf_fibre(np.pi / 6, 2 * np.pi * (k + 0.5) / 5, 600) for k in range(5)]
    xy, dep = zip(*(project(c, rot) for c in fibres))
    under = crossings(xy, dep, [True] * len(fibres))
    span = np.ptp(np.vstack(xy), axis=0).max()
    pieces = []
    for c, g in zip(xy, under):
        pieces += cut(c, True, g, span * 0.008)
    return svg_fit([(pieces, 0.9, 1)], 420, "Hopf fibration")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("torus", torus), ("hopf", hopf), ("knot", knot)]:
        for icon in (False, True):
            path = OUT / f"{name}{'-icon' if icon else ''}.svg"
            path.write_text(fn(icon))
            print(f"{path.relative_to(HERE)}: {path.stat().st_size // 1024 + 1} KB")
    for name, fn in [("bg-torus", bg_torus), ("bg-knot", bg_knot), ("bg-hopf", bg_hopf)]:
        path = HERE / "images" / f"{name}.svg"
        path.write_text(fn())
        print(f"{path.relative_to(HERE)}: {path.stat().st_size // 1024 + 1} KB")


if __name__ == "__main__":
    main()
