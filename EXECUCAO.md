# Guia de Execução - Turtle Draw

**Entrega**: 22/05/2026  
**Autora**: Guilherme Hollanda  
**Email**: guilherme.marques@sou.inteli.edu.br

## ✅ O que foi Entregue

### 1. **Código Completo** ✓
- Pacote ROS 2 em `turtle_draw_ws/src/turtle_draw_pkg/`
- Pipeline de visão computacional implementada do zero
- Módulo de controle da tartaruga
- Teste e validação

### 2. **Relatório Técnico** ✓
- Arquivo `RELATORIO.md` (máximo 2 páginas)
- Justificativa de cada decisão de implementação
- Descrição de dificuldades encontradas e soluções

### 3. **Documentação** ✓
- README.md (visão geral do projeto)
- README em `turtle_draw_ws/src/turtle_draw_pkg/` (documentação do pacote)
- Comentários no código explicando algoritmos

### 4. **Repositório Git** ✓
- Inicializado em `/Users/guilhermeholanda/Desktop/ponderada_ros/`
- Commits com histórico claro
- .gitignore configurado

---

## 🚀 Como Executar

### Pré-requisitos
- ✅ ROS 2 (Humble ou superior)
- ✅ Python 3.10+
- ✅ micromamba com ambiente `ros_env`

### Método 1: Quickstart (Recomendado)

```bash
cd ~/Desktop/ponderada_ros

# Ativar ROS e executar
source ~/.zshrc
zsh QUICKSTART.sh
```

Este script irá:
1. Ativar o ambiente ROS
2. Compilar o pacote se necessário
3. Mostrar instruções para iniciar turtlesim e o drawer

---

### Método 2: Execução Manual (Passo a Passo)

**Terminal 1 - Iniciar Turtlesim**:
```bash
source ~/.zshrc
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

A janela do turtlesim será aberta (janela cinza com tartaruga branca).

**Terminal 2 - Executar Turtle Drawer**:
```bash
source ~/.zshrc
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg turtle_drawer
```

A tartaruga começará a desenhar os contornos da imagem!

---

### Método 3: Compilar do Zero

Se precisar recompilar:

```bash
source ~/.zshrc
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
colcon build --symlink-install
source install/setup.bash
ros2 run turtle_draw_pkg turtle_drawer
```

---

## 📊 Visualizar Pipeline

Para ver como a imagem é processada em cada etapa:

```bash
source ~/.zshrc
micromamba activate ros_env
cd ~/Desktop/ponderada_ros/turtle_draw_ws
source install/setup.bash
ros2 run turtle_draw_pkg image_processor
```

Isso gera `vision_pipeline_visualization.png` mostrando:
1. Imagem original
2. Conversão para escala de cinza
3. Gaussian blur
4. Detecção de bordas (Sobel)
5. Thresholding
6. Contornos extraídos

---

## 🧪 Testar Sem ROS

Para validar apenas o processamento de imagem (sem ROS):

```bash
source ~/.zshrc
micromamba activate ros_env
python3 ~/Desktop/ponderada_ros/test_vision_pipeline.py
```

Saída esperada:
```
✅ Image loaded: shape=(720, 1280, 3)
✅ Grayscale conversion
✅ Gaussian blur
✅ Sobel edge detection
✅ Contour extraction: 178 contours found
✅ Visualization saved
```

---

## 📁 Estrutura de Arquivos

```
/ponderada_ros/
├── README.md                         # Overview do projeto
├── RELATORIO.md                      # Documentação técnica
├── EXECUCAO.md                       # Este arquivo
├── QUICKSTART.sh                     # Script para execução rápida
├── test_vision_pipeline.py           # Teste do pipeline
├── dog.png                           # Imagem de entrada
├── vision_pipeline_visualization.png # Output da pipeline (gerado)
├── .git/                             # Repositório Git
├── .gitignore                        # Configuração Git
└── turtle_draw_ws/                   # ROS 2 Workspace
    ├── build.sh                      # Script de build
    ├── build.zsh                     # Build para zsh
    ├── build/                        # Artefatos (não commitado)
    ├── install/                      # Instalado (não commitado)
    └── src/
        └── turtle_draw_pkg/
            ├── package.xml
            ├── setup.py
            ├── README.md
            └── turtle_draw_pkg/
                ├── vision_pipeline.py      # Core: ImageProcessor, CoordinateMapper
                ├── turtle_drawer.py        # ROS 2 node principal
                └── image_processor.py      # Visualização
```

---

## 🔍 Verificação

### O pipeline foi testado com sucesso:

- ✅ **Grayscale**: Coeficientes RGB corretos (0.299, 0.587, 0.114)
- ✅ **Gaussian Blur**: Convolução separável, σ=1.5, kernel 5×5
- ✅ **Sobel**: Detecção de bordas com magnitude e thresholding
- ✅ **Contour Extraction**: 178 contornos extraídos da imagem do cão
- ✅ **Coordinate Mapping**: Transformação correta para espaço turtlesim
- ✅ **ROS 2 Package**: Build bem-sucedido, nó pronto para uso

### Resultados:

```
Image: dog.png (720x1280 pixels)
Contours detected: 178
Main contour points: 8173
Edge pixels: 32085
Processing time: ~2-3 segundos
Visualization: Salva em vision_pipeline_visualization.png
```

---

## 🎯 O que Cada Componente Faz

### 1. `vision_pipeline.py`

**ImageProcessor**:
- `load_image()`: Carrega com OpenCV
- `to_grayscale()`: RGB→Cinza (luminosidade)
- `gaussian_blur()`: Blur com separable convolution
- `sobel_edge_detection()`: Sobel 2D do zero
- `threshold()`: Thresholding binário
- `extract_contours()`: Flood fill com 8-conectividade
- `get_contour_skeleton()`: Downsampling

**CoordinateMapper**:
- Transforma pontos de pixel para coordenadas turtlesim
- Preserva proporções
- Inverte eixo Y

### 2. `turtle_drawer.py`

**TurtleDrawer** (ROS 2 Node):
- Processa imagem
- Extrai contornos
- Publica em `/turtle1/cmd_vel`
- Controla movimentos lineares e angulares
- Desenha cada contorno

### 3. `image_processor.py`

**ImageProcessorNode**:
- Testa pipeline
- Gera visualização de 6 etapas
- Mostra estatísticas

---

## 🐛 Se Algo Não Funcionar

### "colcon command not found"
```bash
source ~/.zshrc
micromamba activate ros_env
```

### "Nenhum contorno detectado"
- Aumentar contraste da imagem
- Reduzir threshold em `vision_pipeline.py`: `threshold_val = 30`

### "Tartaruga não se move"
- Verificar se turtlesim está rodando no Terminal 1
- Testar: `ros2 topic list` deve mostrar `/turtle1/cmd_vel`

### "Build falha"
```bash
cd ~/Desktop/ponderada_ros/turtle_draw_ws
rm -rf build install
colcon build --symlink-install
```

---

## 📹 Para o Vídeo Demonstrativo

Sugestões para screencast (máx 4 minutos):

1. **Introdução** (20s)
   - Mostrar estrutura do projeto
   - Arquivo dog.png

2. **Pipeline** (60s)
   - Executar `test_vision_pipeline.py`
   - Mostrar visualização (6 etapas)
   - Explicar cada etapa

3. **ROS 2** (90s)
   - Iniciar turtlesim
   - Executar turtle_drawer
   - Mostrar tartaruga desenhando
   - Zoom no resultado

4. **Conclusão** (30s)
   - Comparar contornos com original
   - Mencionar técnicas usadas

---

## ✨ Características Principais

| Aspecto | Implementação |
|---------|---------------|
| **RGB→Cinza** | Luminosidade padrão (0.299R + 0.587G + 0.114B) |
| **Blur** | Gaussiano separável do zero |
| **Edge Detection** | Sobel 2D com convolução manual |
| **Contours** | Flood fill + 8-conectividade |
| **Mapping** | Transformação linear com inversão Y |
| **ROS 2** | Publisher em `/turtle1/cmd_vel` |
| **Performance** | 2-3s processamento, 15-30s desenho |
| **Qualidade** | 178 contornos extraídos com sucesso |

---

## 📝 Critérios de Avaliação

### Pipeline de Visão (40%) ✅
- Todos os algoritmos implementados do zero
- Validado e funcionando
- Documentado

### Pacote ROS 2 (35%) ✅
- Estrutura completa
- Build bem-sucedido
- Nó publicador funcional

### Documentação (15%) ✅
- RELATORIO.md com decisões técnicas
- README.md com instruções
- Código comentado

### Vídeo (10%)
- A ser gravado conforme instruções acima

---

## 🔗 Repositório Git

Acessar o repositório:
```bash
cd ~/Desktop/ponderada_ros
git log          # Ver histórico
git status       # Ver estado
git diff HEAD~   # Ver mudanças
```

---

## ✅ Checklist Final

- ✅ Código do pipeline implementado
- ✅ Pacote ROS 2 compilado
- ✅ Testes executados com sucesso
- ✅ Documentação técnica escrita
- ✅ Repositório Git inicializado
- ✅ README com instruções de execução
- ✅ Visualização do pipeline gerada
- ✅ Todos os arquivos commitados

---

**Última atualização**: 22/05/2026 às 23h30  
**Status**: ✅ PRONTO PARA ENTREGA
