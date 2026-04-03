from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect
from shapes.corner import draw_corner


class LowercaseGGlyph(Glyph):
    name = "lowercase_g"
    unicode = "0x67"
    offset = 15
    corner_width = 220
    corner_hx = 100
    corner_hy = 200
    tail_offset = 20  # Y-axis offset of the tail above the descender line

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )

        # Bowl (open on the right, mirrored from b)
        draw_superellipse_arch(
            pen,
            dc.stroke,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            dent=dc.dent + dc.v_overshoot,
            side="right",
        )
        # Right stem with gap at baseline and dent inset
        draw_rect(pen, b.x2 - dc.stroke + dc.gap, 0, b.x2, dc.x_height)
        draw_rect(pen, b.x2 - dc.stroke, dc.dent, b.x2, dc.x_height - dc.dent)

        # Corner curving down-left into the descender
        draw_corner(
            pen,
            dc.stroke - dc.gap,
            b.x2,
            0,
            b.x2 - b.width / 2,
            dc.descent + self.tail_offset,
            b.hx * 0.5,
            b.hy,
            orientation="bottom-left",
        )
        # Horizontal tail along the descender
        draw_rect(
            pen,
            b.x1 + dc.stroke / 2,
            dc.descent + self.tail_offset,
            b.x2 - b.width / 2,
            dc.descent + self.tail_offset + dc.stroke - dc.gap,
        )
