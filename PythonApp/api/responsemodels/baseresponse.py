import json

from api.apiencoder import ResponseEncoder
import api.apicache as apicache

"""
Just a standard response with a data object
"""
class BaseResponse():
    def __init__(self):
        self.data = {}

    def __str__(self):
        return json.dumps(self.data, cls=ResponseEncoder)

"""
An extension of the base response but with statusCode = 0
"""
class SuccessResponse(BaseResponse):
    def __init__(self):
        BaseResponse.__init__(self)
        self.data["statusCode"] = 0

"""
An extension of the base response but with a statusCode and errorMessage
"""
class FailureResponse(BaseResponse):
    def __init__(self, error_message, status_code=1):
        BaseResponse.__init__(self)
        self.data["statusCode"] = status_code
        self.data["errorMessage"] = error_message

"""
An extension of the success response but with a network
"""
class NetworkChangeSuccessResponse(SuccessResponse):
    def __init__(self):
        SuccessResponse.__init__(self)
        self.data["network"] = apicache.current_network
