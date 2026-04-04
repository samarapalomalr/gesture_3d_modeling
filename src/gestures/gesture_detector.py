import math

class GestureDetector:
    def __init__(self):
        self.pinch_threshold = 32 

    def _distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def _fingers_up(self, landmarks):
        """Analisa quais dedos estão esticados."""
        fingers = []

        # 1. Polegar (Análise de abertura lateral)
        thumb_is_open = abs(landmarks[4][0] - landmarks[2][0]) > 40
        fingers.append(thumb_is_open)

        # 2. Indicador, Médio, Anelar e Mínimo
        # Comparamos a ponta (TIP) com a junta do meio (PIP)
        tips = [8, 12, 16, 20]
        joints = [6, 10, 14, 18]
        
        for tip, joint in zip(tips, joints):
            # Se o Y da ponta for menor, o dedo está para cima (esticado)
            fingers.append(landmarks[tip][1] < landmarks[joint][1])

        return fingers 

    def detect(self, landmarks):
        if not landmarks:
            return "none"

        fingers = self._fingers_up(landmarks)
        
        # --- 1. PINÇA (Criar) ---
        dist_pinch = self._distance(landmarks[4], landmarks[8])
        if dist_pinch < self.pinch_threshold:
            return "pinch"

        # --- 2. APONTAR (Mover) ---
        # Apenas o indicador (fingers[1]) levantado. 
        # Ignoramos o polegar (fingers[0]) para dar mais conforto ao mover.
        if fingers[1] and not any(fingers[2:]):
            return "point"

        # --- 3. MÃO FECHADA / GRAB (Remover) ---
        # Se todos os dedos principais (indicador ao mínimo) estiverem fechados
        if not any(fingers[1:]):
            return "grab"

        # --- 4. PALMA ABERTA (Reset/Soltar) ---
        if all(fingers[1:]):
            return "open_hand"

        return "none"