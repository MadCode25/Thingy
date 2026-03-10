# Developed by AmadOS
# Dev: March, 2, 2026
# Current version: 0.0.3
# Current version dev: March 3 2026

class CPU:
    def __init__(self, debug=False):
        self.A = 0
        self.B = 0
        self.savedtxt = []
        self.PC = 0
        self.RAM = [0] * 64
        self.running = True
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(message)

    def load_program(self, program):
        for i, instr in enumerate(program):
            self.RAM[i] = instr & 0b111111

    def fetch(self):
        instr = self.RAM[self.PC]
        self.log(f"[FETCH] PC={self.PC:06b} INSTR={instr:06b}")
        self.PC = (self.PC + 1) & 0b111111
        return instr

    def execute(self, instr):
        if instr == 0b000000:  # NOP
            self.log("[EXEC] NOP")

        elif instr == 0b000001:  # LDA
            addr = self.fetch()
            self.log(f"[EXEC] LDA from addr {addr:06b}")
            self.A = self.RAM[addr]
            self.log(f"       A <= {self.A:06b}")

        elif instr == 0b000010:  # LDB
            addr = self.fetch()
            self.log(f"[EXEC] LDB from addr {addr:06b}")
            self.B = self.RAM[addr]
            self.log(f"       B <= {self.B:06b}")

        elif instr == 0b000011:  # ADD
            self.log(f"[EXEC] ADD A({self.A:06b}) + B({self.B:06b})")
            self.A = (self.A + self.B) & 0b111111
            self.log(f"       RESULT A={self.A:06b}")

        elif instr == 0b000100:  # SUB
            self.log(f"[EXEC] SUB A({self.A:06b}) - B({self.B:06b})")
            self.A = (self.A - self.B) & 0b111111
            self.log(f"       RESULT A={self.A:06b}")

        elif instr == 0b000101:  # STA
            addr = self.fetch()
            self.log(f"[EXEC] STA to addr {addr:06b}")
            self.RAM[addr] = self.A
            self.log(f"       RAM[{addr:06b}] <= {self.A:06b}")

        elif instr == 0b000110:  # JMP
            addr = self.fetch()
            self.log(f"[EXEC] JMP to {addr:06b}")
            self.PC = addr

        elif instr == 0b000111:  # OUT
            self.log(f"[EXEC] OUT A={self.A:06b}")
            if self.savedtxt:
                print("\n\nOUTPUT:", self.A, "")
                for txt in self.savedtxt:
                    print(txt)
                print("\n\n")
                self.savedtxt.clear()
            else:
                print("\n\nOUTPUT:", self.A, "\n\n")

        
        elif instr == 0b010011:   # PRINT
            addr = self.fetch()
            self.log(f"[FETCH] PC=010011 INSTR={addr:06b}")
            self.log(f"        \"{self.RAM[addr]}\" => STXT(A)")
            self.savedtxt.append(self.RAM[addr])
        
        elif instr == 0b110011:  # SET (Immediate)
            value = self.fetch()
            self.log(f"[EXEC] SET A <= {value:06b}")
            self.A = value & 0b111111

        elif instr == 0b110100: # SETB (Immediate)
            value = self.fetch()
            self.log(f"[EXEC] SET B <= {value:06b}")
            self.B = value & 0b111111


        elif instr == 0b111111:  # HALT
            self.log("[EXEC] HALT")
            self.running = False

        else:
            self.log("[EXEC] UNKNOWN INSTRUCTION — HALT")
            self.running = False

    def run(self):
        while self.running:
            instr = self.fetch()
            self.execute(instr)

# REMEMBER THESE:
# Every instruction is 6 bit (Change it to add MORE custom instructions)
# Also, turn debug on to see what's going on
# IMPORTANT: Do not store data in the instruction indexes. Check testo.py for clarity.
# 0b000000 = NOP (Do nothing)
# 0b000001 = LDA (Load everything in A)
# 0b000010 = LDB (Load everything in B)
# 0b000011 = ADD (Add value in A and B)
# 0b000100 = SUB (Subtract value A and B)
# 0b000101 = STA (Store everything in A)
# 0b000110 = JMP (Jump to other instruction)
# 0b000111 = OUT (Output)
# 0b111111 = HALT (VERY IMPORTANT - Halts execution when done.)
# Custom ones:
# 0b010011 = PRINT (Print smth, I'm just bored :) )
# 0b110011 = SET (Change value in A)
# 0b110100 = SETB (Change value in B)


cpu = CPU(debug=True)

program = [
    0b110011, 0b001010,
    0b110100, 0b000101,
    0b000011,
    0b000111,
    0b111111,
]

cpu.load_program(program)
cpu.run()

