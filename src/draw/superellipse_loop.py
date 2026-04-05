from shapes.superellipse import Superellipse


def draw_superellipse_loop(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    cut=None,
) -> dict:
    outer_se = Superellipse(x1=x1, y1=y1, x2=x2, y2=y2, hx=hx, hy=hy)
    outer_se.draw(pen, clockwise=False, cut=cut)

    inner_se = outer_se.reduce(
        right=stroke_x, left=stroke_x, top=stroke_y, bottom=stroke_y
    )
    inner_se.draw(pen, clockwise=True, cut=cut)

    return {
        "outer": outer_se,
        "inner": inner_se,
    }
