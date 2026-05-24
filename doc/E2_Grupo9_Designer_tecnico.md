# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 13 de abril de 2026  
> **Peso:** 20% da nota final  

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

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Dijkstra |
| Categoria | Busca / Caminho mínimo |
| Complexidade de tempo | O((V + E) log V) com fila de prioridade |
| Complexidade de espaço | O(V + E) |
| Problema que resolve | Encontra o caminho de menor distância entre dois estados em um grafo ponderado não-dirigido. |

**Por que este algoritmo foi escolhido?**

Dijkstra é eficiente para grafos com pesos positivos, como rotas rodoviárias com distâncias em quilômetros. Ele permite calcular rapidamente o menor caminho entre dois estados brasileiros, atendendo ao objetivo principal do projeto. A implementação utilizou a estrutura `heapq` do Python, garantindo a complexidade O((V + E) log V).

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| Bellman-Ford | Apesar de resolver o problema de caminho mínimo, possui complexidade O(V · E), menos eficiente que Dijkstra. Sua principal vantagem é lidar com pesos negativos, o que não se aplica ao domínio turístico, já que distâncias são sempre valores positivos. |

**Limitações no contexto do problema:**

- Não resolve roteiros completos envolvendo múltiplos destinos (Problema do Caixeiro Viajante).
- Calcula apenas o caminho de menor distância; não considera simultaneamente outros fatores como custo monetário ou tempo de viagem.

**Referência bibliográfica:**

> NUNES, Iago Victor Pires de Souza. Fluxo em grafos: uma aplicação da teoria dos grafos. 2023. Trabalho de Conclusão de Curso (Licenciatura em Matemática) – Universidade Estadual de Goiás, Anápolis, 2023.

---

### 1.2 Algoritmo Adicional

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Heurística do Vizinho Mais Próximo (Nearest Neighbor) |
| Categoria | Guloso |
| Complexidade de tempo | O(n²) |
| Complexidade de espaço | O(n) |

**Justificativa:**

O algoritmo do Vizinho Mais Próximo complementa o Dijkstra ao possibilitar a geração de roteiros completos para múltiplos destinos, oferecendo uma solução aproximada para o Problema do Caixeiro Viajante. Apesar de não garantir a rota ótima, é simples, rápido e fornece resultados suficientemente bons para aplicações práticas em turismo, onde o foco é reduzir o total de quilômetros percorridos em um circuito entre vários estados.

**Referência bibliográfica:**

> ERTEL, Paula C. R.; BIRGIN, Ernesto G. Um método heurístico para o Problema do Caixeiro Viajante Suficientemente Próximo. In: XLIII Congresso Nacional de Matemática Aplicada e Computacional (CNMAC). Porto de Galinhas: Sociedade Brasileira de Matemática Aplicada e Computacional, 2024.

---

## 2. Arquitetura em Camadas

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/Pygame) | Interface gráfica com mapa interativo do Brasil para seleção de origem/destino e visualização das rotas | `turisgraph_main.py` |
| Aplicação (Service) | Orquestração das chamadas ao algoritmo e controle de estado da aplicação | `turisgraph_main.py` — classe `TurisGraphApp` |
| Domínio (Core) | Estruturas de dados do grafo e lógica do algoritmo Dijkstra | `core/grafo.py`, `algorithms/dijkstra.py` |
| Infraestrutura (I/O) | Leitura do arquivo JSON com os dados do mapa e escrita de resultados | `infra/file_reader.py`, `mapa.json` |

---

## 3. Estrutura de Diretórios

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

> **Observação:** A interface final foi implementada com Pygame (gráfica) em vez de CLI, pois permitiu apresentar o mapa do Brasil de forma visual e mais intuitiva para o domínio turístico.

---

## 4. Definição do Dataset

**Formato de entrada aceito:** JSON

**Estrutura do arquivo `mapa.json`:**

```json
{
  "vertices": 27,
  "arestas": [
    { "origem": "Paraná", "destino": "São Paulo", "peso": 400 },
    { "origem": "Paraná", "destino": "Santa Catarina", "peso": 400 },
    { "origem": "Santa Catarina", "destino": "Rio Grande do Sul", "peso": 320 }
  ]
}
```

O dataset utilizado contém 27 estados brasileiros como vértices e 38 conexões rodoviárias como arestas, com pesos representando distâncias em quilômetros. As conexões são baseadas nas principais rodovias federais que ligam estados vizinhos.

**Estratégia de geração do dataset:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | 27 (estados brasileiros, exceto o Distrito Federal) |
| Número de arestas | 38 (rodovias federais entre estados vizinhos) |
| Faixa de pesos | 100 km (RJ–ES) a 1200 km (RR–AP e MA–PA) |
| Critério de conexão | Adjacência geográfica real entre estados |

---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que foi implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 | Leitura do grafo a partir de arquivo JSON | Alta | Dado um arquivo `mapa.json` válido, quando o sistema carregar, então os vértices e arestas são carregados corretamente na estrutura de adjacência |
| 2 | Implementação do Dijkstra para caminho mínimo | Alta | Dado um grafo com pesos positivos, quando o usuário escolher origem e destino, então o sistema retorna o menor caminho em km e a sequência de estados |
| 3 | Interface gráfica com mapa do Brasil (Pygame) | Alta | Dado o mapa carregado, quando o usuário selecionar dois estados, então o sistema exibe o caminho destacado sobre o mapa com as rodovias percorridas |
| 4 | Exibição do roteiro com custo total e rodovias | Média | Dado um cálculo de rota concluído, quando exibido no painel, então o sistema mostra a sequência de estados, o total em km e as rodovias federais do trajeto |
| 5 | Testes unitários do algoritmo Dijkstra | Média | Dado o módulo de testes, quando executado com `pytest`, então os casos de teste base, grafo vazio e grafo completo passam com sucesso |

### 5.2 Out-of-Scope — O que NÃO foi feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Implementação exata do TSP | Complexidade computacional inviável no prazo acadêmico |
| Integração com APIs externas (Google Maps, OSRM) | Fora do escopo acadêmico |
| Consideração simultânea de múltiplos critérios (custo + tempo + distância) | Aumentaria a complexidade sem ganho direto para os objetivos do projeto |

---

## Checklist de Entrega

- [x] Big-O de tempo e espaço declarados para cada algoritmo
- [x] Ao menos 1 alternativa descartada com justificativa
- [x] Diagrama de arquitetura com 4 camadas identificadas
- [x] Referência bibliográfica para cada algoritmo (ABNT)
- [x] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [x] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [x] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
