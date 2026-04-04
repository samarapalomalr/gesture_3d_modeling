import cv2


class Camera:
    def __init__(self, index=0, width=480, height=360):
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            raise RuntimeError("❌ Não foi possível abrir a câmera.")

        # 🔥 resolução menor = MUITO mais FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # ⚡ buffer menor (menos delay)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def get_frame(self):
        success, frame = self.cap.read()

        if not success or frame is None:
            return None

        # 🪞 espelha imagem
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        if self.cap:
            self.cap.release()