# librerias

import networkx as nx
import matplotlib.pyplot as plt
import random as ran
import numpy as np

#---------------------------------------------------------------------------
 
N=50
def infectadoinicial(G):  #denicion de varibale infectados 
    inf=ran.randint(0,N)   # generar N nodos
    G.node[inf]['Estado']='I'  # estado de los infectados
    return G, inf

#def diagnosticado(D):
#    diag=ran.choce(inf)
#    G.node[diag]['Estado']= 'D'
#    return D, diag
    
def hallarpareja(inf):    # definir la variable hallar pareja   
    if ran.choice(['si', 'no']) == 'si':
           diagnosticado=(inf)
           if inf == diag:
             print('el infectado', inf, ' esta diagnosticado')
           else:
             print('el infectado', inf, ' no esta diagnosticado') 
             print('el infectado', inf, ' si se va a emparejar')
             vecinos=[]
        for i in range(N):    
            if G.has_edge(i,inf):
                vecinos=vecinos+[i]     
        print('las posibles parejas del nodo infectado', inf, '  son: ', vecinos)
        pareja=ran.choice(vecinos)
        print('la pareja del infectado', inf, '  va a ser el nodo: ', pareja)
        riesgo=np.random.rand()
        print('el riesgo de infeccion es: ', riesgo)
        if riesgo > 0.5 : 
           G.node[pareja]['Estado']='I'
           print('el nodo ', pareja, 'se infecto')
        else:
           print('el nodo', pareja, 'no se infecto')          
    else:
         print('el infectado', inf, '  no se va a emparejar')  
    
#---------------------------------------------------------------------------

#G = nx.scale_free_graph(N,0.41, 0.54, 0.05)     #alpha, beta, gamma  +=1
G = nx.erdos_renyi_graph(N,0.2)
for i in range(N):
    G.node[i]['Estado']='S'

color_map={'S': 'green', 'I': 'red'}
    
pos=nx.circular_layout(G)

#---------------------------------------------------------------------------

G,inf=infectadoinicial(G)
nx.draw(G,pos,node_color=[color_map[G.node[node]['Estado']] for node in G], node_size = 100)
plt.show()


n=10
for i in range(n):
    print('iteracion: ', i)
    for j in range(N):
        if G.node[j]['Estado']=='I':
           hallarpareja(j)
    nx.draw(G,pos,node_color=[color_map[G.node[node]['Estado']] for node in G], node_size = 100)
    plt.show()

