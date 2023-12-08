def main():
    with open("input.txt", "r") as fh:
        final_sum = 0

        for line in fh.readlines():
            numbers_in_line = [c for c in line if c.isdigit()]

            if len(numbers_in_line) == 0:
                continue

            # Repeat the first digit if there is only one:
            number_str = numbers_in_line[0] + numbers_in_line[-1]

            number = int(number_str)
            final_sum += number

        print("Final sum:", final_sum)


if __name__ == "__main__":
    main()
