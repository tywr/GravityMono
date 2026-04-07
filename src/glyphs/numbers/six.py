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
    width_ratio = 1.06
    top_ratio = 0.8

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
        ytop = b.y1 + self.top_ratio * b.height

        # Bottom loop
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="right",
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
            taper=dc.taper,
            side="left",
            cut="bottom",
        )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.y1 + (ymid - b.y1) / 2,
            b.xmid,
            b.y1,
            b.hx,
            b.hy * self.vertical_ratio,
            orientation="bottom-left"
        )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            ytop,
            b.xmid,
            b.y2,
            b.hx,
            b.hy * 2 * (b.y2 - ytop) / b.height,
            orientation="top-left"
        )

        # Cap
        # draw_superellipse_loop(
        #     pen,
        #     dc.stroke_x,
        #     dc.stroke_y,
        #     b.x1,
        #     ytop,
        #     b.x2,
        #     b.y2,
        #     b.hx,
        #     b.hy * self.top_ratio,
        #     cut="bottom",
        # )
