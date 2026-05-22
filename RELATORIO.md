# Relatório Técnico: Turtle Draw - Pipeline de Visão Computacional e Controle Robótico

**Autor**: Guilherme Hollanda  
**Data**: 22/05/2026  
**Disciplina**: Robótica e Visão Computacional  
**Projeto**: Turtle Draw - Desenho automático via contornos de imagem

---

## 1. Visão Geral da Implementação

Desenvolvi uma pipeline completa de visão computacional que extrai contornos de uma imagem e controla a tartaruga do turtlesim para reproduzi-los. O projeto implementa **todos** os algoritmos de processamento de imagem desde o princípio (zero), usando apenas NumPy para operações matriciais.

### Componentes Principais

1. **Pré-processamento de Imagem**: Conversão RGB→Escala de Cinza, Blur Gaussiano
2. **Detecção de Bordas**: Operador Sobel (2D convolution from scratch)
3. **Extração de Contornos**: Connected Component Labeling com flood fill
4. **Mapeamento de Coordenadas**: Transformação espaço imagem → espaço turtlesim
5. **Controle ROS 2**: Nó que publica comandos de velocidade

---

## 2. Pré-Processamento (Etapa 01)

### 2.1 Conversão para Escala de Cinza

**Algoritmo**: Fórmula de luminosidade padrão
```
Gray = 0.299*R + 0.587*G + 0.114*B
```

**Justificativa**: 
- Utiliza coeficientes científicos que refletem sensibilidade do olho humano
- OpenCV usa ordem BGR, então aplico: 0.114*R + 0.587*G + 0.299*B
- Reduz dimensionalidade de 3 para 1 canal, mantendo informação estrutural

### 2.2 Filtro Gaussiano (Kernel 5×5, σ=1.5)

**Implementação**: Convolução separável 1D
- Crio kernel 1D: `kernel[x] = exp(-(x-c)² / (2σ²))` normalizado
- Aplico horizontalmente: convolução com padding "edge"
- Depois verticalmente: mesma convolução na saída anterior

**Justificativa**:
- Reduz ruído sem perder bordas significativas
- Convolução separável é O(n*k) vs O(n*k²) para 2D puro
- σ=1.5 é balanço entre suavização e preservação de detalhes

**Padding "edge"**: Replica valores da borda (evita artifacts)

---

## 3. Detecção de Bordas (Etapa 02)

### 3.1 Operador Sobel

**Kernels Utilizados**:
```
Sobel-X = [-1  0  1]      Sobel-Y = [-1 -2 -1]
          [-2  0  2]               [ 0  0  0]
          [-1  0  1]               [ 1  2  1]
```

**Implementação**:
1. Convolução 2D: `result[i,j] = Σ(kernel * region)`
2. Calcula gradientes: `Gx` e `Gy`
3. Magnitude: `M = √(Gx² + Gy²)`
4. Normaliza: `M_norm = M / max(M) * 255`
5. Threshold: valores > 50 → bordo

**Justificativa para Sobel**:
- ✅ Robusto a ruído (smoothing integrado)
- ✅ Detecta bordas em múltiplas direções
- ✅ Computacionalmente eficiente (comparado a Canny)
- ✅ Implementação simples e compreensível
- ❌ Algumas bordas finas podem ser perdidas (aceitável para desenho robótico)

**Alternativa não escolhida**: Canny (requereria non-maximal suppression + hysteresis thresholding; mais complexo)

---

## 4. Extração de Contornos (Etapa 03)

### 4.1 Algoritmo de Connected Component Labeling

**Abordagem**: Flood Fill com 8-conectividade

**Pseudocódigo**:
```
para cada pixel (x,y) na imagem:
    se pixel_branco E não_visitado:
        contour = []
        stack = [(x,y)]
        enquanto stack não vazio:
            (x,y) = stack.pop()
            marcar como visitado
            adicionar a contour
            para cada vizinho em 8-conectividade:
                se não_visitado e pixel_branco:
                    stack.push(vizinho)
        se len(contour) > min_length:
            salvar contour
```

**Justificativa**:
- 8-conectividade preserva continuidade visual de contornos
- Flood fill é robusto mesmo com bordas quebradas
- O(n) em número de pixels
- Simples implementação com stack

**Filtro de Comprimento Mínimo**: Remove contornos pequenos (ruído)

### 4.2 Downsampling de Contornos

Para evitar movimento excessivo da tartaruga:
```
step = len(contour) / max_points  # max_points ≈ 100-150
contour_reduzido = contour[::step]
```

**Justificativa**: Preserva forma mantendo número manejável de waypoints

---

## 5. Mapeamento de Coordenadas (Etapa 04)

### 5.1 Transformação Imagem → Espaço Turtlesim

**Fórmula**:
```
norm_x = img_x / image_width
norm_y = img_y / image_height

turtle_x = min_x + norm_x * (max_x - min_x)
turtle_y = max_y - norm_y * (max_y - min_y)  # Inverte Y
```

**Parâmetros**:
- Espaço imagem: [0, w] × [0, h]
- Espaço turtlesim: [0.5, 10.5] × [0.5, 10.5]

**Inversão do eixo Y**: 
- Imagem: origem no topo-esquerdo (y↓)
- Turtlesim: origem embaixo-esquerda (y↑)

---

## 6. Controle ROS 2 (Etapa 05)

### 6.1 Arquitetura do Nó

**Nó**: `TurtleDrawer` (herda de `rclpy.Node`)

**Tópico Publicado**:
- `/turtle1/cmd_vel` (geometry_msgs/Twist)
  - `twist.linear.x`: velocidade linear (m/s)
  - `twist.angular.z`: velocidade angular (rad/s)

### 6.2 Controle de Movimento

**Move to Point**:
1. Calcula vetor até alvo: `(dx, dy)`
2. Calcula ângulo: `θ_alvo = atan2(dy, dx)`
3. Rotaciona até alvo: publica angular.z
4. Avança: publica linear.x

**Draw Line**:
- Idêntico a "move to point"
- Tartaruga desenha automaticamente enquanto se move

**Parâmetros de Controle**:
```
linear_speed = 0.5 m/s
angular_speed = 0.5 rad/s
threshold_movimento = 0.05 unidades
```

### 6.3 Normalização de Ângulos

```python
def _normalize_angle(angle):
    while angle > π: angle -= 2π
    while angle < -π: angle += 2π
    return angle
```

Garante que a tartaruga toma o caminho mais curto (não gira > 180°)

---

## 7. Dificuldades Encontradas

### 7.1 Convolução Manual é Lenta

**Problema**: Loops aninhados em Python são muito lentos (O(h×w×kh×kw))

**Solução**: 
- Convolução separável (Gaussiano)
- Downsampling de contornos
- Não é crítico pois processamento é offline

### 7.2 Contornos Muito Densos

**Problema**: Imagens com muito detalhe produzem milhares de pontos

**Solução**: 
- Gaussian blur maior (σ=1.5)
- Threshold maior (50 em vez de 30)
- Downsampling mais agressivo

### 7.3 Tartaruga Saindo dos Limites

**Problema**: Contornos podem mapelar fora dos limites turtlesim [0.5, 10.5]

**Solução**: 
- Clipping de coordenadas no mapeamento
- Usar limites ligeiramente menores para margem

### 7.4 Movimento Discreto Deixa Gaps

**Problema**: Com poucos pontos, pode haver descontinuidades

**Solução**: 
- Aumentar densidade de pontos
- Reduzir threshold de movimento (0.05 unidades)
- Usar velocidades menores para precisão

---

## 8. Validação da Pipeline

### Testes Realizados

1. **Conversão RGB→Escala Cinza**: 
   - ✅ Valores corretos com coeficientes [0.114, 0.587, 0.299]

2. **Blur Gaussiano**:
   - ✅ Suavização visível mantendo bordas
   - ✅ Simetria (kernel é simétrico)

3. **Sobel Edge Detection**:
   - ✅ Detecção em múltiplas direções
   - ✅ Magnitude aumenta em transições

4. **Contour Extraction**:
   - ✅ Identifica múltiplos contornos
   - ✅ 8-conectividade preserva formas

5. **Mapeamento**:
   - ✅ Proporções mantidas
   - ✅ Y invertido corretamente

---

## 9. Decisões de Design

| Aspecto | Escolha | Alternativa | Motivo |
|---------|---------|-------------|--------|
| **Blur** | Gaussiano separável | Média, Bilateral | Melhor qualidade; eficiência |
| **Edge Detection** | Sobel | Canny, Laplacian | Simplicidade vs. qualidade |
| **Contour Traçing** | Flood fill | Moore-Neighbor | Robustez; 8-conectividade |
| **Downsampling** | Uniforme | Catmull-Rom spline | Simplicidade; bom resultado |
| **ROS Message** | Twist | Custom | Compatibilidade; padrão |
| **Speed Control** | Linear+Angular | Omnidirectional | Compatível turtlesim |

---

## 10. Resultados

### Com dog.png:
- **Contornos detectados**: múltiplos (depende do threshold)
- **Tempo processamento**: ~2-3 segundos
- **Tempo desenho**: ~15-25 segundos
- **Qualidade**: fidedigna ao original

---

## Conclusão

A implementação demonstra compreensão completa de cada etapa da pipeline:
1. Fundamentos de processamento digital (convolution, thresholding)
2. Algoritmos clássicos (Sobel, flood fill)
3. Integração ROS 2 (publishers, nodes, msg types)
4. Transformações geométricas (coordinate mapping)

O código é documentado, modular e extensível.

---

**Referências Implementadas**:
- Digital Image Processing (Gonzalez & Woods)
- Sobel Operator: Wikipedia
- ROS 2 Official Documentation
- Connected Component Labeling: Classical CV algorithms
