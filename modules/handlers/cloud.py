import http.client
from flask import request
from modules.code.lex_rank import generate_title_with_probabilities


def get_cloud_data():
    print(request.json)
    data = generate_title_with_probabilities(request.json[0])
    print(data)
    return {'data': data}, http.client.OK
