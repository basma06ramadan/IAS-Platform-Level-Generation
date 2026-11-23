MIN_HEIGHT = 2
MAX_HEIGHT = 6
MAX_GAP_WIDTH = 2
GAP_PROBABILITY = 0.15
MIN_GROUND_BETWEEN_GAPS = 2

def validate_level(heights):

    gap_width = 0

    for height in heights:

        if height == 0:
            gap_width += 1

            if gap_width > MAX_GAP_WIDTH:
                return False

        else:
            if not MIN_HEIGHT <= height <= MAX_HEIGHT:
                return False

            gap_width = 0

    return True