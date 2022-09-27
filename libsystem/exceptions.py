class ValidationError(Exception):
    pass

class ObjectDoesNotExist(Exception):
    pass

class JSONError(Exception):
    pass

class PublisherError(Exception):
    pass

class PublisherDoesNotExist(Exception):
    pass

class LanguageError(Exception):
    pass

class LanguageDoesNotExist(Exception):
    pass

class AuthorError(Exception):
    pass

class AuthorDoesNotExist(Exception):
    pass

class BookDoesNotExist(Exception):
    pass

class BookError(Exception):
    pass

class ObjectAlreadyExist(Exception):
    pass

class FieldBlank(Exception):
    pass