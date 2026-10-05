# Road Trip Overhaul - Vehicle Tuning

![Road Trip Overhaul - Vehicle Tuning](assets/workshop_preview.jpg)

An **American Truck Simulator** mod that gives the cars of the **Road Trip: Ford** DLC their real-world performance.

Weight, drag and engine output of every car are calibrated so acceleration and top speed match the real car (with no factory speed governor). Engines still show their real power and torque figures. Tyre grip is lowered for a realistic feel (old bias-ply tyres on the Mustang grip least), so hills, grass and dirt need the right drive mode and some care.

| Car | 0-60 mph | Top speed |
|---|---|---|
| Ford Bronco 2024 | ~6 s | ~130 mph |
| Ford F-150 2023 | ~5.5-6 s | ~125 mph |
| Ford Mustang 1967 | ~8.5-9 s | ~115-120 mph |
| Ford Crown Victoria 2006 | ~7.5-8 s | ~130 mph |

Changes apply to cars you already own. Only the Road Trip cars are changed; trucks are not affected. The mod is optional in SCS Convoy.

**Requires** ATS 1.61 and the Road Trip: Ford DLC.

## Recommended (optional): Road Trip Overhaul plugin

[Road Trip Overhaul](https://github.com/PicSoul/road-trip-overhaul) is a separate SDK plugin with realistic throttle-based automatic shifting, real 2H / 4H on the Bronco and F-150 and surface-dependent tyre grip. The mod and the plugin each work on their own, or together.

## Install

- **[Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3812313188):** subscribe, then enable it in the in-game Mod Manager.
- **Manual:** build it (see [Building](#building)), put `dist/road_trip_overhaul_vehicles.scs` in `Documents\American Truck Simulator\mod` and enable it in the Mod Manager.

## What is changed

| File | Change |
|---|---|
| `def/vehicle/car/<car>/engine/*.sii` | internal `torque` calibrated to real 0-60 times (the info lines keep the real figures); shift ranges and torque curves are stock |
| `def/vehicle/car/<car>/chassis/*.sii` | `air_resistance` and `kerb_weight` calibrated to the real car |
| `def/vehicle/{p,q,x,y}_tire/*.sii` | `grip_factor` lowered (front and rear tyres separately) |
| `sound/car/tires/concrete_oldtimer.soundref` | added: the DLC's Mustang tyres reference this file, but the game ships it misspelled (`conrete_oldtimer`); this copy fixes the missing concrete tyre sound and the Workshop Uploader's "Soundref file not found" error |

Every changed value has a comment with the stock value next to it.

## Building

```
python build.py            -> dist/road_trip_overhaul_vehicles.scs  (standard mod)
                              dist/workshop/                         (for the SCS Workshop Uploader)
python build.py --install  also copies the .scs into Documents\American Truck Simulator\mod
python tools/make_icon.py  redraws mod/mod_icon.jpg and assets/workshop_preview.jpg
```

Requires Python 3 and Pillow. `dist/workshop/` follows the Workshop layout: `versions.sii` plus a `universal` package whose manifest leaves out `display_name` and `compatible_versions` (the uploader and `versions.sii` provide them). `assets/workshop_description.txt` is the Steam-formatted description and `assets/workshop_preview.jpg` the preview image for the uploader.

## License

MIT - see [LICENSE](LICENSE). The vehicle definitions are modified copies of SCS Software's game data; American Truck Simulator, the Road Trip DLC and Ford names belong to their respective owners.
