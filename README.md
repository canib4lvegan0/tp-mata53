# Implementation of the Suurballe Algorithm
Suurballe's Algorithm,  for find 2-disjoint path.
Robson Sousa, UFBA, june 2021
____
## 1. Proposta de trabalho
Trabalho final da disciplina MATA53 - **Teoria dos Grafos**.
DCC - UFBA, 2021.1

**Prof:** Tiago Januário.
**Aluno:** Robson Sousa

**Visualizando algoritmos em grafos**, inspirado no Visualgo[6].

**Objetivo:** *Implementar uma ferramenta que permita visualizar algoritmos em grafos para atrair a atenção de pessoas interessadas em algoritmos e grafos*

**Tema escolhido:** Suurballe's Algorithm.

**Link do vídeo-demonstração:** 
___
## 2. Algoritmo de Suurballe
Concebido por John W. Suurballe  em 1974 (--daí o nome),   Algoritmo de Suurballe é um algoritmo para encontrar 2-disjuntos caminhos em um grafo direcionado e com ponderação não-negativa, fazendo com que ambos caminhos tenham o mínimo comprimento e conectem o mesmo par de vértice [1].

A ideia por trás deste algoritmo é utilizar o algoritmo de Dijkstra[2] para encontrar um menor caminho, modificar do grafo e depois executar Dijkstra novamente.

O algoritmo retorna um grafo resultado da combinação dos dois caminhos, após descartar as arestas que opostas de cada caminho e usando as arestas restantes pra formar os caminhos disjuntos.

### Definição
Seja um grafo direcionado e ponderado *G*, com conjuntos de vértices *V* e de arestas E. Seja *s* e *t* em *G*, vértices de origem e destino, respectivamente. Faça com que cada aresta *(u, v)* em *G* tenha um custo não negativo definido por *w(u, v)*. Então, defina *d(s, u)* como sendo o custo do caminho mais curto de *s* para *u*.

### Algoritmo
* **passo 1:** Encontre  o menor caminho, *P1*,  entre *s* e *t* em G. **[figura B]**
* **passo 2:** Atualize o custo de cada aresta de G por *w'(u, v) = w(u, v) - d(s, v) + d(s, u)*. Ou seja, *o novo peso é o peso corrente - comprimento minimo da *origem* à *v* + comprimento minimo da *origem* à *u*. Observe que após essa atualização, todas as arestas orientadas com incidência em vértices de P1 terão custo 0 ou não-negativo. **[figura D]**
* **passo 3:** Crie um grafo residual *G_2* formado a partir de G menos as arestas de P1 direcionadas à origem *s* (i.e *v -> ... -> s*), e inverta o sentido das arestas de peso 0. **[figura D]**
* **passo 4:** Encontre o menor caminho *P2* em *G_2* (ussando Dijkstras). **[figura E]**
* **passo 5:** Descarta as arestas invertidas de *P2* em ambos caminhos.  **[figura F]** As arestas de *P1* e *P2* restantes formam um subgrafo com duas arestas saindo de *s* e duas chegando em *t*.  **[figura G]** Retorna os 2-disjuntos caminhos.

### Exemplo
O exemplo abaixo mostra o passo a passo do algoritmo de Suurballe na busca par de caminhos mais curtos de *A* a *F*.
![First graph.jpg](https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/First_graph.jpg/900px-First_graph.jpg)

### Corretude
O peso de qualquer caminho de *s* para *t* em um grafo com os pesos modificados é o mesmo do peso original, exceto de *d(s,t)*. Ou seja, os 2-disjuntos menores caminhos com pesos modificados são os mesmo do grafo original, mas com pesos totais distintos.

### Análise:
Considerando que o algoritmo de Suurballe executa duas iterações do algoritmo de Dijkstra, e este último no pior caso executa em *O(|E|+|V| log |V|)*, onde *|V|* e *|E|* são as quantidades de vértices e arestas, respectivamente.  Logo podemos limitar o algoritmo de Suurballe da mesma forma.
   
## 3. Implementação
A linguagem **Python** (>=3.8) foi escolhida para implementação deste trabalho por dois motivos: 1) familiaridade do autor e 2) grande disponibilidade de bibliotecas para visualização de grafos. 
A biblioteca para visualização foi **Graphviz** (=0.16) [4].

### Design pattern e organização projeto
O trabalho segue a estrutura descrita abaixo (a partir da raiz)
* *dataset/*:  arquivos para carregamento de grafos (no padrão csv).
	* *graph-1.csv*: 
	* *graph-2.csv*:
	* *...*
* *dijkstra/*:  modulo/implementação do Algoritmo de Dijkstra por David Eppstein [4].
	* *dijkstra*: 
	* *priodict*: 
* *doc/*:	
	* *Suurballe sequence.jpg*:
* *output/*:	**arquivos (.gv e .png) gerados pela implementação deste trabalho.** Cada novo grafo terá seu próprio diretório e o nome de cada arquivo (.gv e .png) refere ao passo do algortimo de Suurballe que foi executado.
	* *graph-1/*:
	* *graph-2/*:
	* *...*
* *SuurballeGraph*: **implementação do Algoritmo de Suurballe**
* *GraphView*: implementação das *views*/arquivos gerados nos passos do Algoritmo de Suurballe.
* *main*:
* *requirements.txt*: dependências do projeto.
____
## 4. Executando
1. Antes de executar, certifique-se que tenha instalado Python 3.x:
``` $ python --version ``` 
``` Python 3.x ```

2. Instale as dependências:
```pip install -r requirements.txt```

3. Executando:
``` $ python main.py```
____
## 5. Referências
* [1] https://en.wikipedia.org/wiki/Suurballe%27s_algorithm
* [2] https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm  
* [3] https://graphviz.org/documentation/  
* [4] https://gist.github.com/theObs: dependendo do execuçãoonewolf/6175427
* [5] https://visualgo.net/en