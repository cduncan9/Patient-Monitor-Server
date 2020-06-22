import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import base64
import io
import matplotlib.image as mpimg


server_name = ""


def load_image_for_display(file_name):
    image_object = Image.open(file_name)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def get_available_patient_ids():
    # This will make a request
    return


def load_patient_data():
    # This will make a request
    return


def get_past_ecg_files():
    # This will make a request
    return


def load_ecg_image(timestamp):
    # This will make a request
    return


def get_image_file():
    # this will make a request
    return


def load_medical_image(timestamp):
    # this will make a request
    return


def design_window():

    def display_image(base64_string):
        image_bytes = base64.b64decode(base64_string)
        image_buf = io.BytesIO(image_bytes)
        i = mpimg.imread(image_buf, format='JPG')
        plt.imshow(i, interpolation='nearest')
        plt.show()
        return

    def display_patient_data():
        patient_dict = load_patient_data()
        pat_id = patient_dict["Patient ID"]
        pat_name = patient_dict["Name"]
        pat_hr = patient_dict["Heart Rate"]
        pat_time = patient_dict["timestamp"]

        display_patient_id_value.configure(text=pat_id)
        display_patient_name_value.configure(text=pat_name)
        display_patient_hr_value.configure(text=pat_hr)
        display_timestamp_value.configure(text=pat_time)

    def cancel():
        root.destroy()

    def reset():
        nonlocal display_patient_id_value
        nonlocal display_patient_name_value
        nonlocal display_patient_hr_value
        nonlocal display_timestamp_value
        nonlocal display_ecg_value

        display_patient_id_value.configure(text="")
        display_patient_name_value.configure(text="")
        display_patient_hr_value.configure(text="")
        display_timestamp_value.configure(text="")

    root = tk.Tk()
    root.title("Monitoring Station User Interface")

    patient_id_text = ttk.Label(root, text="Select Patient ID")
    patient_id_text.grid(column=0, row=0)

    file_choice = tk.StringVar()
    patient_id_box = ttk.Combobox(root, textvariable=file_choice)
    patient_id_box['values'] = get_available_patient_ids()
    patient_id_box.state(["readonly"])
    patient_id_box.grid(column=1, row=0)

    load_patient_button = ttk.Button(root, text="Load Patient Data",
                                     command=display_patient_data)
    load_patient_button.grid(column=2, row=0)

    display_patient_id_text = ttk.Label(root, text="Patient ID:")
    display_patient_id_text.grid(column=0, row=2, sticky="E")

    display_patient_name_text = ttk.Label(root, text="Patient Name:")
    display_patient_name_text.grid(column=0, row=3, sticky="E")

    display_patient_hr_text = ttk.Label(root, text="Most Recent Heart Rate:")
    display_patient_hr_text.grid(column=0, row=4, sticky="E")

    display_ecg_text = ttk.Label(root, text="Most Recent ECG:")
    display_ecg_text.grid(column=0, row=5, sticky="E")

    display_timestamp_text = ttk.Label(root,
                                       text="Time of Most Recent Reading:")
    display_timestamp_text.grid(column=0, row=6)

    display_patient_id_value = ttk.Label(root)
    display_patient_id_value.grid(column=1, row=2, sticky="E")

    display_patient_name_value = ttk.Label(root)
    display_patient_name_value.grid(column=1, row=3, sticky="E")

    display_patient_hr_value = ttk.Label(root)
    display_patient_hr_value.grid(column=1, row=4, sticky="E")

    display_ecg_value = ttk.Label(root)
    display_ecg_value.grid(column=1, row=5, sticky="E")

    display_timestamp_value = ttk.Label(root)
    display_timestamp_value.grid(column=1, row=6, sticky="E")

    past_ecg_text = ttk.Label(root, text="Load Past ECG")
    past_ecg_text.grid(column=0, row=7)

    past_ecg_file = tk.StringVar()
    past_ecg_box = ttk.Combobox(root, textvariable=past_ecg_file)
    past_ecg_box['values'] = get_past_ecg_files()
    past_ecg_box.state(['readonly'])
    past_ecg_box.grid(column=1, row=7)

    past_ecg_button = ttk.Button(root, text="Load Data",
                                 command=load_ecg_image)
    past_ecg_button.grid(column=2, row=7)

    load_image_text = ttk.Label(root, text="Load Medical Image")
    load_image_text.grid(column=0, row=8)

    load_image_file = tk.StringVar()
    load_image_box = ttk.Combobox(root, textvariable=load_image_file)
    load_image_box['values'] = get_image_file()
    load_image_box.state(['readonly'])
    load_image_box.grid(column=1, row=8)

    load_image_button = ttk.Button(root, text="Load Image",
                                   command=load_medical_image)
    load_image_button.grid(column=2, row=8)

    exit_button = ttk.Button(root, text="Exit",
                             command=cancel)
    exit_button.grid(column=2, row=9)

    reset_button = ttk.Button(root, text="Reset Data",
                              command=reset)
    reset_button.grid(column=1, row=9)

    root.mainloop()


if __name__ == '__main__':
    design_window()
