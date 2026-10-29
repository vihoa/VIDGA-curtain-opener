# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Motor doesn't turn at all | Wrong holes / loose contact | Run the motor pin test; wires must turn the motor both ways in phases 1 and 2 |
| Motor turns only a little | One wire on GND instead of A/B | Use the two holes that worked in phases 1 and 2 |
| Wheels spin, carriage stands | Too little grip | Shorten the spring loops, softer tyres, clean the rail underside |
| Motor hums / stops, wheels don't turn | Too little force | Test on USB (≈4.7 V vs ≈2.5 V on batteries). Then: slower worm motor, smaller wheels (Ø20 ≈ 1.7× force), or 4×AA + DRV8833 driver |
| Curtain is hard to pull | Friction | Silicone spray in the track (no oil), check for stuck gliders, curtain not dragging. Pull test: ≤3–5 N is fine |
| Carriage nods forward/back | Frame can rock around the line between the 2 gliders | Option: add 2 more gliders + springs so each corner is held (4 in total, each spring weaker) |
| Carriage twists and drops off | Soft, uneven springs | Equal loop length, spring pulling straight up; keep heavy parts centred under the middle |
| Something catches in the middle slot | Guide pegs / axles in the slot | Don't put anything into the slot – shorten/round the pegs, or use extra gliders as guides |
| B (close) does nothing in `carriage-dock` | P0 not wired → reads "docked" | Wire the 10k/10k divider, or use `carriage-simple` |
| Opener drives the wrong way | Motor polarity | Swap the motor wires or set `OPEN_DIR = -1` |
| Batteries flat after 2–4 days | Calliope 1.3 can't deep-sleep (~15 mA) | Use the charging dock; the curtain must be open (docked) several hours a day |
| Dock pin 1 shows ~2.5 V when undocked | Diode reversed | Turn the diode: stripe towards the battery |
| Carriage sticks to the dock | Magnets too strong | Smaller connector, or mount it so the halves slide apart sideways |
