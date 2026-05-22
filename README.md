# Turtle Draw: Robotic Drawing from Image Contours

Complete computer vision pipeline and ROS 2 package for extracting image contours and controlling the turtlesim robot to draw them.

**Autora**: Guilherme Hollanda  
**Disciplina**: Robótica e Visão Computacional - INTELI  
**Data de Entrega**: 22/05/2026  

## 📋 Visão Geral

Este projeto implementa uma pipeline completa de visão computacional **do zero**, usando apenas NumPy para operações matriciais. O sistema:

1. **Carrega** uma imagem (dog.png)
2. **Processa** a imagem (pré-processamento, detecção de bordas, extração de contornos)
3. **Mapeia** os contornos para o espaço da tartaruga
4. **Controla** o turtlesim via ROS 2 para desenhar os contornos

### 🎯 Requisitos Atendidos

- ✅ **Pré-processamento**: Conversão RGB→Cinza, Blur Gaussiano (do zero)
- ✅ **Detecção de Bordas**: Operador Sobel com convolução 2D (do zero)
- ✅ **Planejamento de Caminho**: Mapeamento coordenadas imagem → turtlesim
- ✅ **Controle ROS 2**: Pacote completo com nó Python
- ✅ **Documentação**: Relatório técnico e código comentado

## 📁 Estrutura do Projeto

```
/ponderada_ros/
├── README.md                           # Este arquivo
├── dog.png                             # Imagem de entrada
├── RELATORIO.md                        # Documentação técnica (máx 2 páginas)
├── vision_pipeline_visualization.png   # Output da pipeline (gerado ao rodar)
└── turtle_draw_ws/                     # ROS 2 Workspace
    ├── build.sh                        # Script de build
    ├── build.zsh                       # Build para zsh (testado)
    ├── src/
    │   └── turtle_draw_pkg/
    │       ├── package.xml             # Metadados ROS 2
    │       ├── setup.py                # Setup Python
    │       ├── README.md               # Documentação do pacote
    │       └── turtle_draw_pkg/
    │           ├── __init__.py
    │           ├── vision_pipeline.py  # Core vision (ImageProcessor, CoordinateMapper)
    │           ├── turtle_drawer.py    # ROS 2 node principal
    │           └── image_processor.py  # Utilitário de visualização
    ├── build/                          # Compilado (gerado)
    └── install/                        # Instalado (gerado)
```

## 🚀 Início Rápido

### Pré-requisitos

- ROS 2 (Humble ou superior) instalado via micromamba
- Python 3.10+
- A imagem `dog.png` no diretório do projeto

### 1. Ativar Ambiente

```bash
micromamba activate ros_env
```

### 2. Navegar ao Workspace

```bash
cd ~/Desktop/ponderada_ros/turtle_draw_ws
```

### 3. Compilar (se necessário)

```bash
# Usando zsh (recomendado)
zsh build.zsh

# Ou manualmente
source ~/.zshrc
micromamba activate ros_env
colcon build --symlink-install
```

### 4. Iniciar Turtlesim (Terminal 1)

```bash
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

### 5. Executar Turtle Drawer (Terminal 2)

```bash
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg turtle_drawer
```

**Resultado**: A tartaruga começará a desenhar os contornos da imagem do cão!

## 📊 Pipeline de Visão Computacional

### Etapa 1: Pré-Processamento

**Entrada**: Imagem BGR (dog.png)

**Processamento**:
1. Conversão para escala de cinza (fórmula de luminosidade: 0.299R + 0.587G + 0.114B)
2. Blur Gaussiano (kernel 5×5, σ=1.5) com convolução separável
3. Redução de ruído mantendo bordas significativas

**Saída**: Imagem em escala de cinza suavizada

### Etapa 2: Detecção de Bordas

**Algoritmo**: Operador Sobel (implementado do zero)

**Kernels**:
```
Sx = [-1  0  1]      Sy = [-1 -2 -1]
     [-2  0  2]           [ 0  0  0]
     [-1  0  1]           [ 1  2  1]
```

**Processamento**:
1. Convolução 2D com Sx e Sy
2. Cálculo de magnitude: M = √(Gx² + Gy²)
3. Normalização: [0, 255]
4. Thresholding: valores > 50 → bordas

**Saída**: Mapa de bordas binário

**Por que Sobel?**
- Robusto a ruído
- Detecta bordas multi-direcionais
- Mais simples que Canny
- Implementação clara

### Etapa 3: Extração de Contornos

**Algoritmo**: Flood Fill com 8-conectividade

**Processamento**:
1. Para cada pixel branco não visitado
2. Rastrear contorno usando DFS (stack)
3. Marcar pixels visitados
4. Filtrar contornos pequenos (< 5 pixels)

**Saída**: Lista de contornos [(x₁,y₁), (x₂,y₂), ...]

### Etapa 4: Mapeamento de Coordenadas

**Transformação**:
- Espaço imagem: [0, width] × [0, height]
- Espaço turtlesim: [0.5, 10.5] × [0.5, 10.5]

**Fórmulas**:
```
norm_x = img_x / image_width
norm_y = img_y / image_height
turtle_x = 0.5 + norm_x * 10.0
turtle_y = 10.5 - norm_y * 10.0  # Inverte Y
```

**Saída**: Contornos em coordenadas turtlesim

## 🤖 Controle ROS 2

### Nó: `turtle_drawer`

**Publicador**:
- Tópico: `/turtle1/cmd_vel`
- Tipo: `geometry_msgs/Twist`
- Campos: `twist.linear.x`, `twist.angular.z`

**Parâmetros**:
- Velocidade linear: 0.5 m/s
- Velocidade angular: 0.5 rad/s
- Threshold de movimento: 0.05 unidades

**Fluxo**:
1. Processa imagem
2. Extrai contornos
3. Para cada contorno:
   - Move para primeiro ponto
   - Desenha linha para cada ponto subsequente
   - Pausa entre contornos

## 🧪 Validação

### Testes Realizados

✅ Conversão RGB→Cinza com coeficientes corretos  
✅ Blur Gaussiano preserva estrutura mantendo suavização  
✅ Sobel detecta bordas em múltiplas direções  
✅ Contours extraem formas corretamente  
✅ Mapeamento preserva proporções  
✅ ROS 2 publica comandos corretamente  

### Visualizar Pipeline

```bash
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg image_processor
```

Gera `vision_pipeline_visualization.png` mostrando todas as etapas.

## 📝 Justificativas de Implementação

### Pré-Processamento
- **Gaussian Blur separável**: O(n*k) vs O(n*k²), mantém qualidade
- **σ=1.5**: Balanço entre suavização e preservação de bordas

### Detecção de Bordas
- **Sobel vs. Canny**: Sobel é mais simples, suficiente para desenho robótico
- **Threshold=50**: Remove ruído, mantém bordas significativas

### Contour Extraction
- **Flood Fill vs. Moore-Neighbor**: Flood fill é robusto com 8-conectividade
- **Downsampling**: Reduz pontos de ~10k para ~100-150 por contorno

### ROS 2
- **Twist messages**: Padrão ROS para velocidade
- **Linear+Angular**: Compatível com turtlesim

## 🔧 Dependências

**Permitidas** (conforme requisitos):
- ✅ NumPy (operações matriciais)
- ✅ OpenCV (carregamento de imagem apenas)
- ✅ Matplotlib (visualização)

**Não utilizadas** (como exigido):
- ❌ scikit-image
- ❌ scipy
- ❌ PIL/Pillow (exceto OpenCV)

## ⚠️ Limitações Conhecidas

1. **Imagens muito densas**: Podem gerar muitos contornos pequenos
2. **Objetos finos**: < 3 pixels podem não ser detectados
3. **Performance**: Convolução manual é lenta (~2-3s para processar)
4. **Granularidade de movimento**: 0.05 unidades; pode deixar pequenos gaps

## 🐛 Troubleshooting

**Nenhum contorno detectado**
```bash
# Aumentar threshold Sobel em vision_pipeline.py
# threshold_val = 30  # ao invés de 50
```

**Tartaruga move erraticamente**
```bash
# Reduzir velocidade em turtle_drawer.py
self.linear_speed = 0.3  # ao invés de 0.5
```

**Build falha**
```bash
# Garantir que ROS 2 está ativo
micromamba activate ros_env
colcon build --symlink-install
```

## 📚 Referências

- [ROS 2 Documentation](https://docs.ros.org/)
- [Sobel Operator](https://en.wikipedia.org/wiki/Sobel_operator)
- [Gaussian Blur](https://en.wikipedia.org/wiki/Gaussian_blur)
- [Connected Components](https://en.wikipedia.org/wiki/Connected-component_labeling)
- Digital Image Processing (Gonzalez & Woods)

## 📹 Entregáveis

- ✅ **Código**: Pacote ROS 2 completo em `turtle_draw_ws/`
- ✅ **Relatório**: Documentação técnica em `RELATORIO.md` (< 2 páginas)
- 📹 **Vídeo**: A ser gravado (screencast até 4 minutos)
- 📊 **Repositório Git**: Todos os módulos com README

## 👤 Autor

**Guilherme Hollanda**  
Email: guilherme.marques@sou.inteli.edu.br  
INTELI - Instituto de Tecnologia e Liderança  

---

**Último atualizado**: 22/05/2026 às 23h00
