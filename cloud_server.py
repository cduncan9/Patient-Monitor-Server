from flask import Flask, jsonify, request
from datetime import datetime
import requests
import logging
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors


app = Flask(__name__)


class NewPatient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    heart_rate = fields.ListField()
    timestamp = fields.ListField()
    ecg_images = fields.ListField()
    medical_images = fields.ListField()


def init_db():
    """
    This function is responsible for connecting to the MongoDB database

    This function is used to connect to MongoDB. It has several print
    statements which are used as user feedback to the terminal and it
    connects to the address of the MongoDB database 'finalproject' that
    was used in this database.
    :return:
    """
    print("Connecting to database...")
    connect("mongodb+srv://cduncan9:BME547@cluster0.conjj.mongodb.net/"
            "finalproject?retryWrites=true&w=majority")
    print("Database connected.")


def check_patient_exists(patient_id):
    """
    This function checks to see if a patient id is in the database

    This function receives a patient_id as input and uses a try-except
    statement to check whether the given id is in the database. This
    function first tries to make a query for an object with the
    given patient_id. If a DoesNotExist arises then the function
    returns False, but if it successfully completes the query the
    function returns True
    :param patient_id: a number potentially identifying a patient
    :return: True if the patient exist or False if the patient is
    not in the database
    """
    try:
        db_item = NewPatient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return True


def append_to_patient(info):
    """
    This function appends patient data to an already existing patient

    This function is called if a patient already exists in a database.
    The function first makes a query to get the object that stores
    the patient info. Then if the name assigned to the patient id is
    different to what was sent in the input, then the name is switched
    to the name given in the input list. After that, any of the other
    elements in the list that have lengths greater than 0 are appended
    to their respective parameters. The object is then saved back to
    the database.
    :param info: a list containing patient data to be added to a
    patient object
    :return: True if the data was added
    """
    patient_id = int(info[0])
    patient = NewPatient.objects.raw({"_id": patient_id}).first()
    if patient.patient_name != info[1]:
        patient.patient_name = info[1]
    if len(info[2]) > 0:
        patient.heart_rate.append(info[2][0])
    if len(info[3]) > 0:
        patient.timestamp.append(info[3][0])
    if len(info[4]) > 0:
        patient.ecg_images.append(info[4][0])
    if len(info[5]) > 0:
        patient.medical_images.append(info[5][0])
    patient.save()
    return True


def add_new_patient(info):
    """
    This function adds a new patient to the database

    This function is called when it's patient id is not already in
    the database. This function first makes a object from the
    NewPatient class and assigns the patient id and name to it. Then,
    if any of the other data in the list has a length that is greater
    than 0, it is added to it's parameter. The NewPatient object is
    then saved to the database.
    :param info: a list containing patient data to be added to a
    patient object
    :return: True if the data was added
    """
    patient = NewPatient(patient_id=info[0],
                         patient_name=info[1])
    if len(info[2]) > 0:
        patient.heart_rate = info[2]
    if len(info[3]) > 0:
        patient.timestamp = info[3]
    if len(info[4]) > 0:
        patient.ecg_images = info[4]
    if len(info[5]) > 0:
        patient.medical_images = info[5]
    patient.save()
    return True


def retrieve_timestamps(patient_id):
    """
    This function gets a list of times that ECG data was uploaded

    This function makes a query to get a NewPatient object from
    the database using a specified patient_id. This function then
    gets the timestamp parameter from the object and returns that
    list of times
    :param patient_id: a number representing a patient in the
    database
    :return: a list of times that ECG data was uploaded
    """
    patient = NewPatient.objects.raw({"_id": patient_id}).first()
    return patient.timestamp


def retrieve_patient_id_list():
    """
    This function gets a list of patient ids

    This function creates an empty list called ret.
    This function then gets all of the objects from the database
    and loops through the objects, storing the patient_ids of
    each object in ret.
    :return: a list of patient_ids in the database
    """
    ret = list()
    for patient in NewPatient.objects.raw({}):
        ret.append(patient.patient_id)
    return ret


def get_ecg_string(patient_id, timestamp):
    """
    This function gets the base64 string of an ecg image for a
    specific time and patient

    This function first gets the object that has the patient_id
    that is specified in the input and gets the list of times that
    are stored in the object. This list of times is then looped through.
    At the index where the time is the same as the time given in the
    input, the string in the ecg list at the same index is returned.
    :param patient_id: a number specifying a patient in the database
    :param timestamp: a time of an ECG upload
    :return: a base64 string containing an ECG image
    """
    patient = NewPatient.objects.raw({"_id": patient_id}).first()
    times = patient.timestamp
    ecg_list = patient.ecg_images
    for i in range(len(times)):
        if times[i] == timestamp:
            return ecg_list[i]
    return ''


def get_latest_data(patient_id):
    """
    This function returns a list of the most recent data for a patient

    This function first makes a query to get the object that has the
    patient_id that it given in the input. Then this function gets the
    patient name, heart rate list, time list, and base64 ecg list. This
    function returns the last value in each list.
    :param patient_id: a number representing a patient
    :return: a list of recent patient data
    """
    patient = NewPatient.objects.raw({"_id": patient_id}).first()
    name = patient.patient_name
    hr = patient.heart_rate
    time = patient.timestamp
    ecg = patient.ecg_images
    return [patient_id, name, hr[-1], time[-1], ecg[-1]]


# Verification functions
def verify_patient_id(patient_id):
    """
    This function is meant to check if the patient id is the right
    format

    This function first checks to see if the patient id is an integer.
    If it is an integer than that number is returned without
    manipulation. If the patient_id is a string then this function checks
    to see if it is a numeric string. If it is then the function converts
    the patient id into an integer and returns it. If the patient id is
    the wrong format, then this function returns false.
    :param patient_id: a number identifying a patient
    :return: either an integer patient id or False
    """
    if type(patient_id) == int:
        return patient_id
    if type(patient_id) == str:
        if patient_id.isdigit():
            return int(patient_id)
    return False


def verify_timestamp_exists(patient_id, timestamp):
    """
    This function verifies that a specific time is in the time list
    for a patient

    This function makes a query to get an object that has the
    same patient_id that what given in the input. Then this
    function checks to see if the timestamp given in the input
    is contained in the list of times stored in the database.
    :param patient_id: a number identifying a patient
    :param timestamp: a given time of ECG upload
    :return: True or False depending on if the time is in the
    database
    """
    patient = NewPatient.objects.raw({"_id": patient_id}).first()
    times = patient.timestamp
    if timestamp in times:
        return True
    return False


def get_file_names(in_list):
    """Makes a list of each index[1] in a list of lists

    This method is deployed in the get_medical_image_list route

    :param in_list: list of lists containing patient medical
                    images and file names
    :return: list containing file names
    """

    temp = list()
    for item in in_list:
        temp.append(item[1])
    return temp


def find_key(in_list, key):
    """In list of lists returns index[0] if index[1] == key

    This method is deployed in the get_medical_image() route
    It find the medical image string for an input file_name (key)

    :param in_list:
    :param key: str containing medical image in base 64
    :return:
    """

    for item in in_list:
        if item[1] == key:
            return item[0]


# Route functions should be placed below this line
@app.route("/api/new_patient", methods=['POST'])
def add_patient():
    """Adds patient to database

    POST request receives patient information from client,
    calls append_to_patient(in_data) if the patient already exists,
    otherwise calls add_new_patient()

    :return: str "Patient added", int 200
    """
    in_data = request.get_json()
    verify_id = verify_patient_id(in_data[0])
    check = check_patient_exists(verify_id)
    if check:
        append_to_patient(in_data)
    else:
        add_new_patient(in_data)
    return "Patient added", 200


@app.route("/patient_id_list", methods=['GET'])
def get_patient_id_list():
    """Retrieves list of patient IDs

    GEt request, Calls retrieve_patient_id_list() and returns the
    list of patient IDs in json format

    :return: json containing list of patient IDs
    """
    return jsonify(retrieve_patient_id_list())


# This is actually getting a list of timestamps
@app.route("/<patient_id>/ecg_image_list", methods=['GET'])
def get_ecg_image_list(patient_id):
    """Retrieves list of ECG images (timestamps)

    GET requests, makes a query for the list of patient
    ECG timestamps from the database

    :param patient_id: int containing patient ID
    :return: json containing list of string timestamps,
             str containing error message if error
    """
    verify_id = verify_patient_id(patient_id)
    if verify_id is False:
        return "{} is not a correct format for patient id".format(patient_id),\
               400
    check = check_patient_exists(verify_id)
    if check is not True:
        return "Patient {} not found".format(verify_id), 400
    return jsonify(retrieve_timestamps(verify_id))


@app.route("/<patient_id>/medical_image_list", methods=['GET'])
def get_medical_image_list(patient_id):
    """Retrieves list of medical images

    Get request, This method makes a query to the database for the
    list of patient medical images. It makes sure the patient exists
    in the database before making the query.

    :param patient_id: int containing patient ID
    :return: json containing patient medical images
             str containing error message otherwise
    """
    patient_id = int(patient_id)
    if check_patient_exists(patient_id):
        patient = NewPatient.objects.raw({"_id": patient_id}).first()
        print(get_file_names(patient.medical_images))
        return jsonify(get_file_names(patient.medical_images))
    return "Patient not found", 400


@app.route("/<patient_id>/load_recent_data", methods=['GET'])
def load_recent_patient_data(patient_id):
    """Loads recent patient data

    If the patient id is verified, makes a query to the database
    for the patients most recent data. This is primarily used
    to update the GUI with most recent files.

    :param patient_id: int containing patient ID
    :return: json containing requested patient data
             str with error message otherwise
    """
    # Verify that the patient_id exists
    verify_id = verify_patient_id(patient_id)
    if verify_id is False:
        return "{} is not a correct format for patient id".format(patient_id),\
               400
    check = check_patient_exists(verify_id)
    if check is not True:
        return "Patient {} not found".format(verify_id), 400
    data = get_latest_data(verify_id)
    return jsonify(data)


@app.route("/<patient_id>/load_ecg_image/<timestamp>", methods=['GET'])
def load_ecg_image(patient_id, timestamp):
    """Loads individual ECG image

    GET request, queries database for a specific ECG image
    identified by the input timestamp string

    :param patient_id: int containing patient ID
    :param timestamp: str containing timestamp
    :return: str containing b64 ECG image
    """
    # Verify that the patient_id exists
    verify_id = verify_patient_id(patient_id)
    if verify_id is False:
        return "{} is not a correct format for patient id".format(patient_id),\
               400
    check = check_patient_exists(verify_id)
    if check is not True:
        return "Patient {} not found".format(verify_id), 400
    verify_timestamp = verify_timestamp_exists(verify_id,
                                               timestamp)
    if verify_timestamp is False:
        return "timestamp not found", 400
    ecg_string = get_ecg_string(verify_id, timestamp)
    return ecg_string


@app.route("/<patient_id>/load_medical_image/<medical_image>", methods=['GET'])
def load_medical_image(patient_id, medical_image):
    """Loads specified medical image

    GET request, queries the server for a specific medical image specified
    by the input medical image name.

    :param patient_id: int containing patient ID
    :param medical_image: str containing medical image file name
    :return: json containing str of base 64 medical image
    """
    patient_id = int(patient_id)
    if check_patient_exists(patient_id):
        patient = NewPatient.objects.raw({"_id": patient_id}).first()
        print(find_key(patient.medical_images, medical_image))
        return jsonify(find_key(patient.medical_images, medical_image))
    return "Image not found", 400


if __name__ == '__main__':
    logging.basicConfig(filename="code_status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
