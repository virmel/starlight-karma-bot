from unittest.mock import Mock
from util import (
    sort_dict_by_values,
    first_entry,
    number_list,
    results_to_map,
    get_name,
    to_leaderboard_string,
)
from karma import KarmaUser


def test_first_entry():
    test_dict = {"a": 1, "b": 2}
    actual = first_entry(test_dict)
    assert actual == {"a": 1}


def test_sort_dict_by_values():
    unsorted_dict = {"a": 1, "b": 2}
    actual = sort_dict_by_values(unsorted_dict)
    assert actual == {"b": 2, "a": 1}


def test_number_list():
    test_list = ["a", "b"]
    actual = number_list(test_list)
    assert actual == ["#1 a", "#2 b"]


def test_results_to_map():
    member = Mock()
    member.id = 123
    member.display_name = "Test"
    test_results = [member]
    actual = results_to_map(test_results)
    assert actual == {"123": "Test"}


def test_get_name():
    test_dict = {"123": "Test"}
    actual = get_name("123", test_dict)
    assert actual == "Test"
    actual = get_name("456", test_dict)
    assert actual is None


def test_to_leaderboard_string():
    users = [KarmaUser(1, "test", 2)]
    actual = to_leaderboard_string(users)
    assert actual == "#1 test (2 karma)"
