from config import FontConfig as fc
from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class LowercaseBGlyph(Glyph):
    name = "lowercase_b"
    unicode = "0x62"
    offset = 26

    def draw(
        self,
        pen,
        dc,
    ):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_right=True,
        )
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
            side="left",
        )
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x - dc.gap, dc.ascent)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)
        draw_rect(pen, b.x1, y1, b.x1 + dc.stroke_x, y2)
