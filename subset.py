"""Construcción de subconjuntos: convierte un AFN en un AFD equivalente."""
import re
import sys
from collections import deque

VACIO = frozenset()  # el conjunto vacío (se escribe 0): es un estado más del AFD
CONJUNTO_O_NUMERO = re.compile(r"\{[^}]*\}|\d+")  # encuentra "{1 5}" o "3"


# lectura

def leer_numeros(linea):
    """'3 5' -> [3, 5]. Una línea con solo '0' significa sin estados -> []."""
    return [int(palabra) for palabra in linea.split() if int(palabra) != 0]


def leer_conjunto(token):
    """'{1 5}' -> {1, 5}; '0' -> {}; '4' -> {4}."""
    if token.startswith("{"):
        return frozenset(int(palabra) for palabra in token[1:-1].split())
    numero = int(token)
    return VACIO if numero == 0 else frozenset([numero])


def leer_fila(linea, alfabeto):
    """'3 {2 4} 0' -> (3, {'a': {2, 4}, 'b': {}})."""
    estado, *destinos = CONJUNTO_O_NUMERO.findall(linea)
    fila = {simbolo: leer_conjunto(token) for simbolo, token in zip(alfabeto, destinos)}
    return int(estado), fila


def leer_caso(lineas):
    """Devuelve (estados_iniciales, alfabeto, estados_finales, delta), donde
    delta[(estado, simbolo)] es el conjunto de estados alcanzables.
    """
    cantidad_estados = int(next(lineas))
    estados_iniciales = frozenset(leer_numeros(next(lineas)))
    alfabeto = next(lineas).split()
    estados_finales = frozenset(leer_numeros(next(lineas)))

    delta = {}
    for _ in range(cantidad_estados):
        estado, fila = leer_fila(next(lineas), alfabeto)
        for simbolo, destinos in fila.items():
            delta[(estado, simbolo)] = destinos
    return estados_iniciales, alfabeto, estados_finales, delta


# algoritmo

def mover(delta, estados, simbolo):
    """Unión de delta(q, simbolo) para cada q en estados."""
    resultado = set()
    for estado in estados:
        resultado |= delta.get((estado, simbolo), VACIO)
    return frozenset(resultado)


def construccion_subconjuntos(estados_iniciales, alfabeto, delta):
    estados_afd = [estados_iniciales]
    delta_afd = {}
    pendientes = deque([estados_iniciales])

    while pendientes:
        actual = pendientes.popleft()
        for simbolo in alfabeto:
            destino = mover(delta, actual, simbolo)
            delta_afd[(actual, simbolo)] = destino
            if destino not in estados_afd:
                estados_afd.append(destino)
                pendientes.append(destino)
    return estados_afd, delta_afd


def finales_del_afd(estados_afd, finales_afn):
    """Un estado del AFD es final si contiene al menos un final del AFN."""
    return [A for A in estados_afd if A & finales_afn]


# salida

def formato_conjunto(estados):
    """{1, 5} -> '{1 5}'; el conjunto vacío -> '0'."""
    if not estados:
        return "0"
    return "{" + " ".join(str(q) for q in sorted(estados)) + "}"


def marca_fila(estado, estado_inicial, estados_finales):
    """Marca antes de la fila: '->' inicial, '<-' final, '<->' ambos."""
    es_inicial = estado == estado_inicial
    es_final = estado in estados_finales
    if es_inicial and es_final:
        return "<->"
    if es_inicial:
        return "->"
    if es_final:
        return "<-"
    return ""


def imprimir_afd(estados_afd, delta_afd, alfabeto, estado_inicial, estados_finales):
    ancho = max(len(formato_conjunto(A)) for A in estados_afd)
    encabezado = [" " * 3, " " * ancho] + [f"{simbolo:<{ancho}}" for simbolo in alfabeto]
    print(" ".join(encabezado).rstrip())
    for estado in estados_afd:
        columnas = [f"{marca_fila(estado, estado_inicial, estados_finales):<3}",
                    f"{formato_conjunto(estado):<{ancho}}"]
        for simbolo in alfabeto:
            columnas.append(f"{formato_conjunto(delta_afd[(estado, simbolo)]):<{ancho}}")
        print(" ".join(columnas).rstrip())


# main

def resolver_caso(lineas):
    estados_iniciales, alfabeto, finales_afn, delta = leer_caso(lineas)
    estados_afd, delta_afd = construccion_subconjuntos(estados_iniciales, alfabeto, delta)
    finales = finales_del_afd(estados_afd, finales_afn)
    imprimir_afd(estados_afd, delta_afd, alfabeto, estados_iniciales, finales)


def main():
    todas_las_lineas = [linea.strip() for linea in sys.stdin if linea.strip()]
    lineas = iter(todas_las_lineas)
    cantidad_casos = int(next(lineas))
    for _ in range(cantidad_casos):
        resolver_caso(lineas)


if __name__ == "__main__":
    main()