from simple_graph import Graph
from louv_first_phase import louvain_first_phase

def louvain_second_phase(graph, communities):
    new_graph = Graph()
    for community in communities:
        if communities[community]:
            new_graph.add_node(community)

    for node, edges in graph.items():
        node_community = get_current_community(communities, node)
        for edge, weight in edges.items():
            edge_community = get_current_community(communities, edge)

            new_graph.add_edge(node_community, edge_community, weight / 2) # divide by 2 because we are adding the edge twice

            if node == edge:
                new_graph.add_edge(node_community, node_community, weight / 2)
    return new_graph.edges




def get_current_community(communities, node):
    for community, items in communities.items():
        if node in items:
            return community
    return None






if __name__ == '__main__':
    g = Graph()
    g.create_random_unweighted_graph(10, 30)
    graph = g.edges
    #print(louvain_first_phase(graph))
    graph, communities = louvain_first_phase(graph)
    print(graph)
    print(communities)
    print(louv_second_phase(graph, communities))