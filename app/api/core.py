from flask import request

from app.service.convert import convert_image_to_latex, calculate_points_set
from app.utils import *
from . import api


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
        points = calculate_points_set(latex)
        # print("equation")
        if points is None:
            return build_resp(code=-1, msg='The provided text can not be recognized.')
        # print("build")
        # print(len(points))
        return build_resp(code=0, data={
            'latex': latex,
            'points': points
        })


@api.route('/test', methods=['GET'])
def test():
    convert_image_to_latex()
    return 'Converted!'
