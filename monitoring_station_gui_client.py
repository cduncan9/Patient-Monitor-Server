import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import base64
import io
import matplotlib.image as mpimg
import requests

server_name = "http://127.0.0.1:5000"


def load_image_for_display(file_name):
    image_object = Image.open(file_name)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def get_available_patient_ids():
    # This will make a request
    r = requests.get(server_name + "/patient_id_list")
    return r.json()


def get_past_ecg_files(patient_id):
    # This will make a request
    r = requests.get(server_name + "/"+patient_id+"/ecg_image_list")
    return r.json()


def get_image_files():
    # this will make a request
    r = requests.get(server_name + "/<patient_id>/medical_image_list")
    return r.json()


def load_patient_data(patient_id):
    # This will make a request
    r = requests.get(server_name+"/"+patient_id+"/load_recent_data")
    return r.json()


def load_ecg_image(patient_id, timestamp):
    # This will make a request
    r = requests.get(server_name+"/"+patient_id+"/load_ecg_image/"+timestamp)
    return r.text


def load_medical_image(timestamp):
    # this will make a request
    return


def design_window():

    def load_ecg():
        tk_image = load_image_for_display("temp_image")
        display_past_ecg_value.configure(image=tk_image)
        display_past_ecg_value.image = tk.image

    def load_recent_ecg():
        recent_tk_image = load_image_for_display("recent_image")
        display_ecg_value.configure(image=recent_tk_image)
        display_ecg_value.image = tk.image

    def ecg_list():
        return get_past_ecg_files(patient_choice.get())

    def display_ecg_image():
        # Edit this more
        ecg_image = load_ecg_image(patient_choice.get(),
                                   past_ecg_file.get())
        save_ecg_image(ecg_image)
        past_text = "ECG from {}".format(past_ecg_file.get())
        display_past_ecg_text.configure(text=past_text)
        save_past_ecg_button = ttk.Button(root, text="Save Past ECG Image")
        save_past_ecg_button.grid(column=2, row=6)
        load_ecg()

    def display_recent_ecg_image(ecg_string):
        # Edit this more
        save_recent_ecg_image(ecg_string)
        load_recent_ecg()

    def save_ecg_image(ecg_image):
        image_bytes = base64.b64decode(ecg_image)
        with open("temp_image", "wb") as out_file:
            out_file.write(image_bytes)

    def save_recent_ecg_image(ecg_image):
        image_bytes = base64.b64decode(ecg_image)
        with open("recent_image", "wb") as out_file:
            out_file.write(image_bytes)

    def display_medical_image():
        # Edit this more
        return

    def display_patient_data():
        patient_data = load_patient_data(patient_choice.get())
        print(patient_data)
        pat_id = patient_data[0]
        pat_name = patient_data[1]
        pat_hr = patient_data[2]
        pat_time = patient_data[3]

        past_ecg_box['values'] = ecg_list()
        # load_image_box['values'] = get_image_files()

        display_patient_id_value.configure(text=pat_id)
        display_patient_name_value.configure(text=pat_name)
        display_patient_hr_value.configure(text=pat_hr)
        display_timestamp_value.configure(text=pat_time)
        display_recent_ecg_image(patient_data[4])

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

    patient_choice = tk.StringVar()
    patient_id_box = ttk.Combobox(root, textvariable=patient_choice)
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
    past_ecg_box.state(['readonly'])
    past_ecg_box.grid(column=1, row=7)

    past_ecg_button = ttk.Button(root, text="Load Data",
                                 command=display_ecg_image)
    past_ecg_button.grid(column=2, row=7)

    display_past_ecg_text = ttk.Label(root)
    display_past_ecg_text.grid(column=2, row=4)

    display_past_ecg_value = ttk.Label(root)
    display_past_ecg_value.grid(column=2, row=5, sticky="E")

    load_image_text = ttk.Label(root, text="Load Medical Image")
    load_image_text.grid(column=0, row=8)

    load_image_file = tk.StringVar()
    load_image_box = ttk.Combobox(root, textvariable=load_image_file)
    load_image_box.state(['readonly'])
    load_image_box.grid(column=1, row=8)

    load_image_button = ttk.Button(root, text="Load Image",
                                   command=display_medical_image)
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
