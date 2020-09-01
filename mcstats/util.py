import json
import types

def handle_error(e, die = False):
    print(str(e))
    if die:
        exit(1)

class RecursiveNamespace(types.SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, val in kwargs.items():
            if type(val) == dict:
                setattr(self, key, RecursiveNamespace(**val))
            elif type(val) == list:
                setattr(self, key, list(map(lambda x: RecursiveNamespace(**x) if isinstance(x, dict) else x, val)))

class RecursiveNamespaceEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def merge_dict(base, add):
    for key, val in add.items():
        if (key in base and isinstance(base[key], dict) and isinstance(add[key], dict)):
            merge_dict(base[key], add[key])
        else:
            base[key] = add[key]
