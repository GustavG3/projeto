# TurisGraph — Planejador de Rotas Inteligentes

## Entrega E3 - MVP

O **TurisGraph** é um sistema de otimização logística voltado ao setor de turismo, desenvolvido para calcular rotas de menor custo entre destinos utilizando a Teoria dos Grafos.

### 1. Descrição do Projeto
Este projeto simula o planejamento de itinerários, permitindo identificar o caminho mais curto entre localidades específicas ou planejar roteiros completos com foco em eficiência de custo e distância.

### 2. Estrutura do Projeto
Abaixo está a organização das pastas conforme a arquitetura proposta:

```text
TurisGraph/
├── data/
├── src/             
│└── principal.py                           
├── tests/                  
├── requirements.txt        
└── README.md               


3. Como Executar o MVP

Pré-requisitos:

Python 3.x instalado.

Bibliotecas listadas no requirements.txt.

Instalação de Dependências:

pip install -r requirements.txt


Execução do Sistema:
Para iniciar o planejador de rotas, execute o comando abaixo a partir da raiz do projeto:

python src/main.py


4. Algoritmo Implementado

O sistema utiliza o algoritmo de Dijkstra com fila de prioridade (heapq), o que garante a eficiência necessária para o cálculo de rotas em grafos ponderados. Ele processa os pesos (distâncias/custos) definidos no arquivo JSON para retornar o trajeto mais econômico para o usuário.

5. Testes Unitários

O projeto inclui testes automatizados para validar a integridade do algoritmo:

Caso Base: Validação de uma rota comum com peso conhecido.

Grafo Vazio: Tratamento de segurança para quando não há dados carregados.

Grafo Completo: Teste de performance em conexões densas.

Para rodar os testes, utilize o comando:

pytest tests/test_algorithms.py


6. Autores

Gustavo Gomes Guimarães - (RA: 29078784)

Júlia Moreno da Silva - (RA: 39159108)

Thiago de Luca Fernandes - (RA: 38767791)

Projeto desenvolvido para a disciplina de Teoria dos Grafos - Prazo de entrega: 10 de Maio.
