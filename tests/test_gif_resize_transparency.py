# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license

from io import BytesIO
from os.path import abspath, dirname, join

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

STICKER = join(dirname(abspath(__file__)), "..", "course", "images", "sticker.gif")


def test_resized_palette_gif_keeps_transparent_pixels():
    with open(STICKER, "rb") as image_file:
        source_bytes = image_file.read()

    source = Image.open(BytesIO(source_bytes))
    assert "transparency" in source.info
    source_alpha = source.convert("RGBA").getchannel("A")
    assert source_alpha.getextrema()[0] == 0

    config = Config(
        PILLOW_PRESERVE_INDEXED_MODE=True, ALLOW_ANIMATED_GIFS=False
    )
    engine = Engine(Context(config=config))
    engine.load(source_bytes, ".gif")
    engine.resize(240, 160)
    result = engine.read(".gif")

    output = Image.open(BytesIO(result))
    assert "transparency" in output.info

    output_alpha = output.convert("RGBA").getchannel("A")
    assert output_alpha.getpixel((0, 0)) == 0
    assert output_alpha.getextrema()[0] == 0