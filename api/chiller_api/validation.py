class ValidationError(Exception):

    def __init__(self, msg, code):
        self._msg = msg
        self._code = code

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg
