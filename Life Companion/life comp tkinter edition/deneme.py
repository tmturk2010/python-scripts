import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Exit Application Example")
root.geometry("300x100")

# Create a parent frame container
frm = ttk.Frame(root, padding=10)
frm.grid()

# Add a label widget at column 0, row 0
ttk.Label(frm, text="Click to exit:").grid(column=0, row=0, padx=5)

# Your button snippet placed at column 1, row 0
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0, padx=5)

# Start the application event loop
root.mainloop()
