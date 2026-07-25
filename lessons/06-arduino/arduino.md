# Guide to Arduino

**Ages:** about 11+ (younger with help)

**Prerequisites (required):**

- [Beginner Circuits](../03-circuits/beginner.md)
- [Intermediate Circuits](../03-circuits/intermediate.md) — transistors, diodes, voltage
  dividers, and safe motor switching

**Strongly recommended:** the [micro:bit V2 guide](../04-microbit/microbit-v2.md) so you
already practiced sensors and outputs with MakeCode.

**Gentler text path:** If C++ sketches feel like a big jump, start with
[CircuitPython (Pico)](../05-circuitpython/circuitpython.md) first — Python on the board
— then come back here when you want Uno + Arduino IDE.

**Goal:** Install the Arduino IDE, upload your first sketch, map Scratch / MakeCode
ideas to text code, and follow curated beginner projects — reusing the wiring habits
from Circuits.

*Disclaimer: There is no affiliation with Amazon; product links are for convenience
only.*

______________________________________________________________________

## 1. Getting your gear

Start with an **Arduino Uno R3** (or a compatible Uno-shaped board). Uno R4 or a Nano
also works if you pick the matching board name in the IDE.

| Item                                   | What it does                     | Where to find it                                                                                     |
| -------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Arduino Uno R3** (or compatible)     | The board you program            | [Arduino Store](https://store.arduino.cc/), [Uno R3 on Amazon](https://www.amazon.com/dp/B00834SISO) |
| **USB cable** (A to B for classic Uno) | Power + upload                   | Often included with the board                                                                        |
| **Breadboard + jumper wires + parts**  | LEDs, resistors, buttons, motors | Reuse your [Circuits](../03-circuits/beginner.md) kit                                                |

Optional: an electronics starter kit that already includes an Uno-compatible board and
sensors — useful if you want one box, but not required if you already have Circuits
parts.

______________________________________________________________________

## 2. Arduino vs. micro:bit

|              | **micro:bit**                                      | **Arduino Uno**                                 |
| ------------ | -------------------------------------------------- | ----------------------------------------------- |
| Built-ins    | LED matrix, buttons, sensors, speaker on the board | Usually just an onboard LED — you wire the rest |
| Coding start | MakeCode blocks (Scratch-like)                     | Text sketches (`setup` / `loop`)                |
| Strength     | Fast first wins with almost no wiring              | More pins and flexibility for custom circuits   |
| Path here    | Great after Beginner Circuits                      | Next step after Intermediate Circuits           |

Arduino is not “harder electronics magic” — it is the same breadboard skills with a
board that expects you to write (or remix) short text programs.

______________________________________________________________________

## 3. Install and first upload

1. Download the Arduino IDE from
   [arduino.cc/en/software](https://www.arduino.cc/en/software) (Desktop IDE). The
   [Arduino Cloud / Web Editor](https://cloud.arduino.cc/) is a fine alternate if you
   prefer the browser.
2. Install, open the IDE, and connect the Uno with USB.
3. Choose your board and port: **Tools → Board** (e.g. Arduino Uno) and **Tools →
   Port**.
4. Open the Blink example: **File → Examples → 01.Basics → Blink**.
5. Click **Upload**. The onboard LED should blink.

Official help:

- [Getting Started with the Arduino Desktop IDE](https://projecthub.arduino.cc/Arduino_Genuino/getting-started-with-the-arduino-desktop-ide-0aa470)
- [How to write a Sketch](https://docs.arduino.cc/learn/programming/sketches/) —
  structure of a sketch, `setup()`, `loop()`, and how programs run
- [Built-in Examples](https://docs.arduino.cc/built-in-examples/)

If upload fails: check the cable (some charge-only cables do not work), the Port menu,
and that the board selection matches what you plugged in.

______________________________________________________________________

## 4. Scratch / MakeCode → sketch map

Read [How to write a Sketch](https://docs.arduino.cc/learn/programming/sketches/) for
the full official guide. The table below is a quick map from Scratch / MakeCode ideas.

| Scratch / MakeCode idea    | Arduino sketch                                                          |
| -------------------------- | ----------------------------------------------------------------------- |
| When the program starts    | `setup()` — runs once                                                   |
| `forever` / forever loop   | `loop()` — runs again and again                                         |
| Wait / pause               | `delay(milliseconds)`                                                   |
| Set pin / digital write    | `digitalWrite(pin, HIGH)` or `LOW`                                      |
| Read button / digital read | `digitalRead(pin)`                                                      |
| Read sensor (0–1023 style) | `analogRead(pin)`                                                       |
| Dim LED / motor speed idea | `analogWrite(pin, 0–255)` on PWM pins (PWM intuition from Intermediate) |
| Variable                   | `int`, `bool`, etc. at the top or inside functions                      |

A tiny Blink-style sketch (same idea as the built-in example):

```cpp
// setup runs once when the board powers on or resets
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);  // onboard LED pin as output
}

// loop runs forever — like Scratch "forever"
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // LED on
  delay(1000);                      // wait 1 second
  digitalWrite(LED_BUILTIN, LOW);   // LED off
  delay(1000);
}
```

Read the comments in IDE examples — they are written for learners.

______________________________________________________________________

## 5. Wiring habits (do not skip)

Before you follow project tutorials, keep Intermediate Circuits habits:

- An LED needs a series resistor (often **220Ω**).
- A board pin is a **signal**, not a motor power supply — use a transistor (and flyback
  diode) for motors.
- Share **GND** whenever the Arduino and another power source are in the same circuit.
- Power off or unplug USB before major rewires.

Refresh: [Intermediate Circuits](../03-circuits/intermediate.md).

______________________________________________________________________

## 6. Curated projects (build these next)

Work top to bottom. Prefer the examples inside the IDE (**File → Examples**) and the
official docs — then remix (change pins, delays, or thresholds).

### Built-in path (in the IDE)

1. **Blink** — `Examples → 01.Basics → Blink` (onboard LED)
2. **DigitalReadSerial** — read a pin and watch the Serial Monitor
3. **Button** — `Examples → 02.Digital → Button` (external button + LED)
4. **AnalogReadSerial** / **AnalogInput** — potentiometer or sensor voltage
5. **Fade** — `Examples → 03.Analog → Fade` (PWM brightness)

Docs index: [Built-in Examples](https://docs.arduino.cc/built-in-examples/).

### Wiring + code (after Blink feels easy)

- [How to Wire and Program a Button](https://docs.arduino.cc/built-in-examples/digital/button/)
- External LED on a breadboard — many kits walk through pin 13 or another digital pin
  with a 220Ω resistor to GND (same idea as Beginner Circuit 1, plus `digitalWrite`)
- Motor with transistor + flyback diode — reuse
  [Intermediate Circuit 4](../03-circuits/intermediate.md#circuit-4-motor--flyback-diode)
  and drive the transistor base from an Arduino pin through a resistor (never power the
  motor from the pin alone)

### Stretch

Browse [Arduino Project Hub](https://projecthub.arduino.cc/) for ideas once the built-in
examples feel comfortable. Remix one project instead of copying five.

______________________________________________________________________

## 7. Learning checklist

Before you call this module done, you should be able to:

- [ ] Install the IDE (or Web Editor) and upload Blink
- [ ] Explain `setup()` vs `loop()` in your own words
- [ ] Blink an **external** LED with a resistor on the breadboard
- [ ] Read a button or potentiometer in a sketch
- [ ] Explain why a motor needs a transistor driver and flyback diode
- [ ] Complete several built-in Examples and change something in each

______________________________________________________________________

## What’s next

You reached Arduino sketches on the core electronics path. Many learners also complete
[CircuitPython](../05-circuitpython/circuitpython.md) (before or after this guide).

1. **Invent and share** — combine a sensor (divider / pot / LDR) with an output (LED,
   buzzer, or transistor-driven motor).
2. Prefer Python on a Pico? →
   [Guide to CircuitPython](../05-circuitpython/circuitpython.md).
3. Revisit [Beginner](../03-circuits/beginner.md) or
   [Intermediate Circuits](../03-circuits/intermediate.md) anytime wiring feels shaky.
4. Revisit the [micro:bit guide](../04-microbit/microbit-v2.md) if you want more
   block-based practice.

**Coming later on this course (planned):** Arduino schematic mission labs, ESP32, full
Raspberry Pi computer projects, libraries and shields, and a capstone / certificate
track. For now, keep building.
