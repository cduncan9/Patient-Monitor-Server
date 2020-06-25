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
    """
    This is the main function that controls the GUI

    This function contains all of the code important in the GUI display
    and the feedback given to the user. This function includes several
    sub-functions which are responsible for the the loading, converting,
    and saving of data. This GUI is capable of sending and receiving input,
    and this GUI can display ECG and medical images. This GUI uses a grid
    structure for organization.
    :return:
    """

    def save_ecg_to_files(ecg_image):
        """
        This function saves an ECG image to a local computer

        This function receives a base64 string as input which encodes
        an image of an ECG dataset. First, this function uses the
        asksaveasfile() command to let the user open up a file dialog box
        and select a file location and name that they desire. Then this
        function decodes the base64 string into an image format suitable
        for storage as an image file. Lastly this function opens the file
        specified earlier, and writes out the image data into the file.
        :param ecg_image: a base64 string encoding an image
        :return:
        """
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
        """
        This function saves a medical image to a local computer

        This function receives a base64 string as input which encodes
        a medical image. First, this function uses the
        asksaveasfile() command to let the user open up a file dialog box
        and select a file location and name that they desire. Then this
        function decodes the base64 string into an image format suitable
        for storage as an image file. Lastly this function opens the file
        specified earlier, and writes out the image data into the file.
        :param medical_image: a base64 string encoding an image
        :return:
                """
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
        """
        This function stores the tk image object as an image
        variable of the Label widget

        Sometimes when assigning images to Labels in tkinter
        you run into the problem of the python memory manager
        erasing images that are not directly stored to anything.
        To get around this, this function gets the tk image
        object from the function load_image_for_display() and
        it assigns the .image component of the
        display_past_ecg_value to be the tk image object.
        This function then configures the Label to have the
        tk image object as a parameter linked to the label, so
        that the python memory manager does not get rid of it.
        :return:
        """
        tk_image = load_image_for_display("med_image")
        display_past_ecg_value.image = tk_image
        display_past_ecg_value.configure(image=tk_image)

    def load_ecg():
        """
        This function stores the tk image object as an image
        variable of the Label widget

        Sometimes when assigning images to Labels in tkinter
        you run into the problem of the python memory manager
        erasing images that are not directly stored to anything.
        To get around this, this function gets the tk image
        object from the function load_image_for_display() and
        it assigns the .image component of the
        display_past_ecg_value to be the tk image object.
        This function then configures the Label to have the
        tk image object as a parameter linked to the label, so
        that the python memory manager does not get rid of it.
        :return:
        """
        tk_image = load_image_for_display("temp_image")
        display_past_ecg_value.image = tk_image
        display_past_ecg_value.configure(image=tk_image)

    def load_recent_ecg():
        """
        This function stores the tk image object as an image
        variable of the Label widget

        Sometimes when assigning images to Labels in tkinter
        you run into the problem of the python memory manager
        erasing images that are not directly stored to anything.
        To get around this, this function gets the tk image
        object from the function load_image_for_display() and
        it assigns the .image component of the
        display_ecg_value to be the tk image object.
        This function then configures the Label to have the
        tk image object as a parameter linked to the label, so
        that the python memory manager does not get rid of it.
        :return:
        """
        recent_tk_image = load_image_for_display("recent_image")
        display_ecg_value.image = recent_tk_image
        display_ecg_value.configure(image=recent_tk_image)

    def image_list():
        """
        This function calls get_image_files() and sends it
        the patient_choice which is the chosen patient id.

        get_image_files() is the function that returns a list
        of medical image filenames, so this function is essentially a middle
        step in sending the patient id to the GET request function
        so that a list of medical image filenames can populate
        the medical image combobox
        :return: a list of medical image files for a patient id
        """
        return get_image_files(patient_choice.get())

    def ecg_list():
        """
        This function returns a list of ECG times for a patient

        This function is called to populate the ComboBox of ECG
        times. This function sends the patient id to the function
        get_past_ecg_files() which then returns a list of times
        that correspond to ECG scans.
        :return: a list of times that correspond to ECG scans
        """
        return get_past_ecg_files(patient_choice.get())

    def display_ecg_image():
        """
        This function retrieves a base64 string for an ECG image
        and sends it to be displayed in the GUI

        This is the main function that calls other functions in order to
        produce an ECG image in the GUI. First, this function sends the
        patient id and the desired time to the function load_ecg_image(),
        which returns a base 64 string encoding the desired ECG image. Then
        this function calls the save_ecg_image() function which saves the ECG
        image in a file so that the load_ecg() function can display the image
        from the file. This function also creates a Label that makes the time
        of the ECG image displayed on the GUI and it displays the button that
        is used to save the ecg image.
        :return:
        """
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
        """
        This function calls other functions together to produce an ecg image

        This function receives a base64 string as input that encodes a desired
        ecg image. This function then calls save_recent_ecg_image() which
        saves the base64 string to a file so that it can be loaded by the
        function load_recent_ecg()
        :param ecg_string: a base64 string containing a desired ECG image
        :return:
        """
        # Edit this more
        save_recent_ecg_image(ecg_string)
        load_recent_ecg()

    def save_medical_image(medical_image):
        """
        This function saves base64 string of a medical image to
        a temporary file

        This function receives a base64 string containing an encoded
        medical image and decodes that image into a format suitable for
        image files. This is then saved into a temporary file called
        med_image using a with command.
        :param medical_image: a base64 string containing a medical image
        :return:
        """
        image_bytes = base64.b64decode(medical_image)
        with open("med_image", "wb") as out_file:
            out_file.write(image_bytes)

    def save_ecg_image(ecg_image):
        """
        This function saves base64 string of an ecg image to
        a temporary file

        This function receives a base64 string containing an encoded
        ecg image and decodes that image into a format suitable for
        image files. This is then saved into a temporary file called
        temp_image using a with command.
        :param ecg_image: a base64 string containing an ecg image
        :return:
        """
        image_bytes = base64.b64decode(ecg_image)
        with open("temp_image", "wb") as out_file:
            out_file.write(image_bytes)

    def save_recent_ecg_image(ecg_image):
        """
        This function saves base64 string of an ecg image to
        a temporary file

        This function receives a base64 string containing an encoded
        ecg image and decodes that image into a format suitable for
        image files. This is then saved into a temporary file called
        recent_image using a with command.
        :param ecg_image: a base64 string containing an ecg image
        :return:
        """
        image_bytes = base64.b64decode(ecg_image)
        with open("recent_image", "wb") as out_file:
            out_file.write(image_bytes)

    def display_medical_image():
        """
        This function retrieves a base64 string for a medical image
        and sends it to be displayed in the GUI

        This is the main function that calls other functions in order to
        produce a medical image in the GUI. First, this function sends the
        patient id and a filename to the function load_medical_image(),
        which returns a base64 string encoding the medical image. Then
        this function calls the save_medical_image() function which saves the
        image in a file so that the load_medical() function can display the
        image from the file. This function also creates a Label that makes
        the filename of the image displayed on the GUI and it displays the
        button that is used to save the image.
        :return:
        """
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
        """
        This function resets the GUI and calls to display a patient's data

        This function is called whenever a new patient id is selected and
        loaded on the GUI. This function first calls the reset() function
        which clears the GUI, then is calls the function display_patient_data
        which gets the most recent name, heart rate, timestamp, and ecg
        image for a patient id.
        :return:
        """
        reset()
        display_patient_data()

    def display_patient_data():
        """
        This function is responsible for displaying the most recent patient
        data for a specific patient id.

        This function first calls the function load_patient_data() and sends
        it the id of the patient that was chosen. load_patient_data() returns
        that patient's id, name, most recent heart rate, most recent ecg
        image,and the time of the most recent
        upload. Then all of these returned
        parameters are assigned to their corresponding Label in the GUI. Then
        the comboboxes for the ecg images and the medical images are populated
        by calling the functions ecg_list() and image_list() respectively.
        finally the command root.after() is used so that this function is
        called again every 20 seconds, updating the most recent patient data.
        :return:
        """
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
        """
        This function closes the main window
        :return:
        """
        root.destroy()

    def reset():
        """
        This function is responsible for clearing the GUI

        This function first assigns some Labels which were declared outside
        of it's scope as nonlocal. Then, for all of the Labels that display
        text, this function changes their text to be empty strings. After
        that, this function removes the images from the grid and then
        re-assigns them to the grid, so that the Labels can be used again
        in the future.
        :return:
        """
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
