from config import FontConfig as fc
from glyphs.base import superellipse_loop


def draw_o(
    pen,
    stroke: int,
    taper=None,
    taper_ratio=1.0,
    center_x=None,
    x_ratio=1.0,
    height=None,
):
    x1 = fc.width / 2 - fc.o_width / 2 - stroke / 2
    y1 = 0
    x2 = fc.width / 2 + fc.o_width / 2 + stroke / 2
    y2 = fc.x_height
    hx = 150
    hy = 200
    superellipse_loop.draw_superellipse_loop(
        pen, stroke, x1, y1, x2, y2, hx, hy
    )
