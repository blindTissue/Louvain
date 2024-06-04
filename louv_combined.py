from louv_first_phase import louvain_first_phase
from louv_second_phase import louvain_second_phase
from simple_graph import Graph

def louvain(graph):
    graph_node_count = len(graph)
    new_graph_node_count = 0
    graph_save = [graph]
    communities_save = []


    while graph_node_count != new_graph_node_count:
        graph, communities = louvain_first_phase(graph)
        graph = louvain_second_phase(graph, communities)
        graph_save.append(graph)
        communities_save.append(communities)
        graph_node_count = new_graph_node_count
        new_graph_node_count = len(graph)

    return graph_save, communities_save


if __name__ == '__main__':
    g = Graph()
    g.create_random_unweighted_graph(10, 30)
    graph = g.edges
    graphs, communities = louvain(graph)
    print(graphs)
    print(communities)
    print(len(graphs))
    print(len(communities))
