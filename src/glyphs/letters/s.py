from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.cross_curve import draw_cross_curve


class LowercaseSGlyph(Glyph):
    name = "s"
    unicode = "0x73"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width + 2 * fc.h_overshoot
        hx = fc.hx
        hy = fc.hy / 2

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        xmid = x1 + (x2 - x1) / 2
        ymid = y1 + (y2 - y1) / 2

        # Bottom arch
        draw_superellipse_loop(pen, stroke, x1, y1, x2, ymid, hx, hy, cut="top")
        # Upper arch
        draw_superellipse_loop(pen, stroke, x1, ymid, x2, y2, hx, hy, cut="bottom")
        # Upper middle corner
        draw_cross_curve(
            pen,
            stroke,
            x1,
            y1 + (y2 - y1) / 4,
            x2,
            y1 + 3 * (y2 - y1) / 4,
            hx / 2,
            hy,
            invert=True
        )
