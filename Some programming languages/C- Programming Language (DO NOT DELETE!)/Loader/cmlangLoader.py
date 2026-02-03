# C- Language Loader and Standard Library
# Version: 1.1.5
import os
print("Script directory:", os.path.dirname(__file__))
print("Current working directory:", os.getcwd())



# ================================
#      C- Standard Library
# ================================
def printf(*args, sep=' ', end='\n'):
    # behave like Python's print: join args with sep and end with end
    print(*args, sep=sep, end=end)


def scanf(prompt, type):
    value = input(prompt)
    if type == 'int':
        return int(value)
    elif type == 'float':
        return float(value)
    elif type == 'str':
        return value
    else:
        raise ValueError("Unsupported specified type.")


def userInput(prompt):
    x = input(prompt)
    return x


def checklen(var):
    if isinstance(var, (int, float)):
        raise ValueError("checklen only works with strings, not with numbers.")
    elif isinstance(var, str):
        return len(var)
    else:
        raise ValueError("checklen only works with strings, but does not support this type.")


def ascToInt(char):
    if len(char) != 1:
        raise ValueError("ascToInt only works with single characters. Use 'mascToInt' for multi-lettered strings.")
    else:
        return int(ord(char))
    
def intToAsc(num):
    return chr(num)

def mascToInt(string):
    return [ord(c) for c in string]

def openFile(path, mode='r'):
    with open(path, mode) as f:
        return f.read()
def writeFile(path, data, mode='w'):
    with open(path, mode) as f:
        f.write(data)



# ================================
#        C- File Loader
# ================================
def load_file(path):
    with open(path, "rb") as f:
        data = f.read()

    if data.startswith(b"C-"):  # Bytecode format
        run_bytecode(data)
    else:  # Source format (.cms)
        run_source_code(data.decode("utf-8"))

def run_bytecode(data: bytes):
    print("Running C- bytecode...")
    bytecode = data[2:]  # skip "C-"
    print("Bytecode payload:", bytecode)
# ==============================
#       Comment Handler
# ==============================

def remove_comments(source: str) -> str:
    inside_block = False
    filtered_lines = []
    
    for line in source.splitlines():
        # Handle being inside a block comment
        if inside_block:
            if "--!>" in line:
                line = line.split("--!>", 1)[1]  # keep stuff after end
                inside_block = False
            else:
                continue  # skip entire line
       
        # Handle new block comment starts
        while "!--" in line:
            before, after = line.split("!--", 1)
            if "--!" in after:
                after = after.split("--!", 1)[1]
                line = before + after  # glue code back together
            else:
                line = before
                inside_block = True
                break

        # Handle line comments (inline)
        for marker in ("//", "#"):
            if marker in line:
                line = line.split(marker, 1)[0]

        if line.strip():
            filtered_lines.append(line.rstrip())
    return "\n".join(filtered_lines)

def staloop(state):
    while state:
        pass





def run_source_code(source: str):
    print("Running C- source code...")
    safe_globals = {
        "__builtins__": {}
    }
    safe_globals.update({
        "printf": printf,
        "scanf": scanf,
        "userInput": userInput,
        "checklen": checklen,
        "ascToInt": ascToInt,
        "intToAsc": intToAsc,
        "mascToInt": mascToInt,
        "writeFile": writeFile,
        "openFile": openFile,
    })

    # Remove comments before execution
    filtered_source = remove_comments(source)

    try:
        exec(filtered_source, safe_globals)
    except Exception as e:
        print(f"Error while running C- source: {e}")





# ================================
# Example Usage
# ================================
if __name__ == "__main__":
    cms_folder_location = input("PLEASE ENTER THE FOLDER LOCATION OF YOUR .CMS FILE(S): ").strip()
    cms_folder = r"{}".format(cms_folder_location)

    file = input("CMS FILE (include the .cms extension): ").strip()

    # Build the full path automatically
    file_path = os.path.join(cms_folder, file)

    try:
        load_file(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file}' not found in {cms_folder}")
