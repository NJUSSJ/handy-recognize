from flask import request, render_template, current_app, send_from_directory, jsonify
import requests

from . import api
from app.service.convert import convert_image_to_latex, get_latex_equation
from app.utils import *


@api.route('/ping', methods=['GET'])
def ping():
    return 'Link started!'


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=current_app.config['APP_NAME'], host=current_app.config['HOST'])


@api.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        image_uri = request.json.get('image_uri')
        # print(image_uri)
        if image_uri is None:
            return build_resp(code=-1, msg='Param of <image_uri> (image base64) required.')
        latex = convert_image_to_latex(image_uri)
        # print(latex)
        if latex is None:
            print("null")
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        points = get_latex_equation(latex)
        # print("equation")
        if points is None:
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        # print("build")
        return build_resp(code=0, data={
            'latex': latex,
            'points': points
        })


@api.route('/convertUnity', methods=['POST'])
def convertUnity():
    if request.method == 'POST':
        image_uri = str(request.data.decode())
        # print(image_uri)
        latex = convert_image_to_latex(image_uri)
        # print(latex)
        if latex is None:
            print("null")
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        points = get_latex_equation(latex)
        # print("equation")
        if points is None:
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        # print("build")
        print(len(points))
        return build_resp(code=0, data={
            'latex': latex,
            'points': points
        })


@api.route('/test', methods=['GET'])
def test():
    convert_image_to_latex()
    return 'Converted!'
