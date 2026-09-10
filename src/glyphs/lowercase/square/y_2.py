import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from draw.rect import draw_rect
from draw.arch import draw_arch
from draw.polygon import draw_polygon
from draw.corner import draw_corner
from glyphs.lowercase.square import SquareLowercaseGlyph


class LowercaseY2Glyph(SquareLowercaseGlyph):
    name = "lowercase_y_2"
    unicode = "0x79"
    default_italic = True
    offset = 0

    tail_stroke_x_ratio = 0.96
    tail_stroke_y_ratio = 1.01
    tail_hx_ratio = 1.0
    tail_hy_ratio = 0.7
    tail_offset = 0.15
    cut_ratio = 0.265
    tail_offset = 0.04
    y1_offset = 0.065

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )
        ec = self.extra_cut(dc)
        tsx, tsy = (
            self.tail_stroke_x_ratio * dc.stroke_x,
            self.tail_stroke_y_ratio * dc.stroke_y,
        )
        thx, thy = (
            self.tail_hx_ratio * dc.hx,
            self.tail_hy_ratio * dc.hy,
        )
        y1 = b.y1 + self.y1_offset * b.height
        yl = y1 + self.loop_ratio * b.height

        xt = b.x1 + self.tail_offset * b.width

        yo = 3
        # Bottom arch, cut at top (only lower half drawn)
        draw_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            y1,
            b.x2,
            yl,
            self.hx_ratio * b.hx,
            self.hy_ratio * b.hy,
            taper=self.taper * dc.taper,
            side="right",
            cut="top",
        )

        # Right stem — full x_height
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, dc.x_height)

        # Left stem — starts from arch midpoint
        draw_rect(pen, b.x1, (yl + y1) / 2, b.x1 + dc.stroke_x, dc.x_height)

        # Corner curving down-left into the descender
        draw_corner(
            pen,
            dc.stroke_x,
            tsy,
            b.x2,
            0,
            b.xmid,
            dc.descent - dc.v_overshoot,
            thx,
            thy,
            orientation="bottom-left",
        )

        glyph = ufoLib2.objects.Glyph()
        draw_corner(
            glyph.getPen(),
            tsx,
            tsy,
            xt,
            0,
            b.xmid,
            dc.descent - dc.v_overshoot,
            thx,
            thy,
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1 - 10,
            dc.descent - dc.v_overshoot + b.height * self.cut_ratio + ec,
            b.xmid,
            b.ymid,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
