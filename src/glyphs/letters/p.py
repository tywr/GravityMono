from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.rect import draw_rect


class LowercasePGlyph(Glyph):
    name = "p"
    unicode = "0x70"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width + fc.h_overshoot
        hx = fc.hx
        hy = fc.hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot

        # Left-ear
        draw_superellipse_ear(
            pen,
            stroke,
            x1,
            y1,
            x2,
            y2,
            hx,
            hy,
            fc.tooth,
            fc.cover,
            side="left",
        )
        # Descender
        draw_rect(pen, x1, fc.descent, x1 + stroke, fc.x_height)
