from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = 0

    def draw(self, pen, dc):
        loop_ratio = 0.6

        b = dc.body_boundaries(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_left=True,
        )
        # Add dampening on hx to keep ratio with the dent
        hx, hy = dc.hx * 0.8, dc.hy * loop_ratio

        # Lower half half of the bowl
        draw_superellipse_arch(
            pen,
            dc.stroke,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * loop_ratio,
            hx,
            hy,
            tooth=dc.dent + dc.v_overshoot,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            dc.stroke,
            b.x1,
            b.y1 + b.height * loop_ratio / 2,
            b.xmid,
            b.y1 + b.height * loop_ratio,
            hx,
            hy,
            orientation="top-right",
        )
        draw_rect(
            pen,
            b.xmid,
            b.y1 + b.height * loop_ratio - dc.stroke,
            b.x2 - dc.stroke,
            b.y1 + b.height * loop_ratio,
        )
        # Curve to the cap
        draw_corner(
            pen,
            dc.stroke,
            b.x2,
            fc.x_height / 2,
            b.xmid,
            fc.x_height,
            b.hy,
            b.hy,
            orientation="top-left",
        )
        # Cap
        draw_rect(
            pen,
            b.x1 + dc.stroke / 2,
            fc.x_height - dc.stroke,
            b.xmid,
            fc.x_height,
        )

        # Stem
        draw_rect(
            pen,
            b.x2 - dc.stroke + dc.gap,
            0,
            b.x2,
            loop_ratio * (fc.x_height + 2 * dc.v_overshoot) - dc.v_overshoot,
        )
        draw_rect(
            pen,
            b.x2 - dc.stroke,
            dc.dent,
            b.x2,
            loop_ratio * (fc.x_height + 2 * dc.v_overshoot) - dc.v_overshoot,
        )
