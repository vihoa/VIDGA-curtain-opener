# CAD

Both models are parametric Python scripts built with [manifold3d](https://github.com/elalish/manifold).
The rail measurements are constants at the top of each script – change them if your rail differs.

```bash
pip install manifold3d numpy trimesh
```

## `lego/` – LEGO frame (recommended, no 3D printer needed)

```bash
cd cad/lego
python lego_model.py      # writes lego_model.json and ../../docs/lego-model.html
```

Open [`docs/lego-model.html`](../docs/lego-model.html) in a browser to rotate the model.
The script also checks that the frame, wheels and dock don't cut into the rail.

LEGO parts (BrickLink numbers):

| Part | No. | Qty |
|---|---|---|
| Technic brick 1×10 with holes (spine) | 2730 | 1 |
| Technic brick 1×6 with holes (cross bricks) | 3894 | 2 |
| Plate 2×6 | 3795 | 2 |
| Plate 6×10 (electronics panel) | 3033 | 1 |
| Brick, round 2×2 with axle hole (dock) | 3941 | 4 |
| Brick 1×1 + plate 1×1 (motor stops) | 3005 / 3024 | 1 + 1 |

## `printed-frame/` – 3D-printed alternative

An earlier version with a one-piece printed frame (`frame.stl`, PETG or PLA, supports under the forks
and the motor seat). It holds one glider each in tracks 1 and 3 and uses Ø20 mm wheels.

```bash
cd cad/printed-frame
python vidga_3channel_model.py   # writes frame.stl and prints fit checks
```

The glider shape in both models is simplified (estimated from a photo). Measure your gliders and
adjust the `GL_*` / `glider()` values before printing.
