from config import FontConfig as fc
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_a(
    pen,
    stroke: int,
):
    x1 = fc.width / 2 - fc.o_width / 2 - stroke / 2 + fc.a_offset
    y1 = -fc.overshoot
    x2 = fc.width / 2 + fc.o_width / 2 + stroke / 2 + fc.a_offset
    y2 = fc.a_loop_ratio * (fc.x_height + fc.overshoot)
    xmid = x1 + (x2 - x1) / 2

    draw_superellipse_ear(
        pen,
        stroke,
        x1,
        y1,
        x2,
        y2,
        fc.a_hx,
        fc.a_hy,
        fc.tooth,
        fc.cover,
        side="right",
        cut="top"
    )
    draw_rect(pen, x2 - stroke, 0, x2, fc.x_height / 2)
    # Curve to the cap
    draw_corner(
        pen,
        stroke,
        x2,
        fc.x_height / 2,
        xmid,
        fc.x_height,
        fc.o_hx,
        fc.o_hy,
        orientation="top-left",
    )
    # Cap
    draw_rect(pen, x1 + stroke / 4, fc.x_height - stroke, xmid, fc.x_height)
    draw_corner(
        pen,
        stroke,
        x1,
        fc.a_loop_ratio * (fc.x_height + 2 * fc.overshoot) / 2 - fc.overshoot,
        xmid,
        fc.a_loop_ratio * fc.x_height,
        fc.a_hx,
        fc.a_hy,
        orientation="top-right",
    )
    draw_rect(pen, xmid, fc.x_height * fc.a_loop_ratio - stroke, x2 - stroke, fc.x_height * fc.a_loop_ratio)
