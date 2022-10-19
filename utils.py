import json


def json_read(path: str) -> json:
    with open(path, "r") as json_file:
        json_file = json.load(json_file)
    return json_file


def write_to_json(data: dict, path: str, indent: int) -> None:
    json_object = json.dumps(data, indent=indent)
    with open(path, "w") as outfile:
        outfile.write(json_object)