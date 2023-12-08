def get_cube_sets(game_str: str):
    for draw_str in game_str.strip().split(";"):
        cube_set = {}
        for cube_str in draw_str.split(","):
            count_str, _, color = cube_str.strip().partition(" ")
            count = int(count_str)
            cube_set[color] = count

        yield cube_set


def check_game_is_possible(options: dict, game_str: str) -> bool:
    for cube_set in get_cube_sets(game_str):
        for color, count in cube_set.items():
            if count > options[color]:
                return False  # At least one color exceeds, impossible

    return True


def get_game_power(options: dict, game_str: str):
    cubes_min = {color: 0 for color in options.keys()}

    for cube_set in get_cube_sets(game_str):
        for color, count in cube_set.items():
            cubes_min[color] = max(cubes_min[color], count)

    value = 1
    for c in cubes_min.values():
        value *= c

    return value


def main():
    cube_max_counts = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    with open("input.txt", "r") as fh:
        possible_game_id_sum = 0
        power_games_sum = 0

        while (line := fh.readline()) != "":
            game_id_str, _, draws_str = line.partition(":")

            game_id = int(game_id_str[5:])

            if check_game_is_possible(cube_max_counts, draws_str):
                possible_game_id_sum += game_id

            power_games_sum += get_game_power(cube_max_counts, draws_str)

        print("Sum of possible games:", possible_game_id_sum)
        print("Sum of power of all games:", power_games_sum)


if __name__ == "__main__":
    main()
