import random

# simple weighted graph


class Graph:

    def __init__(self):
        self.edges = {}

    def add_node(self, node):
        self.edges[node] = {}

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.edges:
            self.add_node(node1)
        if node2 not in self.edges:
            self.add_node(node2)

        if self.edges[node1].get(node2):
            self.edges[node1][node2] += weight
        else:
            self.edges[node1][node2] = weight

        if self.edges[node2].get(node1):
            self.edges[node2][node1] += weight
        else:
            self.edges[node2][node1] = weight

    def get_edge(self, node1, node2):
        return self.edges[node1][node2]

    def create_random_unweighted_graph(self, n, m):
        for i in range(n):
            self.add_node(str(i))

        edge_list = []
        edge_count = 0
        while edge_count < m:
            node1 = str(random.randint(0, n-1))
            node2 = str(random.randint(0, n-1))

            if node1 == node2:
                continue
            edge = {node1, node2}
            if edge not in edge_list:
                edge_list.append(edge)
                self.add_edge(node1, node2)
                edge_count += 1
            else:
                continue

    def create_clusters(self, node_count, cluster_count):
        for i in range(node_count):
            self.add_node(str(i))

        for i in range(cluster_count):
            cluster = []
            for j in range(node_count//cluster_count):
                cluster.append(str(i*node_count//cluster_count+j))

            for i in range(len(cluster)):
                for j in range(i+1, len(cluster)):
                    self.add_edge(cluster[i], cluster[j])

if __name__ == '__main__':
    g = Graph()
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'C', 10)
    g.add_edge('B', 'C', 3)

    print(g.get_edge('A', 'B'))
    print(g.get_edge('B', 'A'))
    print(g.get_edge('A', 'C'))
    print(g.get_edge('C', 'A'))
    g.add_edge('A', 'B', 5)
    print(g.get_edge('A', 'B'))

    r_g = Graph()
    r_g.create_random_unweighted_graph(10, 20)
    print(r_g.edges)

    c_g = Graph()
    c_g.create_clusters(10, 2)
    print(c_g.edges)
