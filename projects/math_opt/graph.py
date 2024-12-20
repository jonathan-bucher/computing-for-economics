
name = ['jebucher']

# implementing a graph in python

class Graph:

    def __init__(self):
        self.nodes = {}

    def size(self):
        return len(self.nodes)

    def add_nodes(self, names: list):
        # add a node to the graph for every node in the list
        for name in names:
            self.nodes[name] = Node(name)

    def add_edge(self, n1: str, n2: str, w: int):
        # verify that node names are in the node list
        if n1 not in self.nodes or n2 not in self.nodes:
            return
        else:
            self.nodes[n1].add_edge(n2, w)
            self.nodes[n2].add_edge(n1, w)

    def get_names(self):
        return list(self.nodes.keys())
    
    def get_node(self, n):

        if n not in self.nodes:
            return -1
        else:
            return self.nodes[n]
        
    def shortest_path(self, n1: str, n2: str) -> list:

        if n1 not in self.nodes and n2 not in self.nodes:
            return -1

        # initialize a dictionary E that maps all nodes to 0
        # initialize a dictionary D that maps all nodes to anything but 0
        # initialize a dictionary path that maps all nodes to anything
        E = {}
        D = {}
        path = {}
        for n in self.nodes:
            E[n] = 0
            D[n] = 1
            path[n] = 0

        # we want to run a loop that runs until D == E
        while E != D:
            D = E.copy()

            for n in self.nodes:
                if n != n2:
                    E[n] = float('inf')
                    for m in self.nodes[n].get_neighbors():
                        dm = self.nodes[n].get_weight(m) + D[m]

                        # set E[n] to the minimum value of dm
                        if E[n] > dm:
                            E[n] = dm

                            # set path[n] to the m that minimizes dm
                            path[n] = m
        
        # construct list for shortest path:
        # Reconstruct the shortest path from n1 to n2
        shortest_path = []
        current = n1
        while current is not None:
            shortest_path.append(current)
            if current == n2:
                break
            current = path[current]

        # construct return list
        return [D[n1], shortest_path, D]

class Node:

    def __init__(self, name: str):
        self.name = name
        self.edges = {}

    def get_weight(self, n):
        # return weight for the edge between this node and node with name n
        # if no edge exists, return -1
        if n not in self.edges:
            return -1
        else:
            return self.edges[n]
        
    def add_edge(self, n: str, w: int):
        self.edges[n] = w

    def num_neighbors(self):
        return len(self.edges)
    
    def get_neighbors(self):
        return list(self.edges.keys())