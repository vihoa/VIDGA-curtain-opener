// MOTOR PIN TEST 2 – Calliope mini 1.3, full power
// Paste into makecode.calliope.cc → JavaScript view, then download.
// Push the motor wires FIRMLY into the holes (jumper wires or bare wire ends pushed in, not just held).
// Watch the display number and note in which phase the motor turns:
//   1 = single motor, forward (100 %)      2 = single motor, backward (100 %)
//   3 = only output "M0" on (100 %)        4 = only output "M1" on (100 %)
// A+B stops, A restarts.

let running = true

input.onButtonPressed(Button.AB, function () {
    running = false
    motors.motorPower(0)
    motors.dualMotorPower(Motor.M0_M1, 0)
    basic.showIcon(IconNames.No)
})
input.onButtonPressed(Button.A, function () {
    running = true
})

function phase(n: number) {
    basic.showNumber(n)
    basic.pause(2500)
    motors.motorPower(0)
    motors.dualMotorPower(Motor.M0_M1, 0)
    basic.clearScreen()
    basic.pause(700)
}

basic.forever(function () {
    if (!running) { basic.pause(100); return }
    motors.motorPower(100); phase(1)
    if (!running) return
    motors.motorPower(-100); phase(2)
    if (!running) return
    motors.dualMotorPower(Motor.M0, 100); phase(3)
    if (!running) return
    motors.dualMotorPower(Motor.M1, 100); phase(4)
})
