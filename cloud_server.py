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


def check_patient_exists(patient_id):
    try:
        db_item = NewPatient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return True


def add_patient_to_db(info):
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
    return patient.patient_id


def init_db():
    print("Connecting to database...")
    connect("mongodb+srv://cduncan9:BME547@cluster0.conjj.mongodb.net/"
            "finalproject?retryWrites=true&w=majority")
    print("Database connected.")


# Route functions should be placed below this line
@app.route("/api/new_patient", methods=['POST'])
def add_patient():
    in_data = request.get_json()
    # Should we verify this input?
    name = add_patient_to_db(in_data)
    return "Patient added", 200


@app.route("/patient_id_list", methods=['GET'])
def get_patient_id_list():
    ret = list()
    for patient in NewPatient.objects.raw({}):
        ret.append(patient.patient_id)
    return ret


@app.route("/<patient_id>/ecg_image_list", methods=['GET'])
def get_ecg_image_list(patient_id):
    # Verify that the patient_id exists
    return


@app.route("/<patient_id>/medical_image_list", methods=['GET'])
def get_medical_image_list(patient_id):
    # Verify that the patient_id exists
    return


@app.route("/<patient_id>/load_recent_data", methods=['GET'])
def load_recent_patient_data(patient_id):
    # Verify that the patient_id exists
    return


@app.route("/<patient_id>/load_ecg_image/<ecg_image>", methods=['GET'])
def load_ecg_image(patient_id, ecg_image):
    # Verify that the patient_id exists
    return


@app.route("/<patient_id>/load_medical_image/<medical_image>", methods=['GET'])
def load_medical_image(patient_id, medical_image):
    # Verify that the patient_id exists
    return


if __name__ == '__main__':
    logging.basicConfig(filename="code_status.log", filemode='w',
                        level=logging.DEBUG)
    init_db()
    app.run()
