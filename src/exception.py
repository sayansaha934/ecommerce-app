class OrderValidationError(Exception):
    code =409
    message = None

    def __init__(self, message):
        self.message = message

class ProductNameDuplicateError(Exception):
    code =409
    message = None

    def __init__(self, message):
        self.message = message