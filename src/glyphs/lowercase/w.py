from math import atan, cos, sin
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    width_ratio = 400 / 340
    overlap = 40  # Horizontal overlap between the two V shapes at the joint
    joint_ratio = 0.8  # Height of the shared joint as a fraction of x_height
    inner_ratio = 0.6  # Stroke width ratio for the inner branches at the joint

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        half_width = b.width / 2 - dc.stroke / 2
        quarter = half_width / 2

        joint_height = self.joint_ratio * dc.x_height
        xmid1 = b.xmid - dc.window_width / 4 + self.overlap
        xmid2 = b.xmid + dc.window_width / 4 - self.overlap

        branch_h = dc.x_height / 2
        theta = atan(branch_h / quarter)
        x_delta = dc.stroke / sin(theta)
        y_delta = dc.stroke / cos(theta)
        ix_delta = x_delta * self.inner_ratio  # Thinner x_delta for inner branches

        # Left V
        draw_polygon(
            pen,
            points=[
                (xmid1 + ix_delta / 2, 0),  # bottom right (inner, thin)
                (b.xmid + ix_delta / 2, joint_height),
                (b.xmid - ix_delta / 2, joint_height),
                (xmid1, y_delta * self.inner_ratio),
                (xmid1 - quarter + x_delta / 2, dc.x_height),
                (xmid1 - quarter - x_delta / 2, dc.x_height),
                (xmid1 - x_delta / 2, 0),  # bottom left (outer, full)
            ],
        )
        # Right V (mirror of left V)
        draw_polygon(
            pen,
            points=[
                (xmid2 + x_delta / 2, 0),  # bottom right (outer, full)
                (xmid2 + quarter + x_delta / 2, dc.x_height),
                (xmid2 + quarter - x_delta / 2, dc.x_height),
                (xmid2, y_delta * self.inner_ratio),
                (b.xmid + ix_delta / 2, joint_height),
                (b.xmid - ix_delta / 2, joint_height),
                (xmid2 - ix_delta / 2, 0),  # bottom left (inner, thin)
            ],
        )
