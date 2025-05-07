import time
import digitalio
import board
import adafruit_matrixkeypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

time.sleep(3)  # Sleep for a bit to avoid a race condition on some systems

# LED setup
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# Keyboard setup
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
hook = digitalio.DigitalInOut(board.SDA)
hook.direction = digitalio.Direction.INPUT
hook.pull = digitalio.Pull.UP

cols = [digitalio.DigitalInOut(x) for x in (board.SCL, board.D5, board.D6)]
rows = [digitalio.DigitalInOut(x) for x in (
    board.D12, board.D11, board.D10, board.D9)]

keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ('*', 0, '#'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
hookChanged = False
keyDown = False
firstUse = True

while True:
    # if the keypad is pressed, the led will light up. If the keypad is not pressed, the led will not light up.
    # if keypad.pressed_keys:
    #     led.value = True
    # else:
    #     led.value = False

    keys = keypad.pressed_keys

    if hook.value:
        if not hookChanged:
            if firstUse:
                firstUse = False
            else:
                print("hangUp")
                led.value = False
                keyboard.press(Keycode.LEFT_SHIFT, Keycode.LEFT_ALT,
                               Keycode.LEFT_CONTROL, Keycode.H)
                keyboard.release_all()
        hookChanged = True
    else:
        if hookChanged:
            print("pickUp")
            hookChanged = False
            led.value = True
            keyboard.press(Keycode.LEFT_SHIFT, Keycode.LEFT_ALT,
                           Keycode.LEFT_CONTROL, Keycode.P)
            keyboard.release_all()

    if keys:
        if not keyDown:
            key = keys[0]
            print("keyDown", key)
            if key == 0:
                keyboard.press(Keycode.ZERO)
            if key == 1:
                keyboard.press(Keycode.ONE)
            if key == 2:
                keyboard.press(Keycode.TWO)
            if key == 3:
                keyboard.press(Keycode.THREE)
            if key == 4:
                keyboard.press(Keycode.FOUR)
            if key == 5:
                keyboard.press(Keycode.FIVE)
            if key == 6:
                keyboard.press(Keycode.SIX)
            if key == 7:
                keyboard.press(Keycode.SEVEN)
            if key == 8:
                keyboard.press(Keycode.EIGHT)
            if key == 9:
                keyboard.press(Keycode.NINE)
            if key == '*':
                keyboard.press(Keycode.LEFT_SHIFT, Keycode.EIGHT)
            if key == '#':
                keyboard.press(Keycode.LEFT_SHIFT, Keycode.THREE)
        keyDown = True
    else:
        if keyDown:
            print("keyUp")
            keyboard.release_all()
            keyDown = False
    time.sleep(0.025)