# Relatório Técnico: Turtle Draw - Pipeline de Visão Computacional

## 1. Visão Geral

Este projeto implementa uma pipeline completa de visão computacional **do zero** (apenas NumPy para operações matriciais) que lê uma imagem, extrai seus contornos e controla a tartaruga do turtlesim para desenhá-los em tempo real.

### Etapas da Pipeline
1. **Pré-processamento**: Normalização e suavização
2. **Detecção de Bordas**: Operadores Sobel + Non-Maximum Suppression
3. **Extração de Contornos**: Moore-Neighbor tracing
4. **Planejamento de Caminho**: Transformação para espaço turtle + sequenciamento
5. **Controle ROS 2**: Publicação de comandos de movimento

---

## 2. Decisões de Implementação

### 2.1 Pré-processamento (Gaussian Blur)

**Escolha**: Convolução separável com kernel Gaussiano 1D

**Justificativa**:
- Kernel separável reduz complexidade de O(k²) para O(2k) onde k é o tamanho do kernel
- Mais eficiente e reduz ruído mantendo bordas relevantes
- Sigma = 1.5 equilibra suavização e preservação de detalhes

**Implementação**:
```python
# Cria kernel 1D Gaussiano: exp(-0.5 * (x/σ)²)
# Aplica separadamente em X e Y (duas convoluções 1D em vez de uma 2D)
# Padding por reflexão evita artefatos nas bordas
```

---

### 2.2 Detecção de Bordas (Sobel + NMS)

**Escolha**: Operadores Sobel com Non-Maximum Suppression

**Justificativa**:
- Sobel: Combina suavização com derivada = robusto a ruído
- NMS: Afina bordas removendo pixels que não são máximos locais na direção do gradiente
- Emula o comportamento do Canny edge detector sem implementar todas as complexidades

**Operadores Sobel**:
```
Gx = [[-1  0  1]    Gy = [[-1 -2 -1]
      [-2  0  2]          [ 0  0  0]
      [-1  0  1]]         [ 1  2  1]]
```

**Non-Maximum Suppression**:
- Para cada pixel, calcula a direção do gradiente (8 direções)
- Compara magnitude com vizinhos na direção perpendicular ao gradiente
- Mantém apenas máximos locais → bordas mais finas

**Resultado**: Bordas bem definidas, sem espessura excessiva

---

### 2.3 Extração de Contornos (Moore-Neighbor Tracing)

**Escolha**: Moore-Neighbor contour tracing algorithm

**Justificativa**:
- Algoritmo determinístico que segue o contorno de componentes conectadas
- Eficiente: O(n) onde n é o perímetro do contorno
- Produz sequência ordenada de pontos (essencial para desenho)

**Algoritmo**:
1. Busca ponto inicial (primeiro pixel branco não visitado)
2. Segue vizinhança Moore (8 conexões) no sentido do contorno
3. Retorna para ponto inicial → contorno fechado
4. Marca todos como visitados para evitar re-rastreamento

**Filtragens aplicadas**:
- Contornos com < 10 pontos são descartados (ruído)
- Ramer-Douglas-Peucker simplification com ε=3.0
  - Reduz número de pontos mantendo forma
  - Facilita movimento mais suave do turtle

---

### 2.4 Planejamento de Caminho (Transformação de Coordenadas)

**Escolha**: Mapeamento linear com inversão de eixo Y

**Justificativa**:
- Imagem: (0,0) no topo-esquerdo, Y aumenta para baixo
- Turtle: (0,0) no centro, Y aumenta para cima
- Transformação garante que desenho não fica invertido

**Transformação**:
```
turtle_x = (img_x / width) * 11
turtle_y = 11 - (img_y / height) * 11
```

**Sequenciamento de movimento**:
- Para cada par de pontos consecutivos:
  1. Calcula ângulo necessário (arctan2)
  2. Calcula distância (Euclidiana)
  3. Emite comando: rotacionar (se necessário) → mover
- Suavização por média móvel reduz jitter

---

### 2.5 Controle ROS 2 (Turtle Drawer Node)

**Arquitetura**:
- Subscriber em `/turtle1/pose` (recebe posição atual)
- Publisher em `/turtle1/cmd_vel` (envia velocidade)
- Controle proporcional: velocidade proporcional à distância

**Algoritmo de movimento**:
```python
# Para cada ponto alvo:
1. Lê posição atual (callback de pose)
2. Calcula vetor erro (distância + ângulo)
3. Se ângulo > tolerância: rotaciona
   Senão: move na direção do alvo
4. Repete até alcançar alvo (tol = 0.05)
```

**Parâmetros tuning**:
- Linear speed = 2.0 (equilibra precisão e velocidade)
- Angular speed = 1.0 rad/s
- Position tolerance = 0.05 unidades

---

## 3. Dificuldades Encontradas e Soluções

### Problema 1: Bordas grossas
**Causa**: Magnitude de Sobel produz bordas com vários pixels de espessura
**Solução**: Non-maximum suppression baseado em direção de gradiente → bordas de 1 pixel

### Problema 2: Ruído em contornos
**Causa**: Objetos pequenos detectados como contornos (poeira/artefatos)
**Solução**: Filtro de tamanho mínimo (< 10 pontos) + Ramer-Douglas-Peucker

### Problema 3: Turtle oscila ao atingir ponto
**Causa**: Velocidade constante mesmo perto do alvo
**Solução**: Velocidade proporcional à distância restante

### Problema 4: Performance com imagens grandes
**Causa**: Convolução 2D é O(h×w×k²) para cada operação
**Solução**: Usar convolução separável (O(h×w×k)) + reduzir tamanho da imagem

### Problema 5: Coordenadas invertidas
**Causa**: Imagem e turtle têm origem em pontos diferentes
**Solução**: Transformação com inversão de eixo Y

---

## 4. Validação e Testes

A pipeline foi testada com:
- Imagens simples (linhas, retângulos, círculos)
- Imagens complexas (fotografias, desenhos)
- Visualização em cada etapa (pipeline_visualization.png)
- Logs detalhados de execução

---

## 5. Conclusão

A implementação fornece uma solução completa e educativa de visão computacional. Todos os algoritmos foram implementados manualmente (sem OpenCV/scipy para processamento), demonstrando compreensão profunda dos conceitos de processamento de imagem.

**Principais contribuições**:
- Pipeline de Sobel + NMS eficiente
- Moore-Neighbor tracing determinístico
- Integração com ROS 2 para controle robótico
- Ferramentas de visualização para debug
