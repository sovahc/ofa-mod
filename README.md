# ofa-mod
Oled Friendly Axis Mod

This is LinuxCNC AXIS interface mod.

![screenshot](doc/ofa_screnshot.png)

### Features:
* Automatic selection of scale and font size
* Randomizing window position to avoid oled burn-in

### Installation
* Place this script in the folder of your choice. (for example to linuxcnc config folder)
* Tune your ini file like this:

```
[DISPLAY]
DISPLAY = axis
USER_COMMAND_FILE=/home/sova/Desktop/ofa_mod.py

#SCALE = 1
#FULLSCREEN=1
#FONT_SIZE=10
#FONT_NAME=Mono
#BACKGROUND=grey20
#BACKGROUND2=grey30
## e.t.c
```
