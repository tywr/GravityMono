from math import tan
from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class AmpersandGlyph(Glyph):
    name = "ampersand"
    unicode = "0x26"
    offset = 0
    width_ratio = 1.2
    upper_width = 0.8
    upper_height = 0.4
    lower_height = 0.6
    hook_ratio = 0.1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )

        h = self.upper_height * b.height
        w = self.upper_width * b.width
        xu1, xu2 = b.xmid - w / 2, b.xmid + w / 2
        yu1, yu2 = b.y2 - h, b.y2
        hux, huy = b.hx * w / b.width, b.hy * h / b.height

        params = draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xu1,
            yu1,
            xu2,
            yu2,
            hux,
            huy,
            cut="bottom",
        )

        xj = xu1 + self.hook_ratio * w
        (_, y1), (_, y2) = params["outer"].intersection_x(x=xj)
        yj = min(y1, y2)

        # Draw the parallelogramm to the bottom right
        theta, delta = draw_parallelogramm(
            pen, dc.stroke_x, dc.stroke_y, b.x2, b.y1, xj, yj, direction="top-left"
        )

        # Draw the curve to the intersection
        hy = (0.5 * yu1 + 0.5 * yu2 - yj) - tan(theta) * (xj - xu1)
        pen.moveTo((xu1, 0.5 * yu1 + 0.5 * yu2))
        pen.curveTo(
            (xu1, 0.5 * yu1 + 0.5 * yu2 - hy),
            (xj, yj),
            (xj, yj),
        )
        pen.lineTo((xj + delta, yj))
        pen.curveTo(
            (xj + delta, yj),
            (xu1 + dc.stroke_x, 0.5 * yu1 + 0.5 * yu2 - hy),
            (xu1 + dc.stroke_x, 0.5 * yu1 + 0.5 * yu2),
        )
        pen.closePath()
