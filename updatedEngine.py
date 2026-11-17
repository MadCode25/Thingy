import struct
import os

MAGIC_BYTES = b"ENPY"  # 4 bytes
FILE_VERSION = 2       # 1 byte

def save_game(filename, player_health, player_x, player_y):
    with open(filename, "wb") as f:
        f.write(MAGIC_BYTES)
        f.write(struct.pack("<B", FILE_VERSION))
        
        packed_data = struct.pack("<iff", player_health, player_x, player_y)
        f.write(packed_data)

def load_game(filename):
    with open(filename, "rb") as f:
        magic = f.read(4)
        if magic != MAGIC_BYTES:
            raise ValueError("Invalid file format! Not a valid .enpy file.")
        
        version = struct.unpack("<B", f.read(1))[0]
        
        raw_data = f.read(12)
        health, x, y = struct.unpack("<iff", raw_data)
        
        return {"version": version, "health": health, "x": x, "y": y}

us = input("Make new? (Y/N): ").strip().lower()
target_file = ""

def verLoad(f): 
    target_file = f
    if target_file and os.path.exists(target_file):
        loaded_data = load_game(target_file)
        print("DEBUG:", loaded_data)
    
        if loaded_data["version"] < FILE_VERSION: 
            print("Warning: This save file is from an older version of the game.")
    else:
        print(f"No save file named '{target_file}' found!")


if us in ("y", "yes"):
    name = input("Configuration name: ").strip()
    h = int(input("Health: "))
    x = float(input("PX: "))
    y = float(input("PY: "))
    
    target_file = f"{name}.enpy"
    print(f"Saving to {target_file}...")
    save_game(target_file, h, x, y)
    print("Complete.")
elif us in ("n", "no"):
    name = input("Enter configuration name to load (default: slot1): ").strip()
    target_file = f"{name or 'slot1'}.enpy"
    print(f"Loading {target_file}...")
    verLoad(target_file)
else:
    print("Y/N only or Yes/No")

