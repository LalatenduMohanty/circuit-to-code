# Robot Missions — coach map

Learner materials live in [`lessons/07-robot-missions/`](../lessons/07-robot-missions/).
They use everyday language on purpose. This page maps those labs to competition-robot
skills and hub tooling for mentors.

This file is under `docs/`, so it is **not** included in the printable lesson PDF.

## Vocabulary

| Kid / lesson wording          | Competition-robot habit                  |
| ----------------------------- | ---------------------------------------- |
| Timed mission                 | Autonomous-style program                 |
| Driver control / remote drive | Driver-controlled (TeleOp-style) program |
| Set up → wait for start → run | Init / waitForStart / active loop        |
| Named parts list              | Hardware map / configured device names   |
| Competition robot brain       | REV Control Hub (or Expansion Hub)       |
| Motor counters / ticks        | Motor encoders                           |
| Typed team code               | OnBot Java-style samples on the hub      |
| Build log                     | Engineering notebook habit               |

## Lab → skill map

| Lab | Practice path (classroom)              | Team kit path                                    |
| --- | -------------------------------------- | ------------------------------------------------ |
| A   | Timed blink vs button-driven loop      | Blocks: wait for start; auto blink/motor; TeleOp |
| B   | Intermediate motor driver + button/LDR | Named motor + touch/color; optional typed remake |
| C   | Servo angles or LED named states       | Servo to three positions                         |
| D   | Pot/buttons as stick stand-ins         | Gamepad → motor/servo; deadband                  |
| E   | Timed drive failure demo               | Run to encoder count (no PID required)           |

## Suggested 6–8 meeting sequence

Assume ~60–90 minutes per meeting; Intermediate Circuits already done.

1. Mission 0 + Lab A (both program kinds)
2. Lab B practice path (safe motor)
3. Lab B team kit (if available) + parts list discipline
4. Lab C arm positions
5. Lab D driver mapping + partner drive test
6. Lab E counting intuition
7. Invent 30-second mission + driver mode; build log review
8. Optional: typed remake of Lab B only

Skip or compress team-kit days if the group has only classroom boards — practice path
still builds the same mental model.

## Official docs (product / vendor)

Prefer current vendor pages over copied wiring from random videos:

- [REV Robotics Control Hub](https://www.revrobotics.com/rev-31-1595/) — product + docs
  hub for the competition brain
- [REV Docs](https://docs.revrobotics.com/) — Control Hub, sensors, motors
- Hub programming: Blocks and OnBot Java getting-started guides linked from current REV
  documentation (search “Control Hub Blocks” for the live entry point; URLs change over
  time)

When pairing a Driver Station phone/tablet, follow the hub manufacturer’s current
checklist for app install, Wi‑Fi, and firmware.

## Coaching tips

- Keep kid-facing talk on **missions and driving**, not league acronyms.
- Require a written parts list before any hub configuration.
- Cap motor power low until driving is boringly safe.
- Celebrate build logs that show a failed timed drive and a fix — that is Lab E working.
- Classroom transistor motor labs must keep the flyback diode; hub motor ports already
  manage drive electronics — do not parallel-wire a breadboard motor driver onto a hub
  motor port.
