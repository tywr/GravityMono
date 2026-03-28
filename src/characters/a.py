import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o
from shapes.flat_hook import flat_hook


def draw_a(pen, font_config: FontConfig, stroke: int):
    """Draw an 'a' starting from a short tapered 'o' loop."""
    loop_height = FontConfig.A_LOOP_HEIGHT * FontConfig.X_HEIGHT

    rec = RecordingPen()
    draw_o(
        rec,
        font_config=font_config,
        stroke=stroke,
        taper="right",
        taper_ratio=FontConfig.TAPER_RATIO,
        height=loop_height,
    )

    path = pathops.Path()
    rec.replay(path.getPen())

    # Cut the top-right quarter: above loop mid-height, right of center
    cut = pathops.Path()
    cp = cut.getPen()
    cp.moveTo((FontConfig.WIDTH / 2, loop_height))
    cp.lineTo((FontConfig.WIDTH / 2, loop_height / 2))
    cp.lineTo((FontConfig.WIDTH + 50, loop_height / 2))
    cp.lineTo((FontConfig.WIDTH + 50, loop_height))
    cp.closePath()

    result = pathops.op(path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Horizontal bar extending from cut point to the right edge of the letter
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    bar = pathops.Path()
    bp = bar.getPen()
    bar_center = loop_height - stroke / 2
    bp.moveTo((FontConfig.WIDTH / 2, bar_center - stroke / 2))
    bp.lineTo((FontConfig.WIDTH / 2, bar_center + stroke / 2))
    bp.lineTo((outer_right, bar_center + stroke / 2))
    bp.lineTo((outer_right, bar_center - stroke / 2))
    bp.closePath()

    result = pathops.op(result, bar, pathops.PathOp.UNION, fix_winding=True)

    # Flat hook: right stem curving at top-left
    hook_corner_y = FontConfig.X_HEIGHT
    hook = pathops.Path()
    hook_pen = hook.getPen()
    flat_hook(
        hook_pen,
        corner_x=outer_right,
        corner_y=hook_corner_y,
        vertical_end=0,
        horizontal_end=FontConfig.WIDTH / 2
        - (FontConfig.A_TAIL_RATIO * FontConfig.X_WIDTH) / 2,
        radius=FontConfig.HOOK_RADIUS,
        stroke=stroke,
    )

    result = pathops.op(result, hook, pathops.PathOp.UNION, fix_winding=True)

    result.draw(pen)
