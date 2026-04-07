import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.superellipse_loop import draw_superellipse_loop


class ThreeGlyph(NumberGlyph):
    name = "three"
    unicode = "0x33"
    offset = 0
    mid_ratio_y = 0.52
    mid_ratio_x = 0.35
    junction_ratio = 0.25

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        xj = b.x1 + self.junction_ratio * b.width
        ymid = b.y1 + self.mid_ratio_y * b.height
        xmid = b.x1 + self.mid_ratio_x * b.width

        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)


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
        draw_rect(
            cut_glyph.getPen(),
            b.x1,
            (ymid + dc.stroke_y) / 2,
            xj,
            ymid + dc.stroke_y,
        )

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Reach to middle
        (_, y1), (_, y2) = params["inner"].intersection_x(x=xj)
        yj = max(y1, y2)

        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xj,
            yj,
            b.x2,
            b.y2,
        )
