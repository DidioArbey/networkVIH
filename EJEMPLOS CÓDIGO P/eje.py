def imc(masa, estatura):
  altura=pow(estatura,2)
  imc= masa/altura
  return imc
# print(imc(84,1.70))


def velocidad(distancia, tiempo):
    tiempoH=tiempo/3600
    distanciam=distancia*1000
    velk=(distancia/tiempoH)
    vels=(distanciam/tiempo)
    resultado = f"La velocidad es {velk} km/h o {vels} m/s"
    return resultado
# print(velocidad(191.53372403684486,3037.098012217049))

# def xor(a, b):
#     xor = False
#     if bool(a) == bool(b):
#         return False
#     else:
#         return a or b
#     return xor
# print(xor(True,False))

# a = 15
# b = 10
# if a == b:
#     print("Son iguales")
#     print("Adiós")
# else:
#     print("Son distintos")
#     print("Adiós")
# print("a y b son dos números")

# c = float(input("Ingrese temperatura del agua"))
# if c <= 0:
#     print("Su agua está congelada")
# elif c >= 0 and c < 100:
#     print("Su agua está líquida") 
# elif:
#     print("Su agua está hirviendo")

# n = 20
# if (n <= 100 and n % 2 == 0) or (n < 5):
#     if n != 21:
#         print("1")
#     else:
#         print("2")
# else:
#     if n == 20:
#         print("3")
#     else:
#         print("4")

# numero = int(input("Ingrese calidad del aire"))
# if numero >= 0 and numero <= 99:
#     print("Bueno")
# elif numero >= 100 and numero <= 199:
#     print("Regular")
# elif numero >= 200 and numero <= 299:
#     print("Alerta")
# elif numero >= 300 and numero <= 499:
#     print("Preemergencia")
# else:
#     print("Emergencia")

# numero = int(input("Ingrese calidad del aire"))
# if numero>=0 and numero<=99:
#     print("Bueno")
# if numero>=100 and numero<=199:
#     print("Regular")
# if numero>=200 and numero<=299:
#     print("Alerta")
# if numero>=300 and numero<=499:
#     print("Preemergencia")
# else:
#     print("Emergencia")

# numero = int(input("Ingrese numero"))
# if numero%2==0:
#     print("Es par")
A=2004
if A % 100 == 0 and A % 4 == 0 and A % 400 ==0:
    print("Es bisiesto")