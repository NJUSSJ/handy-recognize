import base64
import json

import requests
from flask import current_app
from latex2sympy_custom4.process_latex import process_sympy
from sympy import Add
import sympy
import math
import datetime


def convert_image_to_latex(image_uri=None):
    start = datetime.datetime.now()
    if image_uri is None:
        # test mode
        file_path = '../../tmp/test3.jpg'
        image_uri = base64.b64encode(open(file_path, 'rb').read()).decode()
        f = open('image_base64.txt', 'w')
        f.write(image_uri)
        f.close()

    with open('.tmp/test4.jpg', 'wb') as file:
        file.write(base64.b64decode(image_uri))
    image_uri = "data:image/jpg;base64," + image_uri
    resp = requests.post(
        url=current_app.config['MATHPIX_API'],
        data=json.dumps({
            'src': image_uri,
            'formats': ['text', 'data'],
            'data_options': {
                'include_latex': True,
                'include_asciimath': True
            }
        }),
        headers={
            'app_id': current_app.config['MATHPIX_APP_ID'],
            'app_key': current_app.config['MATHPIX_APP_KEY'],
            'Content-type': 'application/json'
        }
    )
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        if 'confidence' not in resp_data.keys() or resp_data['confidence'] < current_app.config[
            'MATHPIX_CONFIDENCE_THRESHOLD']:
            end = datetime.datetime.now()
            end = datetime.datetime.now()
            print('recognize time: ' + str((end - start).microseconds) + ' us')
            return None
        if 'data' not in resp_data.keys():
            end = datetime.datetime.now()
            end = datetime.datetime.now()
            print('recognize time: ' + str((end - start).microseconds) + ' us')
            return None
        for item in resp_data['data']:
            t, v = item['type'], item['value']
            if t == 'latex':
                end = datetime.datetime.now()
                print('recognize time: ' + str((end - start).microseconds) + ' us')
                return v
    end = datetime.datetime.now()
    print('recognize time: ' + str((end - start).microseconds) + ' us')
    return None


def get_latex_equation(latex_text):
    try:
        return _calculate(latex_text)
    except Exception as e:
        print(e)
        return None


def _calculate(latex_text=None):
    start = datetime.datetime.now()
    print(latex_text)
    range_bottom = -5
    range_ceil = 5
    sympy_expr = process_sympy(latex_text)
    f = sympy_expr.rewrite(Add)
    y = sympy.symbols('y')
    funcs = sympy.solve(f, y)
    print(funcs)
    res = []
    if len(funcs) == 1:
        res = calculate_in_cartesian(funcs, range_bottom, range_ceil)
    elif len(funcs) == 2:
        res = calculate_in_polar(funcs, range_bottom, range_ceil)
    end = datetime.datetime.now()
    print('calculate time: ' + str((end - start).microseconds) + ' us')
    return res
    # return sympy_expr.evalf()


def calculate_in_cartesian(funcs, range_bottom, range_ceil, step=0.1):
    x = sympy.symbols('x')
    res = []
    func = funcs[0]
    pointer = range_bottom
    while pointer <= range_ceil:
        pointer = round(pointer, 2)

        # deal with divide 0
        if pointer == 0:
            pointer += step
            continue
        if func.evalf(subs={x: pointer}).is_real:
            res.append([str(pointer), str(round(func.evalf(subs={x: pointer}), 5))])
        pointer += step
    return res


def calculate_in_polar(funcs, range_bottom, range_ceil, step=9):
    x = sympy.symbols('x')
    y = sympy.symbols('y')
    res = []
    for func in funcs:
        pointer = 0.00001
        while pointer <= 180:
            pointer = round(pointer, 5)
            radius = (math.pi / 180) * pointer
            k = math.tan(radius)
            if radius == 0.5:
                k = 0
            f1 = y - k * x
            f2 = y - func
            point = sympy.solve([f1, f2], [x, y])
            point_list = list(point[0])
            point_list[0] = str(round(point_list[0], 5))
            point_list[1] = str(round(point_list[1], 5))
            res.append(point_list)
            pointer += step
    res.append(res[0])
    return res


if __name__ == '__main__':
    inputLatex = 'y=1/x'
    _calculate(inputLatex)
