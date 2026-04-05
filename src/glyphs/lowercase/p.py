from glyphs import Glyph

# from shapes.superellipse_arch import draw_superellipse_arch
from draw.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercasePGlyph(Glyph):
    name = "lowercase_p"
    unicode = "0x70"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_right=True,
        )

        # Bowl (open on the left, same as b)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            dc.hx,
            dc.hy,
            taper=dc.taper,
            side="left",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Left descender stem
        draw_rect(pen, b.x1, dc.descent, b.x1 + dc.stroke_x - dc.gap, dc.x_height)
        draw_rect(pen, b.x1, y1, b.x1 + dc.stroke_x, y2)
