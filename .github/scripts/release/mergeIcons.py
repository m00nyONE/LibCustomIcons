from wand.image import Image
import re
import math
import os
from typing import Dict, Set, List, Tuple

# Type aliases
Folder = str
ImageName = str
Size = Tuple[int, int]
CoordTuple = Tuple[int, int, int, int, int, int, int, int]

ICONS_DIR = "icons"  # base directory for icon processing


def get_folders() -> List[Folder]:
    """Return folder names derived from .lua filenames in icons dir."""
    return [item[:-4] for item in os.listdir(ICONS_DIR) if item.endswith(".lua")]


def collect_images_per_folder(folders: List[Folder]) -> Dict[Folder, Set[ImageName]]:
    """Scan all lua files to find referenced image names per folder."""
    images_per_folder: Dict[Folder, Set[ImageName]] = {folder: set() for folder in folders}
    for folder in folders:
        regex = rf's\[.*?\].*?=(?!.*?{{).*?"LibCustomIcons/icons/{folder}/([^"]+)"'
        for cFolder in folders:
            lua_path = os.path.join(ICONS_DIR, f"{cFolder}.lua")
            with open(lua_path, "r", encoding="utf-8") as fil:
                content = fil.read()
                found = re.findall(regex, content)
                images_per_folder[folder].update(found)
    return images_per_folder


def group_by_size(images_per_folder: Dict[Folder, Set[ImageName]]) -> Dict[Size, List[Tuple[Folder, ImageName]]]:
    """Open each image to group by (width, height)."""
    size_groups: Dict[Size, List[Tuple[Folder, ImageName]]] = {}
    for folder, images in images_per_folder.items():
        for imageName in images:
            img_path = os.path.join(ICONS_DIR, folder, imageName)
            if not os.path.exists(img_path):
                print(f"Warning: {img_path} missing, skipped")
                continue
            try:
                with Image(filename=img_path) as im:
                    wh = (im.width, im.height)
                size_groups.setdefault(wh, []).append((folder, imageName))
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
    return size_groups


def build_atlases(size_groups: Dict[Size, List[Tuple[Folder, ImageName]]]) -> Dict[Tuple[Folder, ImageName], CoordTuple]:
    """Create atlases per size group and return coordinate map."""
    coord_map: Dict[Tuple[Folder, ImageName], CoordTuple] = {}
    for (w, h), entries in size_groups.items():
        count = len(entries)
        if count == 0:
            continue
        columns = max(1, math.floor(math.sqrt(count)))
        rows = math.ceil(count / columns)
        total_w = columns * w - 1
        total_h = rows * h - 1
        print(f"Creating global atlas {w}x{h}: {columns}x{rows} (images: {count})")
        with Image(background=None) as atlas:
            for i, (folder, imageName) in enumerate(entries):
                img_path = os.path.join(ICONS_DIR, folder, imageName)
                try:
                    with Image(filename=img_path) as item:
                        item.border_color = 'none'
                        item.matte_color = 'none'
                        item.background_color = 'none'
                        atlas.image_add(item)
                except Exception as e:
                    print(f"Error adding {img_path}: {e}")
            atlas.background_color = "none"
            atlas.montage(mode='concatenate', tile=f'{columns}x{rows}')
            atlas.compression = "dxt5"
            atlas.background_color = "none"
            atlas.format = "dds"
            out_name = os.path.join('compiled', f'merged_static_{w}x{h}.dds')
            atlas.save(filename=out_name)
        for i, (folder, imageName) in enumerate(entries):
            column = i % columns
            row = i // columns
            left = column * w
            right = left + w - 1
            top = row * h
            bottom = top + h - 1
            coord_map[(folder, imageName)] = (w, h, left, right, top, bottom, total_w, total_h)
    return coord_map


def generate_static_lines(coord_map: Dict[Tuple[Folder, ImageName], CoordTuple], folders: List[Folder]) -> List[str]:
    """Collect and optionally replace s[\" lines with atlas references."""
    lines_out: List[str] = []
    for cFolder in folders:
        lua_path = os.path.join(ICONS_DIR, f"{cFolder}.lua")
        with open(lua_path, "r", encoding="utf-8") as fil:
            for raw_line in fil:
                line_no_nl = raw_line.rstrip('\n')
                stripped = line_no_nl.lstrip()
                if not stripped.startswith('s["'):
                    continue
                replaced_line = None
                for (folder, imageName), (w, h, left, right, top, bottom, total_w, total_h) in coord_map.items():
                    needle = f'"LibCustomIcons/icons/{folder}/{imageName}"'
                    if needle not in line_no_nl:
                        continue
                    regex = rf'(s\[.*?\].*?=)(?!.*?{{).*?"LibCustomIcons/icons/{folder}/{re.escape(imageName)}"'
                    m = re.search(regex, line_no_nl)
                    if not m:
                        continue
                    prefix = m.group(1).rstrip()
                    replaced_line = (
                        f'{prefix} {{"LibCustomIcons/compiled/merged_static_{w}x{h}.dds", '
                        f'{left}, {right}, {top}, {bottom}, {total_w}, {total_h}}} -- {folder}/{imageName}'
                    )
                    break
                lines_out.append(replaced_line if replaced_line else line_no_nl)
    return lines_out


def write_output(lines_out: List[str], output_path: str = os.path.join('compiled', 'static.lua')) -> None:
    """Write the static.lua file with header and replaced lines."""
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write('-- SPDX-FileCopyrightText: 2025 m00nyONE\n')
        out.write('-- SPDX-License-Identifier: Artistic-2.0\n\n')
        out.write('-- auto generated by compile script --\n\n')
        out.write('local lib_name = "LibCustomIcons"\n')
        out.write('local lib = _G[lib_name]\n')
        out.write('local s = lib.GetStaticTable()\n')
        out.write('local a = lib.GetAnimatedTable()\n\n')
        for l in lines_out:
            out.write(l + '\n')
    print(f"Done. Wrote {len(lines_out)} lines to {output_path}.")


def main():
    """Orchestrate the full merge + atlas creation process."""
    folders = get_folders()
    os.makedirs(os.path.join('compiled'), exist_ok=True)
    images_per_folder = collect_images_per_folder(folders)
    size_groups = group_by_size(images_per_folder)
    coord_map = build_atlases(size_groups)
    lines_out = generate_static_lines(coord_map, folders)
    write_output(lines_out)


if __name__ == "__main__":
    main()
