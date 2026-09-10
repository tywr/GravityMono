from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.square_corner import draw_square_corner
from glyphs.lowercase.single_story import SingleStoryLowercaseGlyph


class LowercaseA2Glyph(SingleStoryLowercaseGlyph):
    name = "lowercase_a_2"
    default_italic = True
    unicode = "0x61"
    offset = -10
    tail_offset = 0.03

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy
        bsx, bsy = (
            self.bowl_stroke_x_ratio * dc.stroke_x,
            self.bowl_stroke_y_ratio * dc.stroke_y,
        )
        dx = bsx - dc.stroke_x
        # ot = self.tail_offset * b.width

        draw_arch(
            pen,
            bsx,
            bsy,
            b.x1,
            b.y1,
            b.x2 + dx,
            b.y2,
            hx,
            hy,
            taper=dc.taper * self.taper,
            side="right",
        )

        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, dc.x_height)
        # draw_square_corner(
        #     pen,
        #     dc.stroke_x,
        #     dc.stroke_y,
        #     b.x2 - dc.stroke_x,
        #     b.y2,
        #     dc.window_width - ot,
        #     b.y1,
        #     orientation="bottom-right",
        # )
