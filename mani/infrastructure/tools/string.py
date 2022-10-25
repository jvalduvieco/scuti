import re


def is_enum(name):
    tmp = name
    return tmp.replace("_", "").isupper() or name[0].isupper()


def is_camel(name):
    return name != name.lower() and name != name.upper() and "_" not in name


def camel_to_underscore(name):
    if not is_camel(name):
        return name
    if type(name) == str:
        camel_pat = re.compile(r'([A-Z])')
        result = camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)
        return result[1:] if result[0] == '_' else result
    else:
        return name


def underscore_to_lower_camel(name):
    if type(name) == str:
        under_pat = re.compile(r'_([a-z])')
        return under_pat.sub(lambda x: x.group(1).upper(), name)
    else:
        return name


def underscore_to_upper_camel(name):
    lower_camel = underscore_to_lower_camel(name)
    return lower_camel[:1].upper() + lower_camel[1:]
