import tkinter as tk

H = 20
W = 50
F = "Courier New", 14

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LTS Schedules for students | LTSS")
        self.root.resizable(False, False)
        self.students = {
            "Amado": "10:00-5:00-7:00"
        }
        self.text = tk.Text(
            root,
            width=W,
            height=H,
            bg="black",
            fg="lime",
            font=F,
            insertbackground="lime",
            borderwidth=0,
            highlightcolor="lime",
            highlightthickness=0
        )


        self.text.pack()
        self.text.focus()
        self.text.insert("end","Welcome to BASIC's schedule maker\n(exclusively for: LTS)\n")
        self.text.insert("end", "Type help or ? for commands to add, remove,\nor reschedule a student.\n\n")
        self.text.bind("<Return>", self.handle_enter)
        self.text.bind("<Key>", self.prevent_edit_above_prompt)
        self.prompt_index = "1.0"
        self.new_prompt()


    def new_prompt(self):
        self.text.insert("end",">")
        self.prompt_index = self.text.index("insert")
        self.text.mark_set("insert", "end")

    def handle_enter(self, event):
        cmd = self.text.get(self.prompt_index, "end-1c").strip()
        self.text.insert("end", "\n")
        self.execute_command(cmd)
        return "break"
    def prevent_edit_above_prompt(self, event):
        if self.text.compare("insert", "<", self.prompt_index):
            return "break"
    
    def execute_command(self,cmd):
        if not cmd:
            self.new_prompt()
            return
        parts = cmd.split()
        command = parts[0].upper()
        # WARNING EDITORS!: When adding a new command, please add self.new_prompt() at the end of your command code.
        if command == "help" or command == "?":
            self.text.insert("end", "\nCommands:\n")
            self.text.insert("end", "Add - Adds a student to student list. (Usage: <name> HH:MM)\n")
            self.text.insert("end", "Remove - Removes a student from list\n")
            self.text.insert("end", "Resch - Reschedules a student. (Usage <name> HH:MM)\n")
            self.text.insert("end", "GUI2 - Switches to the user-friendly mode\nwhich will remove the\nsimulator's original\nfeeling.\n")
            self.new_prompt()
        elif command == "Add ":
            if len(parts) < 2:
                self.text.insert("end", "\nUsage of command 'Add':\n<student name> HH:MM\n")

        else:
            self.text.insert("end", f"Unknown command: {cmd}\n")
            self.new_prompt()

        


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop() 