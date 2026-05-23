# Roteiro de Vídeo - Turtle Draw
**Duração total: ~4 minutos**

---

## 📹 Cena 1: Introdução (0:00 - 0:20)

**O que falar:**
"Olá! Eu sou [seu nome] e este é o Turtle Draw, um projeto que implementa uma pipeline completa de visão computacional do zero para fazer a tartaruga do ROS 2 desenhar o contorno de uma imagem."

**O que mostrar:**
- Tela com o projeto aberto (VS Code com a pasta `turtle_draw_ws`)
- Mostrar a estrutura de pastas rapidamente

**Tempo: 20 segundos**

---

## 📹 Cena 2: Pipeline de Visão Computacional (0:20 - 1:30)

### Parte A: Visão Geral (0:20 - 0:35)

**O que falar:**
"A pipeline tem 5 etapas principais: Carregamento da imagem, Pré-processamento com Gaussian Blur, Detecção de bordas com Sobel, Non-Maximum Suppression para afinar as bordas, e finalmente extração dos pontos para desenho."

**O que mostrar:**
- Abrir arquivo: `image_processor.py`
- Mostrar a classe `ImageProcessor` e seus métodos principais
- Scroll rápido pelos métodos: `gaussian_blur()`, `sobel_edge_detection()`, `non_maximum_suppression()`

**Tempo: 15 segundos**

---

### Parte B: Detalhes de um Algoritmo (0:35 - 1:10)

**O que falar:**
"A detecção de bordas é implementada com os operadores Sobel, que calculam a derivada da imagem em X e Y. Isso permite identificar onde há mudanças bruscas de intensidade, que correspondem aos contornos da imagem."

**O que mostrar:**
- Abrir a função `sobel_edge_detection()` em `image_processor.py` (linhas ~95-110)
- Highlight dos kernels Sobel:
  ```python
  sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
  sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
  ```
- Mostrar o cálculo: `magnitude = np.sqrt(gx**2 + gy**2)`

**Tempo: 35 segundos**

---

### Parte C: Visualização dos Resultados (1:10 - 1:30)

**O que falar:**
"Para debugar e visualizar cada etapa, implementei uma ferramenta que mostra o resultado de cada estágio. Vou executar para mostrar como funciona na prática."

**O que mostrar:**
- Terminal rodando:
  ```bash
  ros2 run turtle_draw_pkg vision_pipeline ~/Desktop/ponderada_ros/dog.png
  ```
- Mostrar o output no terminal (pode fazer ahead of time e só mostrar)
- Mostrar as imagens geradas:
  - `pipeline_visualization.png` (6 estágios)
  - `turtle_paths.png` (caminhos no espaço turtle)

**Tempo: 20 segundos**

---

## 📹 Cena 3: Mapeamento para Turtle Space (1:30 - 2:20)

**O que falar:**
"Depois de extrair os pixels das bordas, preciso convertê-los para coordenadas que o Turtlesim entenda. O Turtlesim usa um espaço de 0 a 11 em ambos os eixos. Implementei uma transformação que mapeia os pixels da imagem para esse espaço."

**O que mostrar:**
- Abrir arquivo: `turtle_drawer.py`
- Mostrar função: `extract_points_from_binary_image()` (linhas ~45-80)
- Highlight da transformação:
  ```python
  turtle_x = margin + (x - min_x) * scale
  turtle_y = margin + (max_y - y) * scale
  ```
- Explicar: "A fórmula normaliza as coordenadas da imagem e as escala para caber no espaço do turtle"

**Tempo: 50 segundos**

---

## 📹 Cena 4: Controle ROS 2 (2:20 - 3:10)

**O que falar:**
"Para desenhar, uso dois serviços do ROS 2: TeleportAbsolute para mover a tartaruga, e SetPen para controlar a caneta (levantar e abaixar). A estratégia é: se a distância para o próximo ponto é grande, levanto a caneta, teleporto, e abaixo de novo."

**O que mostrar:**
- Abrir arquivo: `turtle_drawer.py`
- Mostrar função: `draw_image()` (linhas ~90-130)
- Highlight das partes importantes:
  ```python
  self.set_pen(off=1)  # Levanta caneta
  self.teleport_turtle(x, y)  # Teleporta
  self.set_pen(off=0)  # Abaixa caneta
  ```
- Mostrar a lógica de detecção de saltos:
  ```python
  distance = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)
  if distance > jump_threshold:
      # Levanta e pula
  ```

**Tempo: 50 segundos**

---

## 📹 Cena 5: Demonstração ao Vivo (3:10 - 3:50)

**O que falar:**
"Agora vou demonstrar o resultado final. A tartaruga vai desenhar o contorno do cão usando todos os algoritmos que implementei."

**O que mostrar:**
- **Terminal 1:** Turtlesim rodando (já deve estar aberto)
- **Terminal 2:** Executar:
  ```bash
  ros2 run turtle_draw_pkg turtle_drawer ~/Desktop/ponderada_ros/dog.png
  ```
- Mostrar a tartaruga desenhando (deixa uns 30-40 segundos)
- Se possível, fazer zoom no desenho ou mostrar a janela do turtlesim claramente

**O que falar enquanto desenha:**
"Como podem ver, a tartaruga está desenhando o contorno do cão. Ela extrai apenas os pixels das bordas, mapeia para o espaço do turtlesim, e usa teleportação para pular entre partes desconexas do desenho, sem desenhar linhas extras."

**Tempo: 40 segundos**

---

## 📹 Cena 6: Conclusão (3:50 - 4:00)

**O que falar:**
"Este projeto demonstra como integrar visão computacional com robótica usando ROS 2. Todo o processamento de imagem foi implementado do zero, sem usar bibliotecas prontas. Obrigado por assistir!"

**O que mostrar:**
- Logo/nome do projeto
- Ou imagem do desenho final no turtlesim

**Tempo: 10 segundos**

---

## 📋 Checklist para Gravação

- [ ] Terminal pronto com turtlesim rodando em background
- [ ] VS Code aberto com pasta do projeto
- [ ] Imagens de teste (`dog.png`, `test_shapes.png`) disponíveis
- [ ] Arquivos de visualização (`pipeline_visualization.png`, `turtle_paths.png`) já gerados ou prontos para gerar
- [ ] Microfone testado
- [ ] OBS/software de gravação configurado
- [ ] Resolução em 1080p ou superior
- [ ] Iluminação adequada

---

## 🎬 Dicas de Gravação

1. **Gravação em partes:** Não precisa ser tudo ao vivo. Você pode gravar:
   - Código (pausado)
   - Terminal (rodando)
   - Demonstração (ao vivo ou pré-gravada)

2. **Edição simples:** Use DaVinci Resolve (gratuito) para:
   - Juntar clips
   - Adicionar transições
   - Zoom em código importante
   - Adicionar legendas com nomes de funções

3. **Deixar claro:**
   - Qual arquivo está abrindo (mostrar path)
   - Qual função está mostrando (highlight visual)
   - Qual é o output (mostrar terminal ou imagens)

4. **Timing:** Se ficar perto de 4 min, você pode:
   - Cortar a demonstração (30 segundos é suficiente)
   - Acelerar vídeo do turtle desenhando (2x speed)
   - Pular a Cena 3 se ficou longo

---

## 📹 Exemplo de Estrutura de Pasta para Edição

```
Video_TurtleDraw/
├── Cena1_Intro.mp4
├── Cena2A_Visao_Geral.mp4
├── Cena2B_Sobel.mp4
├── Cena2C_Visualizacao.mp4
├── Cena3_Mapeamento.mp4
├── Cena4_ROS2.mp4
├── Cena5_Demo.mp4
├── Cena6_Conclusao.mp4
└── Final_Video.mp4 (após edição)
```

---

## ⏱️ Resumo de Tempos

| Cena | Descrição | Tempo |
|------|-----------|-------|
| 1 | Introdução | 0:20 |
| 2A | Visão Geral | 0:15 |
| 2B | Sobel Details | 0:35 |
| 2C | Visualização | 0:20 |
| 3 | Mapeamento | 0:50 |
| 4 | ROS 2 Control | 0:50 |
| 5 | Demo ao Vivo | 0:40 |
| 6 | Conclusão | 0:10 |
| **TOTAL** | | **~4:00** |

---

**Boa sorte na gravação! 🎥**
