#!/usr/bin/env python3
import os
import sys
import json
import re
from collections import defaultdict
from PIL import Image

def find_dds_files(root_folder):
    dds_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.dds'):
                dds_files.append(os.path.join(dirpath, filename))
    return dds_files

def analyze_textures(dds_files, root_folder):
    squared = defaultdict(lambda: defaultdict(list))
    non_squared = defaultdict(list)
    # Regex for '_anim.dds' and '_anim*.dds'
    anim_pattern = re.compile(r'_anim(.*)?\.dds$', re.IGNORECASE)
    for file_path in dds_files:
        filename = os.path.basename(file_path)
        try:
            with Image.open(file_path) as img:
                width, height = img.size
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        rel_path = os.path.relpath(file_path, root_folder)
        rel_path_norm = rel_path.replace('\\', '/').lstrip('/')
        parts = rel_path_norm.split('/')
        folder = parts[0] if len(parts) > 1 else "root"
        # Check for animated textures and 'animated' subfolder
        if anim_pattern.search(filename) or 'animated/' in rel_path_norm.lower():
            non_squared[folder].append({
                "file": filename,
                "width": width,
                "height": height
            })
        elif width == height:
            squared[width][folder].append(filename)
        else:
            non_squared[folder].append({
                "file": filename,
                "width": width,
                "height": height
            })
    return squared, non_squared

def write_json(squared, non_squared):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parsed_dir = os.path.join(script_dir, "parsed")
    os.makedirs(parsed_dir, exist_ok=True)
    static_json = {"static": [
        {
            "size": size,
            "paths": dict(folders)
        } for size, folders in sorted(squared.items())
    ]}
    with open(os.path.join(parsed_dir, "static.json"), "w", encoding="utf-8") as f:
        json.dump(static_json, f, indent=2, ensure_ascii=False)
    animated_json = {"animated": dict(non_squared)}
    with open(os.path.join(parsed_dir, "animated.json"), "w", encoding="utf-8") as f:
        json.dump(animated_json, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: parser.py <folder>")
        sys.exit(1)
    root_folder = sys.argv[1]
    if not os.path.isdir(root_folder):
        print(f"::error:: ❌ {root_folder} is not a valid folder.")
        sys.exit(1)
    dds_files = find_dds_files(root_folder)
    squared, non_squared = analyze_textures(dds_files, root_folder)
    write_json(squared, non_squared)
    print(f"::notice:: ✅ {len(dds_files)} .dds files analyzed.")

if __name__ == "__main__":
    main()
