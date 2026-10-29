"""
VIDGA 3-channel carriage – parametric 3D model (worm-gear motor, two standard wheels)

Track 1 (room side) and track 3 (wall side): one standard IKEA glider each. A small extension spring
pulls each glider's hook DOWN towards the frame, so the glider wheels press on the lips and the frame
is pulled UP. That presses two standard rubber wheels up against the flat underside of the rail on both
sides of the middle slot. The wheels sit on the two output shafts of a double-shaft N20 worm-gear motor
that lies centred under the middle slot, so the carriage is balanced. The middle channel stays empty.
The track 1 glider is the curtain's leading glider.

Coordinates (mm): x along the rail, y across (middle slot centre = 0, room side +),
z up (z = 0 = top of the lips, rail underside z = -D).
Run:  pip install manifold3d trimesh numpy   then   python vidga_3channel_model.py
"""
import json, base64
import numpy as np
from manifold3d import Manifold
import trimesh

# ---------------- Rail (measured by user) ----------------
A, B, C, D, F, G = 13.0, 12.0, 7.0, 1.0, 22.0, 42.0
WALL = (G - 3 * A) / 4
PITCH = A + WALL                                   # 13.75 mm between channel centres
LAND_IN, LAND_OUT = C / 2, PITCH - C / 2           # flat underside between middle and outer slot: y = 3.5 … 10.25

# ---------------- Bought parts (typical sizes – measure yours and change here) ----------------
# N20 worm-gear motor with DOUBLE output shaft
WG_L, WG_H, WG_T = 18.0, 12.0, 10.0                # gearbox length (along motor axis), height, thickness (across rail)
WG_SHAFT_FROM_END = 5.0                            # output shaft distance from the gearbox end away from the motor
WG_SHAFT_DZ = 0.0                                  # output shaft height offset from the motor axis
WG_SHAFT_L = 8.0                                   # each output shaft (3 mm D-shaft)
MOTOR_D, MOTOR_L = 12.0, 15.0
WHEEL_D, WHEEL_W = 20.0, 4.8                       # standard rubber wheel for 3 mm D-shaft
# IKEA VIDGA glider (simplified – send a photo/measurements to refine)
GL_WHEEL_D, GL_STEM, GL_RING_Z, GL_RING_R = 7.0, 3.0, -7.5, 2.8
CALLIOPE = (60.0, 60.0)
BATT = (65.0, 28.0, 12.0)                          # 2 x AAA holder

# ---------------- Design ----------------
GL_X = 42.0                                        # track 1 glider at x = +42, track 3 glider at x = -42
FORK_Z = (-4.4, -2.4)                              # forks guide the glider stems; 1.4 mm free travel below the rail
BASE_Z = (-27.0, -24.0)
ANCHOR_Z = -20.0                                   # spring anchor (bottom end of the extension springs)
SEG = 64

def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cyl_z(r, z0, z1, x=0, y=0):
    return Manifold.cylinder(z1 - z0, r, r, SEG).translate([x, y, z0])
def cyl_x(r, x0, x1, y=0, z=0):
    return Manifold.cylinder(x1 - x0, r, r, SEG).rotate([0, 90, 0]).translate([x0, y, z])
def cyl_y(r, y0, y1, x=0, z=0):
    return Manifold.cylinder(y1 - y0, r, r, SEG).rotate([-90, 0, 0]).translate([x, y0, z])
def union(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out

WHEEL_Z = -D - WHEEL_D / 2                         # wheel axis: tyres touch the rail underside
motor_z = WHEEL_Z - WG_SHAFT_DZ
gb_x0 = -WG_SHAFT_FROM_END
gb_x1 = gb_x0 + WG_L
wheel_y0 = WG_T / 2 + 0.3                          # wheel inner face
wheel_y1 = wheel_y0 + WHEEL_W                      # wheel outer face
assert wheel_y0 >= LAND_IN - 2 and wheel_y1 <= LAND_OUT - 0.1, "wheels must stay on the flat underside"
assert WG_T / 2 + WG_SHAFT_L >= wheel_y1 - 1, "output shaft too short for the wheel"

# ---------------- Printed: frame (the only printed part) ----------------
base = box(-48, 48, -12, 12, *BASE_Z)
cradle = box(gb_x0 - 2, gb_x1 + MOTOR_L + 2, -WG_T / 2, WG_T / 2, BASE_Z[1], motor_z)
posts = union([box(s * GL_X - 4, s * GL_X + 4, -3, 3, BASE_Z[1], FORK_Z[1]) for s in (1, -1)])
forks = union([box(GL_X - 4, GL_X + 4, -3, PITCH + 4, *FORK_Z), box(-GL_X - 4, -GL_X + 4, -PITCH - 4, 3, *FORK_Z)])
anchor_arms = union([box(GL_X - 4, GL_X + 4, 0, PITCH + 3, *BASE_Z), box(-GL_X - 4, -GL_X + 4, -PITCH - 3, 0, *BASE_Z)])
anchors = union([box(GL_X - 3, GL_X + 3, PITCH - 2.5, PITCH + 2.5, BASE_Z[1], ANCHOR_Z + 2.5),
                 box(-GL_X - 3, -GL_X + 3, -PITCH - 2.5, -PITCH + 2.5, BASE_Z[1], ANCHOR_Z + 2.5)])
panel = box(-32, 32, -2, 2, -92, BASE_Z[0] + 0.01)
frame = union([base, cradle, posts, forks, anchor_arms, anchors, panel])
cuts = [box(gb_x0 - 0.15, gb_x1 + 0.15, -WG_T / 2 - 1, WG_T / 2 + 1, motor_z - WG_H / 2 - 0.15, motor_z + 20),   # gearbox seat
        cyl_x(MOTOR_D / 2 + 0.15, gb_x1 - 0.1, gb_x1 + MOTOR_L + 5, y=0, z=motor_z) ^
        box(gb_x1 - 1, gb_x1 + MOTOR_L + 6, -5.15, 5.15, motor_z - 10, motor_z + 10),                           # motor seat
        box(gb_x1 + 3, gb_x1 + 5, -8, 8, BASE_Z[0] - 1, BASE_Z[1] + 1),                                        # zip-tie slot
        box(GL_X - 1.8, GL_X + 1.8, PITCH - 1.8, PITCH + 5, FORK_Z[0] - 1, FORK_Z[1] + 1),                      # fork slot, track 1
        box(-GL_X - 1.8, -GL_X + 1.8, -PITCH - 5, -PITCH + 1.8, FORK_Z[0] - 1, FORK_Z[1] + 1),                  # fork slot, track 3
        cyl_x(0.9, GL_X - 5, GL_X + 5, y=PITCH, z=ANCHOR_Z),                                                  # spring hook holes
        cyl_x(0.9, -GL_X - 5, -GL_X + 5, y=-PITCH, z=ANCHOR_Z)]
for zc in (-40, -60, -82):
    for xc in (-29, 29):
        cuts.append(box(xc - 1, xc + 1, -3, 3, zc - 2, zc + 2))                                               # zip-tie slots for Calliope + battery
frame = frame - union(cuts)

# ---------------- Context (viewer only) ----------------
rail = box(-130, 110, -G / 2, G / 2, -D, F - D)
for c in (-PITCH, 0.0, PITCH):
    rail = rail - box(-131, 111, c - A / 2, c + A / 2, 0, B) - box(-131, 111, c - C / 2, c + C / 2, -D - 1, 0.01)
motor = box(gb_x0, gb_x1, -WG_T / 2, WG_T / 2, motor_z - WG_H / 2, motor_z + WG_H / 2) + \
        (cyl_x(MOTOR_D / 2, gb_x1, gb_x1 + MOTOR_L, y=0, z=motor_z) ^
         box(gb_x1, gb_x1 + MOTOR_L, -5, 5, motor_z - 7, motor_z + 7)) + \
        cyl_y(1.5, -WG_T / 2 - WG_SHAFT_L, WG_T / 2 + WG_SHAFT_L, x=0, z=WHEEL_Z)
def wheel(y0, y1):
    tyre = cyl_y(WHEEL_D / 2, y0, y1, x=0, z=WHEEL_Z) - cyl_y(WHEEL_D / 2 - 2.5, y0 - 1, y1 + 1, x=0, z=WHEEL_Z)
    hub = cyl_y(WHEEL_D / 2 - 2.5, y0, y1, x=0, z=WHEEL_Z) - cyl_y(1.5, y0 - 1, y1 + 1, x=0, z=WHEEL_Z)
    return tyre, hub
t1, h1 = wheel(wheel_y0, wheel_y1)
t2, h2 = wheel(-wheel_y1, -wheel_y0)
tyres, hubs = t1 + t2, h1 + h2
def glider(x, y):
    r = GL_WHEEL_D / 2
    g = cyl_y(r, y - 6, y - 3.2, x=x, z=r) + cyl_y(r, y + 3.2, y + 6, x=x, z=r)
    g = g + box(x - 5, x + 5, y - 3.2, y + 3.2, 1.5, 7.5)
    g = g + box(x - GL_STEM / 2, x + GL_STEM / 2, y - GL_STEM / 2, y + GL_STEM / 2, GL_RING_Z + GL_RING_R - 0.5, 1.5)
    return g + (cyl_y(GL_RING_R, y - 1, y + 1, x=x, z=GL_RING_Z) - cyl_y(1.6, y - 2, y + 2, x=x, z=GL_RING_Z))
spring_gliders = glider(GL_X, PITCH) + glider(-GL_X, -PITCH)
def ext_spring(x, y):
    z0, z1 = ANCHOR_Z + 2.6, GL_RING_Z - GL_RING_R + 0.3
    return cyl_z(2.2, z0, z1, x=x, y=y) - cyl_z(1.7, z0 - 1, z1 + 1, x=x, y=y)
springs = ext_spring(GL_X, PITCH) + ext_spring(-GL_X, -PITCH)
curtain_gliders = union([glider(x, PITCH) for x in (65, 85, 105)])
curtain = box(GL_X, 110, PITCH - 0.6, PITCH + 0.6, -130, -12)
calliope = box(-CALLIOPE[0] / 2, CALLIOPE[0] / 2, 2, 9, -90, -30)
battery = box(-BATT[0] / 2, BATT[0] / 2, -2 - BATT[2], -2, -31 - BATT[1], -31)

# ---------------- Checks ----------------
def ov(a, b): return (a ^ b).volume()
checks = {
    "frame vs rail": ov(frame, rail),
    "wheels vs rail": ov(tyres + hubs, rail),
    "motor vs rail": ov(motor, rail),
    "motor vs frame": ov(motor, frame),
    "wheels vs frame": ov(tyres + hubs, frame),
    "gliders vs frame (stems in fork slots)": ov(spring_gliders, frame),
    "gliders vs rail": ov(spring_gliders, rail),
    "springs vs frame": ov(springs, frame),
    "curtain gliders vs carriage": ov(curtain_gliders, frame + tyres + motor),
    "Calliope/battery vs frame": ov(calliope + battery, frame),
    "wheels vs track 1/3 slots (should be 0)": ov(tyres, box(-20, 20, LAND_OUT, LAND_OUT + 10, -3, 0) + box(-20, 20, -LAND_OUT - 10, -LAND_OUT, -3, 0)),
}
mass = {"motor": (15, 0.0), "wheels": (6, 0.0), "battery 2xAAA": (36, -2 - BATT[2] / 2), "Calliope": (16, 5.5), "frame": (25, 0.0)}
com_y = sum(m * y for m, y in mass.values()) / sum(m for m, _ in mass.values())

def to_tm(m):
    mesh = m.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=True)

if __name__ == "__main__":
    tm = to_tm(frame); tm.export("frame.stl")
    print(f"frame.stl watertight={tm.is_watertight} vol={tm.volume:.0f} mm3 size={np.round(tm.extents, 1)}")
    for k, v in checks.items():
        print(f"check {k}: {v:.3f} mm3")
    print(f"wheels at y = ±{wheel_y0:.1f}…{wheel_y1:.1f} on the flat underside ±{LAND_IN}…{LAND_OUT}")
    print(f"tyre top z = {WHEEL_Z + WHEEL_D / 2:.2f} (rail underside {-D}); gearbox top z = {motor_z + WG_H / 2:.2f}")
    print(f"estimated centre of mass y = {com_y:+.1f} mm from the middle slot")
    objs = [
        ("rail", "VIDGA rail, 3-track", rail, "#B4B2A9", 0.28, "context", [0, 0, 0]),
        ("frame", "Frame – printed", frame, "#7F77DD", 1, "printed", [0, 0, -35]),
        ("gliders", "IKEA gliders, tracks 1 and 3", spring_gliders, "#1D9E75", 1, "bought", [0, 0, 18]),
        ("springs", "Extension springs", springs, "#97C459", 1, "bought", [0, 0, -12]),
        ("motor", "N20 worm motor, double shaft", motor, "#444441", 1, "bought", [0, 0, -22]),
        ("tyres", "Standard wheels Ø20 (tyres)", tyres, "#2C2C2A", 1, "bought", [0, 0, -22]),
        ("hubs", "Standard wheels (hubs)", hubs, "#EF9F27", 1, "bought", [0, 0, -22]),
        ("calliope", "Calliope mini (placeholder)", calliope, "#AFA9EC", 1, "bought", [0, 25, -35]),
        ("battery", "2×AAA holder (placeholder)", battery, "#FAC775", 1, "bought", [0, -25, -35]),
        ("cgl", "Track 1 curtain gliders", curtain_gliders, "#5DCAA5", 1, "context", [0, 0, 0]),
        ("curtain", "Track 1 curtain", curtain, "#CECBF6", 0.55, "context", [0, 0, 0]),
    ]
    out = []
    for key, label, m, col, op, grp, exp in objs:
        mesh = m.to_mesh()
        v = np.asarray(mesh.vert_properties)[:, :3].astype(np.float32)
        f = np.asarray(mesh.tri_verts).astype(np.uint32)
        out.append(dict(key=key, label=label, color=col, opacity=op, group=grp, explode=exp,
                        v=base64.b64encode(v.tobytes()).decode(), f=base64.b64encode(f.tobytes()).decode()))
    json.dump(out, open("viewer_data_3ch.json", "w"))
    print("viewer data", sum(len(o["v"]) + len(o["f"]) for o in out) // 1024, "KB")
