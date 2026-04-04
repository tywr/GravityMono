from math import tan
from glyph import Glyph
from shapes.rect import draw_rect
from shapes.polygon import draw_polygon
from shapes.parallelogramm import draw_parallelogramm


class LowercaseKGlyph(Glyph):
    name = "lowercase_k"
    unicode = "0x6B"
    offset = 10
    bowl_width = 320
    neck_len = 100
    width_ratio = 1
    branch_ratio = 0.75

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        # x_neck = b.x1 + self.neck_ratio * b.width
        x_branch = b.x1 + (1 - self.branch_ratio) * b.width

        # Angle of each diagonal branch
        # w = b.x2 - x_neck
        # h = dc.x_height / 2 - dc.stroke / 2
        # s = dc.stroke
        # delta = (s * (h * sqrt(w**2 + h**2 - s**2) - s * w)) / (h**2 - s**2)
        # theta = atan2(h, w - delta)
        # delta = s / cos(theta)

        # Left ascender stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.ascent)
        # Upper branch
        draw_parallelogramm(pen, dc.stroke, x_branch, b.ymid + dc.stroke / 2, b.x2, b.y1, direction="bottom")
        theta, delta = draw_parallelogramm(pen, dc.stroke, x_branch, b.ymid - dc.stroke / 2, b.x2, b.y2)
        draw_rect(pen, b.x1, b.ymid - dc.stroke / 2, x_branch + delta / tan(theta), b.ymid + dc.stroke / 2)
