import tkinter as tk

def on_key_press(event):
    print(f'Key pressed: {event.char}')

root = tk.Tk()
root.bind('<KeyPress>', on_key_press)
root.mainloop()

