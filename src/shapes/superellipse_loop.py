from shapes.superellipse import draw_superellipse


def draw_superellipse_loop(
    pen,
    stroke,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
):
    draw_superellipse(pen, x1, y1, x2, y2, hx, hy, clockwise=False)

    w = (x2 - x1) / 2
    h = (y2 - y1) / 2
    inner_hx = hx * (w - stroke) / w
    inner_hy = hy * (h - stroke) / h

    draw_superellipse(
        pen,
        x1 + stroke,
        y1 + stroke,
        x2 - stroke,
        y2 - stroke,
        inner_hx,
        inner_hy,
        clockwise=True,
    )
