from flask import Flask, jsonify, request
from datetime import datetime
import requests
import logging
from pymodm import connect, MongoModel, fields


app = Flask(__name__)


class NewPatient(MongoModel):
    patient_id = fields.IntegerField()
    patient_name = fields.CharField()
    heart_rate = fields.ListField()
    timestamp = fields.ListField()
    ecg_images = fields.ListField()
    medical_images = fields.ListField()


if __name__ == '__main__':
    logging.basicConfig(filename="code_status.log", filemode='w',
                        level=logging.DEBUG)
    app.run()
