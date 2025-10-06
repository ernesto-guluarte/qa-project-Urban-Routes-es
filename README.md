# QA Project: Automatización de Rutas Urbanas

##  Descripción del Proyecto
Este proyecto contiene pruebas automatizadas para validar el flujo completo de solicitud de un taxi en la aplicación web Urban Routes. El objetivo es asegurar la funcionalidad desde la selección de rutas y tarifas hasta la confirmación de la orden con métodos de pago y peticiones adicionales.

##  Tecnologías y Técnicas Utilizadas

| Categoría | Elementos |
| :--- | :--- |
| **Lenguaje** | Python |
| **Framework de Pruebas** | pytest |
| **Automatización Web** | Selenium WebDriver |
| **Patrón de Diseño** | Page Object Model (POM) |
| **Técnicas Clave** | Esperas Explícitas (`WebDriverWait` y `expected_conditions`), Manejo de asincronía (`until_not` para cambio de estado). 

##  Instrucciones para Ejecutar las Pruebas

### Prerrequisitos
1.  Tener instalado Python (versión 3.x recomendada).
2Tener instalado el navegador **Google Chrome**.

### 1. Clonar el Repositorio
```bash
git clone git@github.com:username/qa-project-Urban-Routes-es.git
```

### 2. Instalar dependencias
```bash
pip install selenium pytest
```

### 3. Ejecutar pytest desde la raíz del proyecto
```bash
pytest
```