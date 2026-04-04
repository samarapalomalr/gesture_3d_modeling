from src.utils.constants import CUBE_SIZE

class Cube:
    def __init__(self, position, size=CUBE_SIZE):
        # Posição absoluta e base são as mesmas para travar o movimento
        self.position = list(position)
        self.base_position = list(position)
        self.size = size
        
        # Azul Vibrante (BGR para OpenCV)
        # 255 no canal Blue, 0 no Green, 0 no Red
        self.color = (255, 0, 0) 
        
        self.rotation_y = 0.5 # Ângulo fixo para dar perspectiva 3D constante
        
        self.parent = None
        self.children = []

    def update(self):
        """Zero movimentação automática. O cubo é 100% estático."""
        pass

    def move(self, new_position):
        # Calcula o deslocamento para o grupo
        dx = new_position[0] - self.base_position[0]
        dy = new_position[1] - self.base_position[1]
        dz = new_position[2] - self.base_position[2]

        self.base_position = list(new_position)
        self.position = list(new_position)

        # Move os "filhos" anexados mantendo a estrutura rígida
        for child in self.children:
            child.move_relative(dx, dy, dz)

    def move_relative(self, dx, dy, dz):
        self.base_position[0] += dx
        self.base_position[1] += dy
        self.base_position[2] += dz
        self.position = list(self.base_position)
        for child in self.children:
            child.move_relative(dx, dy, dz)