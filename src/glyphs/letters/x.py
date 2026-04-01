from math import atan, sin
from config import FontConfig as fc
from glyph import Glyph
from shapes.rect import draw_rect
from shapes.polygon import draw_polygon


class LowercaseXGlyph(Glyph):
    name = "x"
    unicode = "0x78"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 350

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = 0
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height

        theta = atan((y2 - y1) / (x2 - x1))
        delta = stroke / sin(theta)

        draw_polygon(
            pen,
            points=[
                (x1, y1),
                (x1 + delta, y1),
                (x2, y2),
                (x2 - delta, y2),
            ],
        )
        draw_polygon(
            pen,
            points=[
                (x2 - delta, y1),
                (x2, y1),
                (x1 + delta, y2),
                (x1, y2),
            ],
        )
