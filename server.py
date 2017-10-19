import re
import select
import socket
import subprocess
import sys
from multiprocessing import Value
import json
import base64
import requests

from flask import Flask, abort
from flask import jsonify
from flask import render_template
from flask import request,send_from_directory
from flask_cors import CORS

import json
import config as conf
import jsonpickle
import controller.helpers 

from controller.chatbot_controller import chatbot_api
from controller.churn_controller import churn_api
from controller.emotion_controller import emotion_api
from controller.argumentation_controller import argumentation_api
from controller.grocery_controller import grocery_api
from controller.kp_extraction_controller import kp_extraction_api
from controller.machine_translation_controller import machine_translation_api
from controller.gsw_controller import gsw_api
from controller.ner_controller import ner_api
from controller.neural_programmer_controller import neural_programmer_api
from controller.opinion_target_controller import opinion_target_api
from controller.sfid_controller import sfid_api
from controller.slot_filling_controller import slot_filling_api
from controller.summary_controller import summary_api


app = Flask(__name__)
CORS(app)

app.register_blueprint(chatbot_api, url_prefix='/chatbot')
app.register_blueprint(neural_programmer_api, url_prefix='/neural_programmer')
app.register_blueprint(opinion_target_api, url_prefix='/opinion_target')
app.register_blueprint(churn_api, url_prefix='/churn')
app.register_blueprint(ner_api, url_prefix='/ner')
app.register_blueprint(kp_extraction_api, url_prefix='/kp')
app.register_blueprint(summary_api, url_prefix='/summary')
app.register_blueprint(machine_translation_api, url_prefix='/translate')
app.register_blueprint(gsw_api, url_prefix='/gsw')
app.register_blueprint(argumentation_api, url_prefix='/argumentation')
app.register_blueprint(slot_filling_api, url_prefix='/slot_filling')
app.register_blueprint(sfid_api, url_prefix='/sfid')
app.register_blueprint(grocery_api, url_prefix='/grocery')
app.register_blueprint(emotion_api, url_prefix='/emotion')


if __name__ == '__main__':
    app.run(host='127.0.0.1')
