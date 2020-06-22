import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


server_name = ""


# def load_image_for_display(file_name):
#     image_object = Image.open(file_name)
#     tk_image = ImageTk.PhotoImage(image_object)
#     return tk_image


def get_available_patient_ids():
    # This should make a request to the server and return
    # available patient_ids
    return "001"  # This is just a place holder


def load_patient_data():
    # I think that I will store everything in a dictionary
    return


def get_past_ecg_files():
    return


def load_ecg_image(timestamp):
    return


def get_image_file():
    return


def load_medical_image(timestamp):
    return


def design_window():

    def display_patient_data():
        # patient_dict = load_patient_data()
        # pat_id = patient_dict["Patient ID"]
        # pat_name = patient_dict["Name"]
        # pat_hr = patient_dict["Heart Rate"]
        # pat_time = patient_dict["timestamp"]
        # ecg_file = load_ecg_image(pat_time)
        #
        # display_patient_id_value = ttk.Label(root, text=pat_id)
        # display_patient_id_value.grid(column=1, row=2, sticky="E")
        #
        # display_patient_name_value = ttk.Label(root, text=pat_name)
        # display_patient_name_value.grid(column=1, row=3, sticky="E")
        #
        # display_patient_hr_value = ttk.Label(root, text=pat_hr)
        # display_patient_hr_value.grid(column=1, row=4, sticky="E")
        #
        # display_ecg_value = ttk.Label(root)
        # display_ecg_value.grid(column=1, row=5, sticky="E")
        #
        # display_timestamp_value = ttk.Label(root, text=pat_time)
        # display_timestamp_value.grid(column=1, row=6, sticky="E")
        return

    def cancel():
        root.destroy()

    def reset():
        return

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
