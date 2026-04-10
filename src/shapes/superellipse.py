from utils.intersection import intersection_superellipses, intersection_superellipse_x, intersection_superellipse_y


class Superellipse:
    __slots__ = ("x1", "y1", "x2", "y2", "hx", "hy")

    def __init__(self, x1, y1, x2, y2, hx, hy):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.hx = hx
        self.hy = hy

    def translate(self, dx=0, dy=0):
        return Superellipse(
            self.x1 + dx,
            self.y1 + dy,
            self.x2 + dx,
            self.y2 + dy,
            self.hx,
            self.hy,
        )

    def reduce(self, right=0, left=0, top=0, bottom=0):
        old_w = self.x2 - self.x1
        old_h = self.y2 - self.y1

        new_x1 = self.x1 + left
        new_y1 = self.y1 + bottom
        new_x2 = self.x2 - right
        new_y2 = self.y2 - top

        new_w = new_x2 - new_x1
        new_h = new_y2 - new_y1

        sx = new_w / old_w if old_w else 1
        sy = new_h / old_h if old_h else 1

        return Superellipse(
            new_x1,
            new_y1,
            new_x2,
            new_y2,
            self.hx * sx,
            self.hy * sy,
        )

    def expand(self, right=0, left=0, top=0, bottom=0):
        old_w = self.x2 + self.x1
        old_h = self.y2 + self.y1

        new_x1 = self.x1 - left
        new_y1 = self.y1 - bottom
        new_x2 = self.x2 + right
        new_y2 = self.y2 + top

        new_w = new_x2 + new_x1
        new_h = new_y2 + new_y1

        sx = new_w / old_w if old_w else 1
        sy = new_h / old_h if old_h else 1

        return Superellipse(
            new_x1,
            new_y1,
            new_x2,
            new_y2,
            self.hx * sx,
            self.hy * sy,
        )

    def intersection_superellipse(self, se: "Superellipse", tol=1e-1):
        return intersection_superellipses(self, se, tol=tol)

    def intersection_x(self, x, tol=1e-3):
        return intersection_superellipse_x(self, x, tol=tol)

    def intersection_y(self, y, tol=1e-3):
        return intersection_superellipse_y(self, y, tol=tol)

    def draw(self, pen, cut=None, clockwise=False):
        mid_x = (self.x1 + self.x2) / 2
        mid_y = (self.y1 + self.y2) / 2

        if clockwise:
            # Winding: left → top → right → bottom → left
            if cut is None:
                pen.moveTo((self.x1, mid_y))
                pen.curveTo(
                    (self.x1, mid_y + self.hy),
                    (mid_x - self.hx, self.y2),
                    (mid_x, self.y2),
                )
                pen.curveTo(
                    (mid_x + self.hx, self.y2),
                    (self.x2, mid_y + self.hy),
                    (self.x2, mid_y),
                )
                pen.curveTo(
                    (self.x2, mid_y - self.hy),
                    (mid_x + self.hx, self.y1),
                    (mid_x, self.y1),
                )
                pen.curveTo(
                    (mid_x - self.hx, self.y1),
                    (self.x1, mid_y - self.hy),
                    (self.x1, mid_y),
                )
            elif cut == "top":
                pen.moveTo((self.x2, mid_y))
                pen.curveTo(
                    (self.x2, mid_y - self.hy),
                    (mid_x + self.hx, self.y1),
                    (mid_x, self.y1),
                )
                pen.curveTo(
                    (mid_x - self.hx, self.y1),
                    (self.x1, mid_y - self.hy),
                    (self.x1, mid_y),
                )
            elif cut == "bottom":
                pen.moveTo((self.x1, mid_y))
                pen.curveTo(
                    (self.x1, mid_y + self.hy),
                    (mid_x - self.hx, self.y2),
                    (mid_x, self.y2),
                )
                pen.curveTo(
                    (mid_x + self.hx, self.y2),
                    (self.x2, mid_y + self.hy),
                    (self.x2, mid_y),
                )
            elif cut == "right":
                pen.moveTo((mid_x, self.y1))
                pen.curveTo(
                    (mid_x - self.hx, self.y1),
                    (self.x1, mid_y - self.hy),
                    (self.x1, mid_y),
                )
                pen.curveTo(
                    (self.x1, mid_y + self.hy),
                    (mid_x - self.hx, self.y2),
                    (mid_x, self.y2),
                )
            elif cut == "left":
                pen.moveTo((mid_x, self.y2))
                pen.curveTo(
                    (mid_x + self.hx, self.y2),
                    (self.x2, mid_y + self.hy),
                    (self.x2, mid_y),
                )
                pen.curveTo(
                    (self.x2, mid_y - self.hy),
                    (mid_x + self.hx, self.y1),
                    (mid_x, self.y1),
                )
        else:
            # Winding: right → top → left → bottom → right
            if cut is None:
                pen.moveTo((self.x2, mid_y))
                pen.curveTo(
                    (self.x2, mid_y + self.hy),
                    (mid_x + self.hx, self.y2),
                    (mid_x, self.y2),
                )
                pen.curveTo(
                    (mid_x - self.hx, self.y2),
                    (self.x1, mid_y + self.hy),
                    (self.x1, mid_y),
                )
                pen.curveTo(
                    (self.x1, mid_y - self.hy),
                    (mid_x - self.hx, self.y1),
                    (mid_x, self.y1),
                )
                pen.curveTo(
                    (mid_x + self.hx, self.y1),
                    (self.x2, mid_y - self.hy),
                    (self.x2, mid_y),
                )
            elif cut == "top":
                pen.moveTo((self.x1, mid_y))
                pen.curveTo(
                    (self.x1, mid_y - self.hy),
                    (mid_x - self.hx, self.y1),
                    (mid_x, self.y1),
                )
                pen.curveTo(
                    (mid_x + self.hx, self.y1),
                    (self.x2, mid_y - self.hy),
                    (self.x2, mid_y),
                )
            elif cut == "bottom":
                pen.moveTo((self.x2, mid_y))
                pen.curveTo(
                    (self.x2, mid_y + self.hy),
                    (mid_x + self.hx, self.y2),
                    (mid_x, self.y2),
                )
                pen.curveTo(
                    (mid_x - self.hx, self.y2),
                    (self.x1, mid_y + self.hy),
                    (self.x1, mid_y),
                )
            elif cut == "right":
                pen.moveTo((mid_x, self.y2))
                pen.curveTo(
                    (mid_x - self.hx, self.y2),
                    (self.x1, mid_y + self.hy),
                    (self.x1, mid_y),
                )
                pen.curveTo(
                    (self.x1, mid_y - self.hy),
                    (mid_x - self.hx, self.y1),
                    (mid_x, self.y1),
                )
            elif cut == "left":
                pen.moveTo((mid_x, self.y1))
                pen.curveTo(
                    (mid_x + self.hx, self.y1),
                    (self.x2, mid_y - self.hy),
                    (self.x2, mid_y),
                )
                pen.curveTo(
                    (self.x2, mid_y + self.hy),
                    (mid_x + self.hx, self.y2),
                    (mid_x, self.y2),
                )

        pen.closePath()
        return self
