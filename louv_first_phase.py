from simple_graph import Graph

#graph will be a dictionary of dictionaries
# might do adjacency matrix later. (Is this better?)
def louvain_first_phase(graph):
    communities = initialize_communities(graph)
    change_count = 10 # for initial run

    while change_count > 0:
        change_count = 0
        for node in graph:
            current_community = get_current_community(communities, node)
            best_community = get_best_community(graph, communities, node)
            if current_community != best_community:
                change_count += 1
                communities[current_community].remove(node)
                communities[best_community].append(node)

    return graph, communities





def total_edges(graph):
    total = 0
    for out in graph:
        for towards in graph[out]:
            if towards != out:
                total += graph[out][towards]
            else:
                total += 2 * graph[out][towards]

    total = int(total / 2)
    return total

def get_node_weight(graph, node):
    weight = 0
    for towards in graph[node]:
        weight += graph[node][towards]
    return weight

def initialize_communities(graph):
    communities = {}
    for node in graph:
        c_name = node + '_c'
        communities[c_name] = [node]
    return communities

# sum of all linke weights of nodes in c
def get_community_weight_tot(graph, communities, community):
    weight = 0
    for node in communities[community]:
        weight += get_node_weight(graph, node)
    return weight

def get_community_weight_in(graph, communities, community):
    weight = 0
    for node in communities[community]:
        for towards in graph[node]:
            if towards in communities[community]:
                weight += graph[node][towards]
    return weight

def modularity_community(graph, communities, community):
    tot = get_community_weight_tot(graph, communities, community)
    in_ = get_community_weight_in(graph, communities, community)
    m = total_edges(graph) * 2
    q = in_/m - (tot/m)**2
    return q

def delta_node_to_other_community(graph, communities, node, community):
    if node in communities[community]:
        return 0


    node_in = 0
    for towards in graph[node]:
        if towards in communities[community]:
            node_in += graph[node][towards]

    # print('node_in: ' + str(node_in))

    node_tot = get_node_weight(graph, node)
    total_edge_count = total_edges(graph) * 2

    q_after = ((get_community_weight_in(graph, communities, community) + node_in) / total_edge_count
               - ((get_community_weight_tot(graph, communities, community) + node_tot) / total_edge_count)**2)

    q_before = (modularity_community(graph, communities, community) + get_self_modularity(graph, node))

    return q_after - q_before

def delta_node_to_remove_community(graph, communities, node, community):
    if node not in communities[community]:
        print('node not in community')
        return 0

    node_in = 0
    for towards in graph[node]:
        if towards in communities[community]:
            node_in += graph[node][towards]

    #print('node_in: ' + str(node_in))

    node_tot = get_node_weight(graph, node)
    total_edge_count = total_edges(graph) * 2

    q_after = (((get_community_weight_in(graph, communities, community) - node_in)/ total_edge_count
               - ((get_community_weight_tot(graph, communities, community) - node_tot) / total_edge_count) ** 2)
               + get_self_modularity(graph, node))


    q_before = modularity_community(graph, communities, community)
    #print('q_before: ' + str(q_before))
    #print('delta_node_to_remove_community: ' + str(q_after - q_before))
    return q_after - q_before

def delta_total(graph, communities, node, from_community, to_community):
    return delta_node_to_other_community(graph, communities, node, to_community) + delta_node_to_remove_community(graph, communities, node, from_community)


def get_best_community(graph, communities, node):
    best_delta = 0
    epsilon = 1e-6
    current_community = None
    for community, items in communities.items():
        if node in items:
            current_community = community

    best_community = current_community
    for community in communities:
        delta = delta_total(graph, communities, node, current_community, community)
        #print(delta)
        if delta > best_delta + epsilon:
            best_delta = delta
            best_community = community
    # print("------------------")
    return best_community

def get_current_community(communities, node):
    for community, items in communities.items():
        if node in items:

            return community
    return None

def get_self_modularity(graph, node):
    edge_to_self = 0 if node not in graph[node] else graph[node][node]
    node_tot = get_node_weight(graph, node)
    total_edge_count = total_edges(graph) * 2

    return (2 * edge_to_self / total_edge_count) - (node_tot / total_edge_count) ** 2




if __name__ == '__main__':
    g = Graph()
    g.create_random_unweighted_graph(10, 30)
    graph = g.edges
    print(total_edges(graph))
    sum = 0
    for node in graph:
        print(get_node_weight(graph, node))
        sum += get_node_weight(graph, node)
    print(sum)


    print(louvain_first_phase(graph))

    graph = Graph()
    graph.create_clusters(10, 5)
    print(graph)
    print(louvain_first_phase(graph.edges))

