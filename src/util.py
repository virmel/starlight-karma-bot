def sort_dict_by_values(input_dict):
    return dict(sorted(input_dict.items(), key=lambda item: item[1], reverse=True))


def first_entry(input_dict):
    if len(input_dict) > 0:
        key = next(iter(input_dict))
        return {key: input_dict[key]}
    return None


def number_list(input_list) -> list[str]:
    return [f"#{index + 1} {value}" for index, value in enumerate(input_list)]


def results_to_map(results) -> dict[str, str]:
    return {str(result.id): result.display_name for result in results}


def get_name(target_key: str, lookup_dict) -> str | None:
    for key, value in lookup_dict.items():
        if target_key == key:
            return value
    return None


def to_leaderboard_string(users) -> str:
    users_as_string = [f"{user[1]} ({user[2]} karma)" for user in users]
    users_as_string = number_list(users_as_string)
    return "\n".join(users_as_string)
