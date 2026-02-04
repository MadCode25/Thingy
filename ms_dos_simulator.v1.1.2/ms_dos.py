# A M A D  O S
# msdos_sim.1.1.2

import tkinter as tk
import time as t


H = 20
W = 60
F = "Courier New", 14

class MSDOS_112:
    def __init__(self, master):
        self.master = master
        self.master.title("MS-DOS Simulator | V1.1.2")
        self.text = tk.Text(
            root,
            width=W,
            height=H,
            bg="black",
            fg="white",
            insertbackground="white",
            font=F,
            borderwidth=0,
            highlightthickness=0
        )
        self.text.focus()
        self.text.pack()
        self.master.resizable(False, False)
        self.prompt_index = "1.0"
        self.text.bind("<Return>", self.handle_enter)
        self.text.bind("<Key>", self.prevent_top_console_edit)

        self.boot()
    # ---- BOOT ---- #

    def boot(self):
        self.text.insert("end", "MS-DOS 1.1.2\n")
        self.text.insert("end", "AmadOS | Microsoft 1981-2026\n\n")
        self.new_prompt()

    def new_prompt(self):
        self.text.insert("end", "> ")
        self.prompt_index = self.text.index("insert")
        self.text.mark_set("insert", "end")

    def handle_enter(self, event):
        cmd = self.text.get(self.prompt_index, "end-1c")
        self.text.insert("end", "\n")
        self.execute_command(cmd.strip())
        return "break"
    
    def prevent_top_console_edit(self, event):
        if self.text.compare("insert", "<", self.prompt_index):
            return "break"
        
    def execute_command(self, cmd):
        parts = cmd.split()
        command = parts[0].upper()
        if not cmd:
            self.new_prompt()
            return

        elif command == "WIN":
            self.text.insert("end", "\nStarting Windows...\n")
            self.text2 = tk.Text(
                root,
                bg="#0015ff",
                font=F,
                fg = "white",
                insertbackground="white",
                width=W,
                height=H
            )
            self.text.pack_forget()
            self.text2.tag_config("center", justify="center")
            self.text2.focus()
            self.text2.pack()
            self.text2.insert("end", "Time: ")
        
        else: 
            self.text.insert("end", "Bad command or filename.\n")
        self.new_prompt()


if __name__ == "__main__":
    root = tk.Tk()
    sim = MSDOS_112(root)

    root.mainloop()
    
