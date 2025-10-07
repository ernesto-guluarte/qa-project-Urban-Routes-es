import data
from selenium import webdriver
from pages import UrbanRoutesPage
import time

class TestUrbanRoutes:
    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        logging_prefs = {'performance': 'ALL'}
        options.set_capability("goog:loggingPrefs", logging_prefs)
        options.add_argument("--lang=es-419")
        options.add_argument("--accept-lang=es-419,es")
        #options.add_experimental_option("detach", True)

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

        # crear el driver para interactuar con la pagina
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)



    # --- 9 Pruebas  ---

    def test_1_definir_ruta(self):
        """Paso 1: Establecer la ruta y verificar que se hayan introducido correctamente."""
        desde = data.address_from
        hasta = data.address_to
        self.routes_page.set_route(desde, hasta)
        self.routes_page.pedir_un_taxi_click()

        assert self.routes_page.get_desde() == desde
        assert self.routes_page.get_hasta() == hasta

    def test_2_seleccionar_tarifa_comfort(self):
        """Paso 2: Seleccionar la tarifa Comfort y verificar que esté activa."""
        self.routes_page.tarifa_comfort_click()
        assert self.routes_page.tarifa_comfort_seleccionada() == True

    def test_3_agregar_numero_de_telefono(self):
        """Paso 3: Introducir el número de teléfono y verificar que el texto del botón de teléfono cambie."""
        self.routes_page.introducir_telefono(data.phone_number)
        assert self.routes_page.get_telefono() == data.phone_number

    def test_4_agregar_tarjeta(self):
        """Paso 4: Añadir una tarjeta de pago y verificar que el método de pago sea 'Tarjeta'."""
        self.routes_page.introducir_tarjeta(data.card_number, data.card_code)
        assert self.routes_page.get_metodo_de_pago() == "Tarjeta"

    def test_5_agregar_mensaje_para_el_conductor(self):
        """Paso 5: Añadir un mensaje para el conductor y verificar que se haya introducido."""
        self.routes_page.set_mensaje_para_el_conductor(data.message_for_driver)
        assert self.routes_page.get_mensaje_para_el_conductor() == data.message_for_driver

    def test_6_agregar_manta_y_panuelos(self):
        """Paso 6: Activar la opción 'Manta y pañuelos' y verificar que el switch esté marcado."""
        self.routes_page.switch_manta_panuelos_click()
        assert self.routes_page.manta_panuelos_seleccionada() == True

    def test_7_agregar_helados(self):
        """Paso 7: Añadir 2 helados y verificar que el contador muestre el valor correcto."""
        self.routes_page.boton_contador_mas_helado_click(data.ice_cream)
        assert self.routes_page.get_valor_contador_helado() == data.ice_cream

    def test_8_esperar_modal_buscando_automovil(self):
        """Paso 8: Finalizar el pedido y verificar que el título cambie a 'Buscando automóvil'."""
        self.routes_page.boton_finalizar_pedido_click()
        assert self.routes_page.get_titulo_de_la_orden() == data.buscar_automovil

    def test_9_esperar_modal_informacion_del_conductor(self):
        """Paso 9: Esperar hasta que se asigne un conductor y verificar que el título cambie de 'Buscando automóvil'
        y aparezca la matricula del vehiculo."""
        # Usamos una espera larga para este paso (60s en el Page Object)
        assert self.routes_page.esperar_orden_asignada(data.buscar_automovil) == True
        # Validamos la aparicion de la matricula en el modal
        assert self.routes_page.verificar_informacion_del_conductor() == True

    @classmethod
    def teardown_class(cls):
        time.sleep(10)
        cls.driver.quit()