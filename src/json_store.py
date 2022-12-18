import json
from typing import NewType
from util import sort_dict

Key = NewType("Key", str)
Value = NewType("Value", int)
Dict = NewType("Dict", dict[Key, Value])


class JsonStore:
    __items: Dict
    __file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.items = self.__load()

    def sorted(self) -> Dict:
        return Dict(sort_dict(self.__items))

    def count(self) -> int:
        return len(self.__items)

    def add(self, key: Key, val: Value) -> Value:
        current = self.get(key)
        new = Value(current + val)
        self.__set(key, new)
        return new

    def __set(self, key: Key, value: Value) -> None:
        self.items[key] = value
        self.__save()

    def get(self, key: Key) -> Value:
        return self.items.get(key, Value(0))

    def __save(self) -> None:
        with open(self.file_name, "w", encoding="utf-8") as file_handle:
            json.dump(self.__items, file_handle)

    def __load(self) -> Dict:
        with open(self.file_name, "r", encoding="utf-8") as file_handle:
            contents = json.load(file_handle)
            file_handle.close()
            return contents
