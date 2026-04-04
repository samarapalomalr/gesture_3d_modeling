import cv2
import time
from src.input.camera import Camera
from src.input.hand_tracking import HandTracker
from src.gestures.gesture_detector import GestureDetector

from src.core.scene_manager import SceneManager
from src.core.controller import Controller
from src.render.camera_3d import Camera3D
from src.render.renderer import Renderer

def main():
    # Inicialização dos componentes
    camera = Camera()
    tracker = HandTracker()
    gesture_detector = GestureDetector()

    # Gerenciador de cena e controle
    scene_manager = SceneManager()
    controller = Controller(scene_manager)

    camera_3d = Camera3D(640, 480)
    renderer = Renderer(camera_3d)

    # Variáveis de estado para a Interface (HUD)
    last_action = "Sistema Pronto"
    action_timer = 0

    # Console Info
    print("\n" + "="*45)
    print("--- SISTEMA DE MODELAGEM 3D LEGO INICIADO ---")
    print("="*45)
    print("CONTROLES DE INTERAÇÃO:")
    print("- PALMA ABERTA: Criar cubo")
    print("- MÃO FECHADA: Segurar e mover blocos")
    print("- TECLA 'R': Remover último cubo (Desfazer)")
    print("- TECLAS 'A'/'D': Girar visualização")
    print("- ESC: Sair do sistema")
    print("="*45 + "\n")

    while True:
        # 1. Captura de frame
        frame = camera.get_frame()
        if frame is None:
            break

        # Espelhamento para coordenação motora
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # 2. Rastreamento e Gestos
        hands, frame = tracker.detect(frame)
        gesture = "none"
        landmarks = None

        if hands:
            landmarks = hands[0]
            gesture = gesture_detector.detect(landmarks)
            
            # Indicador sutil de atividade no punho (Landmark 0)
            wrist_x = int(landmarks[0][0] * w)
            wrist_y = int(landmarks[0][1] * h)
            cv2.circle(frame, (wrist_x, wrist_y), 5, (0, 255, 0), -1)

            # Se detectar um gesto novo, atualiza o HUD
            if gesture != "none":
                last_action = f"Gesto: {gesture.upper()}"
                action_timer = time.time()

        # 3. Lógica de Controle
        controller.update(gesture, landmarks, (h, w))

        # 4. Input de Teclado
        key = cv2.waitKey(1) & 0xFF
        if key == ord('a'):
            camera_3d.angle_y -= 0.1
        elif key == ord('d'):
            camera_3d.angle_y += 0.1
        elif key == ord('r'):
            # O controller já deve tratar a remoção, 
            # aqui apenas atualizamos o feedback visual
            last_action = "Objeto Removido"
            action_timer = time.time()
        elif key == 27: # ESC
            break

        # 5. Renderização 3D (Desenha os cubos sobre o frame)
        frame = renderer.render(frame, scene_manager)

        # --- 6. HUD (Interface Minimalista sobreposta) ---
        
        # Linha decorativa superior (Título)
        cv2.line(frame, (20, 40), (180, 40), (255, 255, 255), 1)
        cv2.putText(frame, "3D MODELING MODE", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        # Notificação de Ação (Desaparece após 1.5 segundos)
        if time.time() - action_timer < 1.5:
            # Retângulo semi-transparente para o texto
            overlay = frame.copy()
            cv2.rectangle(overlay, (w - 220, 20), (w - 20, 60), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
            
            cv2.putText(frame, last_action, (w - 210, 45), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

        # Crosshair central sutil (Muda de cor se houver gesto)
        cross_color = (0, 255, 0) if gesture != "none" else (200, 200, 200)
        cv2.drawMarker(frame, (w//2, h//2), cross_color, 
                       markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1)

        # 7. Exibição
        cv2.imshow("Gesture 3D Modeling", frame)

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()