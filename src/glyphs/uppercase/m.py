from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class UppercaseMGlyph(UppercaseGlyph):
    name = "uppercase_m"
    unicode = "0x4D"
    offset = 0
    width_ratio = 1.2
    overlap = 0.5
    overlap_middle = 0.4
    depth = 0.6
    stroke_thinning = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        st = self.stroke_thinning
        ov = self.overlap * dc.stroke_x
        ovm = self.overlap_middle * dc.stroke_x
        ymid = (1 - self.depth) * b.height

        # Vertical stems
        draw_rect(pen, b.x1, b.y1, b.x1 + dc.stroke_x, b.y2)
        draw_rect(pen, b.x2 - dc.stroke_x, b.y1, b.x2, b.y2)

        # Branches
        draw_parallelogramm(
            pen, st * dc.stroke_x, st * dc.stroke_y, b.xmid - ovm, ymid, b.x2 - ov, b.y2
        )
        draw_parallelogramm(
            pen,
            st * dc.stroke_x,
            st * dc.stroke_y,
            b.xmid + ovm,
            ymid,
            b.x1 + ov,
            b.y2,
            direction="top-left",
        )
