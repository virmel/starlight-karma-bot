from file_store import save


def increment(dictionary, key):
    return add(dictionary, key, 1)


def add(dictionary, key, amount):
    dictionary = dictionary.copy()
    dictionary[key] = dictionary.get(key, 0) + amount
    return dictionary


def increment_and_save(dictionary, key, file_name):
    value = increment(dictionary, key)
    save(value, file_name)
    return value


def add_and_save(dictionary, key, amount, file_name):
    value = add(dictionary, key, amount)
    save(dictionary, file_name)
    return value
