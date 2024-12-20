
import Graph as gr

# construct graph

g = gr.Graph()
g.add_nodes(['0', '1', '2', '3', '4'])
g.add_edge('0', '1', 3)
g.add_edge('0', '3', 7)
g.add_edge('0', '4', 8)
g.add_edge('4', '3', 3)
g.add_edge('3', '1', 4)
g.add_edge('1', '2', 1)
g.add_edge('2', '3', 2)


def test_add_nodes():
    assert g.nodes['0'].name == '0'

def test_size():
    assert g.size() == 5

def test_add_edge():
    assert g.nodes['0'].get_weight('4') == 8

def test_get_names():
    node_set = set(g.get_names())
    
    assert '0' in node_set
    assert '1' in node_set
    assert '2' in node_set
    assert '3' in node_set  
    assert '4' in node_set

def test_get_node():

    assert g.get_node('4').name == g.nodes['4'].name
    # handle edge case
    assert g.get_node('5') == -1

# testing nodes

def test_get_weight():
    assert g.nodes['4'].get_weight('3') == 3
    assert g.nodes['4'].get_weight('7') == -1
    assert g.nodes['0'].get_weight('1') == 3

g.nodes['3'].add_edge('1', 4)

def test_add_edge_node():
    assert g.nodes['3'].get_weight('1') == 4

def test_num_neighbors():
    assert g.nodes['0'].num_neighbors() == 3

def test_get_neighbors():

    assert g.nodes['0'].get_neighbors() == ['1', '3', '4']

# testing the shortest path method

def test_shortest_path1():
    test_list = g.shortest_path('0', '2')

    assert len(test_list) == 3
    assert test_list[0] == 4
    assert test_list[1] == ['0', '1', '2']

print(g.nodes['3'].get_weight('0'))


