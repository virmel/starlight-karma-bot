from file_store import save, load


def increment(file_name, key):
    return add(file_name, key, 1)


def add(file_name, key, amount):
    dictionary = load(file_name)
    dictionary[str(key)] = dictionary.get(str(key), 0) + amount
    save(dictionary, file_name)
    return dictionary
