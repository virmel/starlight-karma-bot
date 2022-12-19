from data import increment, add


def test_increment():
    test_dict = {"a": 1}
    actual = increment(test_dict, "a")
    assert actual == {"a": 2}
    actual = increment(test_dict, "b")
    assert actual == {"a": 1, "b": 1}


def test_add():
    test_dict = {"a": 1}
    actual = add(test_dict, "a", 2)
    assert actual == {"a": 3}
    actual = add(test_dict, "b", 1)
    assert actual == {"a": 1, "b": 1}
    actual = add(test_dict, "a", -1)
    assert actual == {"a": 0}
