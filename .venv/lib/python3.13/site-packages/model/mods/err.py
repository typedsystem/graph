from typed.err import TypeErr

class ModelErr(TypeErr):
    pass

class FieldErr(ModelErr):
    def __init__(self, message=None, field=None, **kwargs):
        self.field = field
        super().__init__(message=message, term=field, **kwargs)
