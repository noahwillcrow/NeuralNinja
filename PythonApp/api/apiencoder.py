import json

"""
Encodes responses into JSON strings
"""
class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        else:
            json.JSONEncoder.default(self, obj)