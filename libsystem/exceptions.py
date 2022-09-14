from .responses import *

class ValidationError(Exception):
    pass

class ObjectDoesNotExist(Exception):
    pass

class JSONError(Exception):
    pass