def sort_dict_by_values(input_dict):
    return dict(sorted(input_dict.items(), key=lambda item: item[1], reverse=True))


def first_entry(input_dict):
    if len(input_dict) > 0:
        key = next(iter(input_dict))
        return {key: input_dict[key]}
    return None


def first_key(input_dict):
    first = first_entry(input_dict)
    if first is None:
        return None
    return list(first.keys())[0]


def first_value(input_dict):
    first = first_entry(input_dict)
    if first is None:
        return None
    return list(first.values())[0]


def number_list(input_list) -> list[str]:
    return [f"#{index + 1}: {value}" for index, value in enumerate(input_list)]


def results_to_map(results) -> dict[str, str]:
    if len(results) == 0:
        return {}
    if hasattr(results[0], "display_name"):
        return {str(result.id): result.display_name for result in results}
    return {str(result.id): result.name for result in results}


def get_name(target_key: str, lookup_dict) -> str | None:
    for key, value in lookup_dict.items():
        if target_key == key:
            return value
    return None


def to_leaderboard_string(entries, unit) -> str:
    as_string = [f"{entry[1]} ({entry[2]} {unit})" for entry in entries]
    as_string = number_list(as_string)
    return "\n".join(as_string)


def load_image(file_path):
    with open(file_path, "rb") as file_handle:
        return file_handle.read()
