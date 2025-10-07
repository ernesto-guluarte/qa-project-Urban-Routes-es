from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from helpers import retrieve_phone_code


class UrbanRoutesPage:
    # LOCALIZADORES
    # paso 1
    LOCATOR_CAMPO_DESDE = (By.ID, 'from')
    LOCATOR_CAMPO_HASTA = (By.ID, 'to')
    LOCATOR_BOTON_PEDIR_TAXI = (By.XPATH, "//div[ @class ='results-container'] // button[@ class ='button round']")
    # paso 2
    LOCATOR_BOTON_TARIFA_COMFORT = (By.XPATH,
                                    "//div[contains(@class, 'tcard') and .//div[@class='tcard-title' and text()='Comfort']]")
    LOCATOR_BOTON_RESERVAR = (By.CLASS_NAME, 'smart-button')
    # paso 3
    LOCATOR_BOTON_TELEFONO = (By.CLASS_NAME, 'np-text')
    LOCATOR_CAMPO_TELEFONO = (By.ID, 'phone')
    LOCATOR_BOTON_SIGUIENTE_TELEFONO = (By.XPATH,
                                        "//div[@class='modal']//button[@type='submit' and text()='Siguiente']")
    LOCATOR_CAMPO_CODIGO_SMS = (By.XPATH, "//div[@class='np-input']//input[@id='code']")
    LOCATOR_BOTON_CONFIRMAR_CODIGO_SMS = (By.XPATH,
                                          "//div[@class='modal']//button[@type='submit' and text()='Confirmar']")
    # paso 4
    LOCATOR_BOTON_METODO_DE_PAGO = (By.XPATH, "//div[@class='pp-value-text']")
    LOCATOR_BOTON_AGREGAR_TARJETA = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    LOCATOR_CAMPO_NUMERO_DE_TARJETA = (By.ID, 'number')
    LOCATOR_CAMPO_CODIGO_DE_TARJETA = (By.XPATH, "//div[@class='card-code']/div/input[@id='code']")
    LOCATOR_BOTON_MODAL_AGREGAR_TARJETA = (By.XPATH,
                                           "//div[@class='pp-buttons']//button[@type='submit' and text()='Agregar']")
    LOCATOR_BOTON_MODAL_CERRAR_METODO_DE_PAGO = (By.XPATH,
                                                 "//div[@class='head' and text()='Método de pago']/preceding-sibling::button[@class='close-button section-close']")
    # paso 5
    LOCATOR_CAMPO_MENSAJE_PARA_EL_CONDUCTOR = (By.ID, 'comment')
    # paso 6
    LOCATOR_SWITCH_MANTA_PANUELOS = (By.XPATH,
                                     "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']")
    LOCATOR_CHECKBOX_MANTA_PANUELOS = (By.XPATH,
                                       "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//input[@type='checkbox']")
    # paso 7
    LOCATOR_BOTON_CONTADOR_MAS_HELADO = (By.XPATH,
                                         "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div//div[@class='counter-plus']")
    # paso 7 (Valor del contador de helado)
    LOCATOR_VALOR_CONTADOR_HELADO = (By.XPATH,
                                     "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div//div[@class='counter-value']")
    # paso 8
    LOCATOR_BOTON_FINALIZAR_PEDIDO = (By.XPATH, "//button[@class='smart-button' and ./span[text()='Pedir un taxi']]")
    LOCATOR_TITULO_DE_LA_ORDEN = (By.CLASS_NAME, 'order-header-title')

    # paso 9
    LOCATOR_MATRICULA_CONDUCTOR = (By.CSS_SELECTOR, ".order-number .number")

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

    # METODOS PARA INTERACTUAR CON LOS ELEMENTOS DE LA PAGINA
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

    # # informacion del conductor (Opcional, para el bonus)
    # def get_info_conductor(self):
    #     return self.get_elemento(self.LOCATOR_INFO_CONDUCTOR).text

    # INTERACCION CON ELEMENTOS CLICKEABLES
    # pedir un taxi
    def pedir_un_taxi_click(self):
        self.elemento_click(self.LOCATOR_BOTON_PEDIR_TAXI)

    # tarifa comfort
    def tarifa_comfort_click(self):
        self.elemento_click(self.LOCATOR_BOTON_TARIFA_COMFORT)

    def tarifa_comfort_seleccionada(self):
        return self.elemento_attributo(self.LOCATOR_BOTON_TARIFA_COMFORT, 'class', 'active')

    # reservar
    def reservar_click(self):
        self.elemento_click(self.LOCATOR_BOTON_RESERVAR)

    # telefono
    def boton_telefono_click(self):
        self.elemento_click(self.LOCATOR_BOTON_TELEFONO)

    def boton_siguiente_modal_telefono_click(self):
        self.elemento_click(self.LOCATOR_BOTON_SIGUIENTE_TELEFONO)

    def boton_confirmar_modal_codigo_sms_click(self):
        self.elemento_click(self.LOCATOR_BOTON_CONFIRMAR_CODIGO_SMS)

    # metodo de pago
    def boton_metodo_de_pago_click(self):
        self.elemento_click(self.LOCATOR_BOTON_METODO_DE_PAGO)

    def boton_agregar_tarjeta_click(self):
        self.elemento_click(self.LOCATOR_BOTON_AGREGAR_TARJETA)

    def boton_modal_agregar_tarjeta_click(self):
        self.elemento_click(self.LOCATOR_BOTON_MODAL_AGREGAR_TARJETA)

    def boton_modal_cerrar_metodo_de_pago_click(self):
        self.elemento_click(self.LOCATOR_BOTON_MODAL_CERRAR_METODO_DE_PAGO)

    # manta y pañuelos
    def switch_manta_panuelos_click(self):
        self.elemento_click(self.LOCATOR_SWITCH_MANTA_PANUELOS)

    def manta_panuelos_seleccionada(self):
        return self.get_elemento(self.LOCATOR_CHECKBOX_MANTA_PANUELOS).is_selected()

    # helados
    def boton_contador_mas_helado_click(self, cantidad):
        self.set_elemento_contador(cantidad, self.LOCATOR_BOTON_CONTADOR_MAS_HELADO)

    def get_valor_contador_helado(self):
        return int(self.get_elemento(self.LOCATOR_VALOR_CONTADOR_HELADO).text)

    # boton para pedir el taxi
    def boton_finalizar_pedido_click(self):
        self.elemento_click(self.LOCATOR_BOTON_FINALIZAR_PEDIDO)

    # METODOS PARA VALIDAR CAMBIOS EN EL MODAL DE ORDEN DE TAXY
    def esperar_orden_asignada(self, texto):
        long_wait = WebDriverWait(self.driver, 60)
        try:
            long_wait.until_not(
                EC.text_to_be_present_in_element(self.LOCATOR_TITULO_DE_LA_ORDEN, texto)
            )
            return True
        except TimeoutException:
            return False

    # INFORMACION DEL CONDUCTOR
    def verificar_informacion_del_conductor(self):
        try:
            # 1. Esperar la visibilidad y obtener el elemento
            elemento = self._wait.until(EC.visibility_of_element_located(self.LOCATOR_MATRICULA_CONDUCTOR))
            matricula_texto = elemento.text
        except TimeoutException:
            return False
        # validar que la matricula no sea vacia
        if len(matricula_texto.strip()) > 0:
            return True
        else:
            return False

    # METODOS PARA AGRUPAR INSTRUCCIONES
    # Introducir from y to, de la ruta
    def set_route(self, address_from, address_to):
        self.set_desde(address_from)
        self.set_hasta(address_to)

    # pasos para introducir telefono
    def introducir_telefono(self, telefono):
        self.boton_telefono_click()
        self.set_telefono(telefono)
        self.boton_siguiente_modal_telefono_click()
        # **Aquí usamos la función de helpers.py**
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