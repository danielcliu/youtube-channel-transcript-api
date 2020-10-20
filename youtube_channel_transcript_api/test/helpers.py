import json
import os
from requests import Response


def make_response(filename, status_code = 200):
    res = Response()
    res.status_code = status_code
    res.header = None
    res.encoding = 'utf-8'
    json_loaded = load_json(filename)
    res._content = json.dumps(json_loaded).encode('utf-8')
    return res

def load_json(filename):
    with open('{dirname}/test_responses/{filename}'.format(dirname=os.path.dirname(__file__), filename=filename)) as jsonfile:
        return json.load(jsonfile)
