def main():
    with open("input.txt", "r") as fh:
        cube_counts = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }

        def check_game_is_possible(game_str: str) -> bool:
            for draw_str in game_str.strip().split(";"):
                for cube_str in draw_str.split(","):
                    count_str, _, color = cube_str.strip().partition(" ")
                    count = int(count_str)
                    if count > cube_counts[color]:
                        return False  # At least one color exceeds, impossible

            return True

        game_id_sum = 0

        while (line := fh.readline()) != "":
            game_id_str, _, draws_str = line.partition(":")

            game_id = int(game_id_str[5:])

            if check_game_is_possible(draws_str):
                game_id_sum += game_id

        print("Sum of possible games:", game_id_sum)


if __name__ == "__main__":
    main()
