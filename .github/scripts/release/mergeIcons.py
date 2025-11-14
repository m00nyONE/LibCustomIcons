from wand.image import Image
import re
import math
import os

os.chdir('icons')
ls = os.listdir()

folders = []
for items in ls:
    if items.endswith(".lua"):
        folders.append(items[:-4])

os.makedirs('compiled', exist_ok=True)

for folder in folders:
    regex = rf's\[.*?\].*?=(?!.*?{{).*?"LibCustomIcons/icons/{folder}/([^"]+)"'
    print("Current folder: " + folder)
    images = []
    foldersFoundIn = []

    # Find ALL images in all Lua files
    for cFolder in folders:
        with open(f"{cFolder}.lua", "r", encoding="utf-8") as fil:
            content = fil.read()
            found = re.findall(regex, content)
            images += found
            if found:
                foldersFoundIn.append(cFolder)

    images = list(dict.fromkeys(images))  # remove duplicates
    numImagesTotal = len(images)
    if numImagesTotal == 0:
        print("")
        continue

    # group images by size
    size_groups = {}
    for src in images:
        img_path = f"{folder}/{src}"
        if not os.path.exists(img_path):
            print(f"Warning: {img_path} not found, skipping")
            continue
        try:
            with Image(filename=img_path) as im:
                wh = (im.width, im.height)
            size_groups.setdefault(wh, []).append(src)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")

    if foldersFoundIn:
        if len(foldersFoundIn) > 1:
            print("Found in folders: " + ', '.join(foldersFoundIn))

    group_meta = {}

    # create combined textures for each size group
    for (w, h), group_images in size_groups.items():
        count = len(group_images)
        if count == 0:
            continue
        columns = max(1, math.floor(math.sqrt(count)))
        rows = math.ceil(count / columns)
        group_meta[(w, h)] = (columns, rows)
        print(f"Creating combined texture {w}x{h}: {columns}x{rows} for folder {folder}")

        with Image(background=None) as atlas:
            for src in group_images:
                img_path = f"{folder}/{src}"
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
            out_name = f'compiled/merged_{folder}_{w}x{h}.dds'
            atlas.save(filename=out_name)

    # Reference combined textures in Lua files
    for cFolder in folders:
        lua_path = f"{cFolder}.lua"
        with open(lua_path, "r+", encoding="utf-8") as fil:
            content = fil.read()
            for (w, h), group_images in size_groups.items():
                columns, rows = group_meta[(w, h)]
                for i, imagePath in enumerate(group_images):
                    column = i % columns
                    row = i // columns
                    left = column * w
                    right = left + w - 1
                    top = row * h
                    bottom = top + h - 1
                    total_w = columns * w - 1
                    total_h = rows * h - 1
                    newregex = rf'(s\[.*?\].*?)("LibCustomIcons\/icons\/{folder}\/{re.escape(imagePath)}")'
                    newstring = rf'\g<1>{{"LibCustomIcons/icons/compiled/merged_{folder}_{w}x{h}.dds", {left}, {right}, {top}, {bottom}, {total_w}, {total_h}}}'
                    content, amnt = re.subn(newregex, newstring, content)
                    if amnt > 1:
                        print(f"{folder}/{imagePath} referenced {amnt}x in {cFolder} (duplicate)")
            fil.seek(0)
            fil.write(content)
            fil.truncate()

    print("")

    #for path in images: ### Delete old images ###
    #    if os.path.exists(f"{folder}/{path}"):
    #        os.remove(f"{folder}/{path}")
    #    else:
    #        print(f"{folder}/{path} does not exist")
