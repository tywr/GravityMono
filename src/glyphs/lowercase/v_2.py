from glyphs import Glyph
from draw.rect import draw_rect
from draw.square_corner import draw_square_corner
from draw.corner import draw_corner


class LowercaseV2Glyph(Glyph):
    name = "lowercase_v_2"
    default_italic = True
    unicode = "0x76"
    offset = 0
    width_ratio = 1.15
    stroke_ratio = 0.96
    overlap = 0.33
    lower_section_height = 1.2
    tail_ratio = 0.2
    loop_ratio = 0.66
    hx_ratio = 0.75

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        xt = b.x1 + self.tail_ratio * b.width
        xt2 = b.x2 - self.tail_ratio * b.width - dc.stroke_x
        hx = self.hx_ratio * b.hx

        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, xt, b.y2)
        draw_rect(pen, xt, b.y1, xt + dc.stroke_x, b.y2)
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.ymid,
            xt + dc.stroke_x,
            b.y1,
            hx,
            b.hy,
            orientation="bottom-left",
        )
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.ymid,
            xt2,
            b.y2,
            orientation="top-left",
        )
