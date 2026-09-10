from glyphs import Glyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm
from draw.square_corner import draw_square_corner


class LowercaseZ2Glyph(Glyph):
    name = "lowercase_z_2"
    default_italic = True
    unicode = "0x7A"
    offset = 0
    diag_stroke_ratio = 0.96
    width_ratio = 1
    right_offset = 0.04
    left_offset = 0.025
    tail_ratio = 0.33

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        sx, sy = dc.stroke_x, dc.stroke_y
        dsx = self.diag_stroke_ratio * dc.stroke_x
        dsy = self.diag_stroke_ratio * dc.stroke_y
        yt2 = b.y2 - self.tail_ratio * b.height
        yt1 = b.y1 + self.tail_ratio * b.height

        xl = b.x1 + self.left_offset * b.width
        xr = b.x2 - self.right_offset * b.width

        # Top and bottom bars
        # draw_rect(pen, xl, dc.x_height - dc.stroke_y, xr, dc.x_height)
        # draw_rect(pen, b.x1, 0, b.x2, dc.stroke_y)

        draw_square_corner(
            pen, sx, sy, b.x1, yt2, xr, b.y2, orientation="top-right"
        )
        draw_square_corner(
            pen, sx, sy, b.x2, yt1, b.x1, b.y1, orientation="bottom-left"
        )

        # Diagonal stroke
        theta, delta = draw_parallelogramm(
            pen,
            dsx,
            dsy,
            b.x1,
            b.y1 + dc.stroke_y,
            xr,
            b.y2 - dc.stroke_y,
        )
