          
                   # Código para generar una red
                   

import networkx as nx           # librería para la red
import matplotlib.pyplot as plt # libreriía para ver el grafo

G = nx.Graph()                  # Grafo vacio
G.add_node("")                  # Creación de un nodo
G.add_nodes_from(["",""])       # Creación de otros nodos
G.add_edge("","")               # Cración de enlaces
nx.draw(G)                      # Dibujo del grafo
plt.show(G)                     # Se muestra en la pantalla
plt.savefig("")                 # Para guardar el archivo
print "Nodos: ", G.number_of_nodes(), G.nodes() # Muestra número de nodos
print "Enlaces: ", G.number_of_edges(),G.edges() # Muestra número de enlaces

