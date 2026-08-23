from typed.checker import (
    Checker,
    check as typed_check,
    require as typed_require
)

class SchemaChecker(Checker):
    def isschema(self, objs) -> bool:
        from model.mods.types.schema import Schema
        from model.helper.check import _base_check
        return _base_check(self, Schema, objs)

    def isordered(self, objs) -> bool:
        from model.mods.types.schema import OrderedSchema
        from model.helper.check import _base_check
        return _base_check(self, OrderedSchema, objs)

    def isstrict(self, objs) -> bool:
        from model.mods.types.schema import StrictSchema
        from model.helper.check import _base_check
        return _base_check(self, StrictSchema, objs)

    def validate(self, typ, fields) -> bool:
        from model.mods.types.schema import Schema
        from model.helper.check import _validate
        return _validate(self, Schema, typ, fields)

class ModelChecker(Checker):
    def ismodel(self, objs) -> bool:
        from model.mods.types.model import Model
        from model.helper.check import _base_check
        return _base_check(self, Model, objs)

    def isordered(self, objs) -> bool:
        from model.mods.types.model import OrderedModel
        from model.helper.check import _base_check
        return _base_check(self, OrderedModel, objs)


    def isstrict(self, objs) -> bool:
        from model.mods.types.model import StrictModel
        from model.helper.check import _base_check
        return _base_check(self, StrictModel, objs)

    def validate(self, typ, fields) -> bool: 
        _defaults = getattr(typ, '__defaults__', {})

        for k, default_val in _defaults.items():
            if k not in fields:
                fields[k] = default_val

        from model.mods.types.model import Model
        from model.helper.check import _validate
        return _validate(self, Model, typ, fields)

__schema_check__ = SchemaChecker(quantifier=None, explode=False)
__schema_require__ = SchemaChecker(quantifier=None, explode=True)

__model_check__ = ModelChecker(quantifier=None, explode=False)
__model_require__ = ModelChecker(quantifier=None, explode=True)

class check(typed_check):
    class schema:
        isschema = __schema_check__.isschema
        isordered = __schema_check__.isordered
        isstrict = __schema_check__.isstrict
        validate = __schema_check__.validate
    class model:
        ismodel = __model_check__.ismodel
        isordered = __model_check__.isordered
        isstrict = __model_check__.isstrict
        validate = __model_check__.validate

class require(typed_require):
    class schema:
        isschema = __schema_require__.isschema
        isordered = __schema_require__.isordered
        isstrict = __schema_require__.isstrict
        validate = __schema_require__.validate

    class model:
        ismodel = __model_require__.ismodel
        isordered = __model_require__.isordered
        isstrict = __model_require__.isstrict
        validate = __model_require__.validate
