# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 18:02:30 2017

@author: HacheUQ
"""

import networkx as nx  
import matplotlib.pyplot as plt 
from matplotlib.pyplot import pause 
import random as ran
import numpy as np
from random import uniform, randint
import matplotlib.animation as animation
import math
import pylab
#from JSAnimation import IPython_display
pylab.ion()

def Ro(u1, u2,beta,Neta,sigma): #######################  CALCULA EL Ro DE CADA NODO
    R0 = beta*Neta*sigma*(1-u1)*(1-u2)/(c*mu)    
    return R0

####################### ECREACIÓN DEL GRAFO 
def Grafo_Ley_Potencia(N,k,gamma):
    while True:  
        s=[]
        while len(s)<N:
            nextval = int(nx.utils.powerlaw_sequence(k, gamma)[0]) #N nodes, power-law exponent 'gamma'
            if nextval!=0:
                s.append(nextval)
        if sum(s)%2 == 0:
            break
    g = nx.configuration_model(s)
    g =nx.Graph(g) # remove parallel edges
    g.remove_edges_from(g.selfloop_edges())
    return g, s
####################### ENCUENTRA NODOS INFECTADOS EN LA RED    
def FindInfected(g):
    NoInfectadosST = 0 
    NoInfectadosCT = 0         ########         NTI=numero total de infectados
    NoSusceptibles = 0
    for i in range(N):
        if (g.node[i]["V"]) > 0.0:
            g.node[i]['Ro'] = Ro(u1[i],u2[i],beta[i],Neta[i],sigma[i])
            if g.node[i]["Estado"] == 'Ct':
                NoInfectadosCT=NoInfectadosCT+1
                PAT=uniform(0,1) #probabilidad de abandonar tto
                if PAT<0.2:
                    g.node[i]["Estado"] = 'St'
                    u1[i]=0
                    u2[i]=0
                    NoInfectadosST = NoInfectadosST+1
                    NoInfectadosCT = NoInfectadosCT-1
            else:
                NoInfectadosST = NoInfectadosST+1
                if g.node[i]["T"]<350: #probabilidad de inciar tto
                    g.node[i]["Estado"] = 'Ct'
                    u1[i]=uniform(0,1)
                    u2[i]=uniform(0,1)
                    NoInfectadosCT = NoInfectadosCT+1
                    NoInfectadosST = NoInfectadosST-1

            #print ('El nodo ',i,' esta infectado, con V=', g.node[i]["V"], ' y con Ro=', g.node[i]["Ro"])
            
             
        NoSusceptibles = N-(NoInfectadosCT+NoInfectadosST) 
    return NoInfectadosST, NoInfectadosCT, NoSusceptibles

####################### GRAFICA Y GUARDA EN PDF LA ITERACIÓN i DE LA RED
def Grafique_Red(g, i):
    prev=(NoInfectadosST+NoInfectadosCT)/N
    fgi = plt.figure(figsize=(6,4),dpi=72)     
    #new_labels = dict(map(lambda x:((x[0],x[1]), str( math.ceil(x[2]['weight']) if x[2]['weight']>0 else "") ), g.edges(data = True)))
    #nx.draw_networkx_edge_labels(g, position, edge_labels = new_labels)
    nx.draw_networkx_edges(g,position,width=Arista, edge_color='gray', arrows=False)
    nx.draw_networkx(g,position, with_labels = etiquetas,node_size=size,edge_color='dimgray', node_color=[color_map[g.node[node]['Estado']] for node in g],font_color='k',alpha=1,linewidths=2,font_size=20)
    plt.tight_layout()
    plt.axis('off')
    if i == -1:
        plt.suptitle(r'Red Inicial, prevalencia: %.4f ' %(prev),y=0.98, fontsize=20)        
    elif i == TP-1: 
        plt.suptitle(r'Red final, prevalencia: %.4f ' %(prev),y=0.99, fontsize=20)
    else:
        plt.suptitle(r'It.: %s, prevalencia: %.4f ' %(i, prev),y=0.98, fontsize=20)
    plt.tight_layout()
    fgi.savefig("Iteracion"+str(i+1)+".pdf".format(i=i),dpi=400) 
    plt.show()

####################### ACTUALIZA LOS ATRIBUTOS (EI) DE CADA NODO DE LA RED
def update_EIall(i,tt,TT,Tss,MM,Mss,VV,WW):
    ti=int(tau[i])
    tf=int(tau[i+1])
    #print()
    print ('ITERACION', i, 'con t in (',ti,',',tf,')')
    for j in range(N):
        T0=g.node[j]["T"]
        Ts0=g.node[j]["Ts"]
        M0=g.node[j]["M"]
        Ms0=g.node[j]["Ms"]
        V0=g.node[j]["V"]
        W0=g.node[j]["W"]
        t = np.linspace(ti,tf,n+1)
        h=(tf-ti)/n
        t, T, Ts, M, Ms, V, W, R0 = EDO(T0,Ts0,M0,Ms0,V0,W0,t,h,u1[j],u2[j],beta[j],Neta[j],sigma[j])
        for l in range(len(t)):
            pos=i*(len(t))+l
                
            tt[j][pos] = t[l]
            TT[j][pos] = T[l]
            Tss[j][pos] = Ts[l]
            MM[j][pos] = M[l]
            Mss[j][pos] = Ms[l]
            VV[j][pos] = V[l]
            WW[j][pos] = W[l]
            
        longEstados = len(t)
        g.node[j]["T"] = T[longEstados-1]
        g.node[j]["Ts"] = Ts[longEstados-1]
        g.node[j]["M"] = M[longEstados-1]
        g.node[j]["Ms"] = Ms[longEstados-1]
        g.node[j]["V"] = V[longEstados-1] 
        g.node[j]["W"] = W[longEstados-1]
        g.node[j]["Ro"] = R0    
        T0=T[longEstados-1]
        Ts0=Ts[longEstados-1]
        M0=M[longEstados-1]
        Ms0=Ms[longEstados-1]
        V0=V[longEstados-1]
        W0=W[longEstados-1]
    return tt,TT,Tss,MM,Mss,VV,WW
    
#######################  SOLUCION DEL SISTEMA DE EDOs EN CADA ITERACION DE LA RED
def EDO(T0,Ts0,M0,Ms0,V0,W0,t,h,u1,u2,beta,Neta,sigma): 
    #------------------------------------------------------------------------
    #PARAMENTROS Y CONDICIONES INICIALES DEL MODELO
    #-------------------------------------------------------------------------
    R0=Ro(u1,u2,beta,Neta,sigma)
    #-------------------------------------------------------------------------
    #SE CREAN VARIABLES DE ESTADO Y VARIABLES AUXILIARES PARA EULER MEJORADO
    #-------------------------------------------------------------------------
    T = np.zeros([n+1],dtype=np.float32)
    Ts = np.zeros([n+1],dtype=np.float32)
    M = np.zeros([n+1],dtype=np.float32)
    Ms = np.zeros([n+1],dtype=np.float32)
    V = np.zeros([n+1],dtype=np.float32)
    W = np.zeros([n+1],dtype=np.float32)
    #-------------------------------------------------------------------------
    #SE ASIGNA LA CONDICION INICIAL
    #-------------------------------------------------------------------------
    T[0]=T0
    Ts[0]=Ts0
    M[0]=M0
    Ms[0]=Ms0
    V[0]=V0
    W[0]=W0
    #-------------------------------------------------------------------------
    #RESUELVE ECUACIONES DE ESTADO HACIA ADELANTE CON EULER MEJORADO
    #-------------------------------------------------------------------------
    for i in range(n):
        T[i+1] = T[i] + h*(sigma-beta*(1-u1)*T[i]*V[i]-mu*T[i])
        Ts[i+1] = Ts[i] + h*(beta*(1-u1)*T[i]*V[i]-varrho*Ts[i]*Ms[i]-delta*Ts[i])
        M[i+1] = M[i] + h*(kappa-psi*Ts[i]*M[i]-rho*M[i])
        Ms[i+1] = Ms[i] + h*(alpha*Ts[i]*Ms[i]+psi*Ts[i]*M[i]-rho*Ms[i])
        V[i+1] = V[i] + h*(Neta*delta*(1-u2)*Ts[i]-c*V[i])
        W[i+1] = W[i] + h*(Neta*delta*u2*Ts[i]-c*W[i])
    return t, T, Ts, M, Ms, V, W, R0
    
def Plot_ODE(tiempo,X1,X2,X3,X4,X5,X6):
    for i in range(N):
        col='k'                 
        f=plt.figure(num=i, figsize=(8, 6),dpi = 72)
        if g.node[i]["Estado"]=='St':
            plt.suptitle(r'Persona %s: infectada sin tratamiento con $R_0=%.2f$'%(i, g.node[i]["Ro"]), y=0.04, fontsize=16)
            col='r' 
        elif g.node[i]["Estado"]=='Ct':
            plt.suptitle(r'Persona %s: infectada con tratamiento con $R_0=%.2f$'%(i, g.node[i]["Ro"]), y=0.04, fontsize=16) 
            col='g' 
        else:
            plt.suptitle(r'Persona %s: susceptible' %(i), y=0.04, fontsize=16)
        plt.subplot(2,3,1),plt.plot(tiempo[i],X1[i],col,linewidth=2)
        plt.title(r'$T(t)$')
        plt.xlabel(r'$t$')      
    
        plt.subplot(2,3,2),plt.plot(tiempo[i],X2[i],col,linewidth=2)
        plt.title(r'$T^*(t)$')
        plt.xlabel(r'$t$')  
        
        plt.subplot(2,3,3),plt.plot(tiempo[i],X3[i],col,linewidth=2)
        plt.title(r'$M(t)$')
        plt.xlabel(r'$t$')
        
        plt.subplot(2,3,4),plt.plot(tiempo[i],X4[i],col,linewidth=2)
        plt.title(r'$M^*(t)$')
        plt.xlabel(r'$t$')
    
        plt.subplot(2,3,5),plt.plot(tiempo[i],X5[i],col,linewidth=2)
        plt.title(r'$V(t)$')
        plt.xlabel(r'$t$')
        
        plt.subplot(2,3,6),plt.plot(tiempo[i],X6[i],col,linewidth=2)
        plt.title(r'$W(t)$')
        plt.xlabel(r'$t$')
        
        f.subplots_adjust(hspace=0.3)
        plt.tight_layout()
        f.savefig("Persona"+str(i)+".pdf".format(i=i), dpi = 400)
    
#######################  ENCUENTRA POSIBLES PAREJAS PARA EL INFECTADO j Y CONSTRUYE UN VECTOR DE RIESGOS L     
def FindTarget():
    for j in range(N):    
        if (g.node[j]["V"]>0.0):
            #g.node[j]["Estado"]='I'
            if (g.node[j]["V"]<50):                 #carga viral baja VALORES TOMADO DE ARIEL Y LASRY 2014
               Lambda=uniform(0.0006,0.0011)
            elif (g.node[j]["V"]<10000):             #carga viral media
               Lambda=uniform(0.0007,0.0168)
            else: 
               Lambda=uniform(0.002,0.025)        #carga viral alta
            target=[]
            L=[]
            for l in range(N):
                if g.has_edge(j,l):
                    if (g.node[l]["Estado"]=='S'):
                        g[j][l]['weight']=Lambda
                        target=target+[l]
                        L=L+[(l+1)*(j+1)*Lambda/avg_deg] 
                    else:
                        g[j][l]['weight']=1
            Emparejar(j,target,L,Lambda)
   
#######################  EMPAREJA A j CON ALGUNO DE LOS TARGETS (O NINGUNO) Y TRANSMITE LA INFECCIÓN         
def Emparejar(j,target,L,Lambda):
    if target != []:
        #print ('El nodo ', j, 'puede infectar a :',target)
        if ran.choice(['Si se empareja','No se empareja'])=='Si se empareja':
            p=ran.randrange(len(target)) 
            pareja=target[p]
            Pinfectarse=uniform(0,1)#probabilidad de infectarse, S se infecta solo si este valor es mayor que el L
            #print(L,g[j][pareja]['weight'])
            #print('El nodo ',j,' se une con el nodo ',pareja)                    
            if Pinfectarse>L[p]:#prom(L): #and g.node[pareja]["T"]<400:
                g.node[pareja]["V"]=(g.node[j]["V"])*0.01
                g.node[pareja]["Estado"]='St'
                #print ('El nodo ',pareja,' SI se ha infectado: Ro=', g.node[pareja]["Ro"], ' y V=', g.node[pareja]["V"],' y Lambda=',g[j][pareja]['weight'])
            #else:
                #print ('El nodo ',pareja,' NO se ha infectado') 
        #else:
            #print('El nodo ', j, 'No se emparejó')

#######################CALCULA EL PROMEDIO DEL VECTOR x
def prom(x): 
    suma=0
    for i in range(len(x)):   
        suma=suma+x[i]
    promedio=suma/len(x)
    return promedio

####################### GRAFICA LAS DENSIDADES ACUMULADAS DE INFECTADOS Y SUSCEPTIBLES
def Plot_II(IST,ICT):
    II = plt.figure(num=1, figsize=(6, 4), dpi=72)
    plt.plot(IST,'k',linewidth=2)
    plt.plot(ICT,'b',linewidth=2)
    plt.ylabel(r'$I_{st}(t)$, $I_{ct}$')
    plt.xlabel(r'$t$')
    plt.tight_layout()
    II.savefig("Infectados.pdf", dpi=400)
    plt.show()


#######################  CREA UNA COPIA DEL GRAFO: NODO i -> NODO Pi
def mapping(x): 
    return 'P'+str(x+1)

def Modify_edges(g):
    Nodo_a_cambiar=ran.randrange(N)
    for l in range(N):
        if l != Nodo_a_cambiar:
            if g.has_edge(l,Nodo_a_cambiar):
                if ran.choice(['Si hay ruptura','No hay ruptura'])=='Si hay ruptura':
                    g.remove_edge(l,Nodo_a_cambiar)
                    print('la personas ', l, ' y ',Nodo_a_cambiar, ' rompieron')
            else:
                if ran.choice(['Es nueva pareja','No es nueva pareja'])=='Es nueva pareja':
                    g.add_edge(l,Nodo_a_cambiar)
                    print('la personas ', l, ' y ',Nodo_a_cambiar, ' son pareja')
                    
                   
        
############################################################## INICIALIZACION DE PARAMETROS
plotEI=False       #DETERMINA SI SE GRAFICAN LOS ESTADOS INMUNOLOGICOS DE TODOS LOS NODOS
plotEP=True          #DETERMINA SI SE GRAFICA LA RED EN CADA ITERACION
plotII=True        #DETERMINA SI SE GRAFICA EL NUMERO ACUMULADO DE INFECTADOS Y SUSCEPIBLES
############################################################## ESCALA INMUNOLOGICA      
mu=0.01 
c=2.4
delta=0.26
psi=0.002
alpha=0.00005
rho=0.1
kappa=5 
varrho=0.002


############################################################## ESCALA POBLACIONAL 
N=20
k=4
gamma=2.7
pr=0.001
if N<=50:
    size=1000
    etiquetas=True
    Arista = 1
else:
    size=20
    etiquetas=False
    Arista = 110

TP=10   ##### TIEMPO FINAL DE LA RED 

tau = np.zeros([TP+1])

Sus = np.zeros([TP],dtype=np.float32)
ICT = np.zeros([TP],dtype=np.float32) 
IST = np.zeros([TP],dtype=np.float32)
Prev=np.zeros([TP],dtype=np.float32)

for i in range(TP+1):
    tau[i]=int((i))
 
print(tau)    
T0 = np.zeros([N],dtype=np.float32)
Ts0 = np.zeros([N],dtype=np.float32)
M0 = np.zeros([N],dtype=np.float32)
Ms0 = np.zeros([N],dtype=np.float32)
V0 = np.zeros([N],dtype=np.float32)
W0 = np.zeros([N],dtype=np.float32)
u1=np.zeros([N],dtype=np.float32)
u2=np.zeros([N],dtype=np.float32)
beta=np.zeros([N],dtype=np.float32)
Neta=np.zeros([N],dtype=np.float32)
sigma=np.zeros([N],dtype=np.float32)
R0=np.zeros([N],dtype=np.float32)
for i in range(0,N):
    T0[i]=randint(200,1000)
    Ts0[i]=0
    M0[i]=randint(70,980)
    Ms0[i]=0
    V0[i]=0
    W0[i]=0
    beta[i]=uniform(0,0.00005)
    Neta[i]=uniform(100,1500)
    sigma[i]=uniform(5,20)
#    u2[i]=uniform(0,1)    

InInicial=randint(0,N-1)
V0[InInicial]=randint(1,1000)



#print('Ro=',R0) 

########################################### CREACION DE LA RED
#create a graph with degrees following a power law distribution
#g = nx.scale_free_graph(N, alpha=0.41, beta=0.54, gamma=0.05, delta_in=0.2, delta_out=0, create_using=None, seed=None)
#g, s = Grafo_Ley_Potencia(N,k,gamma)
g=nx.powerlaw_cluster_graph(N, k,pr, seed=None)
#g=nx.barabasi_albert_graph(N, k, seed=None)
#H=nx.relabel_nodes(g,mapping)

########################################### POCISION DE LOS NODOS 
position = nx.random_layout(g)
#position = nx.circular_layout(g)
#position = nx.spectral_layout(g)
#position = nx.spring_layout(g)
#position = nx.fruchterman_reingold_layout(g)

########################################## COLOR DE LOS NODOS 
color_map = {'St':'red', 'Ct':'yellowgreen', 'S':'cornflowerblue'}
#color_map2 = plt.cm.Blues

########################################## DEFINICION E INICIALIZACION DE ATRIBUTOS DELA RED
for i in range(g.number_of_nodes()):
    g.node[i]['T'] = T0[i]
    g.node[i]['Ts'] = Ts0[i]
    g.node[i]['M'] = M0[i]
    g.node[i]['Ms'] = Ms0[i]
    g.node[i]['V'] = V0[i]
    g.node[i]['W'] = W0[i]
    g.node[i]['Ro'] = R0[i]
    g.node[i]['Estado']='S'
g.node[InInicial]["Estado"]='St'


#for i in range(g.number_of_nodes()):     ########## ACTIVAR PARA IMPRIMIR TODOS LOS NODOS DE LA RED
#        print (i,g.node[i]) 
for i, j in g.edges():
    g[i][j]['weight']=0
  
NoInfectadosST=1;NoInfectadosCT=0;

i = -1                                   ########## SE VA A GRAFICAR LA RED INICIAL 
Grafique_Red(g,i)
#en=int(input('cero o uno'))
NoInfectadosST,NoInfectadosCT,NoSusceptibles=FindInfected(g)

############################################################## ITERACIONES SOBRE LA RED
#ti=int(tau[0])
#tf=int(tau[1])
#print(ti,tf)
n=50#=(tf-ti)
t=np.linspace(tau[0],tau[1],n+1)
print('longitud de t:',len(t))
Dim_tiempo=(len(t))*(TP)
print('Dimension del tiempo:',Dim_tiempo)
tt= [[0] * Dim_tiempo for i in range(N)]
print('Longitud tt',len(tt))

TT=[[0] * Dim_tiempo for i in range(N)]
Tss=[[0] * Dim_tiempo for i in range(N)]
MM=[[0] * Dim_tiempo for i in range(N)]
Mss=[[0] * Dim_tiempo for i in range(N)]
VV=[[0] * Dim_tiempo for i in range(N)]
WW=[[0] * Dim_tiempo for i in range(N)]

N, K = g.order(), g.size()
avg_deg = float(K) / N
               
for i in range(TP):
    NTIant = NoInfectadosST+NoInfectadosCT
    tt,TT,Tss,MM,Mss,VV,WW = update_EIall(i,tt,TT,Tss,MM,Mss,VV,WW)   
    FindTarget()
    NoInfectadosST,NoInfectadosCT,NoSusceptibles = FindInfected(g)  
    ICT[i] = NoInfectadosCT
    IST[i] = NoInfectadosST
    Sus[i] = N-(ICT[i]+IST[i])   
    print('Ahora hay ', NoInfectadosST, 'Infectados sin tratamiento')
    print('Ahora hay ', NoInfectadosCT, 'Infectados con tratamiento')
    Prev[i]=(NoInfectadosST+NoInfectadosCT)/N
    print('Prevalencia=',Prev[i])
    if plotEP == True:
        Grafique_Red(g,i)

#        if NTIant < NoInfectados:
#            Grafique_Red(g,i)
        
    #if uniform(0,1)>0.98:
        #Modify_edges(g)
#print(len(Sus),Sus)       ########## activar para imprimir No. acumulado de susceptibles e infectados 
#print(len(Inf),Inf)

if plotEI == True:
    Plot_ODE(tt,TT,Tss,MM,Mss,VV,WW) 

Grafique_Red(g,i)

tau2 = np.zeros([TP])

print(ICT)
print(len(ICT))
for i in range(TP):
    tau2[i]=int((i))
print(tau2)
print(len(tau2))
conteo=plt.figure(num=1, figsize=(6, 4), dpi=72) 
plt.plot(tau2,ICT,'g.')
plt.plot(tau2,IST,'r.')
conteo.savefig("Conteo.pdf", dpi=400)
plt.show()

pre=plt.figure(num=1, figsize=(6, 4), dpi=72)
plt.plot(tau2,Prev,'r')
pre.savefig("pre.pdf", dpi=400)
plt.show()
#
#clust_coefficients = nx.clustering(g)

N, K = g.order(), g.size()


avg_deg = float(K) / N
print("Nodes: ", N)
print("Edges: ", K)
print('k:',k)
print('gamma:',gamma)
#for i, j in g.edges():
#    print(i, j, g[i][j]['weight'])
    
print("Average degree: ", avg_deg)

#print('Coeficientes de clustering:',nx.clustering(g))
#print('Average clustering:',nx.average_clustering(g))

#g_components = nx.connected_component_subgraphs(g) 
#print('components:',g_components)
#g_mc = g_components
#print('No se que es esto:',g_mc)
# Betweenness centrality
bet_cen = nx.betweenness_centrality(g)
print('bet cen:',bet_cen)
# Closeness centrality
clo_cen = nx.closeness_centrality(g)
print('clo cen:',clo_cen)
# Eigenvector centrality
#eig_cen = nx.eigenvector_centrality(g)

print('average neighbor degree=',nx.average_neighbor_degree(g))
print('average degree connectivity=',nx.average_degree_connectivity(g))
print('average node connectivity=',nx.average_node_connectivity(g))
CL = np.zeros([len(clo_cen)])
CC = np.zeros([len(clo_cen)])
AND = np.zeros([len(clo_cen)])

for i in range(len(clo_cen)):
    CL[i] = clo_cen[i]
    CC[i] = bet_cen[i]
    AND[i] = nx.average_neighbor_degree(g)[i]
cen = plt.figure(num=1, figsize=(6, 4), dpi=72)    
plt.plot(CL,'k.',linewidth=1)
#plt.hold(True)
plt.plot(CC,'b.',linewidth=1)
cen.savefig("Centralities.pdf", dpi=400)
plt.show()

print('El primer nodo infectado fue,', InInicial)
"""
PowerLaw1
Nodes:  1000
Edges:  978
k: 20
gamma: 2.7
average node connectivity= 0.48685485485485486
Average degree:  0.978
"""

"""
PowerLaw2
Nodes:  1000
Edges:  871
k: 20
gamma: 2.9
average node connectivity= 0.3217017017017017
Average degree:  0.871
"""

"""
PowerLaw3
Nodes:  1000
Edges:  827
k: 20
gamma: 2.95
Average degree:  0.827
average node connectivity= 0.19478478478478478
"""

"""
PowerLaw4
Nodes:  1000
Edges:  872
k: 20
gamma: 3
Average degree:  0.872
average node connectivity= 0.27544944944944943
"""

"""
PowerLaw5
Nodes:  1000
Edges:  835
k: 20
gamma: 3
Average degree:  0.835
average node connectivity= 0.27286686686686684
"""

"""
PowerLaw6
Nodes:  1000
Edges:  816
k: 20
gamma: 3.1
Average degree:  0.816
average node connectivity= 0.22273073073073074
"""