import networkx as nx
G = nx.Graph()
G.add_nodes_from([(f'estudante {x}',{"color": "red"}) for x in range(1,6)])
G.add_nodes_from([(f'empresario {x}',{"color": "blue"}) for x in range(1,3)])
print(G)
G.add_edges_from([('estudante 1', 'empresario 2'), ('estudante 2','empresario 2')])
print(G)
