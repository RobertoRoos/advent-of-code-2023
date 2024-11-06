def hash_function(txt: str) -> int:
    """The HASH function."""
    value = 0
    for c in txt:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def main():
    with open("input.txt", "r") as fh:
        line = fh.readline().strip()

    parts = line.split(",")
    value = sum(hash_function(part) for part in parts)

    print("Sum:", value)


if __name__ == "__main__":
    main()
