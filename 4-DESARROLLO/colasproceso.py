from collections import deque

# Crear una cola con deque
cola_procesos = deque()

# Agregar procesos a la cola
cola_procesos.append("Proceso 1")
cola_procesos.append("Proceso 2")
cola_procesos.append("Proceso 3")

# Procesar los elementos de la cola
while cola_procesos:
    proceso_actual = cola_procesos.popleft()  # Extraer el primer elemento
    print(f"Procesando: {proceso_actual}")
