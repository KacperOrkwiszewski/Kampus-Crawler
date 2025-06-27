
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Constants:
    TILES_Y = 50
    TILES_X = 38
    TILE_HEIGHT = 16
    TILE_WIDTH = 16

    WINDOW_HEIGHT = TILES_Y * TILE_HEIGHT
    WINDOW_WIDTH = TILES_X * TILE_WIDTH

    MAP_SCALE = 5

    MUSIC_FADEOUT_SPEED = 200 # miliseconds

    MAP_ORIGIN_X = 360
    MAP_ORIGIN_Y = 280

    entrences_campus_A = {
        "A1": Point(-8440, -1160),
        "A2": Point(-8520, -2040),
        "A3": Point(-9880, -2040),
        "A4": Point(-11000, -2600),
        "A5": Point(-11480, -3720),
        "A6.1": Point(-10200, -3720),
        "A6.2": Point(-10280, -3720),
        "A7": Point(-9640, -3800),
        "A8": Point(-8600, -5160),
        "A9": Point(-9240, -4680),
        "A10.1": Point(-8760, -6520),
        "A10.2": Point(-8840, -6520),
        "A11": Point(-9160, -5240),
        "A12": Point(-9960, -4360),
        "A13": Point(-9320, -7240),
        "A14": Point(-11400, -6360),
        "A15": Point(-11400, -6360),
        "A16.1": Point(-7240, -840),
        "A16.2": Point(-7320, -840),
        "A16.3": Point(-7400, -840),
        "A17": Point(-5960, -920),
        "A18.1": Point(-7000, -2360),
        "A18.2": Point(-7080, -2360),
        "A19": Point(-7320, -3800),
        "A20": Point(-6680, -4360),
        "A21": Point(-6680, -5480),
        "A22": Point(-6680, -6360),
        "A23": Point(-7960, -7160),
        "A24.1": Point(-6120, -2280),
        "A24.2": Point(-6200, -2280),
        "A26.1": Point(-5960, -2840),
        "A26.2": Point(-5880, -2840),
        "A27.1": Point(-6120, -3560),
        "A27.2": Point(-6200, -3560),
        "A28.1": Point(-6360, -4200),
        "A28.2": Point(-5880, -4200),
        "A30": Point(-6280, -6120),
        "A33.1": Point(-5240, -4840),
        "A33.2": Point(-5320, -4840),
        "A33.3": Point(-5240, -6600),
        "A33.4": Point(-5320, -6600),
        "A33.5": Point(-4680, -6600),
        "A33.6": Point(-4760, -6600),
        "A34.1": Point(-4440, -3640),
        "A34.2": Point(-4520, -3640),
        "A34.3": Point(-5000, -2120),
        "A34.4": Point(-4920, -2120),
    }