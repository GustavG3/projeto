# E1 — Proposta e Definição do Projeto

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 19 de março de 2026  
> **Peso:** 10% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | TurisGraph |
| Integrante 1 | Gustavo Gomes Guimarães — 29078784 |
| Integrante 2 | Júlia Moreno da Silva — 39159108 |
| Integrante 3 | Thiago de Luca Fernandes — 38767791 |
| Domínio de aplicação | Logística / Turismo |

---

## 1. Contexto e Motivação

O planejamento de itinerários turísticos é um desafio logístico que envolve múltiplos fatores: distância entre cidades, tempo de deslocamento, custos de viagem e preferências do viajante. Embora ferramentas como Google Maps ou aplicativos de viagem ofereçam rotas ponto a ponto eficientes, elas não foram projetadas para otimizar roteiros completos envolvendo várias cidades de interesse. Além disso, essas ferramentas não permitem simulações comparativas de custo e tempo em pacotes turísticos, o que limita sua utilidade para agências e plataformas que precisam planejar circuitos integrados. Em um cenário real, por exemplo, um viajante que deseja visitar Curitiba, Florianópolis e Foz do Iguaçu em uma mesma viagem não encontra suporte adequado para calcular a ordem ideal das cidades, equilibrando tempo e custo.

Agências de turismo e plataformas digitais enfrentam a necessidade de propor roteiros que maximizem a experiência do cliente e, ao mesmo tempo, minimizem gastos operacionais. A ausência de soluções específicas para roteirização turística integrada torna o problema relevante, pois impacta diretamente a competitividade do setor e a satisfação dos viajantes. Diferente de aplicativos convencionais, um sistema baseado em grafos oferece flexibilidade para simular diferentes cenários, como trajetos de menor custo ou roteiros que conectem múltiplos destinos em uma única viagem.

Este projeto preencheu essa lacuna ao propor um sistema que modela cidades e rotas como grafos, permitindo tanto o cálculo do caminho mais curto entre duas localidades (via Dijkstra) quanto a visualização interativa dos trajetos no mapa do Brasil. Ao delimitar claramente o problema de caminho mínimo, o sistema se diferenciou das ferramentas existentes ao oferecer uma abordagem acadêmica aplicada a um desafio prático do mercado de viagens.

---

## 2. Objetivo Geral

O sistema calcula rotas de menor distância entre estados brasileiros em um itinerário turístico, utilizando o algoritmo de Dijkstra sobre um grafo ponderado não-dirigido e exibindo os resultados em uma interface gráfica interativa.

---

## 3. Objetivos Específicos

- [x] Implementar a modelagem dos estados e rotas utilizando grafos, representando destinos como vértices e conexões rodoviárias como arestas com pesos (distância em km).
- [x] Calcular o caminho mais curto entre dois estados utilizando o algoritmo de Dijkstra com fila de prioridade.
- [x] Exibir o roteiro calculado de forma visual em um mapa interativo do Brasil, destacando o caminho percorrido e as rodovias federais utilizadas.
- [x] Desenvolver uma interface gráfica (Pygame) que permite ao usuário selecionar origem e destino e visualizar os resultados das rotas calculadas.
- [x] Carregar os dados das conexões entre estados a partir de um arquivo JSON, garantindo que o sistema possa ser testado com diferentes configurações de grafo.

---

## 4. Público-Alvo / Caso de Uso Principal

Uma agência de turismo que precisa organizar um pacote rodoviário pelo Brasil pode utilizar o sistema para simular diferentes rotas entre estados, calcular o custo total de deslocamento em quilômetros e identificar as rodovias federais do percurso. O sistema também atende viajantes independentes que desejam comparar rotas entre dois destinos e visualizar graficamente o caminho mais eficiente, considerando as conexões reais entre estados brasileiros.

---

## 5. Justificativa Técnica — Por que Grafos?

A modelagem em grafo foi a abordagem mais adequada porque os elementos do problema mapeiam naturalmente para essa estrutura: estados brasileiros são vértices, e as rodovias federais que os conectam são arestas. Como cada rodovia pode ser percorrida nos dois sentidos, o grafo adotado é não-dirigido, refletindo a bidirecionalidade típica das conexões rodoviárias. Cada aresta possui um peso representando a distância em quilômetros, o que torna possível simular cenários de otimização como minimizar o total de km percorridos.

A estrutura em grafo permitiu aplicar o algoritmo de Dijkstra, que encontra o caminho mínimo de forma eficiente em grafos com pesos positivos — exatamente o caso das distâncias rodoviárias. Comparado a representações matriciais simples, o grafo não-dirigido ponderado oferece maior clareza e eficiência, pois permite explorar propriedades como conectividade e caminhos mínimos, tornando a Teoria dos Grafos a escolha mais adequada para resolver o problema de roteirização turística.

---

## 6. Tipo de Grafo

| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | Não-dirigido | Rodovias federais são bidirecionais. |
| Ponderado ou não-ponderado | Ponderado | Cada aresta tem peso em km de distância. |
| Conectado / bipartido / geral | Conectado | Todos os estados devem estar acessíveis para formar um roteiro válido. |
| Representação interna pretendida | Lista de adjacência | Mais eficiente em memória e adequada para grafos esparsos como redes de estados. |

---

## 7. Diagrama Conceitual

![Diagrama Conceitual — TurisGraph](./diagrama_conceitual.png)

> Grafo com 27 vértices (estados brasileiros) e 38 arestas (rodovias federais), com pesos representando distâncias em km. O diagrama exibe as conexões reais entre estados vizinhos, respeitando a topologia do mapa do Brasil. A rota destacada em verde exemplifica o caminho mínimo calculado pelo algoritmo de Dijkstra entre dois estados.

**Legenda:**  
- Vértices: estados brasileiros  
- Arestas: rodovias federais  
- Pesos: distância em km  

---

## Checklist de Entrega

- [x] Texto entre 300 e 600 palavras (seções 1 a 5)
- [x] Todos os campos da tabela de identificação preenchidos
- [x] Tipo de grafo especificado com justificativa
- [x] Diagrama presente e referenciado no texto
- [x] Arquivo nomeado como `E1_NomeGrupo_Grafos.md`

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
