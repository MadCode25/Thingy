import struct
import os
import re
import sys
import time
import socket
import urllib.request

# Force IPv4 so Python doesn't stall on ISP IPv6 routing
old_getaddrinfo = socket.getaddrinfo
def ipv4_only(*args, **kwargs):
    return [info for info in old_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]
socket.getaddrinfo = ipv4_only

MAGIC_BYTES = b"ENPY"  # 4 bytes
FILE_VERSION = 4       # 1 byte

UPDATELINK = "https://raw.githubusercontent.com/MadCode25/Thingy/refs/heads/main/updatedEngine.py"

def check_for_updates():
    print("Checking for updates...")
    try:
        # 1. Fetch remote script from GitHub (bypassing cache and proxy)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        opener.addheaders = [("User-Agent", "ENPYEngine/1.0")]
        
        url = f"{UPDATELINK}?t={int(time.time())}"
        with opener.open(url, timeout=5) as response:
            remote_code = response.read().decode("utf-8")

        # 2. Extract FILE_VERSION = <number> from the remote code text
        match = re.search(r"^FILE_VERSION\s*=\s*(\d+)", remote_code, re.MULTILINE)
        if not match:
            print("Could not read FILE_VERSION from remote script.")
            return

        remote_version = int(match.group(1))

        # 3. Compare remote version against current FILE_VERSION
        if remote_version > FILE_VERSION:
            print(f"Update available! (v{FILE_VERSION} -> v{remote_version}) Applying update...")
            
            # If running as a raw .py script, overwrite self and restart
            if not getattr(sys, "frozen", False):
                with open(__file__, "w", encoding="utf-8") as f:
                    f.write(remote_code)
                print("Update complete! Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                # If running as a compiled .exe, save the new script alongside it
                with open("engine.new.py", "w", encoding="utf-8") as f:
                    f.write(remote_code)
                print("Saved update to engine.new.py!")
        else:
            print(f"Engine is up to date (v{FILE_VERSION}).")

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
