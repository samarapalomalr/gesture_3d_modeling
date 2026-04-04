import math


class Camera3D:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        self.fov = 500
        self.camera_z = -500

        # 🔄 rotação
        self.angle_y = 0

        # 🔍 zoom
        self.zoom = 1.0

    def rotate_y(self, x, z):
        cos_a = math.cos(self.angle_y)
        sin_a = math.sin(self.angle_y)

        x_new = x * cos_a - z * sin_a
        z_new = x * sin_a + z * cos_a

        return x_new, z_new

    def project(self, x, y, z):
        # aplicar rotação
        x, z = self.rotate_y(x, z)

        # aplicar zoom
        z *= self.zoom

        z = z - self.camera_z

        if z == 0:
            z = 0.0001

        factor = self.fov / z

        x_2d = int(x * factor + self.width / 2)
        y_2d = int(-y * factor + self.height / 2)

        return x_2d, y_2d, factor