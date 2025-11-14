from wand.image import Image
import re
import math
import os

os.chdir('icons')
ls = os.listdir()

# All folder names (Lua files without extension)
folders = [item[:-4] for item in ls if item.endswith(".lua")]

os.makedirs('compiled', exist_ok=True)

# Step 1: Find all image paths per folder in all Lua files
images_per_folder = {folder: set() for folder in folders}
for folder in folders:
    regex = rf's\[.*?\].*?=(?!.*?{{).*?"LibCustomIcons/icons/{folder}/([^"]+)"'
    for cFolder in folders:
        lua_path = f"{cFolder}.lua"
        with open(lua_path, "r", encoding="utf-8") as fil:
            content = fil.read()
            found = re.findall(regex, content)
            images_per_folder[folder].update(found)

# Step 2: Group globally by image size
size_groups = {}  # (w,h) -> list of (folder, imageName)
for folder, images in images_per_folder.items():
    for imageName in images:
        img_path = f"{folder}/{imageName}"
        if not os.path.exists(img_path):
            print(f"Warning: {img_path} missing, skipped")
            continue
        try:
            with Image(filename=img_path) as im:
                wh = (im.width, im.height)
            size_groups.setdefault(wh, []).append((folder, imageName))
        except Exception as e:
            print(f"Error loading {img_path}: {e}")

# Step 3: Generate an atlas per size
coord_map = {}  # (folder,imageName) -> (w,h,left,right,top,bottom,total_w,total_h)
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
            img_path = f"{folder}/{imageName}"
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
        out_name = f'compiled/merged_{w}x{h}.dds'
        atlas.save(filename=out_name)

    # Calculate coordinates
    for i, (folder, imageName) in enumerate(entries):
        column = i % columns
        row = i // columns
        left = column * w
        right = left + w - 1
        top = row * h
        bottom = top + h - 1
        coord_map[(folder, imageName)] = (w, h, left, right, top, bottom, total_w, total_h)

# Step 4: Replace references in all Lua files
for cFolder in folders:
    lua_path = f"{cFolder}.lua"
    with open(lua_path, "r+", encoding="utf-8") as fil:
        content = fil.read()
        for (folder, imageName), (w, h, left, right, top, bottom, total_w, total_h) in coord_map.items():
            regex = rf'(s\[.*?\].*?)("LibCustomIcons\/icons\/{folder}\/{re.escape(imageName)}")'
            replacement = rf'\g<1>{{"LibCustomIcons/icons/compiled/merged_{w}x{h}.dds", {left}, {right}, {top}, {bottom}, {total_w}, {total_h}}}'
            content, amnt = re.subn(regex, replacement, content)
            if amnt > 1:
                print(f"Duplicate: {folder}/{imageName} {amnt}x in {cFolder}")
        fil.seek(0)
        fil.write(content)
        fil.truncate()

print("Done.")
