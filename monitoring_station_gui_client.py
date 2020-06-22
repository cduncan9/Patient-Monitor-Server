import tkinter as tk
from tkinter import ttk


def get_available_patient_ids():
    # This should make a request to the server and return
    # available patient_ids
    return "001"  # This is just a place holder


def load_patient_data():
    return


def design_window():
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
                                     command=load_patient_data)
    load_patient_button.grid(column=2, row=0)

    display_patient_id_text = ttk.Label(root, text="Patient ID:")
    display_patient_id_text.grid(column=0, row=2, sticky="E")

    display_patient_name_text = ttk.Label(root, text="Patient Name:")
    display_patient_name_text.grid(column=0, row=3, sticky="E")

    display_patient_hr_text = ttk.Label(root, text="Heart Rate:")
    display_patient_hr_text.grid(column=0, row=4, sticky="E")

    display_ecg_text = ttk.Label(root, text="ECG Image:")
    display_ecg_text.grid(column=0, row=5)

    display_timestamp_text = ttk.Label(root, text="Date and Time of Last Heart Rate Reading:")
    display_timestamp_text.grid(column=0, row=6, columnspan=2)



    root.mainloop()


if __name__ == '__main__':
    design_window()
