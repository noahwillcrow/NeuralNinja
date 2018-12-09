from api.responsemodels.baseresponse import SuccessResponse

"""
Used for testing
"""
class TestResponse(SuccessResponse):
    def __init__(self, is_even):
        SuccessResponse.__init__(self)
        self.data["isEven"] = is_even