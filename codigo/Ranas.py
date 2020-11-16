from collections import deque
import sys, os
sys.setrecursionlimit(100000)




MOVIMIENTOS=["C11","C12","C21","C22","C31","C32","V11","V12","V21",
             "V22","V31","V32"]

def list2str(lista):
    s=""
    for e in lista:
        s=s+e
    return s

class nodo_estado:
    
    def __init__(self, EA, EP, A, n):
        self.valor = EA
        self.padre = EP
        self.accion = A
        self.nivel = n
        self.distancia = None

    def get_estado(self):
        return self.valor
    
    def get_padre(self):
        return self.padre

    def get_accion(self):
        return self.accion

    def get_nivel(self):
        return self.nivel

    def set_distancia(self, d):
        self.distancia = d
    
    def get_distancia(self):
        return self.distancia

    def __eq__(self, e):
        return self.valor == e

def ordenar_por_heuristica(e):
    return e.get_distancia()

class Juego_De_Ranas:
    estado_final = [nodo_estado("CCC_VVV",None,"Final",None)]
    def __init__(self, EI):
        self.estado_inicial = nodo_estado(EI, None, "Origen", 1)
        self.calcular_heuristica(self.estado_inicial)
        self.estado_actual = None
        self.historial = []
        self.cola_estados = deque()

    def add(self, ET):
        self.cola_estados.append(ET)
        self.historial.append(ET)

    def pop(self):
        return self.cola_estados.popleft()

    def esta_en_historial(self, e):
        return e in self.historial

    def es_final(self):
        return self.estado_actual in self.estado_final

    def mostrar_estado_actual(self):
        print("Estado Actual (H = " + str(
            self.estado_actual.get_distancia()) + ") [" + str(self.estado_actual.get_nivel()) + "] es:\n" + self.estado_actual.get_estado()+"\n")

    def mostrar_estado(self, e):
        print("Estado  (H = " + str(e.get_distancia()) + ")  es:\n" + e.get_estado()+ "\n")

    def buscar_padre(self, e):
        if e.get_padre() == None:
            print("\n" + e.get_accion() + "\n Nivel: 1")
            self.mostrar_estado(e)
        else:
            self.buscar_padre(e.get_padre())
            print("\n" + e.get_accion() + "\n Nivel: " + str(e.get_nivel()))
            self.mostrar_estado(e)

    def mover(self, direccion):
        """editar para que trabaje con el nuevo sistema
        direciones nuevas C12=> rana cafe, numero 1, salta 2 espacios




        """
        aux=list(direccion)
        aux[1]=int(aux[1])
        aux[2] = int(aux[2])
        estado = list(self.estado_actual.get_estado())
        n = len(estado)
        i=0
        #print(aux)
        #print(estado)
        if aux[0]=="C":
            Ranas_Cafes_Vistas=0
            while i<n:
                #print("{},{}:de tipos {},{}".format(
                #    Ranas_Cafes_Vistas,aux[1],type(
                #        Ranas_Cafes_Vistas),type(aux[1])))
                #print(Ranas_Cafes_Vistas==aux[1])
                if estado[i]==aux[0]:
                    Ranas_Cafes_Vistas+=1
                if Ranas_Cafes_Vistas==aux[1]:
                    index=i
                    break
                #print(i)
                i+=1
            if index-aux[2]<0:
                return "illegal"
            else:
                if estado[index-aux[2]]!="_":
                    return "illegal"
                else:
                    estado[index-aux[2]]="C"
                    estado[index] = "_"
                    #

        else:#aux[0]=="V"
            Ranas_Verdes_Vistas = 0
            while i < n:
                if estado[i] == aux[0]:
                    Ranas_Verdes_Vistas += 1
                if Ranas_Verdes_Vistas == aux[1]:
                    index = i
                    break
                i += 1
            if index+aux[2] >=n:
                return "illegal"
            else:
                if estado[index+aux[2]] != "_":
                    return "illegal"
                else:
                    estado[index+aux[2]] = "V"
                    estado[index] = "_"  #

        return list2str(estado)

    def algoritmo_anchura(self, EI):
        iteracion = 1
        self.estado_actual = EI
        #movimientos = ["UP","DOWN","LEFT","RIGHT"]
        movimientos=MOVIMIENTOS

        while(not self.es_final()):
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()

            for movimiento in movimientos:
                estado_temporal = nodo_estado(self.mover(movimiento), self.estado_actual, "Mover a " + movimiento, self.estado_actual.get_nivel() + 1)
                if not self.esta_en_historial(estado_temporal) and not estado_temporal.get_estado() == "illegal":
                    self.add(estado_temporal) # se incluye en historial y en la cola

            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))

            #Paso a siguiente iteracion
            self.estado_actual = self.pop()
            iteracion += 1
        
        print("Iteracion: " + str(iteracion) + "\n")
        self.mostrar_estado_actual()
        print("\n\n\nHa llegado a Solucion!!!")
        self.buscar_padre(self.estado_actual)
        print("\nALGORITMO EN ANCHURA:")
        print("\nElementos en Historial: " + str(len(self.historial)))
        print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
        print("\nCantidad de Iteraciones: " + str(iteracion))

    def add_profundidad(self, pila_sucesores):
        while pila_sucesores.__len__() > 0:
            e = pila_sucesores.pop()
            self.historial.append(e)
            self.cola_estados.appendleft(e)

    def algoritmo_profundidad(self, EI):
        iteracion = 1
        self.estado_actual = EI
        #movimientos = ["UP", "DOWN", "LEFT", "RIGHT"]
        movimientos = MOVIMIENTOS
        sucesores = deque()

        while not self.es_final():
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()

            for movimiento in movimientos:
                estado_temporal = nodo_estado(self.mover(movimiento), self.estado_actual, "Mover a " + movimiento, self.estado_actual.get_nivel() + 1)
                if not self.esta_en_historial(estado_temporal) and not estado_temporal.get_estado() == "illegal":
                    sucesores.append(estado_temporal)
            
            self.add_profundidad(sucesores) 

            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))

            #Paso a siguiente iteracion
            self.estado_actual = self.pop()
            iteracion += 1

        print("Iteracion: " + str(iteracion) + "\n")
        self.mostrar_estado_actual()
        print("\n\n\nHa llegado a Solucion!!!")
        self.buscar_padre(self.estado_actual)
        print("\nALGORITMO EN PROFUNDIDAD:")
        print("\nElementos en Historial: " + str(len(self.historial)))
        print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
        print("\nCantidad de Iteraciones: " + str(iteracion))


    def distancia_estados(self, estado_presente, estado_objetivo):
        """Comparando estados, contando los espacios desubicados"""
        d = 0
        for i in range(len(estado_presente.get_estado())):
            if not estado_presente.get_estado()[i] == estado_objetivo.get_estado()[i]:
                d += 1
        return d

    def distancia_de_edicion(self,estado_presente,estado_objetivo):
        d=0
        Ranas_Verdes_Vistas=0
        Ranas_Cafe_Vistas=0
        estado_final=list(estado_objetivo.get_estado())
        estado_actual=list(estado_presente.get_estado())
        i=0
        n=len(estado_actual)
        print(estado_actual)
        while i<n:
            j=estado_final.index(estado_actual[i])
            if estado_actual[i]=="C":
                j=j+Ranas_Cafe_Vistas
                Ranas_Cafe_Vistas+=1
            if estado_actual[i]=="V":
                j = n-(1+Ranas_Verdes_Vistas)
                if estado_actual[j]==estado_actual[i]:
                    """como el asco esta heuristica y su naturaleza 
                    asimetrica para indicar las posiciones de cada 
                    rana, por lo menos se puede areglar de esta 
                    manera """
                    j=i
                Ranas_Verdes_Vistas+=1
            if i!=j:
                print("{},{}".format(i,j))
                print("{} == {}".format(estado_actual[i],
                                        estado_actual[j]))

            d=d+abs(i-j)
            print("{}->{}".format(i,d))
            i+=1
        return d

    def calcular_heuristica(self, estado):
        primero = True
        for final in self.estado_final:
            if primero:
                distancia = self.distancia_de_edicion(estado, final)
                primero = False
            else:
                nueva_distancia = self.distancia_de_edicion(estado, final)
                if nueva_distancia < distancia:
                    distancia = nueva_distancia
        estado.set_distancia(distancia)


    def algoritmo_primero_mejor(self, EI):
        iteracion = 1
        self.estado_actual = EI
        #movimientos = ["UP", "DOWN", "LEFT", "RIGHT"]
        movimientos=MOVIMIENTOS
        sucesores = []

        while not self.es_final():
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()

            for movimiento in movimientos:
                estado_temporal = nodo_estado(self.mover(movimiento), self.estado_actual, "Mover a " + movimiento, self.estado_actual.get_nivel() + 1)
                if not self.esta_en_historial(estado_temporal) and not estado_temporal.get_estado() == "illegal":
                    self.calcular_heuristica(estado_temporal)
                    sucesores.append(estado_temporal)
            
            sucesores.sort(key=ordenar_por_heuristica)
            self.add_profundidad(sucesores)

            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))

            #Paso a siguiente iteracion
            self.estado_actual = self.pop()
            iteracion += 1

        print("Iteracion: " + str(iteracion) + "\n")
        self.mostrar_estado_actual()
        print("\n\n\nHa llegado a Solucion!!!")
        self.buscar_padre(self.estado_actual)
        print("\nALGORITMO EN PRIMERO EL MEJOR:")
        print("\nElementos en Historial: " + str(len(self.historial)))
        print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
        print("\nCantidad de Iteraciones: " + str(iteracion))

    def add_beam(self, sucesores, b):
        for estado in sucesores:
            if b > 0:
                self.add(estado)
                b -= 1
            else:
                self.historial.append(estado)

    def algoritmo_beam(self, EI):
        iteracion = 1
        b = 3 # variable de corte      ####cambiado de 2=>3 con 2 el
        # algoritmo podaba la rama con la solucion
        sucesores = []
        self.estado_actual = EI
        #movimientos = ["UP","DOWN","LEFT","RIGHT"]
        movimientos = MOVIMIENTOS

        while(not self.es_final()):
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()

            for movimiento in movimientos:
                estado_temporal = nodo_estado(self.mover(movimiento), self.estado_actual, "Mover a " + movimiento, self.estado_actual.get_nivel() + 1)
                if not self.esta_en_historial(estado_temporal) and not estado_temporal.get_estado() == "illegal":
                    self.calcular_heuristica(estado_temporal)
                    sucesores.append(estado_temporal) # se incluye en historial y en la cola

            sucesores.sort(key=ordenar_por_heuristica)
            self.add_beam(sucesores, b)
            sucesores.clear()

            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))

            #Paso a siguiente iteracion
            if len(self.cola_estados)==0:
                print("el algorimo beam no fue capaz de encontrar una solucion, no existe o se encuentra en una rama podada\n")
                return None
            self.estado_actual = self.pop()
            iteracion += 1
        
        print("Iteracion: " + str(iteracion) + "\n")
        self.mostrar_estado_actual()
        print("\n\n\nHa llegado a Solucion!!!")
        self.buscar_padre(self.estado_actual)
        print("\nALGORITMO EN BEAM:")
        print("\nElementos en Historial: " + str(len(self.historial)))
        print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
        print("\nCantidad de Iteraciones: " + str(iteracion))


    def algoritmo_hill_climbing(self, EI):
        #requiere una herustica diferente para llegar a la solucion
        iteracion = 1
        termina_bien = True
        self.estado_actual = EI
        #movimientos = ["UP", "DOWN", "LEFT", "RIGHT"]
        movimientos=MOVIMIENTOS
        sucesores = []

        while not self.es_final():
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()

            for movimiento in movimientos:
                estado_temporal = nodo_estado(self.mover(movimiento), self.estado_actual, "Mover a " + movimiento, self.estado_actual.get_nivel() + 1)
                if not self.esta_en_historial(estado_temporal) and not estado_temporal.get_estado() == "illegal":
                    self.calcular_heuristica(estado_temporal)
                    sucesores.append(estado_temporal)
            
            sucesores.sort(key=ordenar_por_heuristica)
            self.add_profundidad(sucesores)

            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))

            #Paso a siguiente iteracion
            estado_anterior = self.estado_actual
            self.estado_actual = self.pop()

            if estado_anterior.get_distancia() < self.estado_actual.get_distancia():
                print("\n\n\nNO llega a Solucion!!!")
                print("\nALGORITMO EN HILL CLIMBING:")
                print("\nElementos en Historial: " + str(len(self.historial)))
                print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
                print("\nCantidad de Iteraciones: " + str(iteracion))
                termina_bien = False
                break

            iteracion += 1
        
        if termina_bien:
            print("Iteracion: " + str(iteracion) + "\n")
            self.mostrar_estado_actual()
            print("\n\n\nHa llegado a Solucion!!!")
            self.buscar_padre(self.estado_actual)
            print("\nALGORITMO EN HILL CLIMBING:")
            print("\nElementos en Historial: " + str(len(self.historial)))
            print("\nElementos en Cola Estados: " + str(len(self.cola_estados)))
            print("\nCantidad de Iteraciones: " + str(iteracion))
        else:
            print("Termina Mal... que penita :(")

    def busqueda(self,tipo):
        self.add(self.estado_inicial)
        aux={"Anchura":self.algoritmo_anchura,
             "Profundidad": self.algoritmo_profundidad,
             "Primero_El_Mejor":self.algoritmo_primero_mejor,
             "Beam": self.algoritmo_beam,
             "Hill_Climbing":self.algoritmo_hill_climbing


             }
        """

        
        
        """



        aux[tipo](self.pop())


            
