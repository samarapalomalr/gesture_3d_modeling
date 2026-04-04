import math

class SceneManager:
    def __init__(self):
        self.cubes = []
        self.selected_cube = None
        self.CUBE_SIZE = 50  # Tamanho real do cubo no seu motor 3D
        self.snap_threshold = 100 # Sensibilidade do 'clique'

    def create_cube(self, position):
        from src.models.cube import Cube
        
        # Se houver cubos na cena, tenta encaixar no mais próximo
        neighbor = self.get_nearest_cube(position, threshold=150)
        
        if neighbor:
            # Lógica LEGO: Encontra a face mais próxima do vizinho e gruda nela
            new_pos = self._calculate_snap_position(neighbor.position, position)
            new_cube = Cube(new_pos)
            new_cube.parent = neighbor
            neighbor.children.append(new_cube)
            print("LEGO: Encaixado na face do vizinho!")
        else:
            # Se estiver sozinho no espaço, apenas cria
            new_cube = Cube(list(position))
        
        self.cubes.append(new_cube)

    def _calculate_snap_position(self, target_pos, hand_pos):
        """Calcula em qual das 6 faces o cubo deve 'clicar'."""
        res = list(target_pos)
        
        # Diferença entre a mão e o centro do cubo alvo
        dx = hand_pos[0] - target_pos[0]
        dy = hand_pos[1] - target_pos[1]
        dz = hand_pos[2] - target_pos[2]

        # Encontra o eixo de maior diferença para decidir a face
        abs_x, abs_y, abs_z = abs(dx), abs(dy), abs(dz)
        max_val = max(abs_x, abs_y, abs_z)

        if max_val == abs_x:
            res[0] += self.CUBE_SIZE if dx > 0 else -self.CUBE_SIZE
        elif max_val == abs_y:
            res[1] += self.CUBE_SIZE if dy > 0 else -self.CUBE_SIZE
        else:
            res[2] += self.CUBE_SIZE if dz > 0 else -self.CUBE_SIZE
            
        return res

    def move_selected_cube(self, hand_position):
        if not self.selected_cube: return

        # Se o cubo estiver preso (tem pai), ele precisa de força para descolar
        if self.selected_cube.parent:
            dist_to_parent = math.dist(hand_position, self.selected_cube.parent.position)
            if dist_to_parent > 180: # Limiar de 'desgrude'
                self.selected_cube.parent.children.remove(self.selected_cube)
                self.selected_cube.parent = None
            else:
                return # Enquanto estiver perto, ele continua travado no LEGO

        # Movimento livre se não estiver travado
        dx = hand_position[0] - self.selected_cube.position[0]
        dy = hand_position[1] - self.selected_cube.position[1]
        dz = hand_position[2] - self.selected_cube.position[2]
        self._recursive_move(self.selected_cube, dx, dy, dz)
        
        # Tenta travar em outros cubos enquanto move
        self._check_lego_snap(self.selected_cube, hand_position)

    def _check_lego_snap(self, moving_cube, hand_pos):
        for other in self.cubes:
            if other == moving_cube or self._is_descendant(moving_cube, other):
                continue
            
            if math.dist(hand_pos, other.position) < self.snap_threshold:
                # TRAVA AUTOMÁTICA
                new_pos = self._calculate_snap_position(other.position, hand_pos)
                moving_cube.position = new_pos
                moving_cube.parent = other
                other.children.append(moving_cube)
                break

    def remove_last_cube(self):
        if not self.cubes: return
        last = self.cubes.pop()
        if last.parent: last.parent.children.remove(last)
        for c in last.children: c.parent = None

    def _recursive_move(self, cube, dx, dy, dz):
        cube.position[0] += dx
        cube.position[1] += dy
        cube.position[2] += dz
        for child in cube.children:
            self._recursive_move(child, dx, dy, dz)

    def _is_descendant(self, p, t):
        for c in p.children:
            if c == t or self._is_descendant(c, t): return True
        return False

    def get_nearest_cube(self, pos, threshold=200):
        nearest = None
        min_d = float('inf')
        for c in self.cubes:
            d = math.dist(c.position, pos)
            if d < min_d and d < threshold:
                min_d, nearest = d, c
        return nearest

    def select_cube(self, pos):
        target = self.get_nearest_cube(pos, threshold=200)
        if target:
            root = target
            while root.parent: root = root.parent
            self.selected_cube = root
            return True
        return False