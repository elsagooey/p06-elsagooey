# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license

from thumbor.ext.filters import _round_corner

WIDTH = 100
HEIGHT = 100
RADIUS = 30
COLOR = (200, 100, 50)


def test_transparent_round_corner_smooths_edge_through_alpha():
    data = bytes(COLOR + (255,)) * (WIDTH * HEIGHT)
    result = _round_corner.apply(
        1,
        "RGBA",
        RADIUS,
        RADIUS,
        255,
        255,
        255,
        WIDTH,
        HEIGHT,
        data,
        1,
    )
    pixels = [result[i : i + 4] for i in range(0, len(result), 4)]

    assert any(0 < pixel[3] < 255 for pixel in pixels)
    for pixel in pixels:
        if pixel[3] > 0:
            assert tuple(pixel[:3]) == COLOR