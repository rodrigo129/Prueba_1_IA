from Ranas import *

TIPOS=["Anchura","Profundidad","Primero_El_Mejor","Beam","Hill_Climbing"]



# MAIN
if __name__ == "__main__":
    puzzle = Juego_De_Ranas("VVV_CCC")
    puzzle.busqueda(TIPOS[3])
