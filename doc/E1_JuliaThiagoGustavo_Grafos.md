# E1 — Proposta e Definição do Projeto


> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 19 de março de 2026  
> **Peso:** 10% da nota final  


---


## Identificação do Grupo


| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | |
| Integrante 1 | Nome — RA | Gustavo Gomes Guimarães 29078784
| Integrante 2 | Nome — RA | Júlia Moreno da Silva
| Integrante 3 | Nome — RA | Thiago de Luca Fernandes
| Domínio de aplicação | ex.: logística, redes, jogos... | Logística


---


## 1. Contexto e Motivação


> Descreva o problema do mundo real que será abordado. Por que ele é relevante?  
> *Orientação: 2 a 3 parágrafos. Seja específico — evite generalizações.*


<!-- Escreva aqui -->
O planejamento de itinerários turísticos é um desafio logístico que exige a seleção de rotas inteligentes entre diversos destinos, equilibrando fatores como distância, tempo de deslocamento e custos de viagem.
Este projeto propõe o desenvolvimento de uma simulação que permite ao usuário planejar um roteiro completo, interligando todas as cidades de interesse com o menor custo possível, ou identificar o caminho mais curto entre localidades específicas.
---


## 2. Objetivo Geral


> O que o sistema deve ser capaz de fazer ao final?  
> *Orientação: 1 frase clara e objetiva. Ex.: "O sistema deve calcular a rota de menor custo entre dois pontos em um mapa urbano."*


<!-- Escreva aqui -->
A interação com o viajante será simplificada e intuitiva, oferecendo opções diretas para o planejamento de circuitos turísticos integrados ou a definição de trajetos ponto a ponto entre cidades escolhidas.


---


## 3. Objetivos Específicos


> Desmembre o objetivo geral em metas mensuráveis.  
> *Orientação: liste entre 3 e 5 itens. Cada item deve ser verificável — use verbos como "implementar", "calcular", "exibir", "carregar".*


- [ ] Implementar a modelagem das cidades e rotas utilizando grafos, representando destinos como nós e conexões como arestas com pesos (distância ou custo).
- [ ] Calcular o caminho mais curto entre duas cidades específicas utilizando algoritmos de otimização (como Dijkstra).
- [ ] Gerar e exibir um roteiro completo que interligue múltiplas cidades com o menor custo total possível.
- [ ] Desenvolver uma interface simples e intuitiva que permita ao usuário selecionar destinos e visualizar os resultados das rotas calculadas.


---


## 4. Público-Alvo / Caso de Uso Principal


> Para quem ou em qual cenário o sistema seria utilizado?  
> *Orientação: descreva um cenário concreto de uso. Ex.: "Um entregador de aplicativo que precisa otimizar a sequência de entregas em um bairro."*


<!-- Escreva aqui -->
Sua utilidade para agências de turismo que buscam oferecer pacotes otimizados, reduzindo custos operacionais e aumentando a satisfação do cliente. Além de plataformas de viagens online que visam recomendar rotas inteligentes, empresas de transporte e logística turística podem encontrar valor nesta ferramenta ao simular trajetos que minimizem gastos e melhorem a experiência do usuário.
---


## 5. Justificativa Técnica — Por que Grafos?


> Por que a modelagem em grafo é a abordagem mais adequada para este problema?  
> *Orientação: explique quais elementos do problema mapeiam naturalmente para vértices e arestas. Mencione se há pesos, direção, ou restrições que reforçam a escolha.*


<!-- Escreva aqui -->
Ao aplicar a Teoria dos Grafos nesse contexto, é possível visualizar como problemas complexos de organização de viagens podem ser resolvidos de forma clara, transformando cidades em nós e conexões em arestas para oferecer soluções rápidas e eficientes através de algoritmos de otimização.
A estruturação dos dados em forma de grafo permite explorar diferentes estratégias de roteirização, demonstrando como conceitos teóricos podem ser aplicados em situações reais do mercado de viagens e aproximando o aprendizado acadêmico dos desafios práticos do setor.
---


## 6. Tipo de Grafo


> Especifique as características do grafo que o problema requer.


| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | | |
| Ponderado ou não-ponderado | | |
| Conectado / bipartido / geral | | |
| Representação interna pretendida | lista de adjacência / matriz | |



---










## 7. Diagrama Conceitual

> Insira aqui ao menos uma figura que ilustre o domínio do problema.  
> *Pode ser uma imagem exportada do Draw.io, Excalidraw, foto de esboço à mão etc.*  
<!-- Insira a figura aqui ou mande como anexo-->


**Legenda:**











---






## Checklist de Entrega


Antes de submeter, confirme:


- [X] Texto entre 300 e 600 palavras (seções 1 a 5)
- [X] Todos os campos da tabela de identificação preenchidos
- [X] Tipo de grafo especificado com justificativa
- [X] Diagrama presente e referenciado no texto
- [X] Arquivo nomeado como `E1_NomeGrupo_Grafos.docx` (versão Word) ou PR aberto (versão GitHub)


---


*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*


