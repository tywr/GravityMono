from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.corner import draw_corner


class SixGlyph(NumberGlyph):
    name = "six"
    unicode = "0x36"
    offset = 0
    vertical_ratio = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        ymid = b.y1 + self.vertical_ratio * b.height
        hy = b.hy * 4 * (b.y2 - ymid) / b.height
        hx = 2 * b.hx

        # Bottom loop
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.vertical_ratio,
            cut="top",
        )
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.vertical_ratio,
            side="left",
            cut="bottom",
        )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1 + (ymid - b.y1) / 2,
            b.x2 - dc.stroke_x / 2,
            b.y2,
            hx,
            hy,
            orientation="top-right",
        )
