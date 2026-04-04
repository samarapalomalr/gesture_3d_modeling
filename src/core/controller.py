import time
import cv2

class Controller:
    def __init__(self, scene_manager):
        self.scene = scene_manager
        self.create_timer = 0
        self.is_moving = False 
        self.cursor_3d = [0, 0, 400]

    def update(self, gesture, landmarks, frame_shape):
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') or key == ord('R'):
            self.scene.remove_last_cube()

        if not landmarks: 
            self.is_moving = False
            self.scene.selected_cube = None
            return

        # Posição do indicador
        h, w = frame_shape[:2]
        self.cursor_3d = [(landmarks[8][0] - w/2) * 3.5, -(landmarks[8][1] - h/2) * 3.5, 400]

        # CRIAR (Mão Aberta)
        if gesture == "open_hand" and not self.is_moving:
            if self.create_timer == 0:
                self.create_timer = time.time()
            elif time.time() - self.create_timer > 0.7:
                self.scene.create_cube(self.cursor_3d)
                self.create_timer = time.time() + 1.2 
        else:
            self.create_timer = 0

        # MOVER (Mão Fechada)
        if gesture == "grab":
            if not self.is_moving:
                if self.scene.select_cube(self.cursor_3d):
                    self.is_moving = True
            
            if self.is_moving:
                self.scene.move_selected_cube(self.cursor_3d)
        else:
            self.is_moving = False
            self.scene.selected_cube = None

    