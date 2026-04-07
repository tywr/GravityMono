import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.superellipse_loop import draw_superellipse_loop


class FiveGlyph(NumberGlyph):
    name = "five"
    unicode = "0x35"
    offset = 0
    mid_ratio_y = 0.52
    mid_ratio_x = 0.35

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        ymid = b.y1 + self.mid_ratio_y * b.height
        xmid = b.x1 + self.mid_ratio_x * b.width

        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)

        # Bottom loop
        loop_width = (b.x2 - xmid) * 2
        loop_height = ymid + dc.stroke_y - b.y1
        hx = b.hx * loop_width / b.width
        hy = b.hy * loop_height / b.height

        # Half-loop to the bottom
        loop_glyph = ufoLib2.objects.Glyph()
        params = draw_superellipse_loop(
            loop_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x2 - loop_width,
            b.y1,
            b.x2,
            ymid + dc.stroke_y,
            hx,
            hy,
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x2 - loop_width - 10,
            b.y1,
            b.x1,
            ymid + dc.stroke_y,
        )

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Vertical bar
        (_, y1), (_, y2) = params["outer"].intersection_x(x=b.x1)
        yloop = max(y1, y2)
        draw_rect(pen, b.x1, yloop, b.x1 + dc.stroke_x, b.y2)
