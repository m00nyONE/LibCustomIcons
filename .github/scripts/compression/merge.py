#!/usr/bin/env python3
import os
import sys
import json
import math
from PIL import Image

def load_static_json(static_json_path):
    with open(static_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['static']

def chunk_textures(size, textures, max_chunk_size=512):
    # Calculate how many textures fit per row/column
    textures_per_row = max_chunk_size // size
    textures_per_chunk = textures_per_row * textures_per_row
    chunks = []
    for i in range(0, len(textures), textures_per_chunk):
        chunk = textures[i:i+textures_per_chunk]
        chunks.append(chunk)
    return chunks, textures_per_row

def get_texture_positions(chunk, size, textures_per_row):
    positions = []
    for idx, tex_name in enumerate(chunk):
        row = idx // textures_per_row
        col = idx % textures_per_row
        x = col * size
        y = row * size
        positions.append({
            "file": tex_name,
            "x": x,
            "y": y,
            "width": size,
            "height": size
        })
    return positions

def process_static(static_json_path):
    static_data = load_static_json(static_json_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    merged_dir = os.path.join(script_dir, "merged")
    os.makedirs(merged_dir, exist_ok=True)
    chunk_idx = 0
    for entry in static_data:
        size = entry['size']
        folders = entry['paths']
        # Collect all textures with folder info
        all_textures = []
        for folder, files in folders.items():
            for file in files:
                all_textures.append({"file": file, "folder": folder})
        # Chunk calculation
        textures_per_row = 512 // size
        textures_per_chunk = textures_per_row * textures_per_row
        for i in range(0, len(all_textures), textures_per_chunk):
            chunk = all_textures[i:i+textures_per_chunk]
            positions = []
            for idx, tex in enumerate(chunk):
                row = idx // textures_per_row
                col = idx % textures_per_row
                x = col * size
                y = row * size
                positions.append({
                    "file": tex["file"],
                    "folder": tex["folder"],
                    "x": x,
                    "y": y,
                    "width": size,
                    "height": size
                })
            chunk_json = {
                "chunk_index": chunk_idx,
                "size": size,
                "textures": positions
            }
            chunk_json_path = os.path.join(merged_dir, f"chunk_{chunk_idx}.json")
            with open(chunk_json_path, 'w', encoding='utf-8') as f:
                json.dump(chunk_json, f, indent=2, ensure_ascii=False)
            chunk_idx += 1
    print(f"::notice:: ✅ Chunks created: {chunk_idx}")

def generate_chunks_images():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    merged_dir = os.path.join(script_dir, "merged")
    chunk_json_files = [f for f in os.listdir(merged_dir) if f.startswith("chunk_") and f.endswith(".json")]
    if not chunk_json_files:
        print("No chunk JSON files found in merged/")
        return
    for chunk_json_file in chunk_json_files:
        chunk_json_path = os.path.join(merged_dir, chunk_json_file)
        with open(chunk_json_path, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
        size = chunk_data["size"]
        chunk_index = chunk_data["chunk_index"]
        textures = chunk_data["textures"]
        chunk_img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        for tex in textures:
            folder = tex["folder"]
            file = tex["file"]
            tex_path = os.path.join(script_dir, "..", "..", "..", "icons" ,folder, file)
            tex_path = os.path.abspath(tex_path)
            if not os.path.isfile(tex_path):
                print(f"Warning: Texture not found: {tex_path}")
                continue
            try:
                tex_img = Image.open(tex_path).convert("RGBA")
            except Exception as e:
                print(f"Error loading {tex_path}: {e}")
                continue
            tex_img = tex_img.resize((size, size), Image.LANCZOS)
            chunk_img.paste(tex_img, (tex["x"], tex["y"]))
        chunk_png_path = os.path.join(merged_dir, f"chunk_{chunk_index}.png")
        chunk_img.save(chunk_png_path)
        print(f"Chunk image saved: {chunk_png_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: merge.py <static.json>")
        sys.exit(1)
    static_json_path = sys.argv[1]
    if not os.path.isfile(static_json_path):
        print(f"::error:: ❌ {static_json_path} is not a valid file.")
        sys.exit(1)
    process_static(static_json_path)
    generate_chunks_images()

if __name__ == "__main__":
    main()
