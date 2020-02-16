import json
import os

import flask
from flask import request, jsonify, send_from_directory
import parser
from werkzeug.utils import secure_filename

import assembler
import table_info_parser
import utils
from app import app
from models import *

import configuration

import connection

ALLOWED_EXTENSIONS = set(['xlsx'])
app.config['JSON_AS_ASCII'] = False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/v1/upload_file", methods=['GET', 'POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    if file and allowed_file(file.filename):
        print(file.filename)
        filename = "{}.xlsx".format(utils.generate_token(8))
        # file_model = TableFile(filename=filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': 'File successfully uploaded', 'file_id': filename})
        resp.status_code = 201
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are xlsx'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route("/api/v1/parse/<path:file>", methods=['POST'])
def parse(file):
    print(request.form)
    parser_class = parser.Parser(file, request.form)
    assembler_class = assembler.Yml("Test", "Колхоз им. Ленина", parser_class, "data/files/{}.yml".format(str(file).split('.')))
    assembler_class.assemble()
    filename = "{}.yml".format(str(file).split('.'))
    resp = jsonify({'message': 'Successfully converted', 'file_id': filename})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/api/v1/get_required_props", methods=['GET'])
def get_required_props():
    required_props = open("data/static_files/required_props.json", "r", encoding="utf_8").read()
    resp = flask.Response(required_props)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/api/v1/get_table_header/<path:filename>", methods=['GET'])
def get_table_header(filename):
    tip = table_info_parser.TableInfoParser("data/files/{}".format(filename))
    header = tip.get_header()
    resp = flask.Response(header)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/api/v1/get_random_row/<path:filename>", methods=['GET'])
def get_random_row(filename):
    tip = table_info_parser.TableInfoParser("data/files/{}".format(filename))
    row = tip.get_random_row()
    print(row)
    resp = jsonify(row)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/api/v1/download/<path:filename>", methods=['GET'])
def download(filename):
    uploads = "data/files/"
    resp = flask.Response(send_from_directory(directory=uploads, filename=filename))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    app.run()

if __name__ == '__main__':
    app.run(configuration.Configuration.host, configuration.Configuration.port)
