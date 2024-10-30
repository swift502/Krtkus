# Krtkus

An extended 5x12 keyboard with 2 extra keys. The design is intended for ortho layouts with a shifted number row, allowing for the placement of the delete and tilde keys above their usual spots.

PCB is designed in Kicad. Firmware is QMK/VIA compatible. The design for via.app is in the has to be uploaded in the design tab before connecting the keyboard. Case is designed in Blender, and has a fixed tilt of 7 degrees.

## Parts

- Arduino Pro Micro
- 61 Choc V1 switches
- 61 SMD diodes

## Kicad

### Libraries

- [Scottokeebs extras](https://github.com/joe-scotto/scottokeebs/tree/main/Extras/ScottoKicad)

### Switch grid

| Unit | Offset |
| --- | --- |
| Switch | 19.05 |
| Switch 4 | 4.7625 |
| Switch 16 | 1.190625 |
| Switch 64 | 0.29765625 |

## QMK

- Compiler: https://msys.qmk.fm
- Toolbox: https://qmk.fm/toolbox

On Windows, create a "krtkus" folder in `qmk_firmware/keyboards` and copy the contents of the `qmk` folder inside of it. Then in MSYS compile the firmware using the commands below.

Setup:

```
qmk setup
```

Compile:

```
qmk compile -kb krtkus -km default
```