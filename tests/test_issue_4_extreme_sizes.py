# -*- coding: utf-8 -*-

import os
from PIL import Image
from tests.base import ThumborTestCase


class Issue4ExtremeSizesTestCase(ThumborTestCase):
    """Tests for issue #4: zero/extreme dimension handling."""

    def get_config(self):
        cfg = super().get_config()
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "course", "images"
        )
        return cfg

    def test_extreme_dimensions(self):
        # 1. /unsafe/800x20/rainbow.png -> code 200, size (800, 20), max alpha > 0
        result = self.fetch("/unsafe/800x20/rainbow.png")
        assert result.code == 200
        img = Image.open(result.buffer)
        w, h = img.size
        assert w == 800
        assert h == 20
        max_alpha = max(img.getchannel("A").getdata()) if img.mode == "RGBA" else 0
        assert max_alpha > 0, "Image should not be fully transparent"

        # 2. /unsafe/fit-in/1x1/940x2.png -> code 200, size (1, 1)
        result = self.fetch("/unsafe/fit-in/1x1/940x2.png")
        assert result.code == 200
        img = Image.open(result.buffer)
        w, h = img.size
        assert w == 1
        assert h == 1

        # 3. /unsafe/fit-in/100x0/940x2.png -> code 200, size (100, 1)
        result = self.fetch("/unsafe/fit-in/100x0/940x2.png")
        assert result.code == 200
        img = Image.open(result.buffer)
        w, h = img.size
        assert w == 100
        assert h == 1
