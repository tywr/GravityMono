from glyphs import Glyph
from draw.polygon import draw_polygon


class CommaGlyph(Glyph):
    name = "comma"
    unicode = "0x2C"
    offset = 0
    width_ratio = 1
    height_ratio = 0.75
    vertical_offset = 0.25
    foot_offset = 0.15
    taper = 0.5
    stroke_ratio = 1.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        h = self.height_ratio * b.height
        sx = self.stroke_ratio * dc.stroke_x
        oy = self.vertical_offset * b.height
        fx = self.foot_offset * b.width

        draw_polygon(
            pen,
            points=[
                (b.xmid - sx / 2, oy),
                (b.xmid + sx / 2, oy),
                (b.xmid + self.taper * sx / 2 - fx, oy - (h - sx)),
                (b.xmid - sx / 2 - fx, oy - h + sx),
            ],
        )
