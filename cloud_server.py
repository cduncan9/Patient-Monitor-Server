from flask import Flask, jsonify, request
from datetime import datetime
import requests
import logging


app = Flask(__name__)


if __name__ == '__main__':
    logging.basicConfig(filename="code_status.log", filemode='w',
                        level=logging.DEBUG)
    app.run()
