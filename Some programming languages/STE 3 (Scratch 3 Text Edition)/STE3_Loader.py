import os
objects = {}
# ==============================
#        Core Functions
# ==============================

class LoopExit(Exception):
    pass

def forever(condition):
    try:
        while condition:
            pass
    except LoopExit:
        return
    
def IF(condition, whatHappens, elseWhatHappens):
    if condition:
        whatHappens()
    else:
        elseWhatHappens()
def setVar(name, value):
    globals()[name] = value

def changeVar(name, value):
    globals()[name] += value

def say(*message, end='\n'):
    print(*message, end=end)

def ask(prompt):
    return input(prompt)

def add(a, b):
    return int(a) + int(b)

def subtract(a, b):
    return int(a) - int(b)

def multiply(a, b):
    return int(a) * int(b)

def divide(a, b):
    return int(a) / int(b)

def roundNum(number):
    return round(int(number))

def stopLoop():
    raise LoopExit()


def makeError(message):
    raise Exception(message)
def addObject(name, obj):
    objects[name] = obj

# ==============================
#           Loader
# ==============================
def load_file(path):
    with open(path, "rb") as f:
        data = f.read()

    if data.startswith(b"ste3"):  # Bytecode format
        run_bytecode(data)
    else:  # Source format (.ste3)
        run_source_code(data.decode("utf-8"))

def run_bytecode(data: bytes):
    print("Running STE3 bytecode...")
    bytecode = data[4:]  # skip "ste3"
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






def run_source_code(source: str):
    print("Running STE3 File...")
    safe_globals = {
        "__builtins__": {}
    }
    safe_globals.update({
        "say": say,
        "IF": IF,
        "setVar": setVar,
        "changeVar": changeVar,
        "forever": forever,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
        "ask": ask,
        "roundNum": roundNum,
        "stopLoop": stopLoop,
        "makeError": makeError
    })

    # Remove comments before execution
    filtered_source = remove_comments(source)

    try:
        exec(filtered_source, safe_globals)
    except Exception as e:
        print(f"Error while running STE3 source: {e}")





# ================================
# Example Usage
# ================================
if __name__ == "__main__":
    ste3_folder_location = input("enter file loacation (cd) > ").strip()
    ste3_folder = r"{}".format(ste3_folder_location)

    file = input("\n File > ").strip()

    # Build the full path automatically
    file_path = os.path.join(ste3_folder, file)

    try:
        load_file(file_path)
    except FileNotFoundError:
        print(f"Error: No such file: {file} in {file_path}")
