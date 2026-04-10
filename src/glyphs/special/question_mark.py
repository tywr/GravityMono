from glyphs import Glyph
from draw.rect import draw_rect
from draw.superellipse_loop import draw_superellipse_loop


class QuestionMarkGlyph(Glyph):
    name = "question_mark"
    unicode = "0x3F"
    offset = 0
    width_ratio = 1
    loop_ratio = 0.6
    gap = 0.35

    def draw(self, pen, dc):
        from glyphs.special.full_stop import FullStopGlyph

        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        g = self.gap * b.height
        h = self.loop_ratio * b.height
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y2 - h,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.loop_ratio,
            cut="bottom",
        )
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y2 - h,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.loop_ratio,
            cut="left",
        )
        draw_rect(
            pen,
            b.xmid - dc.stroke_x / 2,
            b.y1 + g,
            b.xmid + dc.stroke_x / 2,
            b.y2 - h + dc.stroke_y,
        )

        fsp = FullStopGlyph()
        fsp.draw(pen, dc)
