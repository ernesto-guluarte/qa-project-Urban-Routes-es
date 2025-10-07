import json
import time
from selenium.common.exceptions import WebDriverException


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    code = None
    for i in range(10):
        try:
            # Recuperar logs de red
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]

            # Procesar el log más reciente
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                # Extraer dígitos del cuerpo de la respuesta
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            # Esperar si hay un problema con el driver
            time.sleep(1)
            continue

        # Si se encuentra el código, devolverlo
        if code:
            return code

        # Si no se encuentra después de todas las iteraciones, lanzar excepción
        if not code and i == 9:  # Solo lanzar al final del ciclo
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        time.sleep(1)  # Esperar antes de la siguiente revisión de logs
    return code