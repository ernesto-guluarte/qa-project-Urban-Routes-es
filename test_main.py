import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    #LOCALIZADORES
    #paso 1
    LOCATOR_CAMPO_DESDE = (By.ID, 'from')
    LOCATOR_CAMPO_HASTA = (By.ID, 'to')
    LOCATOR_BOTON_PEDIR_TAXI = (By.XPATH, "//div[ @class ='results-container'] // button[@ class ='button round']")
    #paso 2
    LOCATOR_BOTON_TARIFA_COMFORT = (By.XPATH,"//div[contains(@class, 'tcard') and .//div[@class='tcard-title' and text()='Comfort']]")
    LOCATOR_BOTON_RESERVAR = (By.CLASS_NAME, 'smart-button')
    #paso 3
    LOCATOR_BOTON_TELEFONO = (By.CLASS_NAME, 'np-text')
    LOCATOR_CAMPO_TELEFONO = (By.ID, 'phone')
    LOCATOR_BOTON_SIGUIENTE_TELEFONO = (By.XPATH, "//div[@class='modal']//button[@type='submit' and text()='Siguiente']")
    LOCATOR_CAMPO_CODIGO_SMS = (By.XPATH, "//div[@class='np-input']//input[@id='code']")
    LOCATOR_BOTON_CONFIRMAR_CODIGO_SMS = (By.XPATH, "//div[@class='modal']//button[@type='submit' and text()='Confirmar']")
    #paso 4
    LOCATOR_BOTON_METODO_DE_PAGO = (By.XPATH, "//div[@class='pp-value-text']")
    LOCATOR_BOTON_AGREGAR_TARJETA = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    LOCATOR_CAMPO_NUMERO_DE_TARJETA = (By.ID, 'number')
    LOCATOR_CAMPO_CODIGO_DE_TARJETA = (By.XPATH, "//div[@class='card-code']/div/input[@id='code']")
    LOCATOR_BOTON_MODAL_AGREGAR_TARJETA = (By.XPATH, "//div[@class='pp-buttons']//button[@type='submit' and text()='Agregar']")
    LOCATOR_BOTON_MODAL_CERRAR_METODO_DE_PAGO = (By.XPATH, "//div[@class='head' and text()='Método de pago']/preceding-sibling::button[@class='close-button section-close']")
    #paso 5
    LOCATOR_CAMPO_MENSAJE_PARA_EL_CONDUCTOR = (By.ID, 'comment')
    #paso 6
    LOCATOR_SWITCH_MANTA_PANUELOS = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']")
    LOCATOR_CHECKBOX_MANTA_PANUELOS = (By.XPATH,"//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//input[@type='checkbox']")
    #paso 7
    LOCATOR_BOTON_CONTADOR_MAS_HELADO = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div//div[@class='counter-plus']")
    # paso 7 (Valor del contador de helado)
    LOCATOR_VALOR_CONTADOR_HELADO = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div//div[@class='counter-value']")
    #paso 8
    LOCATOR_BOTON_FINALIZAR_PEDIDO = (By.XPATH,"//button[@class='smart-button' and ./span[text()='Pedir un taxi']]")
    LOCATOR_TITULO_DE_LA_ORDEN = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(driver, 10)

    # METODOS AUXILARES PARA ESPERA DE ELEMENTOS
    def wait_for_element(self, locator):
        return self._wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self._wait.until(EC.element_to_be_clickable(locator))

    def wait_for_attribute(self, locator, attribute, value):
        try:
            self._wait.until(EC.text_to_be_present_in_element_attribute(locator, attribute, value))
            return True
        except TimeoutException:
            return False

    def wait_for_text(self, locator, text):
        try:
            self._wait.until(EC.text_to_be_present_in_element(locator, text))
            return True
        except TimeoutException:
            return False

    # METODOS AUXILARES PARA SET Y GET
    def set_elemento_texto(self, valor, localizador):
        elemento = self.wait_for_clickable(localizador)
        elemento.send_keys(valor)
        return elemento
    def set_elemento_contador(self, valor, localizador):
        boton_mas = self.wait_for_clickable(localizador)
        for _ in range(valor):
            boton_mas.click()
    def get_elemento(self, localizador):
        elemento = self.wait_for_element(localizador)
        return elemento

    # METODOS AUXILIARES PARA CLICKS Y VALORES DE SELECCION
    def elemento_click(self, localizador):
        elemento = self.wait_for_clickable(localizador)
        elemento.click()
    def elemento_attributo(self, locator, attribute, valor):
        elemento = self.wait_for_attribute(locator, attribute, valor)
        return elemento

    # METODOS PARA INTERACTURAR CON LOS ELEMENTOS DE LA PAGINA
    # direccion desde
    def set_desde(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_DESDE)
    def get_desde(self):
        return self.get_elemento(self.LOCATOR_CAMPO_DESDE).get_property('value')
    # direccion hasta
    def set_hasta(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_HASTA)
    def get_hasta(self):
        return self.get_elemento(self.LOCATOR_CAMPO_HASTA).get_property('value')
    # telefono
    def set_telefono(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_TELEFONO)
    def get_telefono(self):
        return self.get_elemento(self.LOCATOR_BOTON_TELEFONO).text
    # codigo sms
    def set_codigo_sms(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_CODIGO_SMS)
    # numero de tarjeta
    def set_numero_de_tajeta(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_NUMERO_DE_TARJETA)
    # metodo de pago
    def get_metodo_de_pago(self):
        return self.get_elemento(self.LOCATOR_BOTON_METODO_DE_PAGO).text
    # codigo de tarjeta
    def set_codigo_de_tajeta(self, valor):
        campo_codigo_de_tarjeta = self.set_elemento_texto(valor, self.LOCATOR_CAMPO_CODIGO_DE_TARJETA)
        # instruccion de tabulacion
        campo_codigo_de_tarjeta.send_keys(Keys.TAB)  # Simula presionar la tecla Tab para quitar el foco
    # mensaje para el conductor
    def set_mensaje_para_el_conductor(self, valor):
        self.set_elemento_texto(valor, self.LOCATOR_CAMPO_MENSAJE_PARA_EL_CONDUCTOR)
    def get_mensaje_para_el_conductor(self):
        return self.get_elemento(self.LOCATOR_CAMPO_MENSAJE_PARA_EL_CONDUCTOR).get_property('value')
    # titulo de la orden
    def get_titulo_de_la_orden(self):
        return self.get_elemento(self.LOCATOR_TITULO_DE_LA_ORDEN).text

    #INTERACCION CON ELEMENTOS CLICKEABLES
    #pedir un taxi
    def pedir_un_taxi_click(self):
        self.elemento_click(self.LOCATOR_BOTON_PEDIR_TAXI)
    #tarifa comfort
    def tarifa_comfort_click(self):
        self.elemento_click(self.LOCATOR_BOTON_TARIFA_COMFORT)
    def tarifa_comfort_seleccionada(self):
        return self.elemento_attributo(self.LOCATOR_BOTON_TARIFA_COMFORT, 'class', 'active')
    #reservar
    def reservar_click(self):
        self.elemento_click(self.LOCATOR_BOTON_RESERVAR)
    #telefono
    def boton_telefono_click(self):
        self.elemento_click(self.LOCATOR_BOTON_TELEFONO)
    def boton_siguiente_modal_telefono_click(self):
        self.elemento_click(self.LOCATOR_BOTON_SIGUIENTE_TELEFONO)
    def boton_confirmar_modal_codigo_sms_click(self):
        self.elemento_click(self.LOCATOR_BOTON_CONFIRMAR_CODIGO_SMS)
    #metodo de pago
    def boton_metodo_de_pago_click(self):
        self.elemento_click(self.LOCATOR_BOTON_METODO_DE_PAGO)
    def boton_agregar_tarjeta_click(self):
        self.elemento_click(self.LOCATOR_BOTON_AGREGAR_TARJETA)
    def boton_modal_agregar_tarjeta_click(self):
        self.elemento_click(self.LOCATOR_BOTON_MODAL_AGREGAR_TARJETA)
    def boton_modal_cerrar_metodo_de_pago_click(self):
        self.elemento_click(self.LOCATOR_BOTON_MODAL_CERRAR_METODO_DE_PAGO)
    #manta y pañuelos
    def switch_manta_panuelos_click(self):
        self.elemento_click(self.LOCATOR_SWITCH_MANTA_PANUELOS)
    def manta_panuelos_seleccionada(self):
        return self.get_elemento(self.LOCATOR_CHECKBOX_MANTA_PANUELOS).is_selected()
    #helados
    def boton_contador_mas_helado_click(self, cantidad):
        self.set_elemento_contador(cantidad, self.LOCATOR_BOTON_CONTADOR_MAS_HELADO)
    def get_valor_contador_helado(self):
        # Es crucial convertir el texto (string) a un entero para la aserción con '2'
        return int(self.get_elemento(self.LOCATOR_VALOR_CONTADOR_HELADO).text)
    #boton para pedir el taxi
    def boton_finalizar_pedido_click(self):
        self.elemento_click(self.LOCATOR_BOTON_FINALIZAR_PEDIDO)

    # METODOS PARA VALIDAR CAMBIOS EN LOS TITULOS
    def esperar_orden_asignada(self, texto):
        long_wait = WebDriverWait(self.driver, 60)
        try:
            long_wait.until_not(
                EC.text_to_be_present_in_element(self.LOCATOR_TITULO_DE_LA_ORDEN, texto)
            )
            return True
        except TimeoutException:
            return False

    # METODOS PARA AGRUPAR INSTRUCCIONES
    # Introducir from y to, de la ruta
    def set_route(self, address_from, address_to):
        self.set_desde(address_from)
        self.set_hasta(address_to)
    #pasos para introducir telefono
    def introducir_telefono(self, telefono):
        self.boton_telefono_click()
        self.set_telefono(telefono)
        self.boton_siguiente_modal_telefono_click()
        self.introducir_codigo_sms()
        self.boton_confirmar_modal_codigo_sms_click()
    def introducir_tarjeta(self, numero_tarjeta, codigo_tarjeta):
        self.boton_metodo_de_pago_click()
        self.boton_agregar_tarjeta_click()
        self.set_numero_de_tajeta(numero_tarjeta)
        self.set_codigo_de_tajeta(codigo_tarjeta)
        self.boton_modal_agregar_tarjeta_click()
        self.boton_modal_cerrar_metodo_de_pago_click()
    def introducir_codigo_sms(self):
        codigo_sms = retrieve_phone_code(self.driver)
        self.set_codigo_sms(codigo_sms)

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        logging_prefs = {'performance': 'ALL'}
        options.set_capability("goog:loggingPrefs", logging_prefs)

        # Forzar el idioma/configuración regional (el idioma principal del navegador)
        options.add_argument("--lang=es-419")  # 'es-419' es español de Latinoamérica, más robusto.
        # Forzar la lista de idiomas aceptados (lo que el navegador le dice al servidor que acepta)
        options.add_argument("--accept-lang=es-419,es")

        # Esto le dice a Chrome que no se cierre cuando el proceso de Python termine.
        # Se agrego para seguir haciendo pruebas en el navegador
        # Se eliminara en la version final del proyecto
        #options.add_experimental_option("detach", True)

        # Inicializar el driver con el objeto options
        cls.driver = webdriver.Chrome(options=options)
        # Establece una espera implícita de 10 segundos
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        #obtener valores de prueba
        desde = data.address_from
        hasta = data.address_to
        telefono = data.phone_number
        numero_tarjeta = data.card_number
        codigo_tarjeta = data.card_code
        mensaje_conductor = data.message_for_driver
        helados = data.ice_cream
        buscar_automovil = data.buscar_automovil

        # crear el driver para interactuar con la pagina
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1. Introducir Direcciones
        routes_page.set_route(desde, hasta)
        routes_page.pedir_un_taxi_click()
        # 2. Seleccionar la tarifa comfort
        routes_page.tarifa_comfort_click()
        # 3. Introducir el numero de telefono
        routes_page.introducir_telefono(telefono)
        # 4. Introducir numero de tarjeta y codigo de tarjeta
        routes_page.introducir_tarjeta(numero_tarjeta, codigo_tarjeta)
        # 5. Introducir un mensaje para el conductor
        routes_page.set_mensaje_para_el_conductor(mensaje_conductor)
        # 6. Activar el requisito "Manta y pañuelos"
        routes_page.switch_manta_panuelos_click()
        # 7. Pedir 2 helados
        routes_page.boton_contador_mas_helado_click(helados)
        # 8. Finalizar pedido
        routes_page.boton_finalizar_pedido_click()

        # paso 1
        assert routes_page.get_desde() == desde, routes_page.get_desde() + ", " + desde
        assert routes_page.get_hasta() == hasta, routes_page.get_hasta() + ", " + hasta
        # paso 2
        assert routes_page.tarifa_comfort_seleccionada() == True, routes_page.tarifa_comfort_seleccionada()
        # paso 3
        assert routes_page.get_telefono() == telefono, routes_page.get_telefono() + ", " + telefono
        # paso 4
        assert routes_page.get_metodo_de_pago() == "Tarjeta", routes_page.get_metodo_de_pago() + ", " + "Tarjeta"
        # paso 5
        assert routes_page.get_mensaje_para_el_conductor() == mensaje_conductor, routes_page.get_mensaje_para_el_conductor() + ", " + mensaje_conductor
        # paso 6
        assert routes_page.manta_panuelos_seleccionada() == True, routes_page.manta_panuelos_seleccionada()
        # paso 7
        assert routes_page.get_valor_contador_helado() == helados, routes_page.get_valor_contador_helado() + ", " + helados
        # paso 8
        assert routes_page.get_titulo_de_la_orden() == buscar_automovil, routes_page.get_titulo_de_la_orden()
        # paso 9
        assert routes_page.esperar_orden_asignada(buscar_automovil)  == True, routes_page.esperar_orden_asignada(buscar_automovil)


    @classmethod
    def teardown_class(cls):
        time.sleep(10)
        cls.driver.quit()
