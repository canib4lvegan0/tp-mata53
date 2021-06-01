#!/usr/bin/env python

from typing import Dict, List, Tuple, Set

# This module implements the Dijkstra algorithm for finding shortest path.
from dijkstra.dijkstra import Dijkstra

# Auxiliary to deep copy od dict.
from copy import deepcopy

# Implements graph visualizaition for Suurballe.
from GraphView import GraphView


"""
Suurballe's Algorithm,  for find 2-disjoint path.
Robson Sousa, UFBA, june 2021
"""


class SuurballeGraph:
    """
    This class implements Suurballe Algorithm.
    """

    # Suurballe Algorithm Steps Dictionary
    _steps: Dict = {
        'step_0': f'[step 0] - Main graph',
        'step_1': '[step 1] - Primary Path 1',
        'step_2': '[step 2] - Graph\' - Updated weights',
        'step_3': '[step 3] - G_3 (G - P1) - Updated edges',
        'step_4': '[step 4] - Primary Path 2 in G_3',
        'step_5': '[step 5]',
        'step_5_1': '[step 5_1] - G_2 - Without edges P1-common-P2',
        'step_5_2': '[step 5_2] - Final Path 1 in G_2',
        'step_5_3': '[step 5_3] - G_2 - Without Final P1 edges',
        'step_5_4': '[step 5_4] - Final Path 2 in G_2',
        'step_5_5': '[step 5_5] - Final G - Both paths (P1 and P2)',
    }

    def __init__(self, graph=None, start: str = None, end: str = None, name: str = 'G'):

        if graph is None:
            graph = {}

        self.graph: dict = graph        # graph (dict[dict]).
        self.start: str = start         # start/root of the graph
        self.end: str = end             # end of the graph
        self.name: str = name           # symbolic name to graph

        # a collection of the graphs of the graph views implemented in this class
        self.graph_view = GraphView(directory=self.name)

    def add_edges(self, edges: Set[Tuple[str, str, int]], graph: dict = None):
        """
        Add edges to self.graph.
        :param graph: a graph in dict.
        :param edges: list of the edges in triple format (node-u, node-v, weight)
        In case node-u and/or node-v are not in the graph, add them.
        """

        if graph is None:
            graph = self.graph

        for u, v, w in edges:

            # Check if node u exists. If not, create it
            if u not in graph.keys():
                graph[u] = {}

            # Check if node v exists. If not, create it
            if v not in graph.keys():
                graph[v] = {}

            # Add edge
            graph[u].update({v: w})

    def set_start_end(self, start: str, end: str):
        self.start = start
        self.end = end

    def remove_edges(self, edges: Set[tuple], graph: object = None) -> None:
        """
        Remove in edges from self.graph.
        :param graph: a graph in dict.
        :param edges: list of the edges in pair format (node-u, node-v, weight)
        In case node-u and/or node-v are not in the graph, raise a friendlier error.
        """
        if graph is None:
            graph = self.graph

        for u, v in edges:
            try:
                graph[u].pop(v)
            except KeyError as err:
                print(f'-ops- I try remove an invalid edge with key [{err}], but o has edge{u, v}! :P2 :p\n')

    def nodes(self, graph: dict = None) -> Tuple[str, ...]:
        """
        Nodes of the graph.
        :graph: a graph in dict.
        :return: list of the nodes.
        """
        if graph is None:
            graph = self.graph

        return tuple(graph.keys())

    def edges(self, graph: dict = None) -> List[Tuple[str, str, int]]:
        """
        Edges of the graph.
        :return: list of the edges in triple-format (node-u, node-v, weight).
        """
        if graph is None:
            graph = self.graph

        edges = []

        for u, lv in graph.items():
            for v in lv:
                edges.append((u, v, lv[v]))

        return edges

    def shortest_path(self, graph: dict = None, start: str = None, end: str = None) -> Tuple[list, dict]:
        """
        Find a single shortest path from start to end.
        The input has the same conventions as (module) Dijkstra().
        :param graph: a graph in dict.
        :param start: start node. If None, assume it is the start of the graph.
        :param end: end node. If None, assume it is the end of the graph.
        :return: a tuple with:
            a list of the nodes in order along the shortest path, and
            a dict with respective weights of the node from start to each node along the shortest path.

        **** Credits ****
        This algorithm is an adaptation of the implementation of the Dijkstra Algorithm, by Wolfgang Richter
        https://gist.github.com/theonewolf/6175427
        """

        if graph is None:
            graph = self.graph
        if start is None:
            start = self.start
        if end is None:
            end = self.end

        path: list = []  # Shortest nodes
        weights: dict = {}  # Shortest path weights

        try:
            weights, path = Dijkstra(graph, start, end)
        except KeyError as err:
            print(f'-ops- You try find an invalid path {start} -> {end}. No key [{err}]! :p\n')

        minimal_path = []
        while end != start:
            minimal_path.append(end)
            try:
                end = path[end]
            except (TypeError, KeyError) as err:
                print(f'-ops- You try find an invalid path {start} -> {end}. No key [{err}]! :p\n')
                return [], {}

        minimal_path.append(start)
        minimal_path.reverse()

        return minimal_path, weights

    def find_2disjoint_path(self, start: str = None, end: str = None, visualization: str = 'A') -> Tuple[List, List]:
        """
        ImplementsSuurballe's algorithm. More about: https://en.wikipedia.org/wiki/Suurballe%27s_algorithm
        Find two disjoint paths, p1 and p2, in a non negative-weighted directed graph, so that both paths connect
        the same pair of nodes (start, end) and have minimum total length.
        :param: start node of the finding
        :param: end node of the finding
        :param: visualization 'A', stacks the respective graph at each step, or just final graph in case 'F'.
        :return: Tuple[List, List], list of nodes of the two disjoint paths from the subgraph.
        """

        # STEP 0 ---------------------------------------------------------------------------------
        # Plot main Graph

        # Stack Main Graph for plot (or not) posteriorly
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_0'] + self.name, g=self.graph, start=self.start,
                                  end=self.end)

        # STEP 1 ---------------------------------------------------------------------------------
        # Find shortest path p1 - path 1.

        p1, weights_p1 = self.shortest_path()
        if not len(p1):
            print('-ops- Could not find the shortest patph.')
            return [], []

        # Stack Path 1 Graph.
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_1'], g=p1)

        # STEP 2 ---------------------------------------------------------------------------------
        # Recalculate the edge weith by w'(u,v) = w(u,v) − d(s,v) + d(s,u).

        # Creates an auxiliary tmp_graph_2 cloning from graph.
        tmp_graph_2: dict = deepcopy(self.graph)

        # Find shortest path for each nodes u and v in graph, starting in start.
        for u, lv in self.graph.items():
            tmp_path_u, tmp_weights_u = self.shortest_path(end=u)

            for v in lv.keys():
                tmp_path_v, tmp_weights_v = self.shortest_path(end=v)

                # Update weight.
                try:
                    tmp_graph_2[u][v] = self.graph[u][v] - tmp_weights_v[v] + tmp_weights_u[u]
                except KeyError as err:
                    print(f'-ops- Could not update weights. No key [{err}]! :p\n')
                    return [], []

        # Stack G_2 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_2'], g=tmp_graph_2)

        # STEP 3 ---------------------------------------------------------------------------------
        # Creates a residual tmp_graph_3 formed from graph by removing the edges of graph on
        # path p1 that are directed to start, and reverses p1-edges with 0 cost.

        # Creates another auxiliary tmp_graph_3 cloning from tmp_graph_2.
        tmp_graph_3: dict = deepcopy(tmp_graph_2)

        edges_to_remove: Set[tuple] = set()
        reversed_edges_p1: Set[tuple] = set()

        # List p1-edges
        for i in range(0, len(p1) - 1):
            edges_to_remove.add((p1[i + 1], p1[i]))  # List p1-edges directed to start to remove them.
            edges_to_remove.add((p1[i], p1[i + 1]))  # List p1-edges directed to end to...
            reversed_edges_p1.add((p1[i + 1], p1[i], 0))  # ... reverse them. Each edge keep its cost, 0, by STEP 2.

        # Update tmp_graph_3's edges.
        self.remove_edges(graph=tmp_graph_3, edges=edges_to_remove)
        self.add_edges(graph=tmp_graph_3, edges=reversed_edges_p1)

        # Stack G_3 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_3'], g=tmp_graph_3)

        # STEP 4 ---------------------------------------------------------------------------------
        # Find shortest path p2 - path 2, in the residual graph tmp_graph_3

        p2, weights_p2 = self.shortest_path(graph=tmp_graph_3)

        # Stack Path 2 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_4'], g=p2)

        # STEP 5 ---------------------------------------------------------------------------------
        # Discard the reversed edges of P2 from both paths

        reversed_edges_p2: Set[tuple] = set()

        # List p2-edges
        for i in range(0, len(p2) - 1):
            reversed_edges_p2.add((p2[i], p2[i + 1], 0))  # List p2-edges that were inverted in step 3.

        # Get common edges between p1 and p2.
        common_edges: set = reversed_edges_p1.intersection(reversed_edges_p2)

        common_edges = {(u, v) for u, v, _ in common_edges}  # Discard weight of the these egdes
        common_edges = {(v, u) for u, v in common_edges}. \
            union({(u, v) for u, v in common_edges})  # Add pair (u, v) and (v, u) -- going and return.

        # Going back to original graph
        tmp_graph_2 = deepcopy(self.graph)

        self.remove_edges(graph=tmp_graph_2, edges=common_edges)  # Remove edges in p1-common-p2.

        # Stack G_2 without P1-common-P2 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_5_1'], g=tmp_graph_2)

        # Find a new shortest p1. Now tmp_graph_2 has no edges p1-common-p2.
        p1, weights_p1 = self.shortest_path(graph=tmp_graph_2)

        # Stack Final Path 1 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_5_2'], g=p1)

        edges_to_remove.clear()

        # List p1-edges
        for i in range(0, len(p1) - 1):
            edges_to_remove.add((p1[i], p1[i + 1]))

        # Removes p1-edges to fetch p2
        self.remove_edges(graph=tmp_graph_2, edges=edges_to_remove)

        # Stack G_2 without p1-edges Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_5_4'], g=tmp_graph_2)

        # Find a new shortest p2
        p2, weights_p2 = self.shortest_path(graph=tmp_graph_2)

        # Stack Final Path 2 Graph
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_5_4'], g=p2)

        # Create a Final Graph with Path 1 and Path 2 edges.
        graph_final: dict = {}
        edges_to_add: set = set()

        for i in range(0, len(p1) - 1):
            edges_to_add.add((p1[i], p1[i + 1], weights_p1[p1[i + 1]] - weights_p1[p1[i]]))
        for i in range(0, len(p2) - 1):
            edges_to_add.add((p2[i], p2[i + 1], weights_p2[p2[i + 1]] - weights_p2[p2[i]]))
        self.add_edges(graph=graph_final, edges=edges_to_add)

        # Stack Final Graph (P1 and P2)
        self.graph_view.add_graph(name=SuurballeGraph._steps['step_5_5'], g=graph_final, )

        if visualization == 'A':
            self.graph_view.view_all()
        elif visualization == 'F':
            self.graph_view.view(name=SuurballeGraph._steps['step_5_5'])

        # Return Path 1 and Path 2 lists
        return p1, p2

    def __str__(self):
        """
        Build a friendlier string to presente graph.
        :return: A formatted string with nodes and edges of the dictionary.
        """
        string: str = ''

        for u, vs in self.graph.items():
            string += f'{u} -> {vs}\n'

        return string
