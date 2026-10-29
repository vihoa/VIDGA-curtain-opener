"""
LEGO version of the VIDGA curtain carriage – parametric 3D model.

Builds the carriage (no 3D printer needed) on a 3-track IKEA VIDGA rail and writes:
  - lego_model.json   mesh data used by the interactive viewer
  - ../../docs/lego-model.html   interactive 3D viewer (three.js from a CDN)

Units: mm. Axes: x along the rail, y across (middle slot = 0, room side +), z up
(z = 0 = top of the lips inside the channel, rail underside at z = -D).

Run:  pip install manifold3d numpy   then   python lego_model.py
"""
import base64, json, os
import numpy as np
from manifold3d import Manifold, CrossSection

SEG = 48
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- Rail (measured on a 3-track VIDGA) ----------------
A, B, C, D, F, G = 13, 12, 7, 1, 22, 42      # channel width/height, slot, lip, rail height/width
P = 13.75                                    # distance between channel centres

# ---------------- Design ----------------
ZB, ZT = -33.6, -24.0                        # Technic brick bottom / top (9.6 mm)
GLIDER_X = 44                                # gliders sit straight above the cross bricks
WHEEL_D, WHEEL_IN, WHEEL_OUT = 34, 5.3, 12.3 # Ø34 wheels, inner/outer face from the middle
MOTOR_Z = -18


def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cz(r, z0, z1, x=0, y=0, seg=SEG):
    return Manifold.cylinder(z1 - z0, r, r, seg).translate([x, y, z0])
def cx(r, x0, x1, y=0, z=0):
    return Manifold.cylinder(x1 - x0, r, r, SEG).rotate([0, 90, 0]).translate([x0, y, z])
def cy(r, y0, y1, x=0, z=0):
    return Manifold.cylinder(y1 - y0, r, r, SEG).rotate([-90, 0, 0]).translate([x, y0, z])
def U(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out
def studs(x0, x1, y0, y1, z):
    return U([cz(2.4, z, z + 1.7, x=xi, y=yi, seg=24)
              for xi in np.arange(x0 + 4, x1, 8) for yi in np.arange(y0 + 4, y1, 8)])

# Rail with three channels
rail = box(-95, 110, -G / 2, G / 2, -D, F - D)
for c in (-P, 0, P):
    rail = rail - box(-96, 111, c - A / 2, c + A / 2, 0, B) - box(-96, 111, c - C / 2, c + C / 2, -2, 0.01)

# LEGO frame: spine 1x10 (2730), two cross bricks 1x6 (3894), two plates 2x6 (3795), plate 6x10 (3033)
spine = box(-40, 40, -3.9, 3.9, ZB, ZT) + studs(-40, 40, -4, 4, ZT)
spine = spine - U([cy(2.4, -5, 5, x=-40 + 8 * k, z=ZB + 5.8) for k in range(1, 10)])
def cross(x0):
    b = box(x0, x0 + 8, -23.9, 23.9, ZB, ZT)
    return b - U([cx(2.4, x0 - 1, x0 + 9, y=yv, z=ZB + 5.8) for yv in (-20, -12, -4, 4, 12, 20)])
cross_r, cross_l = cross(40), cross(-48)
plates = U([box(32, 48, -23.9, 23.9, ZT, ZT + 3.2) + studs(32, 48, -24, 24, ZT + 3.2),
            box(-48, -32, -23.9, 23.9, ZT, ZT + 3.2) + studs(-48, -32, -24, 24, ZT + 3.2)])
panel = box(-40, 40, -1.6, 1.6, ZB - 48, ZB)

# Double-shaft worm motor with two Ø34 wheels
motor = box(-5, 13, -5, 5, MOTOR_Z - 6, MOTOR_Z + 6) + (cx(6, 13, 28, z=MOTOR_Z) ^ box(13, 28, -5, 5, MOTOR_Z - 7, MOTOR_Z + 7))
faces = ((WHEEL_IN, WHEEL_OUT), (-WHEEL_OUT, -WHEEL_IN))
tyres = U([cy(WHEEL_D / 2, a, b, z=MOTOR_Z) - cy(10, a - 1, b + 1, z=MOTOR_Z) for a, b in faces])
rims = U([cy(10, a, b, z=MOTOR_Z) - cy(1.5, a - 1, b + 1, z=MOTOR_Z) for a, b in faces])

# Wheeled VIDGA-size gliders (simplified) – one in track 1 at one end, one in track 3 at the other end
def glider(x, y):
    g = U([cy(3.5, y - 6, y - 3.4, x=x + s * 4, z=3.5) + cy(3.5, y + 3.4, y + 6, x=x + s * 4, z=3.5) for s in (1, -1)])
    g = g + box(x - 7.3, x + 7.3, y - 3.2, y + 3.2, 1.2, 8) + box(x - 3, x + 3, y - 2.5, y + 2.5, -1.1, 1.2)
    g = g + box(x - 7.3, x + 7.3, y - 2.5, y + 2.5, -2.1, -1.1)
    outer = CrossSection([[(-6.2, -2.1), (0, -9.4), (6.2, -2.1)]])
    inner = CrossSection([[(-3.6, -2.1), (0, -6.0), (3.6, -2.1)]])
    return g + (outer - inner).extrude(1.6).rotate([90, 0, 0]).translate([x, y + 0.8, 0])
corners = [(GLIDER_X, P), (-GLIDER_X, -P)]   # two gliders, diagonally opposite
gliders = U([glider(x, y) for x, y in corners])

# Extension springs: glider loop tip → cross-brick hole 12 mm from the middle
def spring(x, ytop, ybot):
    rings = []
    for i in range(14):
        t = i / 13
        z, y = -28.8 + 19.2 * t, ybot + (ytop - ybot) * t
        rings.append(cz(2.3, z - 0.35, z + 0.35, x=x, y=y, seg=20) - cz(1.7, z - 1, z + 1, x=x, y=y, seg=20))
    return U(rings)
springs = U([spring(x, y, 12 if y > 0 else -12) for x, y in corners])

# Electronics (placeholders)
calliope = box(-25, 25, -3.2, -1.6, ZB - 46, ZB - 4)
leds = U([box(-9 + i * 4, -7 + i * 4, -3.6, -3.2, ZB - 26 + j * 4, ZB - 24 + j * 4) for i in range(5) for j in range(5)])
aaa = box(-32.5, 32.5, 3.3, 15.3, ZB - 42, ZB - 14)

# Charging dock: 4 round bricks 2x2 (3941) clamped with M3 x 45, 2-pin magnetic pogo connector
conn_carriage = box(48, 50.5, -7.5, 7.5, -31.8, -25.8)
conn_dock = box(50.5, 53, -7.5, 7.5, -31.8, -25.8)
dock = U([cz(7.9, -1 - 9.6 * (k + 1), -1 - 9.6 * k, x=60) for k in range(4)])
screw = cz(1.5, -43.6, 4.5, x=60) + cz(2.8, -43.6, -40.6, x=60)
washer_nut = (cz(4.5, 0, 0.8, x=60) - cz(1.7, -1, 2, x=60)) + (cz(3.17, 0.8, 3.2, x=60, seg=6) - cz(1.5, 0, 4, x=60))
curtain = box(GLIDER_X, 108, P - 0.6, P + 0.6, -120, -10)

OBJECTS = [
    ("rail", "VIDGA rail, 3-track", rail, "#B4B2A9", 0.25),
    ("spine", "Spine: Technic brick 1×10 (2730)", spine, "#F2C300", 1),
    ("cross_r", "Cross brick: Technic 1×6 (3894)", cross_r, "#C91A09", 1),
    ("cross_l", "Cross brick: Technic 1×6 (3894)", cross_l, "#C91A09", 1),
    ("plates", "Plates 2×6 (3795)", plates, "#0055BF", 1),
    ("panel", "Plate 6×10 (3033)", panel, "#A0A5A9", 1),
    ("motor", "Worm motor, double shaft", motor, "#3A3A3A", 1),
    ("tyres", "Ø34 rubber wheels", tyres, "#1B1B1B", 1),
    ("rims", "Wheel rims", rims, "#E8E8E8", 1),
    ("gliders", "2 wheeled gliders (track 1 and track 3)", gliders, "#D9D9D9", 1),
    ("springs", "2 extension springs", springs, "#9AA0A6", 1),
    ("calliope", "Calliope mini 1.3 (window side)", calliope, "#2A9D8F", 1),
    ("leds", "LED matrix / light sensor", leds, "#FF3B30", 1),
    ("aaa", "2×AAA NiMH holder (room side)", aaa, "#222222", 1),
    ("conn_c", "Pogo connector, carriage half", conn_carriage, "#B87333", 1),
    ("conn_d", "Pogo connector, dock half", conn_dock, "#B87333", 1),
    ("dock", "Dock: 4 round bricks 2×2 (3941)", dock, "#E5E5E5", 1),
    ("screw", "M3 × 45 dock screw", screw, "#D85A30", 1),
    ("washer", "Body washer + nut (inside middle track)", washer_nut, "#185FA5", 1),
    ("curtain", "Curtain (track 1)", curtain, "#CECBF6", 0.5),
]


def export():
    out = []
    for key, label, m, color, opacity in OBJECTS:
        mesh = m.to_mesh()
        v = np.asarray(mesh.vert_properties)[:, :3].astype(np.float32)
        f = np.asarray(mesh.tri_verts).astype(np.uint32)
        assert len(v), key
        out.append(dict(key=key, label=label, color=color, opacity=opacity,
                        v=base64.b64encode(v.tobytes()).decode(), f=base64.b64encode(f.tobytes()).decode()))
    data = json.dumps(out)
    open(os.path.join(HERE, "lego_model.json"), "w").write(data)
    tpl = open(os.path.join(HERE, "viewer_template.html")).read()
    docs = os.path.join(HERE, "..", "..", "docs", "lego-model.html")
    open(docs, "w").write(tpl.replace("__DATA__", data))
    print("wrote lego_model.json and docs/lego-model.html,", len(data) // 1024, "KB")


if __name__ == "__main__":
    # quick clash checks: nothing printed may cut into the rail
    for name, part in (("frame", spine + cross_r + cross_l + plates), ("wheels", tyres), ("dock", dock)):
        print(f"{name} vs rail overlap: {(part ^ rail).volume():.2f} mm3")
    export()
