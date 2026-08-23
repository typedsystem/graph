def _resolve(met, fields, __origin_cls__=None, __extends__=None, __defaults__=None):
    bases_list = []
    if __origin_cls__:
        bases_list.append(__origin_cls__)
    if __extends__:
        for b in __extends__:
            if b not in bases_list:
                bases_list.append(b)
    if not any(issubclass(b, met) for b in bases_list if isinstance(b, type)):
        bases_list.append(met)

    bases = tuple(bases_list)

    _fields = {}
    _defaults = {}

    for b in reversed(bases):
        _fields.update(getattr(b, '__fields__', {}))
        _defaults.update(getattr(b, '__defaults__', {}))

    _fields.update(fields)
    if __defaults__ is not None:
        _defaults.update(__defaults__)

    return bases, _fields, _defaults

def _issub(sub_dict, sup_dict):
    from typed.mods.typesystem import issub
    for k, v_sup in sup_dict.items():
        if k not in sub_dict:
            return False
        v_sub = sub_dict[k]
        if isinstance(v_sub, dict) and isinstance(v_sup, dict):
            if not _issub(v_sub, v_sup):
                return False
        else:
            if not issub(v_sub, v_sup):
                return False
    return True

def _schema(typ):
    if not hasattr(typ, '__schema__'):
        typ.__schema__ = typ.schema()
    return typ.__schema__
