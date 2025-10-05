#
# Universidad Nacional de Itapua - IA 7mo Semestre  
# Proyecto#2: Ta-Te-Ti 3D con Minimax y Poda Alfa-Beta
# Autor: Gabriel Godoy
#

import time

# Pre-computar 76 líneas ganadoras
def _gen():
    L = []
    for i in range(4):
        for j in range(4):
            L.append([(i,j,0),(i,j,1),(i,j,2),(i,j,3)])
            L.append([(i,0,j),(i,1,j),(i,2,j),(i,3,j)])
            L.append([(0,i,j),(1,i,j),(2,i,j),(3,i,j)])
    for i in range(4):
        L.append([(i,0,0),(i,1,1),(i,2,2),(i,3,3)])
        L.append([(i,0,3),(i,1,2),(i,2,1),(i,3,0)])
        L.append([(0,i,0),(1,i,1),(2,i,2),(3,i,3)])
        L.append([(0,i,3),(1,i,2),(2,i,1),(3,i,0)])
        L.append([(0,0,i),(1,1,i),(2,2,i),(3,3,i)])
        L.append([(0,3,i),(1,2,i),(2,1,i),(3,0,i)])
    L += [[(0,0,0),(1,1,1),(2,2,2),(3,3,3)],[(0,0,3),(1,1,2),(2,2,1),(3,3,0)],
          [(0,3,0),(1,2,1),(2,1,2),(3,0,3)],[(0,3,3),(1,2,2),(2,1,1),(3,0,0)]]
    return L

LIN = _gen()

def gana(t, s):
    """Verificar victoria en O(76)"""
    for ln in LIN:
        if all(t[z][x][y]==s for z,x,y in ln):
            return True
    return False

# ============ MINIMAX CON PODA ALFA-BETA ============
def minimax(t, prof, a, b, mx, yo, t0, lim):
    """
    Algoritmo Minimax con poda alfa-beta:
    - prof: profundidad máxima de exploración
    - a, b: ventanas alfa-beta para poda
    - mx: True=maximizar, False=minimizar
    - yo: símbolo del jugador actual
    - t0, lim: control de tiempo
    """
    if time.time()-t0 > lim or prof == 0:
        return 0, None
    
    mv = [(z,x,y) for z in range(4) for x in range(4) for y in range(4) if t[z][x][y]==' ']
    if not mv: return 0, None
    
    # Ordenar por centro primero (mejor poda)
    mv.sort(key=lambda p: abs(p[0]-1.5)+abs(p[1]-1.5)+abs(p[2]-1.5))
    if len(mv) > 10: mv = mv[:10]
    
    op = 'O' if yo == 'X' else 'X'
    mejor = mv[0]
    
    if mx:  # Nodo MAX
        v = float('-inf')
        for z,x,y in mv:
            t[z][x][y] = yo
            if gana(t, yo):
                t[z][x][y] = ' '
                return 10000, (z,x,y)
            e, _ = minimax(t, prof-1, a, b, False, yo, t0, lim)
            t[z][x][y] = ' '
            if e > v:
                v, mejor = e, (z,x,y)
            a = max(a, e)
            if b <= a: break  # Poda
        return v, mejor
    else:  # Nodo MIN
        v = float('inf')
        for z,x,y in mv:
            t[z][x][y] = op
            if gana(t, op):
                t[z][x][y] = ' '
                return -10000, (z,x,y)
            e, _ = minimax(t, prof-1, a, b, True, yo, t0, lim)
            t[z][x][y] = ' '
            if e < v:
                v, mejor = e, (z,x,y)
            b = min(b, e)
            if b <= a: break  # Poda
        return v, mejor

def jugar(tablero, tiempo_limite):
    """
    Estrategia adaptativa:
    - Apertura: Posiciones centrales
    - Juego medio: Detección victoria/bloqueo + heurística simple
    - Juego final: Minimax con alfa-beta (movimiento 45+)
    """
    t0 = time.time()
    nm = sum(1 for z in range(4) for x in range(4) for y in range(4) if tablero[z][x][y]!=' ')
    yo = 'X' if nm%2==0 else 'O'
    op = 'O' if yo=='X' else 'X'
    
    # Apertura
    if nm==0: return (1,1,1)
    if nm==1: return (2,2,2) if tablero[1][1][1]!=' ' else (1,1,2)
    
    mv = [(z,x,y) for z in range(4) for x in range(4) for y in range(4) if tablero[z][x][y]==' ']
    if not mv: return (0,0,0)
    
    # Victoria inmediata / Bloqueo crítico
    for ln in LIN:
        vac = [(z,x,y) for z,x,y in ln if tablero[z][x][y]==' ']
        if len(vac) != 1: continue
        mis = sum(1 for z,x,y in ln if tablero[z][x][y]==yo)
        opo = sum(1 for z,x,y in ln if tablero[z][x][y]==op)
        if mis==3: return vac[0]  # Ganar
        if opo==3: return vac[0]  # Bloquear
    
    # Juego final: Minimax
    if nm >= 45:
        try:
            _, m = minimax(tablero, 4, float('-inf'), float('inf'), True, yo, t0, 0.35)
            if m: return m
        except:
            pass
    
    # Heurística simple: preferir centro
    mv.sort(key=lambda p: abs(p[0]-1.5)+abs(p[1]-1.5)+abs(p[2]-1.5))
    return mv[0]
