// CARRIAGE – charging dock + light sensor (Calliope mini 1.3, 2 x NiMH AAA)
// Works with firmware/remote. Needs the dock-sense wiring on P0 (see docs/wiring.md) –
// without it P0 floats and the program may think it is always docked.
//
// Wiring:
//   Worm motor      → Calliope motor pins A and B (built-in driver)
//   2 x NiMH AAA    → Calliope battery socket (JST)
//   Pogo pin 1 (+5 V when docked) → 1N5819 → 33 Ω → AAA holder +
//   Pogo pin 1      → 10 kΩ → P0 → 10 kΩ → GND      (P0 reads HIGH when docked)
//   Pogo pin 2      → GND ("−" edge pad)
//
// HOME = fully OPEN = carriage touching the charging dock. Closing runs for FULL_MS (measure it).
// Light automation: opens when it has been bright for 5 minutes, closes when dark for 5 minutes.
// It only reacts when day turns to night or night turns to day, so a manual command is not undone.

radio.setGroup(42)

const SPEED = 100          // motor power in % (built-in driver gets battery voltage, ~2.5 V)
const OPEN_DIR = 1         // set to -1 if "open" drives the wrong way
let FULL_MS = 50000        // full travel time for your curtain – measure it (A+B calibration)
const EXTRA_MS = 5000      // extra time allowed when opening before giving up
const DAY_LEVEL = 60       // light level (0–255) counted as day   – calibrate (A+B while idle)
const NIGHT_LEVEL = 15     // light level counted as night
const CONFIRM = 30         // 30 readings × 10 s = 5 minutes before acting

let state = "idle"
let startTime = 0
let startPos = -1          // position in ms from home; -1 = unknown until the first "open"
let pos = -1
let isDay = input.lightLevel() > DAY_LEVEL
let dayCount = 0
let nightCount = 0

function docked(): boolean { return pins.digitalReadPin(DigitalPin.P0) == 1 }

function drive(dir: number) {
    motors.motorPower(dir * SPEED)     // negative = other direction, 0 = stop
}

function elapsed(): number { return input.runningTime() - startTime }

function stopMotor(reply: string) {
    if (state == "closing" && startPos >= 0) pos = Math.min(FULL_MS, startPos + elapsed())
    if (state == "opening" && startPos >= 0) pos = Math.max(0, startPos - elapsed())
    drive(0)
    state = "idle"
    radio.sendString(reply)
    basic.clearScreen()
}

function startOpen() {
    if (state != "idle") return
    if (docked()) { pos = 0; radio.sendString("done"); return }
    state = "opening"; startTime = input.runningTime(); startPos = pos
    drive(OPEN_DIR)
    basic.showArrow(ArrowNames.East)
}

function startClose() {
    if (state != "idle") return
    if (pos < 0) {                       // position unknown: go home to the dock first
        startOpen(); return
    }
    if (pos >= FULL_MS) { radio.sendString("done"); return }
    state = "closing"; startTime = input.runningTime(); startPos = pos
    drive(-OPEN_DIR)
    basic.showArrow(ArrowNames.West)
}

radio.onReceivedString(function (cmd) {
    if (cmd == "open") startOpen()
    else if (cmd == "close") startClose()
    else if (cmd == "stop") stopMotor("done")
})
input.onButtonPressed(Button.A, function () { startOpen() })
input.onButtonPressed(Button.B, function () { startClose() })
input.onButtonPressed(Button.AB, function () {
    if (state == "idle") {               // idle: show the current light level for calibration
        basic.showNumber(input.lightLevel())
        basic.clearScreen()
        return
    }
    const wasClosing = state == "closing"
    const t = elapsed()
    const fromHome = startPos == 0
    stopMotor("done")
    // Travel-time calibration: dock (open), press B, press A+B exactly when fully closed.
    if (wasClosing && fromHome) basic.showNumber(Math.round(t / 100) / 10)
})

// Motor supervision
basic.forever(function () {
    if (state == "opening") {
        if (docked()) {
            drive(0); pos = 0; state = "idle"; radio.sendString("done"); basic.clearScreen()
        } else {
            const limit = (startPos >= 0 ? startPos : FULL_MS) * 1.3 + EXTRA_MS
            if (elapsed() > limit) { stopMotor("error"); basic.showIcon(IconNames.Sad) }   // stuck or slipping
        }
    } else if (state == "closing") {
        if (startPos + elapsed() >= FULL_MS) stopMotor("done")
    }
    basic.pause(20)
})

// Light automation: one reading every 10 s while idle (display off, so the reading is clean)
basic.forever(function () {
    basic.pause(10000)
    if (state != "idle") return
    const level = input.lightLevel()
    if (!isDay) {
        dayCount = level > DAY_LEVEL ? dayCount + 1 : 0
        if (dayCount >= CONFIRM) { isDay = true; dayCount = 0; startOpen() }
    } else {
        nightCount = level < NIGHT_LEVEL ? nightCount + 1 : 0
        if (nightCount >= CONFIRM) { isDay = false; nightCount = 0; startClose() }
    }
})
