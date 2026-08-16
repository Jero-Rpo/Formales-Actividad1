import sys

def leer_entrada():
    datos = sys.stdin.read().split('\n')
    indice = 0

    def siguiente_linea():
        nonlocal indice
        linea = datos[indice]
        indice += 1
        return linea

    casos = []
    cantidad_casos = int(siguiente_linea().strip())
    for _ in range(cantidad_casos):
        num_estados = int(siguiente_linea().strip())
        alfabeto = siguiente_linea().split()
        estados_finales = list(map(int, siguiente_linea().split()))

        tabla_transiciones = [None] * num_estados
        for _ in range(num_estados):
            fila = list(map(int, siguiente_linea().split()))
            id_estado, transiciones = fila[0], fila[1:]
            tabla_transiciones[id_estado] = transiciones

        casos.append((num_estados, alfabeto, estados_finales, tabla_transiciones))
    return casos


def encontrar_pares_equivalentes(num_estados, alfabeto, estados_finales, tabla_transiciones):
    conjunto_finales = set(estados_finales)
    tam_alfabeto = len(alfabeto)

    # marcados[p][q] (con p < q) == True significa que p y q son DISTINGUIBLES (no equivalentes).
  
    marcados = [[False] * num_estados for _ in range(num_estados)]

    # Paso 1: marcar los pares que difieren en si son finales o no
    for p in range(num_estados):
        for q in range(p + 1, num_estados):
            if (p in conjunto_finales) != (q in conjunto_finales):
                marcados[p][q] = True

    # Paso 2: propagar las marcas hasta llegar a un punto fijo
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for p in range(num_estados):
            for q in range(p + 1, num_estados):
                if marcados[p][q]:
                    continue
                for a in range(tam_alfabeto):
                    destino_p = tabla_transiciones[p][a]
                    destino_q = tabla_transiciones[q][a]
                    if destino_p == destino_q:
                        continue
                    menor, mayor = (destino_p, destino_q) if destino_p < destino_q else (destino_q, destino_p)
                    if marcados[menor][mayor]:
                        marcados[p][q] = True
                        hubo_cambio = True
                        break

    # Paso 3: los pares que quedaron sin marcar son equivalentes
    pares_equivalentes = []
    for p in range(num_estados):
        for q in range(p + 1, num_estados):
            if not marcados[p][q]:
                pares_equivalentes.append((p, q))

    return pares_equivalentes


def formatear_salida(casos):
    lineas_salida = []
    for (num_estados, alfabeto, estados_finales, tabla_transiciones) in casos:
        pares = encontrar_pares_equivalentes(num_estados, alfabeto, estados_finales, tabla_transiciones)
        lineas_salida.append(' '.join(f'({p}, {q})' for p, q in pares))
    return '\n'.join(lineas_salida)


def principal():
    casos = leer_entrada()
    print(formatear_salida(casos))


if __name__ == '__main__':
    principal()