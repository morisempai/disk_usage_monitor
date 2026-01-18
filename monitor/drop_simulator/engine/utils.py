def rotate(x, y, sin_coof, cos_coof, clockwise=False):
    if clockwise:
        x_rotated = x*cos_coof + y*sin_coof
        y_rotated = -x*sin_coof + y*cos_coof
    else:
        x_rotated = x*cos_coof - y*sin_coof
        y_rotated = x*sin_coof + y*cos_coof
    return x_rotated, y_rotated