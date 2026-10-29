// REMOTE – Calliope mini (or micro:bit) in your hand
// Paste into makecode.calliope.cc → JavaScript view
// A = open, B = close, A+B = stop

radio.setGroup(42)          // must match the carriage
radio.setTransmitPower(7)   // max range

input.onButtonPressed(Button.A, function () {
    radio.sendString("open")
    basic.showArrow(ArrowNames.West)
})

input.onButtonPressed(Button.B, function () {
    radio.sendString("close")
    basic.showArrow(ArrowNames.East)
})

input.onButtonPressed(Button.AB, function () {
    radio.sendString("stop")
    basic.showIcon(IconNames.No)
})

// Status messages sent back by the carriage
radio.onReceivedString(function (msg) {
    if (msg == "done") {
        basic.showIcon(IconNames.Yes)
    } else if (msg == "error") {
        basic.showIcon(IconNames.Sad)
    }
    basic.pause(1000)
    basic.clearScreen()
})
