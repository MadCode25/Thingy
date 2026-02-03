# Inits for the C- Language, make sure to import this file (sample for the old functions)

def printf(string):
    print(string, end='')

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
    
class checkLength:
    def __init__(self, string):
        self.string = string
    
    def length(self):
        return len(self.string)