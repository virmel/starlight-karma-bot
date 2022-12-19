import os
from file_store import save, load


def test_save_load():
    test_dict = {"a": 1, "b": 2}
    file_name = "test.json"
    save(test_dict, file_name)
    loaded = load(file_name)
    os.remove(file_name)
    assert test_dict == loaded
