"""Builds the mod from mod/ in two forms:

    dist/road_trip_overhaul_vehicles.scs   standard mod (a zip archive), for the game's mod folder
    dist/workshop/                         folder for the SCS Workshop Uploader:
                                             versions.sii + universal/ (manifest without display_name and
                                             compatible_versions, which the uploader and versions.sii provide)

    python build.py            build only
    python build.py --install  build and copy the .scs into Documents\\American Truck Simulator\\mod
"""
import os
import shutil
import sys
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'mod')
DIST = os.path.join(HERE, 'dist')
SCS = os.path.join(DIST, 'road_trip_overhaul_vehicles.scs')
WORKSHOP = os.path.join(DIST, 'workshop')
MOD_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'American Truck Simulator', 'mod')

VERSIONS_SII = '''SiiNunit\r
{\r
package_version_info : .universal\r
{\r
\tpackage_name: "universal"\r
}\r
}\r
'''


def check():
    for required in ('manifest.sii', 'mod_icon.jpg', 'mod_description.txt'):
        if not os.path.exists(os.path.join(SRC, required)):
            sys.exit(f'missing mod/{required}')
    icon = Image.open(os.path.join(SRC, 'mod_icon.jpg'))
    if icon.format != 'JPEG' or icon.size != (276, 162):
        sys.exit(f'mod/mod_icon.jpg must be a 276x162 JPG (is {icon.format} {icon.size[0]}x{icon.size[1]})')
    if os.path.getsize(os.path.join(SRC, 'mod_icon.jpg')) > 1024 * 1024:
        sys.exit('mod/mod_icon.jpg must be under 1 MB')


def files():
    for root, _, names in os.walk(SRC):
        for name in sorted(names):
            path = os.path.join(root, name)
            yield path, os.path.relpath(path, SRC).replace(os.sep, '/')  # paths inside the archive use '/'


def build_scs():
    os.makedirs(DIST, exist_ok=True)
    count = 0
    with zipfile.ZipFile(SCS, 'w', zipfile.ZIP_DEFLATED) as z:
        for path, arc in files():
            z.write(path, arc)
            count += 1
    print(f'Built {SCS} ({count} files, {os.path.getsize(SCS)} bytes)')


def build_workshop():
    if os.path.isdir(WORKSHOP):
        shutil.rmtree(WORKSHOP)
    universal = os.path.join(WORKSHOP, 'universal')
    for path, arc in files():
        out = os.path.join(universal, arc)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if arc == 'manifest.sii':
            with open(path, encoding='utf-8', newline='') as f:
                lines = f.readlines()
            keep = [ln for ln in lines if not ln.strip().startswith(('display_name', 'compatible_versions'))]
            with open(out, 'w', encoding='utf-8', newline='') as f:
                f.writelines(keep)
        else:
            shutil.copy2(path, out)
    with open(os.path.join(WORKSHOP, 'versions.sii'), 'w', encoding='utf-8', newline='') as f:
        f.write(VERSIONS_SII)
    print(f'Built {WORKSHOP} (select this folder in the SCS Workshop Uploader)')


def install():
    if not os.path.isdir(MOD_DIR):
        sys.exit(f'ATS mod folder not found: {MOD_DIR}')
    shutil.copy2(SCS, MOD_DIR)
    print(f'Installed to {MOD_DIR}')


if __name__ == '__main__':
    check()
    build_scs()
    build_workshop()
    if '--install' in sys.argv:
        install()
