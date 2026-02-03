import tkinter as tk
import time
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
        # Current directory, default to A. Directories as lists.
        self.curr_directory = "A."
        base_dir = os.path.abspath(os.getcwd())
        self.dir_map = {
            "A.":base_dir,
            "A.GAMES":os.path.join(base_dir, "A.GAMES"),
            "A.USER": os.path.join(base_dir, "A.USER"),
            "A.UTILS":os.path.join(base_dir, "A.UTILS"),
        }
        # List of alarms
        self.alarms = []  # list of (time, name)


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

        self.text.bind("<Return>", self.handle_enter)
        self.text.bind("<Key>", self.prevent_edit_above_prompt)

        self.prompt_index = "1.0"
        self.running = True

        self.boot()

    # ---------------- BOOT ----------------
    def boot(self):
        self.text.insert("end", "BBC Computer 32K\n")
        self.text.insert("end", "Model B\n\n")
        self.text.insert("end", "BASIC\n\n")
        self.text.insert("end", "Type HELP or ? for help.\n\n")
        self.new_prompt()

    def new_prompt(self):
        self.text.insert("end", f"{self.curr_directory}>")
        self.prompt_index = self.text.index("insert")
        self.text.mark_set("insert", "end")

    # ---------------- INPUT HANDLING ----------------
    def handle_enter(self, event):
        cmd = self.text.get(self.prompt_index, "end-1c").strip()
        self.text.insert("end", "\n")
        self.execute_command(cmd)
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

        elif command == "HELP" or command == "?":
            self.text.insert("end", "Available commands:\n")
            self.text.insert("end", "-PRINT <text>\n")
            self.text.insert("end", "- CLS\n")
            self.text.insert("end", "- TIME\n")
            self.text.insert("end", "- HELP\n")
            self.text.insert("end", "- RUN (Only runs C-, and Py Programs, extension .cms (CMS compiler coming soon))\n")
            self.text.insert("end", "- OPEN (Please, when using \"open\", \nuse CD to navigate to the correct directory first,\nthen use OPEN and your file name, and extension.)\n")
            self.text.insert("end", "- CD <directory>\n")
            self.text.insert("end", "- DIR\n")
            self.text.insert("end", "- ADD_PGM <program_name>\n")
            self.text.insert("end", "- DEL <file_name>\n")
            self.text.insert("end", "- EDIT_PGM <program_name>\n")
            self.text.insert("end", "- ALARM <name> <HH:MM>\n")
            self.text.insert("end", "\nAbout:\nThis is a BBC Micro Model B simulator, creatd\nby AmadOS, programmed in Python using Tkinter.\n")
            self.text.insert("end", "Possible questions:\nWhat does CMS stand for?\nAnswer: CMS stands for 'C Minus', a simplified version of C\nprogramming language made by AmadOS and for educational purposes.\nHow to run CMS programs?\nAnswer: To run CMS code, simply use CD to go to your\nCMS file's location,\n")
            self.text.insert("end", "then use the RUN command followed by your file name with extension.\n")
            self.text.insert("end", "Note: CMS Compiler is still in development, so some features may not\nwork as expected.\n")
        elif command == "TIME":
            self.text.insert("end", time.strftime("%H:%M:%S") + "\n")

        elif command == "RUN":
            pgm = parts[1]
            if len(parts) < 2:
                self.text.insert("end", "No program specified.\n")
                
            elif pgm.endswith(".cms") or pgm.endswith(".CMS"):
                self.text.insert("end", "CMS not found - Run with a compiler, or use the built \nin one. (BASIC.CMSC)\n")

            elif pgm.endswith(".py"):
                self.text.insert("end", f"Running Python Program {pgm}...\n")
                import os, sys, subprocess
                try:
                    real_dir = self.dir_map[self.curr_directory]
                    proc = subprocess.Popen([sys.executable, pgm], cwd=real_dir)
                    self.running_process = proc
                    self.text.insert("end", "\nPlease visit terminal.\n")
                    self.new_prompt()
                except FileNotFoundError:
                    self.text.insert("end", f"\nFile {pgm} not found")

            else:
                self.text.insert("end", f"Cannot run program {pgm}, unsupported format.\n")

        elif command == "CD":
            if len(parts) > 1 and parts[1] in DIRECTORIES:
                self.text.insert("end", f"Changing Directory to {parts[1]}...\n")
                self.curr_directory = parts[1]
                self.text.insert("end", f"Changed to {parts[1]}\n")
            else:
                self.text.insert("end", "Directory not found.\n")

        elif command == "DIR":
            import os
            self.text.insert("end", f"\nFILES IN DIRECTORY \"{self.curr_directory}\":")
            dir_path = self.curr_directory
            try:
                files = os.listdir(dir_path)
                for file in files:
                    self.text.insert("end", f"\n - {file}")
                self.text.insert("end", "\n")
            except FileNotFoundError:
                self.text.insert("end", "\n No files found or directory does not exist.\n")

        elif command == "OPEN":
            prog = parts[1]
            if len(prog) < 2:
                self.text.insert("end", "No file specified.\n")
            else:
                self.text.insert("end", "Operation in progress...\n")

                if self.curr_directory == "A.":
                    self.text.insert(
                    "end",
                    f"Cannot load program {prog}, directory \"A.\"\ndoes not allow program access.\n"
                )
                
                else:
                    self.text.insert("end", f"Opening file {prog} in CodeDisplayer.bex...\n")
                    with open(f"{self.curr_directory}\\{prog}", "r") as f:
                        contents = f.read()
                    self.text.insert("end", contents + "\n")
            # Debugging old code
            #else:
            #    self.text.insert(
            #    "end",
            #    f"Program {prog} does not exist in directory {self.curr_directory}\n"
            #)
                
        elif command == "ADD_PGM":
            name = parts[1]
            if len(parts) < 2:
                self.text.insert("end", "Program must have a name, and extension.\n")
            else:
                self.text.insert("end", "PLEASE VISIT YOUR CONSOLE, THEN ANSWER THE FOLLOWING STEPS.\n")
                name = input("Enter name: ")
                self.text.insert("end","PLEASE WAIT...\nSTATUS: LOADING_EXTREQ\n")
                ext = input("Enter file extension: ")
                self.text.insert("end","PLEASE WAIT...\nSTATUS: LOADING_DIRREQ\n")
                contents = input("Enter file contents: ")
                self.text.insert("end","PLEASE WAIT...\nSTATUS: SAVING_FILE\n")
                print("Please visit the simulator again for more information.")
                if self.curr_directory == "A.":
                    self.text.insert("end", f"\nERROR: CANNOT ADD PROGRAMS TO {self.curr_directory}, PLEASE CHANGE TO AN ANOTHER DIR.\n")
                else:
                    self.text.insert("end", f"\nAdding program {name}.{ext} to current directory...\n")
                    with open(f"{self.curr_directory}\\{name}.{ext}", "w") as f:
                        f.write(contents)
                        self.text.insert("end", "Complete.\n")
        
        elif command == "BASIC.CMSC":
            import cms_compiler as cmsc
            commando = parts[1]
            if len(parts) < 2:
                print("cmsc: Please enter filename. (Ensure you're in the right directory.)")
            else:
                self.text.insert("end", "cmsc: Running CMS file...\n")
                print(f"{self.curr_directory}\\{commando}")
                cmsc.set_output(self.cmsc_terminal)
                returned_data = cmsc.load_code(f"{self.curr_directory}\\{commando}")
                if returned_data:
                    self.text.insert("end", returned_data + "\n")


        
        elif command == "DEL":
            name = parts[0]
            import os
            if len(parts) < 2:
                self.text.insert("end", "File must have a name, and extension.\n")
            else:
                self.text.insert("end", "PLEASE VISIT YOUR CONSOLE, THEN ANSWER THE FOLLOWING STEPS.\n")
                name = input("Enter name: ")
                self.text.insert("end","PLEASE WAIT...\nSTATUS: LOADING_DIRREQ\n")
                file_dir = input(f"Where is this file located?({name}): ")
                self.text.insert("end","PLEASE WAIT...\nSTATUS: DELETING_FILE\n")
                print("Please visit the simulator again for more information.")
                if file_dir == "A.":
                    self.text.insert("end", f"\nERROR: CANNOT DELETE {name} IN A.\n")
                else:
                    self.text.insert("end", "\nDELETION IN PROGRESS...\n")
                    self.text.insert("end", "SUCCESS\n")
                    os.remove(f"{self.curr_directory}\\{name}")
        
        elif command == "EDIT_PGM":
            pgm = parts[1]
            if len(parts) < 2:
                self.text.insert("end", "Must enter the Program's name.\n")
            elif self.curr_directory == "A.":
                self.text.insert("end", f"Cannot edit programs in {self.curr_directory}.\n")

            else:
                self.text.insert("end", "Opening program for editing...\n")
                new_contents = input("Enter new contents: ")
                with open(f"{self.curr_directory}\\{pgm}", "w") as f:
                    f.write(new_contents)
                self.text.insert("end", f"Program {pgm} edited successfully.\n")
        
        
        elif command == "ALARM":
            alarm_name = parts[1]
            alarm_time = parts[2]
            if len(parts) < 3:
                self.text.insert("end", "Usage: ALARM <name> <HH:MM>\n")
            else:
                self.alarms.append((alarm_time, alarm_name))
                self.text.insert("end", f"Alarm '{alarm_name}' set for {alarm_time}.\n")


        else:
            self.text.insert("end", "?SYNTAX ERROR\n")
        self.new_prompt()
        self.check_alarms()
    def check_alarms(self):
        now = time.strftime("%H:%M")
        for alarm_time, alarm_name in self.alarms[:]:
            if alarm_time == now:
                self.text.insert("end", f"\n*** ALARM: {alarm_name} ***\n")
                self.alarm_beep(2)
                self.new_prompt()
                self.alarms.remove((alarm_time, alarm_name))
        self.root.after(1000, self.check_alarms)
    
    
    def alarm_beep(self, count):
        if count <= 0:
            return
        self.root.bell()
        self.root.after(2000, self.alarm_beep, count - 1)

    def cmsc_terminal(self, text):
        self.text.insert("end", text)
        self.text.see("end")
    


    


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    sim = BBCSimulator(root)

    root.mainloop()

