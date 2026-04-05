from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseMGlyph(Glyph):
    name = "lowercase_m"
    unicode = "0x6D"
    offset = 0
    width_ratio = 1.4
    rx = 0.7
    mid_y = 200  # Bottom of the middle stem extension

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )

        # Left arch (x1 to xmid) and store offset
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke,
            b.x1,
            b.y1,
            b.xmid + dc.stroke / 2,
            b.y2,
            dc.hx * self.rx,
            dc.hy,
            dent=dc.dent + dc.v_overshoot,
            side="left",
            cut="m_junction",
        )
        offset = arch_params["offset"]
        # Right arch (xmid to x2)
        draw_superellipse_arch(
            pen,
            dc.stroke,
            b.xmid - dc.stroke / 2 - offset + dc.gap,
            b.y1,
            b.x2,
            b.y2,
            dc.hx * self.rx,
            dc.hy,
            dent=dc.dent + dc.v_overshoot,
            side="left",
            cut="bottom",
        )
        # Left foot
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke - dc.gap, dc.x_height)
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.x_height - dc.dent)
        # Right foot — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke, 0, b.x2, b.ymid)
        # Middle stem extension
        draw_rect(
            pen,
            b.xmid - dc.stroke / 2,
            self.mid_y,
            b.xmid + dc.stroke / 2 - offset + dc.gap,
            dc.x_height - dc.dent,
        )
