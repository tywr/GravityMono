from config import FontConfig as fc
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_a(
    pen,
    stroke: int,
):
    x1 = fc.width / 2 - fc.o_width / 2 - stroke / 2
    y1 = 0
    x2 = fc.width / 2 + fc.o_width / 2 + stroke / 2
    y2 = fc.a_loop_ratio * fc.x_height
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
    draw_corner(
        pen,
        stroke,
        x2,
        fc.x_height / 2,
        fc.width / 2,
        fc.x_height,
        fc.o_hx,
        fc.o_hy,
        orientation="top-left",
    )
    draw_rect(pen, x1 + stroke / 2, fc.x_height - stroke, fc.width / 2, fc.x_height)
