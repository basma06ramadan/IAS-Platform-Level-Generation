import random

from rules import (
    MIN_HEIGHT,
    MAX_HEIGHT,
    MAX_GAP_WIDTH,
    GAP_PROBABILITY,
    MIN_GROUND_BETWEEN_GAPS
)


def generate_heights(width=30):

    heights = []
    current_height = 3
    ground_since_gap = MIN_GROUND_BETWEEN_GAPS

    while len(heights) < width:

        can_create_gap = (
            len(heights) >= 3
            and len(heights) < width - MAX_GAP_WIDTH
            and ground_since_gap >= MIN_GROUND_BETWEEN_GAPS
        )

        if can_create_gap and random.random() < GAP_PROBABILITY:

            gap_width = random.randint(1, MAX_GAP_WIDTH)

            heights.extend([0] * gap_width)

            ground_since_gap = 0

        else:

            movement = random.choice([-1, 0, 1])

            current_height += movement

            current_height = max(
                MIN_HEIGHT,
                min(current_height, MAX_HEIGHT)
            )

            heights.append(current_height)

            ground_since_gap += 1

    return heights