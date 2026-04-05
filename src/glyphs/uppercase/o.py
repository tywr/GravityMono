import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.rect import draw_rect


class UppercaseCGlyph(Glyph):
    name = "uppercase_o"
    unicode = "0x4F"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="ascent",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        draw_superellipse_loop(pen, dc.stroke, b.x1, b.y1, b.x2, b.y2, dc.hx, dc.hy)
