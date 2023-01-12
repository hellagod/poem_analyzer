import logging
from functools import wraps

from flask import jsonify

from .error import ErrorHandling


def in_out_wrap(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            data, code = function(*args, **kwargs)
        except Exception as e:
            logging.excepton(e)
            data, code = ErrorHandling.interior_error(e.args[0])
        finally:
            response = jsonify(data)
            response.status_code = code
            return response
    return wrap
