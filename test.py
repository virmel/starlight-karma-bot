import json
karma_map = {
    "239631525350604801": 6
}
# virmel = 208425244128444418

# read_karma_file = open("karma.txt", "r")
# karma_object = json.load(read_karma_file)
# read_karma_file.close()

# prev_karma = karma_object.get(f'{virmel}', 0)
# karma_object["208425244128444418"] = prev_karma + 1

# write_karma_file = open("karma.txt", "w")
# json.dump(karma_object, write_karma_file)
# write_karma_file.close()

prev_karma = karma_map.get(f'208425244128444418', 0)
karma_map['208425244128444418'] = prev_karma + 1
print(karma_map)
