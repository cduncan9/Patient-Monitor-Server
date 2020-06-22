import tkinter as tk
from tkinter import ttk


def design_window():
    root = tk.Tk()
    root.title("Monitoring Station User Interface")

    patient_id_text = ttk.Label(root, text="Select Patient ID")
    patient_id_text.grid(column=0, row=0)

    patient_id_box = ttk.Combobox(root)
    patient_id_box.grid(column=0, row=1)

    root.mainloop()


if __name__ == '__main__':
    design_window()
