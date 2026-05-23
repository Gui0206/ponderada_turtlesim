# Turtle Draw: Desenhando com Robô a partir de uma Imagem

Uma pipeline completa de visão computacional implementada do zero para extrair contornos de imagens e controlar a tartaruga do turtlesim para reproduzi-los.

## Vídeo Demonstração

[Inserir vídeo aqui (até 4 minutos)]

## 📋 Requisitos

- **ROS 2** (instalado via micromamba)
- **Python 3.8+**
- **NumPy** (para operações matriciais)
- **OpenCV** (apenas para carregar imagens)
- **Matplotlib** (para visualização)

## 🚀 Setup e Execução

### 1. Ativar Ambiente ROS

```bash
micromamba activate ros_env
```

### 2. Compilar o Pacote ROS

```bash
cd ~/Desktop/ponderada_ros/turtle_draw_ws
colcon build
source install/setup.bash
```

### 3. Iniciar turtlesim (em terminal separado)

```bash
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

### 4. Executar a Pipeline

#### Opção A: Visualizar Pipeline (recomendado primeiro)

Visualiza cada etapa do processamento de imagem antes de desenhar:

```bash
ros2 run turtle_draw_pkg vision_pipeline /path/to/image.png
```

Gera:
- `pipeline_visualization.png` - Mostra: imagem original, blur, detecção de bordas, supressão não-máxima, imagem binária, contornos extraídos
- `turtle_paths.png` - Mostra o espaço de desenho do turtle com os caminhos planejados

#### Opção B: Desenhar com Turtle

Processa a imagem e controla a tartaruga para desenhar os contornos:

```bash
ros2 run turtle_draw_pkg turtle_drawer /path/to/image.png
```

## 📚 Arquitetura da Solução

### Módulos Implementados

#### 1. **image_processor.py**
Toda a pipeline de visão computacional do zero (sem OpenCV para processamento):

- **Gaussian Blur**: Implementação de convolução separável com kernel Gaussiano 1D
- **Sobel Edge Detection**: Operadores Sobel X e Y para detecção de bordas
- **Non-Maximum Suppression**: Supressão de não-máximos para afinamento de bordas (estilo Canny)
- **Morphological Operations**: Dilatação e erosão para limpeza
- **Thresholding**: Binarização de imagem

**Algoritmos chave:**
- Convolução 2D com padding por reflexão
- Cálculo de magnitude e direção do gradiente
- Supressão baseada em direção de gradiente local

#### 2. **contour_extractor.py**
Extração de contornos a partir de imagens binárias:

- **Moore-Neighbor Tracing**: Algoritmo de rastreamento de contornos
- **Contour Filtering**: Remove contornos muito pequenos
- **Ramer-Douglas-Peucker Simplification**: Reduz pontos mantendo forma
- **Contour Merging**: Mescla contornos muito próximos

#### 3. **path_planner.py**
Planejamento de movimentos do turtle:

- **Coordinate Transformation**: Converte coordenadas de imagem para espaço turtle
- **Movement Planning**: Calcula sequência de rotação e movimento
- **Path Smoothing**: Suavização por média móvel
- **Path Decimation**: Reduz número de pontos para contornos muito longos

#### 4. **turtle_drawer.py**
Nó ROS 2 que controla a tartaruga:

- **Pose Subscriber**: Recebe posição atual do turtle
- **Velocity Publisher**: Envia comandos de movimento
- **Movement Controller**: Implementa controle proporcional para atingir posições alvo
- **Timeout handling**: Previne travamento

#### 5. **vision_pipeline.py**
Ferramenta de visualização e debug:

- Mostra resultado de cada etapa da pipeline
- Gera gráficos informativos
- Facilita ajuste de parâmetros

## 🔧 Ajustes de Parâmetros

No código, você pode ajustar:

### image_processor.py
```python
# Em preprocess():
gaussian_blur(..., kernel_size=5, sigma=1.5)  # Tamanho do blur
threshold(normalized_mag, threshold_value=0.1)  # Sensibilidade de detecção
```

### contour_extractor.py
```python
# Em find_contours():
if len(contour) > 5:  # Tamanho mínimo do contorno

# Em simplify_contour():
ContourExtractor.simplify_contour(contour, epsilon=3.0)  # Simplificação
```

### turtle_drawer.py
```python
self.linear_speed = 2.0  # Velocidade linear
self.angular_speed = 1.0  # Velocidade angular
self.position_tolerance = 0.05  # Tolerância de posição
```

## 📊 Exemplos de Uso

### Com uma imagem simples (ex: linha, círculo)

```bash
# Criar imagem de teste
python3 << 'EOF'
import numpy as np
from PIL import Image
img = np.zeros((200, 200), dtype=np.uint8)
img[50:150, 75:125] = 255  # Retângulo branco
Image.fromarray(img).save('test_rect.png')
EOF

# Visualizar pipeline
ros2 run turtle_draw_pkg vision_pipeline test_rect.png

# Desenhar
ros2 run turtle_draw_pkg turtle_drawer test_rect.png
```

## 🐛 Troubleshooting

### "Could not load image"
- Verifique o caminho absoluto da imagem
- Formatos suportados: PNG, JPG, BMP, etc (qualquer formato do OpenCV)

### Turtle não se move
- Verifique se turtlesim está rodando: `ros2 topic list` deve mostrar `/turtle1/pose`
- Verifique permissões: `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}}'`

### Contornos não são detectados
- Ajuste o `threshold_value` em `image_processor.py`
- Experimente diferentes valores de sigma para o Gaussian blur
- Use `vision_pipeline` para debugar cada etapa

### Performance lenta
- Reduza o tamanho da imagem (redimensione antes de passar)
- Use `path_planner.decimate_path()` para reduzir pontos

## 📝 Relatório Técnico

Veja [RELATORIO.md](RELATORIO.md) para documentação detalhada das decisões de implementação.

## 📄 Licença

Apache 2.0

## 👤 Autor

Guilherme Hollanda  
guilherme.marques@sou.inteli.edu.br

## 🔗 Referências

- ROS 2 Documentation: https://docs.ros.org/en/humble/
- NumPy Documentation: https://numpy.org/doc/
- Algoritmos implementados:
  - Sobel edge detection
  - Gaussian blur
  - Moore-Neighbor contour tracing
  - Ramer-Douglas-Peucker simplification
