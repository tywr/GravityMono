def interpolate(p1, p2, percentage):
    """Return the point at the given percentage of the way from p1 to p2."""
    return (
        p1[0] + (p2[0] - p1[0]) * percentage,
        p1[1] + (p2[1] - p1[1]) * percentage,
    )
