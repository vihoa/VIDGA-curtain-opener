// CARRIAGE – SIMPLE VERSION (Calliope mini 1.3): buttons + remote, no dock, no light sensor
// Same controls as before: A = open, B = close, press again while moving = stop.
// Remote (firmware/remote, radio group 42): A = open, B = close, A+B = stop.
//
// Software can't give the motor more than 100 % – but it can help it get going:
//  1. Always full power (100 %).
//  2. "Wiggle start": a short push backwards first, then full power forwards.
//     This breaks the curtain free from standing still (static friction).
//  3. Pulse mode: drive PULSE_ON ms, pause PULSE_OFF ms, repeat.
//     The short pauses let the battery voltage recover, so each push is stronger.
//  4. LED display off while driving: saves current, so the motor gets more voltage.

const OPEN_DIR = 1         // set to -1 if A drives the wrong way
const MAX_MS = 60000       // safety stop: your travel time + a few seconds
const WIGGLE_MS = 150      // short push backwards before starting (0 = off)
const PULSE_ON = 1500      // drive time per pulse in ms
const PULSE_OFF = 150      // pause between pulses in ms (0 = drive continuously)

radio.setGroup(42)

let moving = false
let dir = 0
let startTime = 0

function stop() {
    motors.motorPower(0)
    moving = false
    basic.showIcon(IconNames.Square)
    radio.sendString("done")
}

function go(d: number) {
    if (moving) { stop(); return }      // second press = stop
    dir = d
    basic.showArrow(d == OPEN_DIR ? ArrowNames.East : ArrowNames.West)
    basic.pause(300)
    basic.clearScreen()                 // display off while driving
    if (WIGGLE_MS > 0) {
        motors.motorPower(-dir * 100)   // short push the other way …
        basic.pause(WIGGLE_MS)
        motors.motorPower(0)
        basic.pause(80)
    }
    moving = true
    startTime = input.runningTime()
}

input.onButtonPressed(Button.A, function () { go(OPEN_DIR) })
input.onButtonPressed(Button.B, function () { go(-OPEN_DIR) })

radio.onReceivedString(function (cmd) {
    if (cmd == "open") go(OPEN_DIR)
    else if (cmd == "close") go(-OPEN_DIR)
    else if (cmd == "stop" && moving) stop()
})

basic.forever(function () {
    if (!moving) { basic.pause(50); return }
    if (input.runningTime() - startTime > MAX_MS) { stop(); return }
    motors.motorPower(dir * 100)        // … then full power
    basic.pause(PULSE_ON)
    if (moving && PULSE_OFF > 0) {
        motors.motorPower(0)
        basic.pause(PULSE_OFF)
    }
})

basic.showIcon(IconNames.Square)
