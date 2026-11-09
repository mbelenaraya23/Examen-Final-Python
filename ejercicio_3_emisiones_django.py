# EJERCICIO 3 - Tests unitarios e integracion web

import unittest


# Funcion que calcula las emisiones de carbono.
def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    if consumo_kwh < 0:
        raise ValueError("El consumo energetico no puede ser negativo.")

    emisiones = consumo_kwh * factor_emision
    return emisiones


# Procesa los registros de consumo de las plantas.
def obtener_metricas_consumo(registros):
    total_emisiones = 0
    consumo_por_planta = {}

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]

        # Calculamos las emisiones de cada registro.
        emisiones = calcular_emisiones_carbono(consumo)
        total_emisiones += emisiones

        # Acumulamos el consumo cuando una planta aparece varias veces.
        if planta in consumo_por_planta:
            consumo_por_planta[planta] += consumo
        else:
            consumo_por_planta[planta] = consumo

    # Buscamos la planta que acumulo el mayor consumo.
    if len(consumo_por_planta) > 0:
        planta_mayor_consumo = max(
            consumo_por_planta,
            key=lambda nombre: consumo_por_planta[nombre]
        )
    else:
        planta_mayor_consumo = "Sin datos"

    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_por_planta": consumo_por_planta
    }


# Clase de pruebas unitarias.
class TestCalculoEmisiones(unittest.TestCase):

    def test_calculo_correcto(self):
        resultado = calcular_emisiones_carbono(100.0, 0.4)
        self.assertEqual(resultado, 40.0)

    def test_calculo_con_factor_por_defecto(self):
        resultado = calcular_emisiones_carbono(50.0)
        self.assertEqual(resultado, 20.0)

    def test_consumo_negativo_lanza_excepcion(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50.0)


# Vista de Django.
def vista_panel_sustentabilidad(request):
    # La importacion se realiza dentro de la funcion para que el resto
    # del archivo pueda probarse aunque Django no este instalado.
    from django.shortcuts import render

    registros = [
        {"planta": "Planta Norte", "consumo_kwh": 1200},
        {"planta": "Planta Sur", "consumo_kwh": 850},
        {"planta": "Planta Norte", "consumo_kwh": 1400}
    ]

    metricas = obtener_metricas_consumo(registros)

    contexto = {
        "total_emisiones": metricas["total_emisiones"],
        "planta_top": metricas["planta_mayor_consumo"]
    }

    return render(request, "sustentabilidad/panel.html", contexto)


# BLOQUE PRINCIPAL: ejecuta las pruebas unitarias.
if __name__ == "__main__":
    unittest.main()
