import tkinter as tk
from tkinter import ttk
import base64
from tkinter import filedialog
from PIL import Image, ImageTk


def load_image_for_display(file_name):
    image_object = Image.open(file_name)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image

def convert_file_to_b64str(fn):
    with open(fn, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def design_window():

    def cancel():
        root.destroy()

    root = tk.Tk()
    root.title("Patient User Interface")

    name_label = ttk.Label(root, text="Name")
    name_label.grid(column=0, row=1)

    name_entry = tk.StringVar()
    name_entry.set("Enter Your Name")
    name_entry_box = ttk.Entry(root, width=30, textvariable=name_entry)
    name_entry_box.grid(column=1, row=1)

    mrn_label = ttk.Label(root, text="Medical Record Number")
    mrn_label.grid(column=0, row=2)

    mrn_entry = tk.StringVar()
    mrn_entry.set("Enter Your MRN")
    mrn_entry_box = ttk.Entry(root, width=30, textvariable=mrn_entry)
    mrn_entry_box.grid(column=1, row=2)



    root.mainloop()
    print("finished")

if __name__ == "__main__":
    design_window()