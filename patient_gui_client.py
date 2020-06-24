import tkinter as tk
from tkinter import ttk
import base64
from tkinter import filedialog
from PIL import Image, ImageTk
from ECG_analyis import mean_bpm
from ECG_analyis import normalize_data
import matplotlib.pyplot as plt
import requests
from cloud_server import NewPatient

# mrn_entry = 0
# name_entry = ""
# image_name = ""
# file_name = ""

server_name = "http://127.0.0.1:5000"


def load_image_for_display(file_name):
    image_object = Image.open(file_name)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def convert_file_to_b64str(fn):
    with open(fn, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def send_patient_to_server(mrn_val, name):
    info = [mrn_val, name, list(), list(), list(), list()]
    r = requests.post(server_name+"/api/new_patient", json=info)
    print(r.text)
    if r == 200:
        return "Good Post"
    else:
        return "Bad Post"


def design_window():

    def send_patient():
        send_patient_to_server(mrn_entry.get(), name_entry.get())

    def get_file():
        fn = filedialog.askopenfilename()
        file_name.set(fn)

    def get_image():
        im = filedialog.askopenfilename()
        image_name.set(im)

    def load_image():
        fn = image_name.get()
        tk_image = load_image_for_display(fn)
        image_label.configure(image=tk_image)
        image_label.image = tk.image
        result_label.grid_remove()

    def load_ECG_trace():
        fn = file_name.get()
        hr_data = normalize_data(fn)
        plt.plot(hr_data[:, 0], hr_data[:, 1])
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (mV)")
        plt.title("ECG Trace")
        plt.show()
        # result = mean_bpm(fn)

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

    image_name = tk.StringVar()
    image_name_box = ttk.Entry(root, width=50, textvariable=image_name)
    image_name_box.grid(column=0, row=3)

    image_button = ttk.Button(root, text="get image name", command=get_image)
    image_button.grid(column=0, row=4)

    image_ok_button = ttk.Button(root, text="ok", command=load_image)
    image_ok_button.grid(column=1, row=3)

    image_label = ttk.Label(root)
    image_label.grid(column=0, row=0)

    result_label = ttk.Label(root)
    result_label.grid(column=4, row=1)

    file_name = tk.StringVar()
    file_name_box = ttk.Entry(root, width=50, textvariable=file_name)
    file_name_box.grid(column=0, row=5)

    file_button = ttk.Button(root, text="get filename", command=get_file)
    file_button.grid(column=0, row=6)

    file_ok_button = ttk.Button(root, text="ok", command=load_ECG_trace)
    file_ok_button.grid(column=1, row=5)

    upload_data_button = ttk.Button(root, width=20, text="upload to database",
                                    command=send_patient)
    upload_data_button.grid()

    root.mainloop()
    print("finished")


if __name__ == "__main__":
    design_window()
