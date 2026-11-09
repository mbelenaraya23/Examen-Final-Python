# EJERCICIO 2 - Modelo de productos, excepciones y persistencia

import json


# Excepcion personalizada para controlar el stock.
class StockInvalidoError(Exception):
    pass


# Clase base de los dispositivos ecologicos.
class DispositivoEcológico:

    def __init__(self, modelo, precio, stock):
        self.modelo = modelo
        self.precio = precio
        self.set_stock(stock)

    # Getter: permite consultar el stock.
    def get_stock(self):
        return self.__stock

    # Setter: permite modificar el stock aplicando una validacion.
    def set_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise StockInvalidoError("El stock no puede ser negativo.")
        self.__stock = nuevo_stock

    def obtener_ficha_tecnica(self):
        return f"Modelo: {self.modelo} | Precio: ${self.precio} | Stock: {self.get_stock()}"

    # Convierte el objeto en un diccionario que se puede guardar en JSON.
    def a_diccionario(self):
        return {
            "tipo": "DispositivoEcologico",
            "modelo": self.modelo,
            "precio": self.precio,
            "stock": self.get_stock()
        }


# Clase hija que hereda de DispositivoEcológico.
class PanelSolar(DispositivoEcológico):

    def __init__(self, modelo, precio, stock, eficiencia_watts):
        super().__init__(modelo, precio, stock)
        self.eficiencia_watts = eficiencia_watts

    # Polimorfismo: personalizamos la ficha tecnica.
    def obtener_ficha_tecnica(self):
        ficha_base = super().obtener_ficha_tecnica()
        return f"{ficha_base} | Potencia: {self.eficiencia_watts} W"

    # Incluimos tambien el atributo especifico en el diccionario.
    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["tipo"] = "PanelSolar"
        datos["eficiencia_watts"] = self.eficiencia_watts
        return datos


# Clase encargada de guardar el catalogo.
class GestorInventario:

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        # Convertimos cada objeto a diccionario antes de usar json.dump().
        catalogo = []
        for dispositivo in lista_dispositivos:
            catalogo.append(dispositivo.a_diccionario())

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, indent=4, ensure_ascii=False)

        print(f"Catalogo guardado correctamente en {ruta_archivo}")


# BLOQUE PRINCIPAL DE PRUEBA
if __name__ == "__main__":

    # Creamos productos validos.
    dispositivo = DispositivoEcológico("Termostato Eco", 350.0, 8)
    panel = PanelSolar("SolarMax-500", 1200.0, 10, 500)

    print("===== FICHAS TECNICAS =====")
    print(dispositivo.obtener_ficha_tecnica())
    print(panel.obtener_ficha_tecnica())

    # Intentamos asignar un stock negativo y capturamos el error.
    try:
        panel.set_stock(-5)
    except StockInvalidoError as error:
        print(f"[ERROR CONTROLADO]: {error}")

    # Exportamos solamente los productos validos.
    productos_validos = [dispositivo, panel]
    gestor = GestorInventario()
    gestor.guardar_catalogo_json(productos_validos, "catalogo_ecotech.json")
