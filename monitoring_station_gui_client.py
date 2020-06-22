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
    patient_id_text.grid(column=0, row=0, sticky="W")

    file_choice = tk.StringVar()
    patient_id_box = ttk.Combobox(root, textvariable=file_choice)
    patient_id_box['values'] = get_available_patient_ids()
    patient_id_box.grid(column=0, row=1)

    load_patient_button = ttk.Button(root, text="Load Patient Data",
                                     command=load_patient_data)
    load_patient_button.grid(column=1, row=1)

    root.mainloop()


if __name__ == '__main__':
    design_window()
