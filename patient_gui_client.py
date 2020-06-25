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
from io import BytesIO
from datetime import datetime

# mrn_entry = 0
# name_entry = ""
# image_name = ""
# file_name = ""

server_name = "http://127.0.0.1:5000"


def load_image_for_display(file_name):
    """Converts a file to Image object in tkinter

    Uses PIl libraries Image and ImageTk to convert file to image object
    Returns the image object in format that is tkinter compatible.

    :param file_name: str containing path to image file
    :return: ImageTk object of input image file
    """
    image_object = Image.open(file_name)
    image_object = image_object.resize((300, 300), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def convert_file_to_b64str(fn):
    """Converts input file to base 64 string

    Uses base64 library to convert image to a string
    Returns image in base 64 string, utf-8 encoded

    :param fn: str containing input file name
    :return: str containing base 64 image
    """
    with open(fn, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def convert_plot_to_b64str():
    """Converts matplotlib plot to b64 string

    Employs io library to convert mayplotlib plot to png
    and then to b64 string

    :return: str containing the matplotlib plot in base64
    """
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.read())
    return figdata_png


def send_patient_to_server(mrn_val, name, hr, timestamp, ecg, image):
    """Sends new patient to the database

    Makes post request to server with all data input to gui
    which adds a new patient to the database.

    :param mrn_val: int containing medical record number
    :param name: str containing patient name
    :param hr: float containing calculated heart rate
    :param timestamp: str containing timestamp
    :param ecg: str containing ecg plot in base 64
    :param image: str containing the medical image in base 64
    :return: str "Good Post" if post was succesful, "Bad Post" otherwise
    """
    info = [mrn_val, name, hr, timestamp, ecg, image]
    r = requests.post(server_name+"/api/new_patient", json=info)
    print(r.text)
    if r == 200:
        return "Good Post"
    else:
        return "Bad Post"


def design_window():

    def send_patient():
        """Calls send_patient_to_server with local variables

        Uses .get() command on tk.StringVars present in the gui
        to upload user inputed patient to the database
        """
        fn = image_name.get().split("/")
        name = fn[-1]
        send_patient_to_server(mrn_entry.get(),
                               name_entry.get(),
                               [load_ECG_trace()[0]],
                               [datetime.strftime(datetime.now(),
                                                  "%Y-%m-%d %H:%M:%S")],
                               [load_ECG_trace()[1]],
                               [[convert_file_to_b64str(image_name.get()),
                                name]])

    def get_file():
        """Gets file from user's file dialog

        This function is called with a tk button command
        """
        fn = filedialog.askopenfilename()
        file_name.set(fn)

    def get_image():
        """Gets image from user's file dialog

        This function is called with a tk button command
        """
        im = filedialog.askopenfilename()
        image_name.set(im)

    def load_image():
        """Loads Image object into local varaible

        Loads image by calling load_image_for_display()
        and puts the Image object in image_label.image
        to be displayed in GUI
        """
        fn = image_name.get()
        tk_image = load_image_for_display(fn)
        image_label.configure(image=tk_image)
        image_label.image = tk.image
        result_label.grid_remove()

    def save_ecg_image(ecg_image):
        """Decodes ecg image from b64 string

        Writes ecg image to out_file called temp_image

        :param ecg_image: str containing ecg image in base 64
        """
        image_bytes = base64.b64decode(ecg_image)
        with open("temp_image", "wb") as out_file:
            out_file.write(image_bytes)

    def load_ecg():
        """Loads image object into local variable

        Loads image object by calling load_image_for_display()
        into display_past_ecg_value varaible to be displayed in
        GUI
        """
        tk_image = load_image_for_display("temp_image")
        display_past_ecg_value.image = tk_image
        display_past_ecg_value.configure(image=tk_image)

    def load_ECG_trace():
        """Processes input ECG data

        This function takes in ECG data .csv files, calls
        functions from ECG_analysis.py to read and process the data
        THe data is plotted using matplotlib, converted to .png
        and encoded into a b64 string

        :return: [float containing mean bpm, str containing ecg plot in b64]
        """
        fn = file_name.get()
        hr_data = normalize_data(fn)
        plt.clf()
        plt.plot(hr_data[:, 0], hr_data[:, 1])
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (mV)")
        plt.title("ECG Trace")
        plot_bytes = BytesIO()
        plt.savefig(plot_bytes, format='png')
        plot_bytes.seek(0)
        temp = base64.b64encode(plot_bytes.read())
        plot_hash = str(temp, encoding='utf-8')
        result = mean_bpm(fn)
        save_ecg_image(plot_hash)
        load_ecg()
        return [result, plot_hash]

    def cancel():
        """Closes gui

        """
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
    image_label.grid(column=1, row=7)

    result_label = ttk.Label(root)
    result_label.grid(column=4, row=1)

    display_past_ecg_value = ttk.Label(root)
    display_past_ecg_value.grid(column=0, row=7)

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
