# Guide to CircuitPython

**Ages:** about 11+ (younger with help)

**Prerequisites (required):**

- [Beginner Circuits](../03-circuits/beginner.md)
- [Intermediate Circuits](../03-circuits/intermediate.md) — transistors, diodes, voltage
  dividers, and safe motor switching

**Strongly recommended:** the [micro:bit V2 guide](../04-microbit/microbit-v2.md) so you
already practiced sensors and outputs with blocks.

**Goal:** Program a real board with **Python** (CircuitPython) — a gentler text step
after Scratch / MakeCode than jumping straight to Arduino C++ sketches.

**Path choice after Intermediate Circuits**

| Path                                         | Language               | Best when…                                                   |
| -------------------------------------------- | ---------------------- | ------------------------------------------------------------ |
| **This guide (recommended first)**           | CircuitPython (Python) | You want text code that still reads a bit like Scratch ideas |
| [Guide to Arduino](../06-arduino/arduino.md) | C++ sketches           | You specifically need Uno / Arduino IDE sketches             |

You can do **both**. Many learners do CircuitPython first, then Arduino later.

*Disclaimer: There is no affiliation with Amazon; product links are for convenience
only.*

______________________________________________________________________

## 1. Getting your gear

**Default board:**
[Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) (or **Pico
W** if you want Wi‑Fi later). It is inexpensive, widely used with CircuitPython, and
easy to find.

**Arduino-branded option:** [Arduino Nano RP2040 Connect](https://store.arduino.cc/) —
same RP2040 family ideas, Arduino shape and store ecosystem. Setup steps are similar
(install CircuitPython UF2 for that board); pin names differ, so follow the board’s
pinout.

| Item                               | What it does                      | Where to find it                                                                                                                |
| ---------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Raspberry Pi Pico** (or Pico W)  | The board you program             | [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-pico/), [Pico on Amazon](https://www.amazon.com/dp/B08TQSKF45) |
| **USB micro cable** (data-capable) | Power + copy files / serial       | Often sold with the Pico                                                                                                        |
| **Breadboard + jumpers + parts**   | LEDs, resistors, buttons, sensors | Reuse your [Circuits](../03-circuits/beginner.md) kit                                                                           |
| **Optional: Nano RP2040 Connect**  | Arduino-shaped RP2040 board       | [Arduino Store](https://store.arduino.cc/)                                                                                      |

Classic **Arduino Uno** does **not** run CircuitPython. For Uno, use the
[Arduino sketch guide](../06-arduino/arduino.md) instead.

______________________________________________________________________

## 2. Why CircuitPython after Scratch / MakeCode?

- You type **Python**, not C++ — indentation and plain words (`if`, `while`, `print`)
  feel closer to reading Scratch scripts than Arduino sketches do.
- The board shows up like a **USB drive**. You edit `code.py`, save, and it runs — no
  separate “compile and upload” dance at first.
- Adafruit’s Learn guides are written for beginners and match breadboard projects.

Arduino C++ sketches are still useful (especially for Uno). They are just a bigger jump;
save them for when Python on the Pico feels comfortable — or when a project needs Uno.

______________________________________________________________________

## 3. Install CircuitPython (Pico)

Follow Adafruit’s current Pico guide (UF2 files change over time — use the live page):

1. [CircuitPython on Raspberry Pi Pico](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython)
2. Put the Pico in bootloader mode (hold **BOOTSEL**, plug in USB, release).
3. Drag the CircuitPython `.uf2` onto the `RPI-RP2` drive.
4. After it reboots, you should see a **CIRCUITPY** drive with `code.py`.

**Editor:** [Mu Editor](https://codewith.mu/) (CircuitPython mode) or
[Thonny](https://thonny.org/) are both fine for kids.

**Nano RP2040 Connect:** use Adafruit’s CircuitPython installer page for that board
(search “CircuitPython Arduino Nano RP2040 Connect” on
[circuitpython.org](https://circuitpython.org/downloads)) and the same Mu/Thonny
workflow.

______________________________________________________________________

## 4. Scratch / MakeCode → Python map

| Scratch / MakeCode idea    | CircuitPython                                  |
| -------------------------- | ---------------------------------------------- |
| When the program starts    | Top of `code.py` (runs from the start)         |
| `forever`                  | `while True:`                                  |
| Wait / pause               | `time.sleep(seconds)`                          |
| Digital write (LED on/off) | `led.value = True` / `False` (or `digitalio`)  |
| Read button                | `button.value` with `digitalio` + pull-up/down |
| Analog sensor              | `analogio.AnalogIn`                            |
| Print / debug              | `print(...)` (Serial / Mu plotter)             |

Blink-style idea on the Pico (onboard LED — exact pin helper may vary by board; see the
Adafruit Pico guide for the recommended snippet):

```python
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
```

Save as `code.py` on **CIRCUITPY**. The LED should blink. Change the `0.5` values to
remix the timing — same habit as remixing Scratch.

______________________________________________________________________

## 5. Wiring habits (same as Intermediate)

- LED + **220Ω** resistor
- Pin = **signal**, not motor power — transistor + flyback diode for motors
- Common **GND** with any second power source
- Unplug or power off before big rewires

Refresh: [Intermediate Circuits](../03-circuits/intermediate.md).

______________________________________________________________________

## 6. Curated projects

Work through Adafruit Learn (keep the browser guide open; copy patterns into `code.py`):

1. Finish the Pico “getting started” blink / REPL steps on
   [Getting Started with Pico + CircuitPython](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython)
2. External LED on a breadboard — same wiring as Beginner Circuit 1, driven from a GPIO
   pin
3. Button input — digital read + pull resistor (or internal pull)
4. Potentiometer or light sensor — analog input (voltage divider ideas from
   Intermediate)
5. Browse more:
   [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials) and
   project guides on [learn.adafruit.com](https://learn.adafruit.com/)

Remix rule: change pin numbers, delays, or thresholds after each tutorial works.

______________________________________________________________________

## 7. Learning checklist

- [ ] Install CircuitPython so **CIRCUITPY** appears
- [ ] Edit and save `code.py` so the board runs your program
- [ ] Explain `while True:` like Scratch `forever`
- [ ] Blink an **external** LED with a resistor
- [ ] Read a button or analog sensor
- [ ] Explain why a motor still needs a transistor driver

______________________________________________________________________

## What’s next

1. **Invent and share** — sensor in, LED / sound / transistor-driven motor out.
2. Continue to [Robot Missions](../07-robot-missions/robot-missions.md) — timed missions
   and driver control (classroom board or competition robot brain).
3. Ready for Uno + C++ sketches? → [Guide to Arduino](../06-arduino/arduino.md) (you can
   do Arduino before or after Robot Missions).
4. Revisit [Circuits](../03-circuits/beginner.md) or the
   [micro:bit guide](../04-microbit/microbit-v2.md) anytime.
