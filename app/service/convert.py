import base64
import json

import requests
from flask import current_app
from latex2sympy_custom4.process_latex import process_sympy
from sympy import Add
import sympy


def convert_image_to_latex(image_uri=None):
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
            return None
        if 'data' not in resp_data.keys():
            return None
        for item in resp_data['data']:
            t, v = item['type'], item['value']
            if t == 'latex':
                return v
    return None


def get_latex_equation(latex_text):
    try:
        return _calculate(latex_text)
    except Exception as e:
        print(e)
        return None


def _calculate(latex_text=None):
    step = 0.1
    range_bottom = -5
    range_ceil = 5
    sympy_expr = process_sympy(latex_text)
    f = sympy_expr.rewrite(Add)
    x = sympy.symbols('x')
    y = sympy.symbols('y')
    funcs = sympy.solve(f, y)
    print(funcs)
    res = []
    flag = 0
    for func in funcs:
        if flag == 0:
            pointer = range_bottom
            while pointer < range_ceil:
                pointer = round(pointer, 2)
                if func.evalf(subs={x: pointer}).is_real:
                    res.append([str(pointer), str(round(func.evalf(subs={x: pointer}), 5))])
                pointer += step
            flag += 1
        else:
            pointer = range_ceil
            while pointer >= range_bottom:
                pointer = round(pointer, 2)
                if func.evalf(subs={x: pointer}).is_real:
                    res.append([str(pointer), str(round(func.evalf(subs={x: pointer}), 5))])
                pointer -= step
            flag -= 1
    print(res)
    return res
    ## return sympy_expr.evalf()


if __name__ == '__main__':
    inputLatex = 'x^2 + y^2 = 1'
    _calculate(inputLatex)
