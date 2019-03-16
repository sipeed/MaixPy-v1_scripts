import ujson

json_str = '''{
    "name": "sipeed",
    "babies": [
        {
            "name": "maixpy",
            "birthday": 2.9102,
            "sex": "unstable"
        }
    ]
}'''

obj = ujson.loads(json_str)
print(obj["name"])
print(obj["babies"])

