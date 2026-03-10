import tkinter as tk

i = 0  # Initialized to 0 so first click shows "1"

def on_button_click():
    global i  # 1. Tell Python to use the global 'i'
    i += 1    # 2. Increment it
    
    label.config(text="Button clicked!")
    # 3. Manually update the button's text with the new value
    button.config(text=f"You clicked me {i} times")

root = tk.Tk()
root.title("Interactive GUI")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(root, text="Click the button:")
label.pack(pady=10)

# Set the initial text for the button
button = tk.Button(root, text="You didn't click me yet", command=on_button_click)
button.pack(pady=10)

root.mainloop()
