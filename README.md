# QA Automation Technical Test

En este repositorio presento el desarrollo y la ejecución de una suite de pruebas automatizadas E2E orientada a validar con rigor técnico los 5 casos de prueba requeridos sobre la plataforma [DemoQA](https://demoqa.com/). Diseñé la solución contenerizada con Docker Compose para garantizar reproducibilidad total e independencia del sistema operativo anfitrión.

Mi enfoque de testing no se limitó a automatizar clics o transiciones de pantalla: estructuré cada prueba para que verifique de forma fehaciente los cambios de estado, la integridad de los datos procesados y la respuesta del sistema tanto en flujos positivos como en validaciones de error.

---

## Approach

Para abordar esta prueba técnica definí las siguientes decisiones y buenas prácticas de ingeniería de calidad:

- **Comprensión previa del flujo y la aplicación:** Antes de escribir código, analicé el comportamiento dinámico de los componentes React de DemoQA (datepickers, selects compuestos, modales y tablas) para identificar selectores estables y evitar fragilidad en las pruebas.
- **Entorno aislado con Docker Compose:** Orquesté la suite con dos servicios: un contenedor con el runtime de pruebas (`app`) y un contenedor `selenium/standalone-chrome` que actúa como Selenium Grid. Configuré la suite para conectarse de manera predeterminada y transparente al servicio Chrome Standalone.
- **Patrón Page Object Model (POM):** Separé la lógica de negocio y las aserciones de la interacción con el DOM, ubicando los locators y métodos de acción dentro de `src/pages/` (`BasePage`, `PracticeFormPage`, `SelectMenuPage` y `WebTablesPage`).
- **Sincronización robusta con Explicit Waits:** Evité cualquier tipo de `sleep` arbitrario. Utilicé `WebDriverWait` y `expected_conditions` (visibilidad de elementos, estados interactuables y desaparición de transiciones asíncronas como `.modal-backdrop`) para garantizar estabilidad ante la latencia de red.
- **Gestión determinista de datos de prueba:** Implementé fábricas de datos en `src/utils/data_generator.py` para generar usuarios e información de formulario aleatoria pero válida, con soporte para reproducir ejecuciones idénticas mediante la variable `QA_SEED`.
- **Validación real de estados y no solo de acciones:** Me aseguré de que ninguna prueba se considere exitosa únicamente porque Selenium no arrojó excepción; cada caso verifica aserciones estrictas sobre los datos renderizados en tablas, títulos de confirmación y atributos de validación HTML5 (`validity.valid`).

---

## Test Cases

| # | Test Case | What I Validate | Status |
|---|-----------|-----------------|--------|
| 1 | Practice Form | Diligenciamiento completo de todos los campos con datos aleatorios (texto, radios, datepicker, subjects, hobbies, upload de archivo y dropdowns anidados de Estado/Ciudad) y validación exacta de cada dato en el modal de confirmación. | PASS |
| 2 | Web Tables - Create User | Registro de un nuevo usuario con datos dinámicos en la tabla web, verificando su persistencia y la coincidencia de cada celda (First Name, Last Name, Age, Email, Salary, Department). | PASS |
| 3 | Widgets / Select Menu | Selección y persistencia de valores en 5 tipos de menús desplegables: Select Value ("A root option"), Select One ("Ms."), Old Style Select ("Indigo"), Multiselect ("Blue", "Red") y Standard Multi Select ("Volvo", "Opel"). | PASS |
| 4 | Web Tables - CRUD Lifecycle | Ciclo de vida completo sobre un registro propio: creación con datos aleatorios, edición de campos clave (First Name y Department) y eliminación final, confirmando que la fila ya no existe en la tabla. | PASS |
| 5 | Web Tables - Form Validations | Rechazo de envío cuando los campos obligatorios están vacíos y cuando se ingresa un formato de email inválido, comprobando que el modal permanece abierto, que el navegador marca el campo con estado `:invalid` y que el registro no se inserta en la tabla. | PASS |

> **Criterio de PASS:** En esta suite, un caso se marca como **PASS** únicamente cuando la aplicación refleja de forma verificable el resultado esperado de negocio tras interactuar con la interfaz real.

---

## Requirements

Para ejecutar este proyecto se requiere únicamente:

- **Git**
- **Docker Engine** (v20.10+ recomendado)
- **Docker Compose** (v2.0+)

*Nota: No se requiere tener instalados Python, navegadores ni webdrivers localmente en la máquina anfitriona; todo el entorno corre dentro de los contenedores Docker.*

---

## Setup

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

2. **Entrar al directorio del proyecto:**
   ```bash
   cd qa-test
   ```

3. **Levantar los servicios con Docker Compose:**
   ```bash
   docker compose up -d --build
   ```

4. **Comprobar que los contenedores estén corriendo:**
   ```bash
   docker compose ps
   ```
   *Deberás observar los servicios `app` (`demo-test-automation-container`) y `selenium` (`qa-test-selenium-1`) con estado `Up`.*

5. **Verificar la disponibilidad de la aplicación bajo prueba:**
   ```bash
   curl -I https://demoqa.com/
   ```
   *Debe responder con `HTTP/1.1 200 OK`.*

---

## Running the Tests

Una vez levantado el entorno con Docker Compose, ejecuté y configuré los siguientes comandos:

### Ejecutar toda la suite de pruebas
Para correr los 5 casos de prueba completos:
```bash
docker compose exec app python3 -m pytest -v -rP
```

### Ejecutar un caso de prueba individual
Para validar un caso específico de forma aislada:

```bash
# Caso 1: Practice Form
docker compose exec app python3 -m pytest -v test/test_practice_form.py

# Caso 2: Create User
docker compose exec app python3 -m pytest -v test/test_create_user.py

# Caso 3: Select Menu
docker compose exec app python3 -m pytest -v test/test_select_menu.py

# Caso 4: Web Tables CRUD
docker compose exec app python3 -m pytest -v test/test_web_tables_crud.py

# Caso 5: Web Tables Validations (Empty & Invalid Format)
docker compose exec app python3 -m pytest -v test/test_web_tables_validation.py
```

### Detener el entorno
Al finalizar las pruebas:
```bash
docker compose down
```
