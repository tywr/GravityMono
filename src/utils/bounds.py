from dataclasses import dataclass


@dataclass
class BodyBounds:
    """
    Represents the geometric envelope of a glyph body — a rectangle defined
    by its bottom-left (x1, y1) and top-right (x2, y2) corners, along with
    the superellipse curve radii (hx, hy) scaled to that body's dimensions.

    Produced by DrawConfig.body_bounds(). Used by glyph drawing functions
    to position and scale shapes consistently within the body region.

    Attributes:
        x1, y1: Bottom-left corner of the body rectangle.
        x2, y2: Top-right corner of the body rectangle.
        hx, hy: Superellipse curve radii, scaled to the body size.
        width:  Horizontal span (x2 - x1).
        height: Vertical span (y2 - y1).
        xmid:   Horizontal center.
        ymid:   Vertical center.
    """

    x1: float
    x2: float
    y1: float
    y2: float

    def __repr__(self):
        return f"BodyBounds(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2}, hx={self.hx}, hy={self.hy})"

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def xmid(self) -> float:
        return (self.x1 + self.x2) / 2

    @property
    def ymid(self) -> float:
        return (self.y1 + self.y2) / 2
