NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

LEFT_TURN = {
    NORTH: WEST,
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH
}

RIGHT_TURN = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH
}

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}

DIRECTION_TO_CHAR = {
    NORTH: ":up_arrow-emoji:",
    SOUTH: ":down_arrow-emoji:",
    EAST: ":right_arrow-emoji:",
    WEST: ":left_arrow-emoji:"
}

# alternative
# DIRECTION_TO_CHAR = {
#     NORTH: ":arrow_up_small-emoji:",
#     SOUTH: ":arrow_down_small-emoji:",
#     EAST: ":arrow_forward-emoji:",
#     WEST: ":arrow_backward-emoji:"
# }
