import cmd
import tkinter as tk
import time
import subprocess
import sys
import os 
import cms_compiler as cmsc


# BBC Micro screen dimensions
COLS = 80
ROWS = 25
FONT = ("Courier New", 14)
# Available directories
DIRECTORIES = ["A.", "A.USER", "A.GAMES", "A.UTILS"]

class BBCSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("BBC Micro Model B Simulator")
        self.root.configure(bg="black")

        # --- Directories ---
        self.curr_directory = "A."
        base_dir = os.path.abspath(os.getcwd())
        self.dir_map = {
            "A.": base_dir,
            "A.GAMES": os.path.join(base_dir, "A.GAMES"),
            "A.USER": os.path.join(base_dir, "A.USER"),
            "A.UTILS": os.path.join(base_dir, "A.UTILS"),
        }

        # --- Input control ---
        self.waiting_for_input = False
        self.input_value = None
        self.input_ready = tk.BooleanVar(value=False)

        # --- Screen ---
        self.text = tk.Text(
            root,
            width=COLS,
            height=ROWS,
            bg="black",
            fg="lime",
            insertbackground="lime",
            font=FONT,
            borderwidth=0,
            highlightthickness=0
        )
        self.text.pack()
        self.text.focus()
        self.root.resizable(False, False)

        self.text.bind("<Return>", self.handle_enter)
        self.text.bind("<Key>", self.prevent_edit_above_prompt)

        self.prompt_index = "1.0"
        self.alarms = []

        self.boot()

    # ---------------- BOOT ----------------
    def boot(self):
        self.text.insert("end", "BBC Computer 32K\nModel B\n\nBASIC\n\n")
        self.text.insert("end", "Type HELP or ? for help.\n\n")
        self.new_prompt()

    def new_prompt(self):
        self.text.insert("end", f"{self.curr_directory}>")
        self.prompt_index = self.text.index("insert")
        self.text.mark_set("insert", "end")

    # ---------------- INPUT ----------------
    def handle_enter(self, event):
        cmd = self.text.get(self.prompt_index, "end-1c")
        self.text.insert("end", "\n")

        if self.waiting_for_input:
            self.input_value = cmd.strip()
            self.input_ready.set(True)
            return "break"

        self.execute_command(cmd.strip())
        return "break"


    def prevent_edit_above_prompt(self, event):
        if self.text.compare("insert", "<", self.prompt_index):
            return "break"

    # ---------------- COMMANDS ----------------
    def execute_command(self, cmd):
        if not cmd:
            self.new_prompt()
            return

        parts = cmd.split()
        command = parts[0].upper()

        if command == "PRINT":
            self.text.insert("end", " ".join(parts[1:]) + "\n")

        elif command == "CLS":
            self.text.delete("1.0", "end")

        elif command in ("HELP", "?"):
            self.text.insert("end", "Commands:\n")
            self.text.insert("end", "PRINT, CLS, TIME, RUN, CD, DIR, BASIC.CMSC\n")

        elif command == "TIME":
            self.text.insert("end", time.strftime("%H:%M:%S") + "\n")

        elif command == "CD":
            if len(parts) > 1 and parts[1] in self.dir_map:
                self.curr_directory = parts[1]
                self.text.insert("end", f"Changed to {parts[1]}\n")
            else:
                self.text.insert("end", "Directory not found.\n")

        elif command == "DIR":
            path = self.dir_map[self.curr_directory]
            self.text.insert("end", f"\nFILES IN {self.curr_directory}:\n")
            try:
                for f in os.listdir(path):
                    self.text.insert("end", f" - {f}\n")
            except FileNotFoundError:
                self.text.insert("end", "Directory empty or missing.\n")

        elif command == "RUN":
            if len(parts) < 2:
                self.text.insert("end", "No program specified.\n")
            else:
                pgm = parts[1]
                real_dir = self.dir_map[self.curr_directory]
                try:
                    subprocess.Popen(
                        [sys.executable, pgm],
                        cwd=real_dir
                    )
                    self.text.insert("end", f"Running {pgm} (external)\n")
                except FileNotFoundError:
                    self.text.insert("end", "File not found.\n")

        elif command == "BASIC.CMSC":
            if len(parts) < 2:
                self.text.insert("end", "cmsc: missing filename\n")
                self.new_prompt()
                return

            filename = parts[1]
            real_dir = self.dir_map[self.curr_directory]
            path = os.path.join(real_dir, filename)

            cmsc.set_output(self.cmsc_terminal_print)
            cmsc.set_input(self.cmsc_terminal_input)

            returned_data = cmsc.load_code(path)
            if returned_data:
                self.text.insert("end", returned_data + "\n")

            self.new_prompt()
            return


        else:
            self.text.insert("end", "?SYNTAX ERROR\n")

        self.new_prompt()

    # ---------------- CMS I/O ----------------
    def cmsc_terminal_print(self, text):
        self.text.insert("end", text)
        self.text.see("end")

    def cmsc_terminal_input(self, prompt):
        self.text.insert("end", prompt)
        self.text.see("end")

        self.waiting_for_input = True
        self.input_value = None
        self.input_ready.set(False)

        self.root.wait_variable(self.input_ready)

        self.waiting_for_input = False
        return self.input_value


          


    


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    sim = BBCSimulator(root)

    root.mainloop()

