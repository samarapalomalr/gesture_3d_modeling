import cv2
import math
import numpy as np

class Renderer:
    def __init__(self, camera_3d):
        self.camera = camera_3d

    def draw_neon_line(self, frame, p1, p2, color, thickness=1):
        """Desenha uma linha com efeito de brilho neon (núcleo branco + brilho colorido)."""
        # Linha de brilho externa (mais grossa)
        cv2.line(frame, p1, p2, color, thickness + 2, cv2.LINE_AA)
        # Linha de núcleo interna (branca e fina)
        cv2.line(frame, p1, p2, (255, 255, 255), thickness, cv2.LINE_AA)

    def render(self, frame, scene):
        # 1. LINHAS DE CONEXÃO (Hierarquia de Grupo)
        # Desenha uma linha discreta ligando cubos que estão 'grudados'
        for cube in scene.cubes:
            if cube.parent:
                start = self.camera.project(*cube.position)
                end = self.camera.project(*cube.parent.position)
                if start and end:
                    # Linha de conexão em tom de cinza claro para não poluir a visão
                    cv2.line(frame, (start[0], start[1]), (end[0], end[1]), (200, 200, 200), 1, cv2.LINE_AA)

        # 2. RENDERIZAR CUBOS
        for cube in scene.cubes:
            # Atualiza rotação/flutuação antes de desenhar
            cube.update()
            is_sel = (cube == scene.selected_cube)
            
            # UX: Usamos cube.size fixo para evitar o zoom involuntário
            s = cube.size
            
            # Definição dos 8 vértices do cubo 3D
            vertices = [
                (-s,-s,-s), (s,-s,-s), (s,s,-s), (-s,s,-s),
                (-s,-s,s), (s,-s,s), (s,s,s), (-s,s,s)
            ]
            
            projected = []
            for v in vertices:
                # Aplica a rotação Y atual do cubo
                rx = v[0] * math.cos(cube.rotation_y) - v[2] * math.sin(cube.rotation_y)
                rz = v[0] * math.sin(cube.rotation_y) + v[2] * math.cos(cube.rotation_y)
                
                # Projeta o ponto 3D para coordenadas 2D da tela
                p = self.camera.project(cube.position[0] + rx, cube.position[1] + v[1], cube.position[2] + rz)
                projected.append((p[0], p[1]))

            # Define a cor: Amarelo se estiver sendo movido, cor original (Azul) se não
            color = (0, 255, 255) if is_sel else cube.color
            
            # Lista de arestas que conectam os vértices (12 linhas)
            edges = [
                (0,1), (1,2), (2,3), (3,0), # Face traseira
                (4,5), (5,6), (6,7), (7,4), # Face frontal
                (0,4), (1,5), (2,6), (3,7)  # Conexões laterais
            ]
            
            for e in edges:
                # Desenha cada aresta com o efeito neon
                self.draw_neon_line(frame, projected[e[0]], projected[e[1]], color, 2 if is_sel else 1)

        # Retorna o frame diretamente sem chamar a antiga UI verde
        return frame