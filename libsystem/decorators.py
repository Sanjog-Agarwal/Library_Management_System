import json
from .exceptions import *
class Validate_JSON(object):
    def __init__(self,params):
        if not params:
            params=list()
        self.params = params

    def validateJSON(self, meta_data):
        try:
            if meta_data and not json.loads(meta_data):
                raise JSONError
        except:
            pass