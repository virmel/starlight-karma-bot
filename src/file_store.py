import json


def save(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle)


def load(file_name):
    with open(file_name, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)
        file_handle.close()
        return data
