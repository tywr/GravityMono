def draw_rect(pen, x1, y1, x2, y2, clockwise=False, rotate=0):
    """Draw a simple rectangle between two corner points."""
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    if rotate:
        from math import cos, sin, radians
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        a = radians(rotate)
        c, s = cos(a), sin(a)
        corners = [
            (cx + (x - cx) * c - (y - cy) * s,
             cy + (x - cx) * s + (y - cy) * c)
            for x, y in corners
        ]

    if clockwise:
        corners = [corners[0], corners[3], corners[2], corners[1]]

    pen.moveTo(corners[0])
    for pt in corners[1:]:
        pen.lineTo(pt)
    pen.closePath()
