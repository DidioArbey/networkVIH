import networkx as nx
import matplotlib.pyplot as plt

G  =  nx . petersen_graph () 
plt . subplot ( 121 ) 
#<matplotlib.axes._subplots.AxesSubplot objeto en ...> 
nx . draw ( G ,  with_labels = True ,  font_weight = 'bold' ) 
#plt . subplot ( 122 ) 
#<matplotlib.axes._subplots.AxesSubplot object at ...> 
nx . draw_shell ( G , [ range ( 5 ,  10 ),  range ( 5 )],  with_labels = True ,  font_weight = 'bold' )



#options  =  { 'node_color' :  'black' , 'node_size' :  100 , 'width' :  3 , } 
#plt . subplot ( 221 ) 
#nx . draw_random ( G ,  ** opciones ) 
#plt . subtrama ( 222 )
#nx . draw_circular ( G ,  ** opciones ) 
#plt . subplot ( 223 ) 
#nx . draw_spectral ( G ,  ** opciones ) 
#plt . subplot ( 224 ) 
#nx . nlist = [ range ( 5 , 10 ),  range ( 5 )],  ** opciones )


#G  =  nx . dodecahedral_graph () 
#shells  =  [[ 2 ,  3 ,  4 ,  5 ,  6 ],  [ 8 ,  1 ,  0 ,  19 ,  18 ,  17 ,  16 ,  15 ,  14 ,  7 ],  [ 9 ,  10 ,  11 ,  12 ,  13 ]] 
#nx . draw_shell( G ,  nlist = conchas ,  ['node_color' : 'black'] )

G  =  nx . Graph () 
e  =  [( 'a' ,  'b' ,  0.3 ),  ( 'b' ,  'c' ,  0.9 ),  ( 'a' ,  'c' ,  0.5 ),  ( 'c' ,  'd' ,  1,2 )] 
G . add_weighted_edges_from ( e ) 
print ( nx . ,  'd' )) 
['a', 'c', 'd']