![](images/1.webp)

# Krtkus

An extended 5x12 keyboard with 2 extra keys. The design is intended for ortho layouts with a shifted number row, allowing for the placement of the delete and tilde keys above their usual spots. PCBs are designed in Kicad, case in Blender.

- Low profile
- Available in Choc V1 or Gateron KS-27/KS-33 versions
- QMK/VIA compatible
- Fixed 7 degree tilt

To connect the keyboard to [via.app](https://usevia.app), the via design file ([Choc](production/choc_v1/choc_via_design.json), [KS-33](production/gateron_ks33/gateron_via_design.json)) has to be manually uploaded in the design tab.

## Parts

- One of the PCBs:
    - [Choc V1](production/choc_v1/choc_pcb)
    - [KS-33](production/gateron_ks33/gateron_pcb)
- Case: 
    - [STL file](production/krtkus_case.stl)
- Arduino Pro Micro
- 61 SMD diodes
- 61 switches
- 61 keycaps

Optional:

- 90 degree Micro-USB cable
- Rubber feet


## Kicad

### Libraries

- [Scotto Kicad](https://github.com/joe-scotto/scottokeebs/tree/main/Extras/ScottoKicad)
- [MX V2](https://github.com/ai03-2725/MX_V2)
- [Gateron 3D models](https://www.gateron.com/pages/3d)

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

On Windows, create a "krtkus" folder in `qmk_firmware/keyboards` and copy the contents of the corresponding firmware source folder inside of it. Then in MSYS compile the firmware using the commands below.

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