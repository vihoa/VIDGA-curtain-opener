# Firmware

All programs are written for the **Calliope mini 1.3** in MakeCode (JavaScript view).

| Folder | Runs on | What it does |
|---|---|---|
| [`carriage-simple`](carriage-simple/main.ts) | Carriage | **Start here.** Buttons A/B or the remote drive the curtain. Wiggle start + pulse mode for more pulling force. No dock, no light sensor. |
| [`carriage-dock`](carriage-dock/main.ts) | Carriage | Full version: homes on the charging dock (P0), measures position by time, opens/closes by daylight, radio remote. Needs the dock-sense wiring. |
| [`remote`](remote/main.ts) | Second Calliope | Remote control: A = open, B = close, A+B = stop. Shows ✓ / 😞 from the carriage. |
| [`tools/motor-pin-test`](tools/motor-pin-test/main.ts) | Carriage | Finds the motor pins: the motor must turn both ways in phases 1 and 2. |

Both carriage programs and the remote use **radio group 42**. Change it in both if a neighbour uses the same group.

## Load a ready-made program

Pre-built files are in [`hex/`](hex):

1. Connect the Calliope by USB. It appears as a drive called **MINI**.
2. Drag the `.hex` file onto it. The yellow LED flashes; the program starts when it stops.

To edit one: open [makecode.calliope.cc](https://makecode.calliope.cc), **Import → Import File**, choose the `.hex` (the source is embedded).

> The `.hex` files were built offline with `pxt-calliope` 3.0.30. In that version the dual-motor enum is `Motor.A / B / AB`; the current web editor calls them `Motor.M0 / M1 / M0_M1`. The source in `tools/motor-pin-test` uses the web-editor names.

## Settings

At the top of each `main.ts`:

| Constant | Meaning |
|---|---|
| `OPEN_DIR` | `1` or `-1`. Flip it if "open" drives the wrong way (or swap the motor wires). |
| `MAX_MS` / `FULL_MS` | Safety stop / full travel time in ms. |
| `WIGGLE_MS`, `PULSE_ON`, `PULSE_OFF` | (simple) Start help and pulse mode. `PULSE_OFF = 0` drives continuously. |
| `DAY_LEVEL`, `NIGHT_LEVEL`, `CONFIRM` | (dock) Light thresholds 0–255 and how many 10 s readings confirm day/night. |

## Calibration (`carriage-dock`)

1. Press **A** once: the carriage drives to the dock and learns its home position.
2. **Travel time:** at the dock press **B**, then **A+B** exactly when the curtain is fully closed. The display shows seconds → put `seconds × 1000` into `FULL_MS`.
3. **Light levels:** while idle, press **A+B** to show the light level. Do it once by day and once at dusk; set `DAY_LEVEL` / `NIGHT_LEVEL` between the two.

## Build from source (optional)

```bash
npm install pxt-calliope@3.0.30 --ignore-scripts
cd firmware/carriage-simple
ln -s ../../node_modules node_modules
node -e "const p=require('pxt-core/built/pxt.js');const T=require('path').resolve('node_modules/pxt-calliope');p.mainCli(T,['install']).then(()=>p.mainCli(T,['build']))"
# → built/binary.hex
```
