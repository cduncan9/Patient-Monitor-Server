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

    def get_file():
        fn = filedialog.askopenfilename()
        file_name.set(fn)

    def load_image():
        fn = file_name.get()
        tk_image = load_image_for_display(fn)
        image_label.configure(image=tk_image)
        image_label.image = tk.image
        result_label.grid_remove()



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

    file_name = tk.StringVar()
    file_name_box = ttk.Entry(root, width=50, textvariable=file_name)
    file_name_box.grid(column=0, row=3)

    ok_button = ttk.Button(root, text="ok", comman=load_image)
    ok_button.grid(column=1, row=3)

    image_label = ttk.Label(root)
    image_label.grid(column=0, row=0)

    result_label = ttk.Label(root)
    result_label.grid(column=4, row=1)



    root.mainloop()
    print("finished")

if __name__ == "__main__":
    design_window()