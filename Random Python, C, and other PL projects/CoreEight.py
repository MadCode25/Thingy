class CPU:
    def __init__(self, debug=False):
        self.A = 0
        self.B = 0
        self.SD = [] * 16
        self.PC = 0
        self.RAM = [0] * 8
        self.running = True
        self.debug = debug

    def log(self, msg):
        if self.debug:
            print(msg)

    def load(self, pgm):
        for i, instr in enumerate(pgm):
            self.RAM[i] = instr
    

    def fetch(self):
        instr = self.RAM[self.PC]
        self.log(f"[FETCH]: PC={self.PC:04b} INSTR={instr:04b}")
        self.PC = (self.PC + 1) & 0b1111
        return instr
    
    def execute(self, instr):
        if instr == 0b0000: # NOP
            self.log("[EXEC]: NOP")

        elif instr == 0b0001: # LDA
            addr = self.fetch()
            self.log(f"[EXEC]: LDA FROM ADDR {addr:04b}")
            self.A = self.RAM[addr]

        elif instr == 0b0010: # LDB
            addr = self.fetch()
            self.log(f"[EXEC]: LDB FROM ADDR {addr:04b}")
            self.B = self.RAM[addr]

        elif instr == 0b0011: # SD (Set immediate)
            data = self.fetch()
            if self.SD.count(0) != 16:
                self.log("MEMORY EXCEEDED")
                self.running = False
            else:
                data = None
                self.log("[EXEC]: FINDING ADDRESS...")
                self.SD = self.RAM[data]
        
        elif instr == 0b00100: # ADD
            result = (self.A + self.B) & 0b1111
            self.log(f"[EXEC]: ADD (RES: {result:04b})")
            self.A = result & 0b1111


        elif instr == 0b1110: # OUT
            self.log("[EXEC]: OUT")
            print(self.A, *self.SD)
        elif instr == 0b1111: # HALT
            self.log("[EXEC]: HALT")
        else:
            self.log("[EXEC]: UNRECOGNIZED, HALT")

    def run(self):
        while self.running:
            instr = self.fetch()
            self.execute(instr)


cpu = CPU(debug=True)

prog = [
    0b0011, 0b0101,
    0b1110,
    0b1111
]

cpu.load(prog)
cpu.run()