def increment(dictionary, key):
    return add(dictionary, key, 1)


def add(dictionary, key, amount):
    dictionary = dictionary.copy()
    dictionary[str(key)] = dictionary.get(str(key), 0) + amount
    return dictionary
