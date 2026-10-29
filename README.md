# VIDGA curtain opener

A battery-powered curtain robot for the **IKEA VIDGA 3-track ceiling rail**, built from a **Calliope mini 1.3**, a small worm-gear motor and **LEGO** parts – no 3D printer needed. It drives along the underside of the rail, pulls the curtain open at daylight and closed at dusk, takes commands from a second Calliope as a remote, and recharges its batteries on a small magnetic dock whenever the curtain is open.

![LEGO carriage on the VIDGA rail](docs/images/lego-carriage.png)

> **Status: prototype.** The mechanics and firmware work, but on 2×AAA (≈2.5 V) the motor is at its limit with heavier curtains – see [Known issues](#known-issues).

## How it works

- **Grip:** two wheeled gliders run inside track 1 and track 3, one at each end of the carriage. Springs pull them down and the LEGO frame up, so two rubber wheels press against the flat underside of the rail beside the middle slot.
- **Drive:** a double-shaft N20 worm motor sits centred under the middle slot, one wheel on each shaft. The worm gear holds the curtain when stopped.
- **Control:** the Calliope's built-in motor driver, LED matrix (as light sensor) and radio.
- **Charging:** a 2-pin magnetic pogo connector. Pin 1 is 5 V only when docked, so it both trickle-charges the NiMH batteries (diode + 33 Ω) and tells the Calliope it is home (10k/10k divider on P0).

## Repository

| Folder | Contents |
|---|---|
| [`firmware/`](firmware) | MakeCode programs (carriage simple / with dock, remote, motor pin test) and ready-to-load `.hex` files |
| [`cad/`](cad) | Parametric 3D models: LEGO frame (main) and a 3D-printed frame alternative (`frame.stl`) |
| [`docs/`](docs) | [Bill of materials](docs/bom.md) · [Wiring](docs/wiring.md) · [Assembly](docs/assembly.md) · [Troubleshooting](docs/troubleshooting.md) · [3D viewer](docs/lego-model.html) |

## Quick start

1. Get the parts from the [bill of materials](docs/bom.md).
2. Find the motor pins with `firmware/hex/vidga-curtain-motor-pin-test.hex`.
3. Build the frame and mount it as in [assembly](docs/assembly.md).
4. Load `vidga-curtain-carriage-simple.hex` and test with buttons A (open) and B (close).
5. Wire the [charging dock](docs/wiring.md), then switch to `vidga-curtain-carriage-dock.hex` and [calibrate](firmware/README.md#calibration-carriage-dock).
6. Optional: load `vidga-curtain-remote.hex` on a second Calliope.

## Known issues

- **Motor force on 2×AAA:** the built-in driver passes the battery voltage (~2.4–2.8 V) to a 3 V motor. Heavy curtains may stall it. Options: a slower worm motor, Ø20 mm wheels, or 4×AA + an external DRV8833 driver ([troubleshooting](docs/troubleshooting.md)).
- **Battery life:** the Calliope 1.3 can't deep-sleep (~15 mA), so 2×AAA last only 2–4 days off the dock. The dock tops them up while the curtain is open.
- **Glider dimensions** in the CAD models are estimated from photos – measure yours.
- Tested on a 3-track VIDGA rail. A 1-track rail has no outer tracks for the gliders.

## Safety

- Only **NiMH** rechargeables in a holder wired to the dock – never alkaline.
- Never more than 3.3 V on the Calliope mini 1.3 battery socket.
- Keep the speed low and the safety timeout in the firmware so nothing gets pinched.

## License

- Firmware and scripts: [MIT](LICENSE)
- Documentation, drawings and 3D models: [CC BY-SA 4.0](LICENSE-docs)

IKEA and VIDGA are trademarks of Inter IKEA Systems B.V.; LEGO is a trademark of the LEGO Group; Calliope mini is a trademark of Calliope gGmbH. This project is not affiliated with or endorsed by any of them.
