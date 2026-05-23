# Quick Start Guide - Turtle Draw

## Setup Rápido

### 1. Abrir um terminal e ativar ROS

```bash
# Use seu shell (bash ou zsh)
# Micromamba deve estar no seu PATH
micromamba activate ros_env

# Verificar:
ros2 --version
```

Se `micromamba: command not found`, tente:
```bash
source ~/.zshrc  # ou ~/.bashrc
micromamba activate ros_env
```

### 2. Navegar para o workspace

```bash
cd ~/Desktop/ponderada_ros/turtle_draw_ws
```

### 3. Compilar (primeira vez)

```bash
micromamba activate ros_env
colcon build
source install/setup.bash
```

### 4. Em um SEGUNDO terminal, iniciar turtlesim

```bash
micromamba activate ros_env
ros2 run turtlesim turtlesim_node
```

Você deve ver uma janela com a tartaruga no meio.

### 5. No PRIMEIRO terminal, criar imagens de teste

```bash
cd src/turtle_draw_pkg
python3 create_test_image.py
ls test_*.png  # Deve ver test_shapes.png, test_letter.png, etc
```

### 6. Visualizar a pipeline (DEBUG)

```bash
# Isso mostra cada etapa do processamento
ros2 run turtle_draw_pkg vision_pipeline test_shapes.png
```

Você verá:
- `pipeline_visualization.png` - 6 imagens mostrando: original, blur, bordas, NMS, binária, contornos
- `turtle_paths.png` - Os caminhos que a tartaruga vai seguir

### 7. DESENHAR COM A TARTARUGA! 🐢

```bash
# Desenha a imagem em tempo real
ros2 run turtle_draw_pkg turtle_drawer test_shapes.png
```

Você verá a tartaruga movimentando-se na tela do turtlesim!

## Próximos Passos

- Teste com diferentes imagens: `test_shapes.png`, `test_letter.png`, `test_spiral.png`, `test_grid.png`
- Ajuste parâmetros em `image_processor.py` se os contornos não forem bons
- Veja o relatório: `../RELATORIO.md`

## Troubleshooting

**"colcon: command not found"**
- Ative ROS: `micromamba activate ros_env`

**"Cannot open display"**
- Você está em SSH? Use X11 forwarding ou rode turtlesim localmente

**Turtle não se mexe**
- Verifique se turtlesim está rodando no outro terminal
- Teste: `ros2 topic list` - deve listar `/turtle1/pose` e `/turtle1/cmd_vel`

**Nenhum contorno detectado**
- A imagem pode ser muito escura/clara
- Teste com `test_shapes.png` primeiro (com formas bem definidas)

## Estrutura do Projeto

```
turtle_draw_ws/
├── src/turtle_draw_pkg/
│   ├── turtle_draw_pkg/
│   │   ├── image_processor.py      # Visão computacional
│   │   ├── contour_extractor.py    # Extração de contornos
│   │   ├── path_planner.py         # Planejamento de movimento
│   │   ├── turtle_drawer.py        # Nó ROS principal
│   │   └── vision_pipeline.py      # Visualização/debug
│   └── create_test_image.py        # Gera imagens de teste
├── build.sh                         # Script de compilação
└── install/setup.bash              # Sourcing (gerado)
```

## Comandos Úteis

```bash
# Listar tópicos ativos
ros2 topic list

# Ver mensagens sendo publicadas
ros2 topic echo /turtle1/pose

# Parar tudo
Ctrl+C
```

Divirta-se desenhando! 🎨
