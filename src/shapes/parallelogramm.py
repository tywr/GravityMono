from math import sqrt, atan2
from shapes.polygon import draw_polygon


def draw_parallelogramm(pen, stroke, x1, y1, x2, y2, direction="top"):
    w = max(x2, x1) - min(x2, x1)
    h = max(y2, y1) - min(y2, y1)
    s = stroke
    delta = (s * (h * sqrt(w**2 + h**2 - s**2) - s * w)) / (h**2 - s**2)
    theta = atan2(h, w - delta)
    if direction == "top":
        draw_polygon(
            pen, points=[(x1, y1), (x1 + delta, y1), (x2, y2), (x2 - delta, y2)]
        )
        return theta, delta
    elif direction == "bottom":
        draw_polygon(
            pen, points=[(x2 - delta, y2), (x2, y2), (x1 + delta, y1), (x1, y1)]
        )
        return theta, delta
    else:
        raise ValueError("Value should be either `top` or `bottom`")
