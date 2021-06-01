from typing import Any, List
from graphviz import Digraph

"""
Vizualization Graphs for Suurballe's Algorithm
Robson Sousa, UFBA, june 2021
"""


class GraphView:
    """
    This class implements vizualization for Suurballe Algorithm.
    """

    def __init__(self, directory: str):
        self.graphs: dict = {}  # A graph, Node -> {nodes}.
        self.directory = directory  # Relactive directory to saving graph images.
        self._start: str = ''  # Start/root of the graph.
        self._end: str = ''  # End of the graph.

    @staticmethod
    def standardize_edges(g: Any) -> List[tuple]:
        """
        Standardize any G collection to tuple pattern
        :param g: any collection.
        :return: list of the edges tuples.
        """
        edges = []

        if (t := type(g)) == dict:
            for u, lv in g.items():
                for v in lv.keys():
                    edges.append((u, v, g[u][v]))

        elif t == list:
            for i in range(0, len(g) - 1):
                edges.append((g[i], g[i + 1]))

        return edges

    def add_graph(self, name: str, g: Any, start: str = None, end: str = None) -> None:
        """
        Add(stack) a graph to view (or not).
        :param name: is a symbolic name for the graph.
        :param g: a any graph.
        :param start: start/root of the graph.
        :param end: end of the graph
        """

        if start is not None and end is not None:
            self._start = start
            self._end = end

        # Build a graph to save in directory='output/graph-name' with name 'name.png'.
        gv = Digraph(name, directory='output/' + self.directory, filename=name, format="png", engine='sfdp')

        edges = self.standardize_edges(g)

        # stylize start and end nodes
        if self._start:
            gv.node(self._start, shape='doublecircle', color='green')
        if self._end:
            gv.node(self._end, shape='doublecircle', color='orange')

        gv.attr('node', shape='circle', color='black')

        if type(g) == dict:  # Build edges with label=weight
            for e in edges:
                gv.edge(e[0], e[1], label=str(e[2]))
        else:
            for e in edges:  # Build edges without label
                gv.edge(e[0], e[1])

        self.graphs[name] = gv

    def view(self, name: str) -> None:
        """
        Render stacked view mapped by key :param:name.
        """
        self.graphs[name].view()

    def view_all(self):
        """
        Render all views stacked.
        """
        for n in self.graphs.keys():
            self.graphs[n].view()
