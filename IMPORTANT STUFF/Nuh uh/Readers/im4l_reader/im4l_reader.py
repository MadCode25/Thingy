import os
import json

print("Welcome to the .im4l file reader!")
print("This program will help you read and analyze .im4l files.")
print("Note: IM4L files is short for 'Important M4 Lists', which is used by M4 to store information, these files are also shifted from 8, and has its own alphabet.")
print("One of these files is 'im4l_readable.cmds', which contains important commands for M4 operations. There's more types like 'im4l_upgrade.cmds' and 'im4l_compile.c'.")

# Decoder
def decode_im4l(data, alphabet):
    lookup = {c: i for i, c in enumerate(alphabet)}
    alpha_len = len(alphabet)
    decoded = []

    for ch in data:  # ch is now a STRING
        if ch in lookup:
            decoded.append(alphabet[(lookup[ch] - 8) % alpha_len])
        else:
            decoded.append(ch)

    return ''.join(decoded)






file_path = input("Enter the .im4l file's path: ")
file_name = input("Enter the .im4l file's name: ")

print("Searching for .im4l file...")
# Check if file exists
if os.path.isfile(os.path.join(file_path, file_name)):
    print(".im4l file found.")
    with open(os.path.join(file_path, file_name), 'rb') as file:

        # Read file content
        print('Reading file...')
        data = file.read().decode(errors="ignore")
        if file_name.endswith('.im4l'):
            print(f"Text length: {len(data)} bytes")
            with open('settings.json', 'r') as settings_file:
                settings = json.load(settings_file)
        else:
            print("Error: Unsupported file type. Please provide a valid .im4l file.")
            print("Error code: 1738 - IM4L_UNSUPPORTED_FILE_TYPE")
            exit()
        # Analyze content based on settings
        found = False
        # Instead of an another .decode, we'll use "in" instead
        for cmd in settings["commands"]:
            if cmd["command"] in data:
                print(cmd["event"])
                found = True
                print("Decoding file...")
                # Set decoding settings
                print(decode_im4l(data, settings["alphabet"]))

    
    if not found:
        print("This .im4l file does not contain important information.")

else:
    print("Error: .im4l file not found. Please check the path and filename and try again.")
