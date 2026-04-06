from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class LowercaseQGlyph(Glyph):
    name = "lowercase_q"
    unicode = "0x71"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )

        # Bowl (open on the right, same as d)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            taper=dc.taper,
            side="right",
        )
        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x2 - dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Right descender stem
        draw_rect(pen, b.x2 - dc.stroke_x + dc.gap, dc.descent, b.x2, dc.x_height)
        draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, y2)
