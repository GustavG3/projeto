# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 13 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto |TurisGraph |
| Repositório GitHub | |
| Integrante 1 | Nome — RA |Gustavo Gomes Guimarães 29078784
| Integrante 2 | Nome — RA | Júlia Moreno da Silva  39159108
| Integrante 3 | Nome — RA | Thiago de Luca Fernandes 38767791


---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Dijkstra |
| Categoria | busca |
| Complexidade de tempo | 0((V+E)logV) com fila de prioridade|
| Complexidade de espaço | O(V + E ) |
| Problema que resolve |Encontra o caminho mínimo entre duas cidades em um grafo ponderado e não-dirigido.|

**Por que este algoritmo foi escolhido?**

<!-- Justifique a escolha para o seu domínio específico -->

Dijkstra é eficiente para grafos com pesos positivos, como rotas rodoviárias com custos de tempo ou distância. Ele permite calcular rapidamente o menor caminho entre dois pontos turísticos, atendendo ao objetivo principal do projeto.

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
|Bellman-Ford |Apesar de resolver o problema de caminho mínimo, possui complexidade 0(V . E), menos eficiente que Dijkstra. Além disso, sua principal vantagem é lidar com pesos negativos, o que não se aplica ao domínio turístico, já que distância, tempo e custo são sempre valores positivos.  |

**Limitações no contexto do problema:**

<!-- Liste ao menos 1 limitação relevante -->
Não resolve roteiros completos envolvendo múltiplos destinos (TSP).

**Referência bibliográfica:**

> <!-- Formato ABNT ou IEEE. Ex.: CORMEN, T. H. et al. Algoritmos: teoria e prática. 3. ed. Rio de Janeiro: Elsevier, 2012. -->

NUNES, Iago Victor Pires de Souza. Fluxo em grafos: uma aplicação da teoria dos grafos. 2023. Trabalho de Conclusão de Curso (Licenciatura em Matemática) – Universidade Estadual de Goiás, Anápolis, 2023.

---

### 1.2 Algoritmo Adicional *(se houver)*

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo |Heurística do Vizinho Mais Próximo (Nearest Neighbor)|
| Categoria | guloso |
| Complexidade de tempo | O(n2) |
| Complexidade de espaço | O(n) |

**Justificativa:**

<!-- Por que este segundo algoritmo complementa o projeto? -->
O algoritmo do Vizinho Mais Próximo complementa o Dijkstra ao gerar roteiros completos para múltiplos destinos, oferecendo uma solução aproximada para o Problema do Caixeiro Viajante. Apesar de não garantir a rota ótima, é simples, rápido e fornece resultados suficientemente bons para aplicações práticas em turismo, onde o foco é reduzir tempo e custo de viagem.

**Referência bibliográfica:**

> ERTEL, Paula C. R.; BIRGIN, Ernesto G. Um método heurístico para o Problema do Caixeiro Viajante Suficientemente Próximo. In: XLIII Congresso Nacional de Matemática Aplicada e Computacional (CNMAC). Porto de Galinhas: Sociedade Brasileira de Matemática Aplicada e Computacional, 2024.

---

## 2. Arquitetura em Camadas

> Insira o diagrama abaixo. Pode ser exportado do Draw.io, Excalidraw, etc.

![Diagrama de arquitetura](<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/1c979faf-5775-4677-8d97-04529b3d0bab" />)

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/CLI) | Interface simples para entrada de cidades e visualização de rotas| main.py, menus |

| Aplicação (Service) |Orquestração das chamadas de algoritmo e regras de negócio | service.py |

| Domínio (Core) | Estruturas de dados e lógica dos algoritmos| graph.py, algorithms/dijkstra.py, algorithms/tsp.py|

| Infraestrutura (I/O) |Leitura de arquivos CSV/JSON e escrita de resultados | io/file_reader.py |

---

## 3. Estrutura de Diretórios

```
TurisGraph/
├── docs/
│   ├── README.md
│   └── E1_template.md
│   └── E2_template.md
├── src/
│   ├── core/
│   │   ├── graph.py
│   │   └── edge.py
│   ├── algorithms/
│   │   └── algoritmo.py
│   ├── io/
│   │   └── file_reader.py
│   └── main.py
├── tests/
│   ├── test_graph.py
│   └── test_algorithms.py
├── data/
└── requirements.txt

> **Justificativa de desvios** *(se houver)*: 

---

## 4. Definição do Dataset

**Formato de entrada aceito:**

<!-- JSON / CSV / GraphML / lista de adjacência — descreva a estrutura -->

**Exemplo de estrutura do arquivo de entrada:**

```json
{
  "vertices": 5,
  "arestas": [
    { "origem": 0, "destino": 1, "peso": 4 },
    { "origem": 0, "destino": 2, "peso": 2 }
  ]
} 
```

```json
{
  "vertices": 4,
  "arestas": [
    { "origem": "Curitiba", "destino": "Florianópolis", "peso": 300 },
    { "origem": "Curitiba", "destino": "Foz do Iguaçu", "peso": 600 },
    { "origem": "Florianópolis", "destino": "Foz do Iguaçu", "peso": 700 }
  ]
}



**Estratégia de geração aleatória:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | configurável via argumento |
| Densidade | configurável (0.0 a 1.0) |
| Faixa de pesos | mín/máx configuráveis |

---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que será implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 |Implementar leitura de arquivo JSON/CSV | Alta  | Dado um arquivo válido, quando o sistema carregar, então os vértices e arestas são exibidos corretamente |
| 2 |Implementar Dijkstra para caminho mínimo |Alta |Dado um grafo, quando o usuário escolher origem e destino, então o sistema retorna o menor caminho |
| 3 |Implementar heurística TSP (vizinho mais próximo) |Alta | Dado um conjunto de cidades, quando o usuário solicitar roteiro completo, então o sistema retorna uma ordem aproximada|
| 4 |Interface simples (CLI) |Média |Dado um conjunto de entradas, quando o usuário interagir, então o sistema mostra resultados legíveis |
| 5 |Visualização textual das rotas| Média|Dado um cálculo de rota, quando concluído, então o sistema exibe sequência de cidades e custo total |

### 5.2 Out-of-Scope — O que NÃO será feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Visualização gráfica em mapa|Prazo curto e foco acadêmico |
|Algoritmos exatos para TSP |Complexidade computacional inviável |
|Integração com APIs externas (Google Maps) |Fora do escopo acadêmico|

---

## Checklist de Entrega

- [ ] Big-O de tempo e espaço declarados para cada algoritmo
- [ ] Ao menos 1 alternativa descartada com justificativa
- [ ] Diagrama de arquitetura com 4 camadas identificadas
- [ ] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
- [ ] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [ ] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [ ] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
