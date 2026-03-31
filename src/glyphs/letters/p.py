from config import FontConfig as fc
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.rect import draw_rect


def draw_p(
    pen,
    stroke: int,
):
    offset = 0
    width = 320
    hx = 200
    hy = 230

    x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
    y1 = -fc.overshoot
    x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
    y2 = fc.x_height + fc.overshoot

    # Left-ear
    draw_superellipse_ear(
        pen,
        stroke,
        x1,
        y1,
        x2,
        y2,
        hx,
        hy,
        fc.tooth,
        fc.cover,
        side="left",
    )
    # Descender
    draw_rect(pen, x1, fc.descent, x1 + stroke, fc.x_height)
