# 🚕 Automatización de la Solicitud de Viajes en Urban Routes

---

## 📝 Descripción del Proyecto

Este proyecto contiene un conjunto de **pruebas automatizadas** escritas en Python utilizando la librería **Selenium WebDriver** para simular y validar el proceso completo de solicitar un viaje en la aplicación web de Urban Routes.

Las pruebas cubren una secuencia de nueve acciones clave, desde la configuración inicial de la ruta hasta la asignación final de un conductor:

1.  **Definición de Ruta:** Establecer las direcciones de origen y destino.
2.  **Selección de Tarifa:** Elegir la tarifa "Comfort".
3.  **Autenticación:** Introducir y confirmar el número de teléfono con un código SMS simulado.
4.  **Método de Pago:** Agregar y seleccionar una tarjeta de crédito como método de pago.
5.  **Comentario al Conductor:** Incluir un mensaje especial para el conductor.
6.  **Opciones Adicionales:** Solicitar la opción "Manta y pañuelos".
7.  **Productos Adicionales:** Añadir 2 unidades de "Helado".
8.  **Finalización de Pedido:** Verificar la aparición del modal de "Buscando automóvil".
9.  **Asignación de Conductor:** Esperar y verificar que la información del conductor (matrícula del vehículo) aparezca en el modal.

---

## 🛠️ Tecnologías y Técnicas

| Categoría | Tecnología/Técnica | Descripción |
| :--- | :--- | :--- |
| **Lenguaje de Programación** | **Python** | Lenguaje principal utilizado para escribir los scripts de prueba. |
| **Framework de Pruebas** | **Pytest** | Utilizado para estructurar, organizar y ejecutar las pruebas automatizadas (clases y métodos con prefijo `test_`). |
| **Automatización Web** | **Selenium WebDriver** | Herramienta esencial para interactuar con el navegador web (Chrome) y simular las acciones del usuario. |
| **Patrón de Diseño** | **Page Object Model (POM)** | Implementado en el archivo `pages.py`. Este patrón separa la lógica de la prueba de los localizadores de la interfaz, mejorando la **reusabilidad** y **mantenibilidad** del código. |
| **Manejo de Localizadores** | **`By.ID`**, **`By.XPATH`**, **`By.CLASS_NAME`** | Diferentes estrategias de Selenium para localizar elementos en la página web. |
| **Técnicas de Espera** | **`WebDriverWait` y `expected_conditions` (EC)** | Utilizadas para asegurar que los elementos estén presentes, visibles o *clickables* antes de interactuar con ellos, haciendo las pruebas más **estables** y **fiables**. |
| **Simulación de Código SMS** | **`retrieve_phone_code` (CDP)** | Una función auxiliar que simula la recuperación del código de confirmación de teléfono interceptando los logs de red del navegador, lo cual es crucial para automatizar el paso de autenticación. |

---

## 🚀 Ejecución de las Pruebas

Sigue estos pasos para configurar y ejecutar las pruebas en tu entorno local:

### 1. Requisitos Previos

Asegúrate de tener instalado **Python** en tu sistema.

### 2. Instalación de Dependencias

Necesitarás instalar las librerías `selenium` y `pytest`. Abre tu terminal o símbolo del sistema y ejecuta:

```bash
pip install selenium pytest
```

### 3. Configuración del WebDriver

Las pruebas están configuradas para usar **Chrome**. Asegúrate de que el ejecutable de **ChromeDriver** sea accesible para Selenium. Normalmente, esto ya viene incluido o se maneja automáticamente con las versiones recientes de `selenium` y `Google Chrome`.

### 4. Estructura de Archivos

Asegúrate de que los siguientes archivos estén ubicados en el mismo directorio:

* `test_main.py`
* `pages.py`
* `data.py`
* `helpers.py`

### 5. Ejecutar las Pruebas

Para ejecutar el conjunto completo de pruebas, navega hasta el directorio que contiene los archivos en tu terminal y utiliza el comando `pytest`:

```bash
pytest