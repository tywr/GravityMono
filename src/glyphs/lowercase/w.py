from math import atan, cos, sin
from glyph import Glyph
from shapes.polygon import draw_polygon
from shapes.parallelogramm import draw_parallelogramm


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    overlap = 0.06
    inner_stroke_ratio = 1
    inner_height_ratio = 0.6
    width_ratio = 400 / 340

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)

        ov = self.overlap * b.width
        inner_height = self.inner_height_ratio * b.height
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid + 0.25 * b.width,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid - 0.25 * b.width,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            dc.stroke * self.inner_stroke_ratio,
            b.xmid + 0.25 * b.width - ov + delta,
            0,
            b.xmid - ov,
            inner_height,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            dc.stroke * self.inner_stroke_ratio,
            b.xmid - 0.25 * b.width + ov - delta,
            0,
            b.xmid + ov,
            inner_height,
        )

        # joint_height = self.joint_ratio * dc.x_height
        # xmid1 = b.xmid - dc.window_width / 4 + self.overlap
        # xmid2 = b.xmid + dc.window_width / 4 - self.overlap
        #
        # branch_h = dc.x_height / 2
        # theta = atan(branch_h / quarter)
        # x_delta = dc.stroke / sin(theta)
        # y_delta = dc.stroke / cos(theta)
        # ix_delta = x_delta * self.inner_ratio  # Thinner x_delta for inner branches
        #
        # # Left V
        # draw_polygon(
        #     pen,
        #     points=[
        #         (xmid1 + ix_delta / 2, 0),  # bottom right (inner, thin)
        #         (b.xmid + ix_delta / 2, joint_height),
        #         (b.xmid - ix_delta / 2, joint_height),
        #         (xmid1, y_delta * self.inner_ratio),
        #         (xmid1 - quarter + x_delta / 2, dc.x_height),
        #         (xmid1 - quarter - x_delta / 2, dc.x_height),
        #         (xmid1 - x_delta / 2, 0),  # bottom left (outer, full)
        #     ],
        # )
        # # Right V (mirror of left V)
        # draw_polygon(
        #     pen,
        #     points=[
        #         (xmid2 + x_delta / 2, 0),  # bottom right (outer, full)
        #         (xmid2 + quarter + x_delta / 2, dc.x_height),
        #         (xmid2 + quarter - x_delta / 2, dc.x_height),
        #         (xmid2, y_delta * self.inner_ratio),
        #         (b.xmid + ix_delta / 2, joint_height),
        #         (b.xmid - ix_delta / 2, joint_height),
        #         (xmid2 - ix_delta / 2, 0),  # bottom left (inner, thin)
        #     ],
        # )
