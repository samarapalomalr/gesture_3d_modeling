# ✋ Gesture-Based 3D Modeling Interface

Sistema interativo de modelagem que permite criar e manipular objetos 3D em tempo real através de visão computacional. Uma interface "touchless" que elimina a necessidade de mouses ou teclados para a construção de estruturas simples.

## 🚀 Demonstração
*(Adicione aqui um GIF do sistema em funcionamento para impressionar no portfólio!)*

---

## 🧠 Sobre o Projeto

Este projeto utiliza **MediaPipe** para rastreamento de alta precisão e **PyOpenGL** para renderização de baixa latência. O objetivo é criar uma experiência imersiva onde a mão humana se torna a ferramenta de modelagem direta no espaço tridimensional.

### **Funcionalidades Atuais:**
- 🖐️ **Rastreamento em Tempo Real:** Mapeamento de 21 pontos da mão.
- 🧊 **Criação Instintiva:** Gere cubos e objetos com gestos simples.
- 🎮 **HUD Dinâmico:** Interface minimalista integrada ao frame da câmera com notificações de ações.
- 🔄 **Manipulação Espacial:** Rotação de câmera e movimentação de blocos via gestos.
- 🗑️ **Sistema de Desfazer:** Remoção rápida de objetos para iteração criativa.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Visão Computacional:** OpenCV & MediaPipe
- **Renderização 3D:** PyOpenGL & Pygame
- **Matemática:** NumPy

---

## 📁 Estrutura do Projeto

```text
gesture_3d_modeling/
│
├── main.py                  # Ponto de entrada e loop principal
├── config.py                # Parâmetros de sensibilidade e cores
│
├── src/
│   ├── input/               # Captura de vídeo e Hand Tracking
│   ├── gestures/            # Lógica de reconhecimento de padrões
│   ├── core/                # Orquestração da cena e comandos
│   ├── models/              # Definição geométrica (Cubos, etc)
│   ├── render/              # Engine de renderização e câmera 3D
│   └── utils/               # Cálculos matemáticos e constantes
│
└── data/                    # Futura exportação de arquivos JSON/OBJ

⚙️ Instalação e Execução

Clone o repositório:
git clone [https://github.com/seu-usuario/gesture-3d-modeling.git](https://github.com/samarapalomalr/gesture-3d-modeling.git)
cd gesture-3d-modeling

Crie um ambiente virtual:
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

Instale as dependências:
pip install -r requirements.txt

Inicie o sistema:
python main.py

🎮 Comandos e Interação
Gestos (Webcam)
Gesto	        Ação
Palma Aberta	Cria um novo objeto no centro
Mão Fechada	    Seleciona e move objetos próximos

obs: tecla R remove o objeto

