from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.corner import draw_corner


class NineGlyph(NumberGlyph):
    name = "nine"
    unicode = "0x39"
    offset = 0
    vertical_ratio = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        ymid = b.y2 - self.vertical_ratio * b.height
        hy = b.hy * 4 * (ymid - b.y1) / b.height
        hx = 2 * b.hx

        # Upper loop
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            cut="bottom",
        )
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            side="right",
            cut="top",
        )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.y2 - (b.y2 - ymid) / 2,
            b.x1 + dc.stroke_x / 2,
            b.y1,
            hx,
            hy,
            orientation="bottom-left",
        )
