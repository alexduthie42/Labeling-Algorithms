
class Vertex:

    def __init__(self, id, degree, rank):
        self.id = id
        self.degree = degree
        self.rank = rank

    def __repr__(self):
        return "{0}: deg {1} rank {2}".format(self.id, self.degree, self.rank)



def graph_parser(graph):
    "Creates vertex classes with relevant information"
    vertices = graph[0]
    edges = graph[1]

    degrees = {}
    rank_order = []

    vertex_classes = {}

    # Find the degree of each vertex
    for edge in edges:
        if edge[0] not in degrees:
            degrees[edge[0]] = 1
        else:
            degrees[edge[0]] += 1

        if edge[1] not in degrees:
            degrees[edge[1]] = 1
        else:
            degrees[edge[1]] += 1

    #   In case any vertex has no edge connected to it
    for vertex in vertices:
        if vertex not in degrees:
            degrees[vertex] = 0

    # Sort the degrees to get a ranking order
    for key in degrees.keys():
        rank_order.append((degrees[key], key))
    rank_order.sort()

    # Create vertex data structures
    for i in range(len(rank_order)):
        vertex_classes[rank_order[i][1]] = Vertex(rank_order[i][1], rank_order[i][0], i)

    return vertex_classes, edges


def query_label(v1, v2, label_set):

    l1 = label_set[v1]
    l2 = label_set[v2]

    min_dist = float('inf')

    for i in range(len(l1)):
        for j in range(len(l2)):
            if l1[i][0] == l2[j][0]:
                if l1[i][1] + l2[j][1] < min_dist:
                    min_dist = l1[i][1] + l2[j][1]

    return min_dist

def check_remove(label_set, check):

    for item in label_set:
        if item[0] == check:
            label_set.remove(item)

    return label_set


def hdl(graph):
    """ Hop-Doubling Labeling to generate a label set from a graph G=(V,E)"""
    vertices, edges = graph_parser(graph)
    label_set = {}

    # Insert each vertex into its own label set with distance 0
    for vertex in vertices.keys():
        label_set[vertex] = [(vertex, 0)]

    # Initialise previous iteration label set
    prev_label = {}

    # Insert each pair of nodes into the label set (insert higher ranking node into lower rankings set)
    for edge in edges:
        if vertices[edge[0]].rank > vertices[edge[1]].rank:
            label_set[edge[1]].append((edge[0], 1))
            if edge[1] not in prev_label:
                prev_label[edge[1]] = [(edge[0], 1)]
            else:
                prev_label[edge[1]].append((edge[0], 1))
        else:
            label_set[edge[0]].append((edge[1], 1))
            if edge[0] not in prev_label:
                prev_label[edge[0]] = [(edge[1], 1)]
            else:
                prev_label[edge[0]].append((edge[1], 1))


    # Continue until no new labels are added
    while prev_label != {}:
        cur_label = {}

        # For all labels in previous label set
        for u1 in vertices:
            if u1 not in prev_label:
                continue
            for (v1, d1) in prev_label[u1]:

                # For every label in the whole label set
                for u2 in vertices:
                    for (v2, d2) in label_set[u2]:

                        # First candidate generation rule
                        if u1 == u2:
                            from_vert = v1
                            to_vert = v2
                        # Second candidate generation rule
                        elif u1 == v2:
                            from_vert = v1
                            to_vert = u2
                        else:
                            continue

                        # Create new label if the distance between the candidates label is shorter than already is
                        if query_label(from_vert, to_vert, label_set) <= d1 + d2:
                            continue
                        # Add higher ranking vertex to lower ranking vertex's label (and the current label)
                        if vertices[from_vert].rank < vertices[to_vert].rank:
                            # If to_vert already in from_vert label remove
                            label_set[from_vert] = check_remove(label_set[from_vert], to_vert)
                            label_set[from_vert].append((to_vert, d1 + d2))
                            if from_vert not in cur_label:
                                cur_label[from_vert] = [(to_vert, d1 + d2)]
                            else:
                                cur_label[from_vert].append((to_vert, d1 + d2))
                        else:
                            # If from_vert already in to_vert label remove
                            label_set[to_vert] = check_remove(label_set[to_vert], from_vert)
                            label_set[to_vert].append((from_vert, d1 + d2))
                            if to_vert not in cur_label:
                                cur_label[to_vert] = [(from_vert, d1 + d2)]
                            else:
                                cur_label[to_vert].append((from_vert, d1 + d2))
        # Update the previous label set to the current label set
        prev_label = cur_label

    return label_set


def main():
    graph1 = (['a', 'b', 'c', 'd', 'e', 'f'],
              [('a', 'b'), ('a', 'c'), ('b','e'),('b','d'),('c','f'),('c','d')])

    graph2 = (['a', 'b', 'c', 'd', 'e'],
              [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')])

    graph3 = (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
              [('a', 'b'), ('a', 'c'), ('b', 'h'), ('b', 'e'), ('c', 'd'), ('d', 'f'), ('d', 'e'), ('d', 'g')])

    index = hdl(graph2)
    for label in index.keys():
        print("{0}: {1}".format(label, index[label]))

    index_size = 0

    for label in index.keys():
        index_size += len(index[label])

    print('label size {0}'.format(index_size))

    print(query_label('a', 'e', index))


if __name__ == '__main__':
    main()
