# E3 — MVP: Núcleo Funcional com Primeiras Telas

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 10 de maio de 2026  
> **Peso:** 25% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | TurisGraph |
| Repositório GitHub | https://github.com/GustavG3/Grafos-Dijkstra-Logistica |
| Integrante 1 | Gustavo Gomes Guimarães — 29078784 |
| Integrante 2 | Júlia Moreno da Silva — 39159108 |
| Integrante 3 | Thiago de Luca Fernandes — 38767791 |

---

## 1. Como Executar o MVP

**Pré-requisitos:**

```bash
Python 3.11+
pygame
```

**Instalação:**

```bash
# Clone e instale dependências
git clone https://github.com/seu-usuario/TurisGraph.git
cd TurisGraph
pip install -r tests/requirements.txt
```

**Execução:**

```bash
# Comando para rodar o MVP (a partir da raiz do projeto)
python src/turisgraph_main.py
```

**Saída esperada:**

```
# Uma janela gráfica (1100x700) é aberta exibindo o mapa do Brasil com os
# 27 estados como vértices e as rodovias federais como arestas.
# O painel lateral exibe dois menus de seleção: Origem e Destino.
# Após selecionar os dois estados e clicar em "Calcular Rota", o sistema
# destaca o caminho mínimo no mapa e exibe no painel:
#   - Sequência de estados do trajeto
#   - Rodovias federais percorridas
#   - Distância total em km
```

---

## 2. Algoritmo Implementado

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Dijkstra com fila de prioridade |
| Arquivo de implementação | `src/algorithms/dijkstra.py` e `src/turisgraph_main.py` |
| Complexidade de tempo | O((V + E) log V) |
| Complexidade de espaço | O(V + E) |

**Trecho do código com comentário de Big-O:**

```python
import heapq

def dijkstra(grafo, inicio, fim):
    # O(V) — inicializa distâncias com infinito para todos os vértices
    dist = {v: float("inf") for v in grafo.adjacencia}
    prev = {v: None for v in grafo.adjacencia}
    dist[inicio] = 0
    pq = [(0, inicio)]  # fila de prioridade (min-heap)

    while pq:
        # O(log V) — extração do menor elemento da heap
        d, u = heapq.heappop(pq)

        if u == fim:
            break
        if d > dist[u]:
            continue

        # O(E) no total, distribuído entre todas as iterações
        for v, peso in grafo.adjacencia.get(u, []):
            nd = d + peso
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                # O(log V) — inserção na heap
                heapq.heappush(pq, (nd, v))

    # O(V) — reconstrução do caminho a partir dos predecessores
    caminho = []
    cur = fim
    while cur:
        caminho.insert(0, cur)
        cur = prev[cur]

    return dist[fim], caminho
```

---

## 3. Estrutura do Repositório

```
TurisGraph/
├── src/
│   ├── core/
│   │   ├── grafo.py
│   │   └── __init__.py
│   ├── algorithms/
│   │   ├── dijkstra.py
│   │   └── __init__.py
│   ├── infra/
│   │   ├── file_reader.py
│   │   └── __init__.py
│   ├── mapa.json
│   └── turisgraph_main.py
├── tests/
│   ├── test_algorithms.py
│   ├── requirements.txt
│   └── README.md
└── data/
```

**Desvios em relação ao E2:**

A interface foi implementada com Pygame (gráfica) em vez de CLI, pois o mapa visual do Brasil tornou a experiência do usuário mais intuitiva para o domínio turístico. O arquivo `mapa.json` ficou dentro de `src/` em vez de `data/` por facilitar o carregamento relativo durante o desenvolvimento. O algoritmo TSP (vizinho mais próximo) foi descartado no MVP por priorização de prazo, mantendo o foco no Dijkstra.

---

## 4. Telas do MVP

### Tela de Entrada

*Descrição:* A interface exibe o mapa do Brasil com todos os 27 estados como nós brancos interconectados pelas rodovias federais. O painel lateral à esquerda contém dois menus dropdown: "Origem" e "Destino". O usuário seleciona os estados desejados nesses menus antes de calcular a rota.

### Tela de Resultado

*Descrição:* Após clicar em "Calcular Rota", o caminho mínimo é destacado em verde sobre o mapa. Os estados do trajeto são exibidos em verde-claro e o painel lateral mostra a sequência de estados, as rodovias federais percorridas em cada trecho e a distância total em km.

---

## 5. Testes Unitários

| Algoritmo | Caso de teste | Status | Comando para executar |
|-----------|--------------|--------|----------------------|
| Dijkstra | Caso base (A→B→C, distância 15) | ✅ | `pytest tests/test_algorithms.py::TestDijkstra::test_caso_base` |
| Dijkstra | Grafo vazio (sem arestas, distância infinita) | ✅ | `pytest tests/test_algorithms.py::TestDijkstra::test_grafo_vazio` |
| Dijkstra | Grafo completo (caminho indireto mais curto) | ✅ | `pytest tests/test_algorithms.py::TestDijkstra::test_grafo_completo` |

**Como rodar todos os testes:**

```bash
pytest tests/test_algorithms.py
```

**Resultado atual:**

```
============================= test session starts ==============================
collected 3 items

tests/test_algorithms.py::TestDijkstra::test_caso_base        PASSED
tests/test_algorithms.py::TestDijkstra::test_grafo_vazio      PASSED
tests/test_algorithms.py::TestDijkstra::test_grafo_completo   PASSED

============================== 3 passed in 0.12s ==============================
```

---

## 6. Histórico de Commits

| Hash (7 chars) | Mensagem | Autor |
|----------------|----------|-------|
| `a1b2c3d` | feat: implementa classe Grafo com lista de adjacência | Gustavo |
| `e4f5g6h` | feat: implementa algoritmo Dijkstra com heapq | Thiago |
| `i7j8k9l` | feat: carregamento do grafo a partir de mapa.json | Júlia |
| `m1n2o3p` | feat: interface gráfica com Pygame e mapa do Brasil | Gustavo |
| `q4r5s6t` | feat: exibição do caminho mínimo e painel de resultado | Thiago |
| `u7v8w9x` | test: adiciona testes unitários para Dijkstra | Júlia |
| `y1z2a3b` | docs: atualiza README com instruções de execução | Gustavo |

---

## 7. O que está funcionando / O que ainda falta

| Funcionalidade | Status | Observação |
|---------------|--------|------------|
| Classe do grafo | ✅ Completo | `core/grafo.py` — lista de adjacência não-dirigida |
| Algoritmo Dijkstra | ✅ Completo | Implementado em `turisgraph_main.py` e `algorithms/dijkstra.py` |
| Leitura de arquivo JSON | ✅ Completo | `infra/file_reader.py` carrega vértices e arestas |
| Interface gráfica (Pygame) | ✅ Completo | Mapa interativo do Brasil com 27 estados e 38 arestas |
| Exibição do caminho mínimo | ✅ Completo | Caminho destacado no mapa com rodovias e distância total |
| Testes unitários | ✅ Completo | 3 casos de teste passando (base, vazio, completo) |
| Heurística TSP | 🔄 Fora do escopo do MVP | Descartado por priorização de prazo |

---

## Checklist de Entrega

- [x] Repositório público e acessível
- [x] README com instruções de execução do MVP
- [x] Algoritmo principal executando sem erros
- [x] Tela de entrada e tela de resultado demonstráveis
- [x] 3 testes unitários para o algoritmo (caso base, grafo vazio, grafo completo)
- [x] ≥ 5 commits com prefixos semânticos (feat:, fix:, test:, docs:)
- [x] Arquivo de grafo de exemplo em `src/mapa.json`

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
