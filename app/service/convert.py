import json

import requests
from flask import current_app
from latex2sympy_custom4.process_latex import process_sympy
import sympy
import math
import datetime


def convert_image_to_latex(image_uri=None):
    # with open('static/test4.png', 'wb') as file:
    #     file.write(base64.b64decode(image_uri))
    start = datetime.datetime.now()

    res = None
    image_uri = "data:image/png;base64," + image_uri
    resp = requests.post(
        url=current_app.config['MATHPIX_API'],
        data=json.dumps({
            'src': image_uri,
            'formats': ['text', 'data', 'html'],
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
            res = None
        if 'data' not in resp_data.keys():
            res = None
        for item in resp_data['data']:
            t, v = item['type'], item['value']
            if t == 'latex':
                res = v
    end = datetime.datetime.now()
    print('recognize time: ' + str((end - start).seconds) + ' s\n')
    return res


def calculate_points_set(latex_text=None):
    start = datetime.datetime.now()
    latex_text = latex_text.replace('\\left', '').replace('\\right', '')
    range_bottom = -5
    range_ceil = 5
    try:
        sympy_expr = process_sympy(latex_text)
    except:
        return []
    y = sympy.symbols('y')
    funcs = sympy.solve(sympy_expr, y)
    print(funcs)

    res = []
    if len(funcs) == 1:
        res = _calculate_in_cartesian(funcs, range_bottom, range_ceil)
    elif len(funcs) == 2:
        res = _calculate_in_polar(sympy_expr, range_bottom, range_ceil)

    end = datetime.datetime.now()
    print('calculate time: ' + str((end - start).seconds) + ' s\n')
    return res


def _calculate_in_cartesian(funcs, range_bottom, range_ceil, step=0.1):
    # 在笛卡尔坐标系中计算点集
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
        if func.evalf(subs={x: pointer, 'pi': math.pi}).is_real:
            res.append([str(pointer), str(round(func.evalf(subs={x: pointer, 'pi': math.pi}), 5))])
        else:
            print(func.evalf(subs={x: pointer, 'pi': math.pi}))
        pointer += step
    return res


def _calculate_in_polar(func, range_bottom, range_ceil, step=9):
    # 极坐标中求解点集
    res = []
    res1 = []

    pointer = 180
    while pointer >= 0:
        points = _calculateUnionFunction(pointer, func)
        res.append(points[0] if pointer > 90 else points[1])
        res1.append(points[1] if pointer > 90 else points[0])
        pointer -= step
    res.extend(res1)
    return res


def _calculateUnionFunction(pointer, func):
    x = sympy.symbols('x')
    y = sympy.symbols('y')
    pointer = round(pointer, 5)
    radius = (math.pi / 180) * pointer
    # 直线斜率k
    k = math.tan(radius)
    if radius == 0.5:
        k = 0
    f1 = y - k * x
    f2 = func

    # 联立直线和方程求解交点
    points = sympy.solve([f1, f2], [x, y])
    res = []

    for point in points:
        point = list(point)
        point[0] = str(round(point[0], 5))
        point[1] = str(round(point[1], 5))
        res.append(point)
    return res


if __name__ == '__main__':
    latex = 'x^2 + y^2 = 1'
    data_set = calculate_points_set(latex)
    print(data_set)
