import board
import digitalio
import keymap
from adafruit_hid.keycode import Keycode
import time
import bt

pins = [
    board.IO6, board.IO21, board.IO10, board.IO9,
    board.IO4, board.IO3,  board.IO2, board.IO0
]
buttons = [digitalio.DigitalInOut(pin) for pin in pins]
for btn in buttons:
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP

def read_keys():
    result = []
    
    last_held = [
        False, False, False, False,
        False, False, False, False
    ]
    
    while True:
        blocked = len(result) > 0
        released = [btn.value for btn in buttons]
        held = [not btn for btn in released]
    
        up = [before and not now for (before, now) in zip(last_held, held)]
    
        if any(up) and not blocked:
            result = last_held
            continue

        if all(released) and blocked:
            return result
            
        last_held = held

while True:
    combo = read_keys()

    matches = [meaning for meaning, keys in keymap.base.items() if keys == combo]
    if len(matches) != 1:
        print("unknown combo")
        print(combo[0:4])
        print(combo[4:8])
        continue
    if not bt.ble.connected:
        print("not connected and memory is not implemented yet")

    sym = matches[0]
    if sym == "backspace":
        bt.k.press(Keycode.BACKSPACE)
    elif sym == "enter":
        bt.k.press(Keycode.ENTER)
    else:
        bt.kl.write(sym)
    bt.k.release_all()
    
    # kb_demo()
