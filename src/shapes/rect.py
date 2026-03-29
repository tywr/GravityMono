def draw_rect(pen, x1, y1, x2, y2):
    """Draw a simple rectangle between two corner points."""
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()
