import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import base64
import io
import matplotlib.image as mpimg
import requests
from tkinter.filedialog import asksaveasfile

server_name = "http://127.0.0.1:5000"


def load_image_for_display(file_name):
    """
    This function converts image files to be displayed using tkinter

    To load an image onto a tkinter window, you have to ensure that
    it is in the proper format for tkinter to use it. This function
    uses the Pillow package to prepare an image for use. First the image
    is loaded from a filename into a PIL image object. Then, as the images
    are generally very large, the images are resized to be 350X250. Then
    The PIL image objects are converted into a Tk image object, and this
    object is returned.
    :param file_name: The file storing the desired image
    :return: Tk image object for use in a Tk interface
    """
    image_object = Image.open(file_name)
    image_object = image_object.resize((350, 250), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(image_object)
    return tk_image


def get_available_patient_ids():
    """
    This function makes a GET request and returns a list of patient ids

    This function makes a GET request to the cloud server that stores
    patient data. This GET request will return a list of patient ids
    that are present in the database. This list is returned.
    :return: a list of patient ids in the database
    """
    # This will make a request
    r = requests.get(server_name + "/patient_id_list")
    return r.json()


def get_past_ecg_files(patient_id):
    """
    This function returns a list of ECG timestamps for a patient

    This function receives a patient id as input and includes that
    in the server name when it makes a GET request. The GET
    request is for a list of ECG times for that specific patient.
    This list of times is returned.
    :param patient_id: The id number of the patient of interest
    :return: a list of times that ECG data sets were uploaded
    """
    # This will make a request
    r = requests.get(server_name + "/"+patient_id+"/ecg_image_list")
    return r.json()


def get_image_files(patient_id):
    """
    This function returns the a list of filenames of stored medical
    images for a patient

    This function receives a patient id a input and included it
    in it's GET request. This GET request returns a list of filenames
    that correspond to medical images. This list of filenames is returned.
    :param patient_id:
    :return:
    """
    # this will make a request
    r = requests.get(server_name + "/" + patient_id + "/medical_image_list")
    return r.json()


def load_patient_data(patient_id):
    """
    This function returns recent patient data for a specific id

    This function makes a GET request for a specific patient id that
    returns the patient's name, id, most recent heart rate, most
    recent ecg image, and time of the most recent ecg upload.
    :param patient_id: the id number of the patient of interest
    :return: a list containing recent patient information
    """
    # This will make a request
    r = requests.get(server_name+"/"+patient_id+"/load_recent_data")
    return r.json()


def load_ecg_image(patient_id, timestamp):
    """
    This function returns the base64 string for a desired ECG

    This function receives a patient id and timestamp as input,
    and from those two parameters, makes a GET request for a specific
    ECG image. The GET request returns a base64 string which encodes
    an image of a plot of ECG readings over time.
    :param patient_id: the id number of a specific patient
    :param timestamp: the time of interest for a ECG image
    :return: the base64 string encoding a ECG image
    """
    # This will make a request
    r = requests.get(server_name+"/"+patient_id+"/load_ecg_image/"+timestamp)
    return r.text


def load_medical_image(patient_id, filename):
    """
    This function returns a base64 string of a medical image

    This function accepts as inputs the patient id and the filename
    of interest. This function makes a GET request, and if the patient
    of interest has an image stored on the database with the matching
    filename, the base64 string for that medical image will be returned.
    :param patient_id: the id number of the patient of interest
    :param filename: a string that marks a certain image
    :return: the base64 string of the desired filename
    """
    r = requests.get(server_name + "/" + patient_id +
                     "/load_medical_image/" + filename)
    return r.text


def design_window():

    def save_ecg_to_files(ecg_image):
        files = [('All Files', '*.*'),
                 ('PNG', '*.png'),
                 ('JPEG', '*.jpg')]
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if not file:
            return
        image_bytes = base64.b64decode(ecg_image)
        with open(file, "wb") as out_file:
            out_file.write(image_bytes)

    def save_medical_to_files(medical_image):
        files = [('All Files', '*.*'),
                 ('PNG', '*.png'),
                 ('JPEG', '*.jpg')]
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if not file:
            return
        image_bytes = base64.b64decode(medical_image)
        with open(file, "wb") as out_file:
            out_file.write(image_bytes)

    def load_medical():
        tk_image = load_image_for_display("med_image")
        display_past_ecg_value.image = tk_image
        display_past_ecg_value.configure(image=tk_image)

    def load_ecg():
        tk_image = load_image_for_display("temp_image")
        display_past_ecg_value.image = tk_image
        display_past_ecg_value.configure(image=tk_image)

    def load_recent_ecg():
        recent_tk_image = load_image_for_display("recent_image")
        display_ecg_value.image = recent_tk_image
        display_ecg_value.configure(image=recent_tk_image)

    def image_list():
        return get_image_files(patient_choice.get())

    def ecg_list():
        return get_past_ecg_files(patient_choice.get())

    def display_ecg_image():
        # Edit this more
        ecg_image = load_ecg_image(patient_choice.get(),
                                   past_ecg_file.get())
        save_ecg_image(ecg_image)
        past_text = "ECG from {}".format(past_ecg_file.get())
        display_past_ecg_text.configure(text=past_text)
        save_past_ecg_button = ttk.Button(root, text="Save Past ECG Image",
                                          command=lambda:
                                          save_ecg_to_files(ecg_image))
        save_past_ecg_button.grid(column=2, row=6)
        load_ecg()

    def display_recent_ecg_image(ecg_string):
        # Edit this more
        save_recent_ecg_image(ecg_string)
        load_recent_ecg()

    def save_medical_image(medical_image):
        image_bytes = base64.b64decode(medical_image)
        with open("med_image", "wb") as out_file:
            out_file.write(image_bytes)

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
        print(patient_choice.get())
        print(load_image_file.get())
        medical_image = load_medical_image(patient_choice.get(),
                                           load_image_file.get())
        print(medical_image)
        save_medical_image(medical_image)
        text = "Image from {}".format(load_image_file.get())
        display_past_ecg_text.configure(text=text)
        save_image_button = ttk.Button(root, text="Save Medical Image",
                                       command=lambda:
                                       save_medical_to_files(medical_image))
        save_image_button.grid(column=2, row=6)
        load_medical()

    def new_patient():
        reset()
        display_patient_data()

    def display_patient_data():
        patient_data = load_patient_data(patient_choice.get())
        print(patient_data)
        pat_id = patient_data[0]
        pat_name = patient_data[1]
        pat_hr = patient_data[2]
        pat_time = patient_data[3]

        past_ecg_box['values'] = ecg_list()
        load_image_box['values'] = image_list()

        display_patient_id_value.configure(text=pat_id)
        display_patient_name_value.configure(text=pat_name)
        display_patient_hr_value.configure(text=pat_hr)
        display_timestamp_value.configure(text=pat_time)
        display_recent_ecg_image(patient_data[4])
        root.after(20000, display_patient_data)

    def cancel():
        root.destroy()

    def reset():
        nonlocal display_patient_id_value
        nonlocal display_patient_name_value
        nonlocal display_patient_hr_value
        nonlocal display_timestamp_value
        nonlocal display_ecg_value
        nonlocal display_past_ecg_value

        display_patient_id_value.configure(text="")
        display_patient_name_value.configure(text="")
        display_patient_hr_value.configure(text="")
        display_timestamp_value.configure(text="")
        display_past_ecg_text.configure(text="")
        display_ecg_value.grid_remove()
        display_ecg_value = ttk.Label(root)
        display_ecg_value.grid(column=1, row=5)
        display_past_ecg_value.grid_remove()
        display_past_ecg_value = ttk.Label(root)
        display_past_ecg_value.grid(column=2, row=5)
        past_ecg_box['values'] = ""
        past_ecg_file.set("")

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
                                     command=new_patient)
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
    display_patient_id_value.grid(column=1, row=2)

    display_patient_name_value = ttk.Label(root)
    display_patient_name_value.grid(column=1, row=3)

    display_patient_hr_value = ttk.Label(root)
    display_patient_hr_value.grid(column=1, row=4)

    display_ecg_value = ttk.Label(root)
    display_ecg_value.grid(column=1, row=5)

    display_timestamp_value = ttk.Label(root)
    display_timestamp_value.grid(column=1, row=6)

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
    display_past_ecg_value.grid(column=2, row=5)

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
