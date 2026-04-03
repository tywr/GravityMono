from math import atan, cos
from glyph import Glyph
from shapes.rect import draw_rect
from shapes.polygon import draw_polygon


class LowercaseZGlyph(Glyph):
    name = "lowercase_z"
    unicode = "0x7A"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset)

        theta = atan((dc.x_height - 2 * dc.stroke) / b.width)
        delta = dc.stroke / cos(theta)

        # Top and bottom bars
        draw_rect(pen, b.x1, dc.x_height - dc.stroke, b.x2, dc.x_height)
        draw_rect(pen, b.x1, 0, b.x2, dc.stroke)
        # Diagonal stroke
        draw_polygon(
            pen,
            points=[
                (b.x1, dc.stroke),
                (b.x1 + delta, dc.stroke),
                (b.x2, dc.x_height - dc.stroke),
                (b.x2 - delta, dc.x_height - dc.stroke),
            ],
        )
