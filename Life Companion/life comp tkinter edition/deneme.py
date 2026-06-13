import tkinter as tk

# 1. Define the function first so the button can see it
def save_input():
    user_text = entry_box.get()  # <--- This is the "quick" grab
    print(user_text)

root = tk.Tk()

# 2. Create the box
entry_box = tk.Entry(root)
entry_box.pack()

# 3. Create the button LAST, pointing to the function above
button = tk.Button(root, text="Save", command=save_input)
button.pack()

root.mainloop()