#!/usr/bin/env python

# -*- coding: utf-8 -*-



#Se importa la libreria networkx como nx

import networkx as nx

#Se importa la libreria pyplot de matplotlib como plt

import matplotlib.pyplot as plt

#Se crea un grafo vacio

G=nx.Graph()



#Se crean los nodos:

#Nodo Venezuela

G.add_node("Venezuela")

#Se crean los nodos de los estados

G.add_nodes_from(["Carabobo","Miranda","Aragua","Merida","Lara","Distrito Capital"])

#Se crean los nodos de las ciudades.

G.add_nodes_from((["Valencia","Barquisimeto","Merida","Caracas","Guacara","Carora","Cubiro"]))

#Se crean los enlaces de los estados al país

G.add_edge("Carabobo","Venezuela")

G.add_edge("Lara","Venezuela")

G.add_edge("Merida","Venezuela")

G.add_edge("Distrito Capital","Venezuela")

G.add_edge("Aragua","Venezuela")

G.add_edge("Miranda","Venezuela")

#Se crean los nodos de las ciudades a su respectivo estado

v1 = ("Valencia","Carabobo")

v2 = ("Guacara","Carabobo")

dc = ("Caracas","Distrito Capital")

G.add_edge(*v1)

G.add_edge(*v2)

G.add_edge("Tocuyito","Carabobo")

G.add_edge("San Diego","Carabobo")

G.add_edge("Puerto Cabello","Carabobo")

G.add_edge("Moron","Carabobo")

G.add_edge("Rafael Urdaneta","Valencia")

G.add_edge(u"Miguel Peña","Valencia")

G.add_edge("Santa Rosa","Valencia")

G.add_edge("Candelaria","Valencia")

G.add_edge(*dc)

G.add_edge("Barquisimeto","Lara")

G.add_edge("Carora","Lara")

G.add_edge("Cubiro","Lara")

G.add_edge("Merida","Merida")

G.add_edge("El Vigia","Merida")

G.add_edge("Ejido","Merida")

#Se dibuja el grafo

nx.draw(G)

#Se muestra en pantalla

plt.show()

#Se vuelve a dibujar el grafo y se salva en un archivo png.

nx.draw(G)

plt.savefig("networkx1.png")

#Se muestra información de los nodos (cantidad, nodos)

print "Nodos: ", G.number_of_nodes(), G.nodes()

#SE muestra información de los enlaces (cantidad, enlaces)

print "Enlaces: ", G.number_of_edges(),G.edges()
