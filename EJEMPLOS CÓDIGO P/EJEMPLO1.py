import networkx as nx
import matplotlib.pyplot as plt
import random as ran

#---------------------------------------------------------------------------
 
N=500
def  cambiarcolor(G):  #program no hace nada como 
    NaC=ran.randint(0,N)
    G.node[NaC]['Estado']='I'
    return G, NaC

#---------------------------------------------------------------------------

G = nx.scale_free_graph(N)
for i in range(N):
    G.nodes[i]['Estado']='S'

color_map={'S': 'green', 'I': 'red'}
    
plt.figure(num=None, figsize=(8, 6), dpi=80)
pos=nx.circular_layout(G)
nx.draw(G,pos,node_size = 30,)
plt.show()

#---------------------------------------------------------------------------

G,numero=cambiarcolor(G)

nx.draw(G,pos,node_color=[color_map[G.node[node]['Estado']] for node in G], node_size = 30)
plt.show()
print(numero)

#---------------------------------------------------------------------------

