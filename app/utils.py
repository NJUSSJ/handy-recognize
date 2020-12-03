import math
import json


def convert_file_size_to_mb(size_bytes):
    return math.ceil(size_bytes / math.pow(1024, 2))


def build_resp(code=0, msg='', data=None):
    result_dict = {}
    if data is not None:
        result_dict = {'code': 0, 'data': data}
    else:
        result_dict = {'code': code, 'msg': msg}
    return json.dumps(result_dict)
