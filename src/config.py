from dataclasses import dataclass
from utils.bounds import Bounds


@dataclass
class FontConfig:
    family_name: str = "Kassiopea"

    units_per_em: int = 1000
    window_ascent: int = 1020
    window_descent: int = -300
    window_width: int = 600
    ascent: int = 730
    descent: int = -200
    cap: int = 730
    x_height: int = 550
    accent: int = 710


@dataclass
class DrawConfig(FontConfig):
    # Default parameters
    stroke: int = 90
    width: int = 340
    hx: int = 200
    hy: int = 200
    dent: int = 68
    gap: int = 5
    v_overshoot: int = 10
    h_overshoot: int = 5

    def body_boundaries(
        self,
        offset: int,
        overshoot_left=False,
        overshoot_right=False,
        overshoot_top=False,
        overshoot_bottom=False,
        height="x_height",
    ):
        """
        Abstraction for storing common metrics relative to the body
        of a character. For most lowercase, the boundaries are
        a centered rectangle of length `width` and of height `x-height`.
        For most capital letters, it's a centered rectangle of length
        `width` of a of height `ascent`.
        """
        if height not in ["x_height", "ascent"]:
            raise ValueError(f"Value {height} should be `x_height` or `ascent`")
        x1 = self.window_width / 2 - self.width / 2 - self.stroke / 2 + offset
        y1 = 0
        x2 = self.window_width / 2 + self.width / 2 + self.stroke / 2 + offset
        y2 = getattr(self, height)

        # Add horizontal overshoots
        if overshoot_left:
            x1 -= self.h_overshoot
        if overshoot_right:
            x2 += self.h_overshoot

        if overshoot_bottom:
            y1 -= self.v_overshoot
        if overshoot_top:
            y2 += self.v_overshoot

        hx = self.hx * (x2 - x1 - self.stroke) / self.width
        hy = self.hy * (y2 - y1 - self.stroke) / self.x_height
        return Bounds(x1=x1, y1=y1, x2=x2, y2=y2, hx=hx, hy=hy)
