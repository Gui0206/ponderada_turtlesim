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

### Parte C: Resultados da Pipeline (1:10 - 1:30)

**O que falar:**
"Aqui estão os resultados de cada etapa do processamento. Você pode ver como a imagem original do cachorro passa por transformações até extrair apenas as bordas relevantes."

**O que mostrar:**
- Mostrar imagem estática: `dog.png` (imagem original)
- Mostrar imagem estática: `pipeline_dog.png` (6 estágios de processamento)
- Mostrar imagem estática: `paths_dog.png` (caminhos mapeados no espaço turtle)

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
  turtle_x = margem + (x - min_x) * escala
  turtle_y = margem + (max_y - y) * escala
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

## 📹 Cena 5: Demonstração do Resultado Final (3:10 - 3:50)

**O que falar:**
"Este é o resultado final: a tartaruga desenhou com sucesso o contorno do cachorro usando todos os algoritmos que implementei. A imagem original foi processada, os contornos extraídos, mapeados para o espaço do Turtlesim, e a tartaruga reproduziu o desenho com precisão."

**O que mostrar:**
- Mostrar imagem estática: `desenho_dog.png` (resultado final no turtlesim)
- Pode fazer zoom ou mostrar em tela cheia
- Apontar para os detalhes do desenho (cabeça, orelhas, corpo)

**O que falar enquanto mostra a imagem:**
"Como podem ver, a tartaruga extraiu apenas os pixels das bordas, mapeou para o espaço do Turtlesim, e usou teleportação para pular entre partes desconexas do desenho, sem desenhar linhas extras. O resultado é um desenho fiel ao contorno do cachorro."

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

- [ ] VS Code aberto com pasta do projeto
- [ ] Imagens prontas:
  - [ ] dog.png (imagem original)
  - [ ] pipeline_dog.png (6 estágios)
  - [ ] paths_dog.png (caminhos turtle)
  - [ ] desenho_dog.png (resultado final)
- [ ] Microfone testado
- [ ] OBS/software de gravação configurado
- [ ] Resolução em 1080p ou superior
- [ ] Iluminação adequada

---

## 🎬 Dicas de Gravação

1. **Estrutura simples:** Sem código em execução, apenas mostrar imagens e explicar o código visualmente

2. **Edição recomendada:** Use DaVinci Resolve (gratuito) para:
   - Juntar clips/imagens
   - Adicionar transições suaves
   - Zoom em código importante (quando mostrar telas de código)
   - Adicionar legendas com nomes de funções
   - Inserir timestamps ou marcadores

3. **Deixar claro:**
   - Qual arquivo está abrindo (mostrar path no título)
   - Qual função está mostrando (highlight visual)
   - Qual é o resultado (mostrar imagens sequencialmente)

4. **Pacing:** Como não há execução ao vivo:
   - Pode gravar tudo em estúdio com controle total
   - Gravar código com zoom e destaques
   - Gravar imagens com apresentação clara
   - Deixar tempo suficiente para ler código

---

## 📹 Exemplo de Estrutura de Gravação

```
Gravações Necessárias:
├── Intro.mp4 (0:00-0:20)
├── CodeOverview.mp4 (0:20-0:35) - Mostrar image_processor.py
├── SobelAlgorithm.mp4 (0:35-1:10) - Mostrar função Sobel
├── ImageResults.mp4 (1:10-1:30) - Mostrar imagens estáticas
├── Mapping.mp4 (1:30-2:20) - Mostrar turtle_drawer.py
├── ROS2Control.mp4 (2:20-3:10) - Mostrar serviços ROS
├── FinalResult.mp4 (3:10-3:50) - Mostrar desenho_dog.png
└── Conclusion.mp4 (3:50-4:00) - Conclusão
```

---

## ⏱️ Resumo de Tempos

| Cena | Descrição | Tempo |
|------|-----------|-------|
| 1 | Introdução | 0:20 |
| 2A | Visão Geral | 0:15 |
| 2B | Sobel Details | 0:35 |
| 2C | Resultados Imagens | 0:20 |
| 3 | Mapeamento | 0:50 |
| 4 | ROS 2 Control | 0:50 |
| 5 | Resultado Final | 0:40 |
| 6 | Conclusão | 0:10 |
| **TOTAL** | | **~4:00** |

---

## 🎯 Fluxo Visual Recomendado

1. **Código em VS Code** → Zoom nos pontos importantes
2. **Imagens estáticas** → Apresentar sequencialmente
3. **Explicação verbal** → Sincronizada com o visual

Isso cria uma apresentação limpa, profissional e fácil de acompanhar.

---

**Boa sorte na gravação! 🎥**
