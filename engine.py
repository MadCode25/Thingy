import struct
import os
import time
import socket
import urllib.request

# Force IPv4 so Python doesn't stall on ISP IPv6 routing
old_getaddrinfo = socket.getaddrinfo
def ipv4_only(*args, **kwargs):
    return [info for info in old_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]
socket.getaddrinfo = ipv4_only

MAGIC_BYTES = b"ENPY"  # 4 bytes
FILE_VERSION = 2       # 1 byte

UPDATELINK = "https://raw.githubusercontent.com/MadCode25/Thingy/refs/heads/main/updatedEngine.py"

def check_for_updates():
    print("Checking for updates...")
    try:
        # Bypass any broken Windows proxy settings and avoid GitHub's 5-min cache
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        opener.addheaders = [("User-Agent", "ENPYEngine/1.0")]
        
        url = f"{UPDATELINK}?t={int(time.time())}"
        with opener.open(url, timeout=5) as response:
            remote_code = response.read().decode("utf-8")

        # Compare against the current script if running as .py, or save the update
        with open("updatedEngine.py", "w", encoding="utf-8") as f:
            f.write(remote_code)
            
        print("Engine synced with latest GitHub version!")

    except Exception as e:
        print(f"Update check skipped (offline or unavailable): {e}")

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
        
        version = struct.unpack("<B", f.read(1))
        
        raw_data = f.read(12)
        health, x, y = struct.unpack("<iff", raw_data)
        
        return {"version": version, "health": health, "x": x, "y": y}

def verLoad(f): 
    if f and os.path.exists(f):
        loaded_data = load_game(f)
        print("DEBUG:", loaded_data)
    
        if loaded_data["version"] < FILE_VERSION: 
            print("Warning: This save file is from an older version of the game.")
    else:
        print(f"No save file named '{f}' found!")

# --- Startup ---
check_for_updates()

us = input("\nMake new? (Y/N): ").strip().lower()
target_file = ""

if us in ("y", "yes"):
    name = input("Configuration name: ").strip()
    h = int(input("Health: "))
    x = float(input("PX: "))
    y = float(input("PY: "))
    
    target_file = f"{name or 'slot1'}.enpy"
    print(f"Saving to {target_file}...")
    save_game(target_file, h, x, y)
    print("Complete.")
    verLoad(target_file)
elif us in ("n", "no"):
    name = input("Enter configuration name to load (default: slot1): ").strip()
    target_file = f"{name or 'slot1'}.enpy"
    print(f"Loading {target_file}...")
    verLoad(target_file)
else:
    print("Y/N only or Yes/No")
