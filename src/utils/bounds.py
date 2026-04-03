from dataclasses import dataclass


@dataclass
class Bounds:
    """
    Abstraction class to store the coordinates for:
        - x1, y1: Bottom-left start of rectangle
        - x2, y2: Top-right end of rectangle
        - ohx, ohy: Radius for corresponding superellipse
    """

    x1: float
    x2: float
    y1: float
    y2: float
    hx: float
    hy: float

    def __repr__(self):
        return f"Bounds(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2}, hx={self.hx}, hy={self.hy})"

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
