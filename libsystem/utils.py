import json
from .exceptions import *

def get_and_validate(params, required_keys=[]):
    keys=params.keys()
    for key in required_keys:
        if key not in keys:
            raise ValidationError("Required Key Missing : " + key)
        if not params.get(key):
            raise FieldBlank(key + " can not be blank")

def validateJSON(meta_data):
    try:
        json.loads(meta_data)
    except:
        return False
    return True