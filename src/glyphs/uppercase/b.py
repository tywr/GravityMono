from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.rect import draw_rect
from utils.intersection import intersection_superellipses


class UppercaseBGlyph(Glyph):
    name = "uppercase_b"
    unicode = "0x42"
    offset = 0
    loop_ratio = 1  # Horizontal split between left stem and loops
    upper_ratio = 0.9  # Upper loop width as a fraction of the lower loop width

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="ascent",
            overshoot_right=True,
        )
        lower_x1 = b.x1 + (1 - self.loop_ratio) * b.width
        lower_x2 = b.x2
        lower_width = lower_x2 - lower_x1
        upper_width = self.upper_ratio * lower_width
        delta = lower_width - upper_width
        upper_x1 = lower_x1 + delta / 2
        upper_x2 = lower_x2 - delta / 2
        # gap_x = upper_x2 - dc.stroke + (lower_x2 - upper_x2) * 0.63
        gap_x = upper_x2 - dc.stroke + 2.5 * dc.gap

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.ascent)

        # Upper loop (narrower, displaced left)
        arch1 = draw_superellipse_arch(
            pen,
            dc.stroke,
            upper_x1,
            b.ymid - dc.stroke / 2,
            upper_x2,
            b.y2,
            dc.hx,
            dc.hy,
            offset=0.75 * dc.stroke,
            side="bottom",
            cut="left",
        )
        # Lower loop (full width)
        arch2 = draw_superellipse_arch(
            pen,
            dc.stroke,
            lower_x1,
            0,
            lower_x2,
            b.ymid + dc.stroke / 2,
            dc.hx,
            dc.hy,
            offset=0.75 * dc.stroke,
            side="top",
            cut="left",
        )

        # Compute the intersection of the two outer superellipses
        # where there would be a dc.gap sized gap
        intersection_x = max(
            intersection_superellipses(
                arch1["outer"], arch2["outer"].translate(dy=dc.gap)
            ),
            key=lambda x: x[0],
        )[0]

        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke, upper_x2 - upper_width / 2, b.y2)
        draw_rect(pen, b.x1, 0, b.x2 - lower_width / 2, dc.stroke)
        draw_rect(
            pen,
            b.x1,
            b.ymid - dc.stroke / 2,
            intersection_x,
            b.ymid + dc.stroke / 2,
        )
