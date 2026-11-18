import struct
import os
import re
import sys
import time
import socket
import urllib.request
import subprocess
import shutil
# Force IPv4 so Python doesn't stall on ISP IPv6 routing
old_getaddrinfo = socket.getaddrinfo
def ipv4_only(*args, **kwargs):
    return [info for info in old_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]
socket.getaddrinfo = ipv4_only

MAGIC_BYTES = b"ENPY"  # 4 bytes
FILE_VERSION = 7       # 1 byte

UPDATELINK = "https://raw.githubusercontent.com/MadCode25/Thingy/refs/heads/main/engine.py"

def check_for_updates():
    print("Checking for updates...")
    part_file = "upd.part"

    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        opener.addheaders = [("User-Agent", "ENPYEngine/1.0")]
        url = f"{UPDATELINK}?t={int(time.time())}"

        with opener.open(url, timeout=5) as response:
            # Grab total file size from server headers (if provided)
            total_bytes = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 8192  # 8 KB per chunk (zero RAM spike)

            with open(part_file, "wb") as out_file:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)

                    # Draw live progress bar on the same console line using \r
                    if total_bytes > 0:
                        percent = int((downloaded / total_bytes) * 100)
                        filled = int(20 * downloaded // total_bytes)
                        bar = "█" * filled + "░" * (20 - filled)
                        print(f"\rDownloading: [{bar}] {percent}% ({downloaded}/{total_bytes} B)", end="", flush=True)
                    else:
                        print(f"\rDownloading: {downloaded} bytes...", end="", flush=True)

        print()  # Move to a clean new line after download finishes

        # Read ONLY the first 30 lines of 'upd.part' to find FILE_VERSION
        remote_version = None
        with open(part_file, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(30):
                line = f.readline()
                if not line:
                    break
                match = re.match(r"^FILE_VERSION\s*=\s*(\d+)", line)
                if match:
                    remote_version = int(match.group(1))
                    break

        if remote_version is None:
            print("Could not find FILE_VERSION in update.")
            os.remove(part_file)
            return

        if remote_version > FILE_VERSION:
            print(f"Update available! (v{FILE_VERSION} -> v{remote_version}) Applying update...")

            if not getattr(sys, "frozen", False):
                os.replace(part_file, __file__)
                print("Update complete! Restarting...")
                subprocess.run([sys.executable] + sys.argv)
                sys.exit()
            else:
                os.replace(part_file, "engine.new.py")
                print("Saved update to engine.new.py!")
        else:
            os.remove(part_file)
            print(f"Engine is up to date (v{FILE_VERSION}).")

    except Exception as e:
        print()
        if os.path.exists(part_file):
            os.remove(part_file)
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
        
        version = struct.unpack("<B", f.read(1))[0]
        
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
