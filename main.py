from generator import generate_heights
from display import display_level
from rules import validate_level


def main():

    heights = generate_heights()

    print("Generated level heights:")
    print(heights)

    print("Level valid:", validate_level(heights))

    display_level(heights)


if __name__ == "__main__":
    main()