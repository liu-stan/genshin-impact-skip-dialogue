import pytest

import cv2
from gs_skip import *

from loguru import logger


def test_match_resize():
    ui = UI()
    image = cv2.imread("test/ui-capture.jpg")
    ui._capture = cv2.resize(image, (1920, 1080))
    assert ui.match_button(interact_button)


def test_match():
    ui = UI()
    for i in range(7):
        image = cv2.imread(f"test/talk-match-0{i}.jpg")
        ui._capture = image
        if ui.match_button(interact_button):
            x0, y0 = interact_button.crop_posi[:2]
            x, y = interact_button.max_loc
            p = [x0 + x + 110, y0 + y + 5, x0 + x + 230, y0 + y + 30]
            dialog = ui.crop(p)
            gray = cv2.cvtColor(dialog, cv2.COLOR_BGR2GRAY)
            _, thresh1 = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
            assert (thresh1 == 0).all()
