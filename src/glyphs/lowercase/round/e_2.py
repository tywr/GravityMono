from draw.loop import draw_loop
from draw.corner import draw_corner
from draw.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs.lowercase.round import RoundLowercaseGlyph


class LowercaseE2Glyph(RoundLowercaseGlyph):
    name = "lowercase_e_2"
    unicode = "0x65"
    default_italic = True
    offset = 5
    width_ratio = 1
    mid_height = 0.52
    thinning = 1
    tail_offset = 0.00
    tail_height = 0.268
    right_hy_ratio = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )
        ec = self.extra_cut(dc)
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        yo = b.y1 + self.tail_height * b.height + ec
        ymid = b.y1 + self.mid_height * b.height
        xt = b.x2 + self.tail_offset * b.width
        rhy = self.right_hy_ratio * b.hy

        # Half-left as the o-shape
        draw_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="right",
        )

        draw_corner(
            pen,
            sx,
            sy,
            b.x2,
            (b.y2 + ymid) / 2,
            b.xmid,
            b.y2,
            b.hx,
            rhy,
            orientation="top-left",
        )

        draw_corner(
            pen,
            sx,
            dc.stroke_alt,
            b.x2,
            (b.y2 + ymid) / 2,
            b.xmid,
            ymid - dc.stroke_alt / 2,
            b.width / 2,
            rhy,
            orientation="bottom-left",
        )

        loop_glyph = ufoLib2.objects.Glyph()
        draw_corner(
            loop_glyph.getPen(),
            sx * self.thinning,
            sy,
            xt,
            b.ymid,
            b.xmid,
            b.y1,
            b.hx,
            b.hy,
            orientation="bottom-left",
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid,
            yo,
            b.xmid + b.width,
            b.ymid,
        )
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        draw_rect(
            pen,
            b.x1 + sx / 2,
            ymid,
            b.xmid,
            ymid + dc.stroke_alt / 2,
        )
        draw_rect(
            pen,
            b.x1 + sx / 2,
            ymid - dc.stroke_alt / 2,
            b.xmid,
            max(ymid, b.ymid),
        )
