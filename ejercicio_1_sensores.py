# EJERCICIO 1 - Sanitizacion y analisis estadistico de sensores

def limpiar_registro_sensor(registro_raw):
    """
    Recibe un diccionario con datos crudos y devuelve
    un nuevo diccionario con los datos normalizados.
    """
    sensor_id = registro_raw.get("sensor_id", "").strip()

    # Limpiamos los espacios y quitamos la unidad de temperatura.
    temperatura_texto = registro_raw.get("temperatura", "0")
    temperatura_texto = temperatura_texto.strip()
    temperatura_texto = temperatura_texto.replace("°", "")
    temperatura_texto = temperatura_texto.replace("C", "")
    temperatura = float(temperatura_texto)

    # Si no hay ubicacion o esta vacia, usamos un valor por defecto.
    ubicacion = registro_raw.get("ubicacion", "").strip()
    if ubicacion == "":
        ubicacion = "Ubicacion desconocida"

    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

    return registro_limpio


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Devuelve una tupla con los IDs de sensores en alerta
    y el promedio general de temperatura.
    """

    # Filtramos los sensores que superan el umbral.
    sensores_alerta = list(filter(
        lambda sensor: sensor["temperatura"] > umbral_temperatura,
        lista_sensores_limpios
    ))

    # Extraemos solamente los identificadores.
    lista_sensores_alerta = list(map(
        lambda sensor: sensor["sensor_id"],
        sensores_alerta
    ))

    # Calculamos el promedio de todas las temperaturas.
    if len(lista_sensores_limpios) > 0:
        suma_temperaturas = 0
        for sensor in lista_sensores_limpios:
            suma_temperaturas += sensor["temperatura"]

        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0.0

    return (lista_sensores_alerta, promedio_temperatura)


# BLOQUE PRINCIPAL DE EJECUCION
if __name__ == "__main__":

    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": " SENSOR-002 ", "temperatura": "31.2C", "ubicacion": "Planta Sur"},
        {"sensor_id": " SENSOR-003 ", "temperatura": "28.0C"},
        {"sensor_id": " SENSOR-004 ", "temperatura": "22.5C", "ubicacion": "Planta Este"}
    ]

    # Limpiamos todos los registros crudos.
    sensores_limpios = []
    for registro in registros_crudos:
        sensor_limpio = limpiar_registro_sensor(registro)
        sensores_limpios.append(sensor_limpio)

    # Generamos el resumen.
    umbral = 25.0
    resultado = generar_resumen_sensores(sensores_limpios, umbral)

    lista_sensores_alerta = resultado[0]
    promedio_temperatura = resultado[1]

    print("===== REPORTE DE SENSORES ECOTECH =====")
    print(f"Sensores que superan los {umbral} grados: {lista_sensores_alerta}")
    print(f"Promedio general de temperatura: {promedio_temperatura:.2f} C