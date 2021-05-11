from flask import request

from app.service.convert import convert_image_to_latex, calculate_points_set
from app.service.transform import transform as transform_latex
from app.utils import *
from . import api
import datetime
from app.service.latex2image import latex2image


@api.route('/convertUnity', methods=['POST'])
def convertUnity():
    if request.method == 'POST':
        image_uri = str(request.data.decode())
        latex = convert_image_to_latex(image_uri)
        if latex is None:
            print("null")
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        print('recognize result: ' + latex)
        if '\\rightarrow' not in latex and '\\longrightarrow' not in latex:
            points = calculate_points_set(latex)
        else:
            points = []
        # latex_image = latex2image(latex)
        return build_resp(code=0, data={
            'latex': latex,
            'points': points,
            # 'image': latex_image
        })


@api.route('/recognize', methods=['POST'])
def recognize():
    json_data = request.form
    image = str(json_data['image'])
    latex = convert_image_to_latex(image)
    if latex is None:
        print("null")
        return build_resp(code=-1, msg='The provided text can not be recognized.')
    print('recognize result: ' + latex)
    # latex_image = latex2image(latex)
    return build_resp(code=0, data={
        'latex': latex,
        # 'image': latex_image
    })


@api.route('/getDataSet', methods=['POST'])
def getDataSet():
    json_data = request.form
    latex = str(json_data['latex'])
    if '\\rightarrow' not in latex and '\\longrightarrow' not in latex:
        points = calculate_points_set(latex)
    return build_resp(code=0, data={
        'points': points
    })


@api.route('/transform', methods=['POST'])
def transform():
    json_data = request.form
    transform_content = str(json_data["transform_content"])
    latex = str(json_data["latex"])
    result_latex = transform_latex(latex, transform_content)
    print('transform result: ' + result_latex)
    points = calculate_points_set(result_latex)
    if points is None:
        return build_resp(code=-1, msg='transform failed.')
    # latex_image = latex2image(result_latex)
    return build_resp(code=0, data={
        'latex': result_latex,
        'points': points,
        # 'image': latex_image
    })


@api.route('/test', methods=['GET'])
def test():
    convert_image_to_latex()
    return 'Converted!'


@api.route('/phieldTest', methods=['GET'])
def phieldTest():
    data = request.form
    image_data = str(data["image"])
    start = datetime.datetime.now()
    latex = convert_image_to_latex(image_data)
    end = datetime.datetime.now()
    print('recognize time: ' + str((end - start).seconds) + ' s')
    if latex is None:
        print("null")
        return build_resp(code=-1, msg='The provided text can not be recognized.')
    print('recognize result: ' + latex)
    return build_resp(code=0, data={
        'latex': latex
    })
