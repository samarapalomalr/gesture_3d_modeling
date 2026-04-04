import math


# -------------------------
# Distância 2D
# -------------------------
def distance_2d(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1]
    )


# -------------------------
# Distância 3D
# -------------------------
def distance_3d(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2 +
        (p2[2] - p1[2]) ** 2
    )


# -------------------------
# Interpolação (suavização)
# -------------------------
def lerp(current, target, smooth=0.2):
    return current + (target - current) * smooth


# -------------------------
# Suavizar vetor 3D
# -------------------------
def smooth_vector(current, target, smooth=0.2):
    return [
        lerp(current[0], target[0], smooth),
        lerp(current[1], target[1], smooth),
        lerp(current[2], target[2], smooth),
    ]


# -------------------------
# Clamp (limitar valores)
# -------------------------
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


# -------------------------
# Normalizar valor
# -------------------------
def normalize(value, min_val, max_val):
    if max_val - min_val == 0:
        return 0
    return (value - min_val) / (max_val - min_val)


# -------------------------
# Mapear valor (escala)
# -------------------------
def map_value(value, in_min, in_max, out_min, out_max):
    return out_min + (float(value - in_min) / (in_max - in_min)) * (out_max - out_min)


# -------------------------
# Converter 2D → 3D
# -------------------------
def screen_to_3d(x, y, center_x, center_y, base_z, z_sensitivity=1.5):
    x_3d = x - center_x
    y_3d = -(y - center_y)
    z_3d = base_z + (y - center_y) * z_sensitivity

    return [x_3d, y_3d, z_3d]