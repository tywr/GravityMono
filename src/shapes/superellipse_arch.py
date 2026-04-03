import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from shapes.rect import draw_rect
from shapes.superellipse import draw_superellipse
from utils.intersection import find_offset, find_offset_horizontal


def draw_superellipse_arch(
    pen,
    stroke,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    dent=70,
    side="right",
    cut=None,
    offset=None,
):
    w, h = (x2 - x1) / 2, (y2 - y1) / 2
    y_mid = y1 + h

    if offset is None:
        if side in ("left", "right"):
            offset = find_offset(x1, y1, x2, y2, hx, hy, stroke, dent)
        else:
            offset = find_offset_horizontal(x1, y1, x2, y2, hx, hy, stroke, dent)

    # Outer box
    ox1 = x1 + (stroke - offset if side == "left" else 0)
    oy1 = y1 + (stroke - offset if side == "bottom" else 0)
    ox2 = x2 - (stroke - offset if side == "right" else 0)
    oy2 = y2 - (stroke - offset if side == "top" else 0)
    ohx = hx * (w - offset) / w
    ohy = hy * (h - offset) / h

    ihx = hx * (w - stroke) / w
    ihy = hy * (h - stroke) / h

    # Inner box
    ix1 = x1 + stroke
    iy1 = y1 + stroke
    ix2 = x2 - stroke
    iy2 = y2 - stroke

    loop_glyph = ufoLib2.objects.Glyph()
    draw_superellipse(
        loop_glyph.getPen(), ox1, oy1, ox2, oy2, ohx, ohy, clockwise=False
    )
    draw_superellipse(loop_glyph.getPen(), ix1, iy1, ix2, iy2, ihx, ihy, clockwise=True)

    if cut == "bottom":
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1 - 10, y1, x2 + 10, y_mid)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "top":
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1 - 10, y_mid, x2 + 10, y2)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "left":
        x_mid = x1 + w
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1, y1 - 10, x_mid, y2 + 10)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "right":
        x_mid = x1 + w
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x_mid, y1 - 10, x2, y2 + 10)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    else:
        result = BooleanGlyph(loop_glyph)
        result.draw(pen)

    # # Draw the covers
    # xl = junction_x if side == "left" else junction_x - stroke / 8
    # xr = junction_x if side == "right" else junction_x + stroke / 8
    # y_low = y1 + dent - stroke / 2
    # y_high = y2 - dent + stroke / 2
    # if cut != "bottom":
    #     draw_rect(pen, xl, y_low - cover, xr, y_low)
    # if cut != "top":
    #     draw_rect(pen, xl, y_high, xr, y_high + cover)
