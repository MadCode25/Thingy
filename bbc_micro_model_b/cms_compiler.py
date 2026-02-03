# C- Language Loader and Standard Library
# Version: 1.1.5


OUTPUT = print
INPUT = input


# ================================
#      C- Standard Library
# ================================
def printf(*args, sep=' ', end='\n'):
    # behave like Python's print: join args with sep and end with end
    OUTPUT(sep.join(map(str, args)) + end)


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
#        C- Program Loader
# ================================
result = ""


def set_output(func):
    global OUTPUT
    OUTPUT = func

def load_code(file):
    global result
    try:
        with open(file, "r") as f:
            source = f.read()
        result = source
    except FileNotFoundError:
        return "cmsc: File does not exist."


def run_code(source: str):
    global result
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
        "openFile": openFile,
        "writeFile": writeFile
    })

    try:
        exec(source, safe_globals)
        return None
    except Exception as e:
        return f"cmsc: ERROR: {e}"
    

