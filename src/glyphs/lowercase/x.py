from math import atan, sin
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseXGlyph(Glyph):
    name = "lowercase_x"
    unicode = "0x78"
    offset = 0
    width_ratio = 380 / 340

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)

        theta = atan(dc.x_height / b.width)
        delta = dc.stroke / sin(theta)

        # Forward diagonal (bottom-left to top-right)
        draw_polygon(
            pen,
            points=[
                (b.x1, 0),
                (b.x1 + delta, 0),
                (b.x2, dc.x_height),
                (b.x2 - delta, dc.x_height),
            ],
        )
        # Backward diagonal (bottom-right to top-left)
        draw_polygon(
            pen,
            points=[
                (b.x2 - delta, 0),
                (b.x2, 0),
                (b.x1 + delta, dc.x_height),
                (b.x1, dc.x_height),
            ],
        )
