def _base_check(self, met, objs):
    from typed import check
    q = self.quantifier
    if q is None:
        res = check.isterm(objs, met)
        if not res:
            if self.explode:
                from typed.err import TypeErr
                from typed import prop
                raise TypeErr(
                    func="isschema",
                    term=objs,
                    expected=(met,),
                    received=prop.typeof(objs)
                )
            return False
        return True

    res = q(check.isterm(obj, met) for obj in objs)
    if not res:
        if self.explode:
            from typed.err import TypeErr
            from typed import prop
            raise TypeErr(
                func="isschema",
                term=objs,
                expected=(met,),
                quantifier=q,
                received=prop.typeof(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(prop.typeof(obj) for obj in objs)
            )
        return False
    return True

def _validate(self, met, typ, fields):
    from typed import check
    if not check.isterm(typ, met):
        if self.explode:
            from typed.mods.err import TypeErr
            from model.mods.meta.schema import SCHEMA
            raise TypeErr(
                func="validate",
                term=typ,
                expected=(SCHEMA,)
            )
        return False

    if not fields or not getattr(typ, '__check__', True):
        return True

    _fields = getattr(typ, '__fields__', {})

    if self.isordered(typ):
        extra = [k for k in fields if k not in _fields]
        if extra:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message=f"Received extra keys",
                    keys=extra,
                    term=fields,
                    expected=(typ,)
                )
            return False

    if self.isstrict(typ):
        expected_order = [k for k in fields if k in _fields]
        provided_order = list(fields.keys())
        if expected_order != provided_order:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message="Keys are not in the expected order",
                    term=fields,
                    expected=(typ,)
                )
            return False

    for k, expected_type in fields.items():
        if k not in _fields:
            if self.explode:
                from model.mods.err import FieldErr
                raise FieldErr(
                    message=f"Missing required key",
                    key=k,
                    term=fields,
                    expected=(typ,)
                )
            return False

        val = fields[k]

        from typed import check
        if not check.isterm(val, expected_type):
            if self.explode:
                from model.mods.err import ModelErr
                from typed import prop
                raise ModelErr(
                    message=f"Field has invalid type",
                    term=val,
                    field=k,
                    expected=(expected_type,),
                    received=prop.typeof(val)
                )
            return False
    return True
