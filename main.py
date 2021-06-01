from math import floor
from typing import Set

from SuurballeGraph import SuurballeGraph
from csv import reader

INPUT_DIR = 'dataset/'
DEFAULT_GRAPHS = ('graph-1.csv',
                  'graph-2.csv',
                  'graph-3.csv',)
MARGIN = '\t\t'
BREAK_LINE = '*' * 47
NEW_PAGE = '\n' * 30


def load_csv_graph(fname: str) -> Set[tuple]:
    """
    Load a graph from csv-file named :param: fname:
    :return:
    """
    loaded_edges = set()

    with open(INPUT_DIR + fname) as file:  # Open file
        file = reader(file, delimiter=',')

        for u, v, w in file:
            loaded_edges.add((u, v, int(w)))

    return loaded_edges


if __name__ == '__main__':

    filename: str = ''
    while True:

        header = f'{BREAK_LINE} SUURBALLE ALGORITHM {BREAK_LINE} \n'
        menu = MARGIN * 2 + f"Type number corresponding to the graphic you want to demonstrate\n" \
                            f"{MARGIN}[1] graph-1" \
                            f"{MARGIN}[2] graph-2" \
                            f"{MARGIN}[3] graph-3" \
                            f"{MARGIN}[4] external graph" \
                            f"{MARGIN}[0] quit"
        print(header)
        print(menu)

        if (op := input('\n' + MARGIN * 2 + 'Type option: ')) == '1':
            filename = DEFAULT_GRAPHS[0]
        elif op == '2':
            filename = DEFAULT_GRAPHS[1]
        elif op == '3':
            filename = DEFAULT_GRAPHS[2]
        elif op == '4':
            filename = input(f'{MARGIN}Type graph filename: ')
        elif op == '0':
            break
        else:
            print('Invalid option.')
            break

        # Getting graph parameters
        edges: Set[tuple] = load_csv_graph(fname=filename)
        start: str = input(f'{MARGIN}Type start node: ')
        end: str = input(f'{MARGIN}Type end node: ')
        visualization = input(f'\n{MARGIN}View the graphs of [A]LL steps of the algorithm or just the [F]INAL graph?'
                              f'Answer with [A or F]: ')

        print(BREAK_LINE * 2 + NEW_PAGE)
        # print("\n" * 130)
        # Build graph
        G = SuurballeGraph(name=filename[:-4:])
        G.add_edges(edges)
        G.set_start_end(start=start, end=end)

        # Find 2-disjoint paths
        G.find_2disjoint_path(visualization=visualization.upper())
