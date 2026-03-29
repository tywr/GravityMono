from config import FontConfig as fc
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_f(
    pen,
    stroke: int,
):
    xmid = fc.width / 2 + fc.f_offset
    draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
    draw_corner(
        pen,
        stroke,
        xmid - stroke / 2,
        fc.x_height,
        xmid + fc.o_width / 2,
        fc.ascent,
        fc.a_hx,
        fc.a_hy,
        orientation="top-right",
    )
    draw_rect(
        pen,
        xmid - fc.f_len_left - stroke / 2,
        fc.bar_height - stroke,
        xmid + fc.f_len_right + stroke / 2,
        fc.bar_height,
    )
    if fc.f_len_right > fc.o_width / 2:
        draw_rect(
            pen,
            xmid + fc.o_width / 2,
            fc.ascent - stroke,
            xmid + fc.f_len_right + stroke / 2,
            fc.ascent,
        )
