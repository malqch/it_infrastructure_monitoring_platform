import json

def format_result(result):
    data = dict()
    for k, v in result.items():
        try:
            value = json.loads(str(v, encoding="utf-8"))
        except Exception as e:
            value = str(v, encoding="utf-8")
        data[k.decode('utf-8')] = value
    return data