from math import atan, cos, sin
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseYGlyph(Glyph):
    name = "lowercase_y"
    unicode = "0x79"
    offset = 0
    width_ratio = 380 / 340

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        half_width = b.width / 2 - dc.stroke / 2

        branch_h = dc.x_height / 2
        theta = atan(branch_h / half_width)
        x_delta = dc.stroke / sin(theta)
        y_delta = dc.stroke / cos(theta)

        # Horizontal projection of the tail and dent offsets
        x_delta_desc = -dc.descent * half_width / dc.x_height
        x_delta_dent = dc.dent * half_width / dc.x_height

        draw_polygon(
            pen,
            points=[
                # Tail at descender
                (b.xmid - x_delta / 2 - x_delta_desc, dc.descent),
                (b.xmid + x_delta / 2 - x_delta_desc, dc.descent),
                # Top-right branch
                (b.xmid + half_width + x_delta / 2, dc.x_height),
                (b.xmid + half_width - x_delta / 2, dc.x_height),
                # Inner junction
                (b.xmid, y_delta),
                # Top-left branch
                (b.xmid - half_width + x_delta / 2, dc.x_height),
                (b.xmid - half_width - x_delta / 2, dc.x_height),
                # Dent on left stem
                (b.xmid - x_delta / 2 - x_delta_dent, dc.dent),
                (b.xmid - x_delta / 2 + x_delta_dent, dc.dent),
            ],
        )
