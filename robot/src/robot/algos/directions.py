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

# DIRECTION_TO_CHAR = {
#     NORTH: "\u25B2",
#     SOUTH: "\u25BC",
#     EAST: "\u25BA",
#     WEST: "\u25C4"
# }
DIRECTION_TO_CHAR = {
    NORTH: "\u2191",
    SOUTH: "\u2193",
    EAST: "\u2192",
    WEST: "\u2190"
}