from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class UppercaseBGlyph(Glyph):
    name = "uppercase_b"
    unicode = "0x42"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 26
        width = 420
        offset = 3 * stroke / 4
        overlap = 0
        upper_loop_ratio = 0.95
        hx = fc.side_hx
        hy = fc.side_hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = 0
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset + fc.h_overshoot
        y2 = fc.ascent
        ymid = y1 + (y2 - y1) / 2

        draw_rect(pen, x1, 0, x1 + stroke, fc.ascent)
        draw_superellipse_arch(
            pen,
            stroke,
            x1 - upper_loop_ratio * width,
            ymid - stroke / 2 - overlap,
            x1 + upper_loop_ratio * width,
            y2,
            hx * upper_loop_ratio,
            hy,
            offset=offset,
            side="bottom",
            cut="left",
        )
        draw_superellipse_arch(
            pen,
            stroke,
            x1 - width,
            0,
            x1 + width,
            ymid + stroke / 2 + overlap,
            hx,
            hy,
            offset=offset,
            side="top",
            cut="left",
        )
