from werkzeug.http import HTTP_STATUS_CODES


class ErrorHandling:

    @classmethod
    def bad_request(cls, message=''):
        return cls.error_response(400, message)
    
    @classmethod
    def internal_error(cls, message=''):
        return cls.error_response(500, message)
    
    @staticmethod
    def error_response(status_code, message=''):
        payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'), 'message': message,
                   'status_code': status_code}
        return payload, status_code
