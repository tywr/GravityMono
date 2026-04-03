from math import atan, cos, sin
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseVGlyph(Glyph):
    name = "lowercase_v"
    unicode = "0x76"
    offset = 0
    width_ratio = 380 / 340

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        half_width = b.width / 2 - dc.stroke / 2

        branch_h = dc.x_height
        theta = atan(branch_h / half_width)
        x_delta = dc.stroke / sin(theta)

        # Right branch
        draw_polygon(
            pen,
            points=[
                (b.xmid + x_delta / 2, 0),
                (b.xmid + half_width + x_delta / 2, dc.x_height),
                (b.xmid + half_width - x_delta / 2, dc.x_height),
                (b.xmid - x_delta / 2, 0),
            ],
        )
        # Left branch
        draw_polygon(
            pen,
            points=[
                (b.xmid + x_delta / 2, 0),
                (b.xmid - half_width + x_delta / 2, dc.x_height),
                (b.xmid - half_width - x_delta / 2, dc.x_height),
                (b.xmid - x_delta / 2, 0),
            ],
        )
