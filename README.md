![](images/1.webp)

# Krtkus

An extended 5x12 keyboard with 2 extra keys. The design is intended for ortho layouts with a shifted number row, allowing for the placement of the delete and tilde keys above their usual spots. PCB is designed in Kicad. Case is designed in Blender.

- Low profile
- QMK/VIA compatible
- Fixed 7 degree tilt

To connect the keyboard to via.app, the [via design file](production/krtkus_via_design.json) has to be manually uploaded in the design tab.



## Parts

- PCB found in `production/krtkus_pcb`
- Case found in `production/krtkus_case.stl`
- Arduino Pro Micro
- 61 SMD diodes
- 61 Choc V1 switches
- 61 Choc V1 keycaps

Optional:

- 90 degree Micro-USB cable
- Rubber feet


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

On Windows, create a "krtkus" folder in `qmk_firmware/keyboards` and copy the contents of the `source/krtkus_qmk` folder inside of it. Then in MSYS compile the firmware using the commands below.

Setup:

```
qmk setup
```

Compile:

```
qmk compile -kb krtkus -km default
```

## Showcase

![](images/2.webp)
![](images/3.webp)
![](images/4.webp)
<p align="center">Krtkus vs. Keychron K3 Pro</p>