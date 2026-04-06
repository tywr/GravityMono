from math import cos, sin

from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class UppercaseYGlyph(UppercaseGlyph):
    name = "uppercase_y"
    unicode = "0x59"
    offset = 0
    width_ratio = 1.3
    junction_ratio = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        ov = 0.5 * dc.stroke_x
        yj = b.x1 + self.junction_ratio * b.height

        theta, delta = draw_parallelogramm(
            pen, dc.stroke_x, dc.stroke_y, b.xmid - ov, yj, b.x2, b.y2
        )
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid + ov,
            yj,
            b.x1,
            b.y2,
            direction="top-left",
        )

        # Draw main step
        draw_rect(pen, b.xmid - dc.stroke_x / 2, b.y1, b.xmid + dc.stroke_x / 2, yj)

        # Draw junction to fill the gaps
        draw_polygon(
            pen,
            points=[
                (b.xmid + ov - delta, yj),
                (b.xmid + ov - delta + ov * cos(theta), yj - ov * sin(theta)),
                (b.xmid, yj),
            ],
        )
        draw_polygon(
            pen,
            points=[
                (b.xmid, yj),
                (b.xmid - ov + delta - ov * cos(theta), yj - ov * sin(theta)),
                (b.xmid - ov + delta, yj),
            ],
        )
