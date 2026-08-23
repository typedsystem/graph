from typed import null

def _null(typ):
    required = dict(getattr(typ, '_required_attributes_and_types', {}))
    optional = getattr(typ, '_optional_attributes_and_defaults', {})
    ordered_keys = getattr(typ, '_ordered_keys', None)
    all_keys = []
    data = {}
    if ordered_keys:
        for name in ordered_keys:
            if name in required:
                val = null(required[name])
                data[name] = val
            elif name in optional:
                wrapper = optional[name]
                if wrapper.default_value is not None:
                    data[name] = wrapper.default_value
                else:
                    data[name] = null(wrapper.type)
            else:
                pass
    else:
        for name, field_type in required.items():
            data[name] = null(field_type)
        for name, wrapper in optional.items():
            if wrapper.default_value is not None:
                data[name] = wrapper.default_value
            else:
                data[name] = null(wrapper.type)
    try:
        return typ(**data)
    except Exception as e:
        return None
