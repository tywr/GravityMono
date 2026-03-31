from config import FontConfig as fc
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph


def draw_c(
    pen,
    stroke: int,
):
    offset = 0
    width = 320
    hx = 200
    hy = 230
    opening = 0.5

    x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
    y1 = -fc.overshoot
    x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
    y2 = fc.x_height + fc.overshoot
    xmid = x1 + (x2 - x1) / 2

    loop_glyph = ufoLib2.objects.Glyph()
    draw_superellipse_loop(
        loop_glyph.getPen(), stroke, x1, y1, x2, y2, hx, hy
    )

    cut_glyph = ufoLib2.objects.Glyph()
    draw_rect(
        cut_glyph.getPen(),
        xmid,
        fc.x_height * (1 - opening) / 2,
        xmid + fc.width / 2,
        fc.x_height * (1 + opening) / 2,
    )

    result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
    result.draw(pen)

