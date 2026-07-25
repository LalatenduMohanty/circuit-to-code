# Course path

**Core path:** Scratch → Beginner Circuits → micro:bit → Intermediate Circuits → then
choose a text path:

- **Recommended:** [CircuitPython](05-circuitpython/) (Python on Pico / Nano RP2040)
- **Also available:** [Arduino](06-arduino/) (Uno + C++ sketches)

Then continue to **[Robot Missions](07-robot-missions/)** (timed missions, driver
control, safe motors). You can do both text paths first; CircuitPython is usually the
gentler jump from Scratch / MakeCode.

**Optional:** After Scratch, try SPIKE Prime if you have the kit — then continue to
Beginner Circuits. Skipping SPIKE is fine.

**Circuits module:** Beginner and Intermediate are two sections in
[`03-circuits/`](03-circuits/). Do Beginner before micro:bit; do Intermediate after
micro:bit (and before CircuitPython or Arduino).

Each folder is a self-contained unit with its lesson markdown and any diagrams it needs.

| Order | Module                                     | What you learn                                      |
| ----- | ------------------------------------------ | --------------------------------------------------- |
| 1     | [`01-scratch/`](01-scratch/)               | Block coding foundations with Scratch               |
| 2     | [`02-spike-prime/`](02-spike-prime/)       | *(Optional)* Same ideas on LEGO SPIKE Prime         |
| 3     | [`03-circuits/`](03-circuits/)             | Breadboard electronics — Beginner + Intermediate    |
| 4     | [`04-microbit/`](04-microbit/)             | Physical computing with the BBC micro:bit V2        |
| 5     | [`05-circuitpython/`](05-circuitpython/)   | Python on Pico (or Nano RP2040) — gentler text path |
| 6     | [`06-arduino/`](06-arduino/)               | C++ sketches on Arduino Uno                         |
| 7     | [`07-robot-missions/`](07-robot-missions/) | Mission robots — timed + driver control             |

**Mentors:** skills map and meeting ideas for Robot Missions are in
[`docs/robot-missions-coach.md`](../docs/robot-missions-coach.md).

**Coming later:** deeper mission labs, ESP32, full Raspberry Pi, libraries/shields, and
a capstone / certificate track.

## Contents

### 1. [Learning Scratch Programming](01-scratch/scratch-programming.md)

- [Why learn Scratch?](01-scratch/scratch-programming.md#why-learn-scratch)
- [Getting started](01-scratch/scratch-programming.md#getting-started)
- [Core skills (watch these first)](01-scratch/scratch-programming.md#core-skills-watch-these-first)
- [Beginner projects](01-scratch/scratch-programming.md#beginner-projects)
- [Intermediate projects](01-scratch/scratch-programming.md#intermediate-projects)
- [Advanced projects](01-scratch/scratch-programming.md#advanced-projects)
- [What’s next](01-scratch/scratch-programming.md#whats-next)

### 2. [LEGO SPIKE Prime (optional)](02-spike-prime/spike-prime.md)

- [Why try SPIKE after Scratch?](02-spike-prime/spike-prime.md#why-try-spike-after-scratch)
- [What you need](02-spike-prime/spike-prime.md#what-you-need)
- [How to learn (use official lessons)](02-spike-prime/spike-prime.md#how-to-learn-use-official-lessons)
- [Learning outline (checklist)](02-spike-prime/spike-prime.md#learning-outline-checklist)
- [Scratch → SPIKE reminder](02-spike-prime/spike-prime.md#scratch--spike-reminder)
- [What’s next](02-spike-prime/spike-prime.md#whats-next)

### 3. Circuits — [Beginner](03-circuits/beginner.md) and [Intermediate](03-circuits/intermediate.md)

#### Beginner

- [What you need](03-circuits/beginner.md#what-you-need)
- [Mission 0: The Maker Rules](03-circuits/beginner.md#mission-0-the-maker-rules)
- [If it doesn’t work (Troubleshoot)](03-circuits/beginner.md#if-it-doesnt-work-troubleshoot)
- [Phase 1: The Basics of Flow](03-circuits/beginner.md#phase-1-the-basics-of-flow)
- [Phase 2: Sensors and Adjustments](03-circuits/beginner.md#phase-2-sensors-and-adjustments)
- [Phase 3: Hardware Magic (Logic & Timers)](03-circuits/beginner.md#phase-3-hardware-magic-logic-timers)
- [What’s next](03-circuits/beginner.md#whats-next)

#### Intermediate (after micro:bit; before CircuitPython or Arduino)

- [What you need](03-circuits/intermediate.md#what-you-need)
- [Mission 0: Intermediate Maker Rules](03-circuits/intermediate.md#mission-0-intermediate-maker-rules)
- [Phase 1: Stronger Switching](03-circuits/intermediate.md#phase-1-stronger-switching)
- [Phase 2: Signals Boards Can Read](03-circuits/intermediate.md#phase-2-signals-boards-can-read)
- [Phase 3: Motors and Speed](03-circuits/intermediate.md#phase-3-motors-and-speed)
- [Mission wrap: Power checklist](03-circuits/intermediate.md#mission-wrap-power-checklist-before-arduino)
- [What’s next](03-circuits/intermediate.md#whats-next)

### 4. [Guide to micro:bit V2](04-microbit/microbit-v2.md)

- [1. Getting your gear](04-microbit/microbit-v2.md#1-getting-your-gear)
- [2. Micro:bit vs. Arduino](04-microbit/microbit-v2.md#2-microbit-vs-arduino)
- [3. Extra electronic components](04-microbit/microbit-v2.md#3-extra-electronic-components)
- [4. Setting up your lab](04-microbit/microbit-v2.md#4-setting-up-your-lab)
- [5. Video tutorials and project ideas](04-microbit/microbit-v2.md#5-video-tutorials-and-project-ideas)
- [6. Other starter kits](04-microbit/microbit-v2.md#6-other-starter-kits)
- [What’s next](04-microbit/microbit-v2.md#whats-next)

### 5. [Guide to CircuitPython](05-circuitpython/circuitpython.md)

- [1. Getting your gear](05-circuitpython/circuitpython.md#1-getting-your-gear)
- [2. Why CircuitPython after Scratch / MakeCode?](05-circuitpython/circuitpython.md#2-why-circuitpython-after-scratch--makecode)
- [3. Install CircuitPython (Pico)](05-circuitpython/circuitpython.md#3-install-circuitpython-pico)
- [4. Scratch / MakeCode → Python map](05-circuitpython/circuitpython.md#4-scratch--makecode--python-map)
- [5. Wiring habits](05-circuitpython/circuitpython.md#5-wiring-habits-same-as-intermediate)
- [6. Curated projects](05-circuitpython/circuitpython.md#6-curated-projects)
- [7. Learning checklist](05-circuitpython/circuitpython.md#7-learning-checklist)
- [What’s next](05-circuitpython/circuitpython.md#whats-next)

### 6. [Guide to Arduino](06-arduino/arduino.md)

- [1. Getting your gear](06-arduino/arduino.md#1-getting-your-gear)
- [2. Arduino vs. micro:bit](06-arduino/arduino.md#2-arduino-vs-microbit)
- [3. Install and first upload](06-arduino/arduino.md#3-install-and-first-upload)
- [4. Scratch / MakeCode → sketch map](06-arduino/arduino.md#4-scratch--makecode--sketch-map)
- [5. Wiring habits](06-arduino/arduino.md#5-wiring-habits-do-not-skip)
- [6. Curated projects](06-arduino/arduino.md#6-curated-projects-build-these-next)
- [7. Learning checklist](06-arduino/arduino.md#7-learning-checklist)
- [What’s next](06-arduino/arduino.md#whats-next)

### 7. [Robot Missions](07-robot-missions/robot-missions.md)

- [You’re building mission robots](07-robot-missions/robot-missions.md#youre-building-mission-robots)
- [Two ways to practice](07-robot-missions/robot-missions.md#two-ways-to-practice)
- [Mission 0: Robot lab rules](07-robot-missions/robot-missions.md#mission-0-robot-lab-rules)
- [Lab A: Two kinds of programs](07-robot-missions/robot-missions.md#lab-a-two-kinds-of-programs)
- [Lab B: One motor + one sensor](07-robot-missions/robot-missions.md#lab-b-one-motor--one-sensor)
- [Lab C: Arm positions (servo)](07-robot-missions/robot-missions.md#lab-c-arm-positions-servo)
- [Lab D: Driver station thinking](07-robot-missions/robot-missions.md#lab-d-driver-station-thinking)
- [Lab E: Move by counting](07-robot-missions/robot-missions.md#lab-e-move-by-counting)
- [Mission ready checklist](07-robot-missions/robot-missions.md#mission-ready-checklist)
- [What’s next](07-robot-missions/robot-missions.md#whats-next)
