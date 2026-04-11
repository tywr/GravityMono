from config import FontConfig as fc
from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseA2Glyph(Glyph):
    name = "lowercase_a_2"
    font_feature = {"ss01": 1}
    unicode = "0x61"
    offset = 0
    loop_ratio = 0.6
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
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
            side="right",
        )
        # Stem
        draw_rect(pen, b.x2 - dc.stroke_x + dc.gap, 0, b.x2, b.y2)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x2 - dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)
        draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, y2)
