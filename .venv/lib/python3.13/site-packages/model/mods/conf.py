from typed.mods.conf import Conf as TypedConf, __CONF__

class ModelConf(metaclass=__CONF__):
    def __init__(self, check: bool = True, lazy: bool = False):
        from typed.mods.check import check as _check
        _check.isinstance(check, bool)
        _check.isinstance(lazy, bool)
        self.check = check
        self.lazy = lazy

class Conf(TypedConf):
    def __init__(
        self, 
        logic=None, 
        typesystem=None, 
        err=None, 
        typecheck=None, 
        model: ModelConf = None
    ):
        super().__init__(
            logic=logic, 
            typesystem=typesystem, 
            err=err, 
            typecheck=typecheck
        )

        if model is None:
            model = ModelConf()

        from typed.mods.check import check as _check
        _check.isinstance(model, ModelConf)
        self.model = model
