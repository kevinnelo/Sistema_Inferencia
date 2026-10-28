# Descripción
El código implementa un sistema de apoyo para un DJ que recomienda qué acción musical tomar según el tipo de evento, su momento y la reacción del público. Utiliza probabilidades bayesianas para actualizar y ordenar cinco posibles acciones a partir de las respuestas ingresadas, y guarda un registro de los cálculos. Además, permite ejecutar un cuestionario interactivo, una demostración con datos predeterminados y pruebas automáticas para verificar su funcionamiento.

# Tabla de Hipotesis
| Código | Siguiente acción principal | Probabilidad inicial |
| :--- | :--- | :--- |
| H1 | Mantener género y energía | 20 % |
| H2 | Aumentar gradualmente la energía | 20 % |
| H3 | Disminuir energía o preparar cierre | 20 % |
| H4 | Cambiar al género solicitado | 20 % |
| H5 | Consultar preferencias o causa de la reacción | 20 % |

## Ejecución

Ejecución del cuestionario
```bash
python3 main.py
```
Ejecución de ejemplo predeterminado
```bash
python3 main.py --demo
```
Verificar funcionamiento de todas las partes del codigo
```bash
python3 -m unittest -v
```
#Funcionamiento
El código está organizado en tres capas principales que trabajan juntas para recomendar acciones musicales a un DJ:

* **Presentación (`main.py`):** Realiza el cuestionario, recibe y valida las respuestas del usuario y muestra las recomendaciones ordenadas por probabilidad. También permite ejecutar una demostración con respuestas predeterminadas.
* **Negocio (`negocio.py`):** Procesa cada respuesta mediante cálculos bayesianos, actualiza la probabilidad de las cinco acciones posibles y genera el ranking de recomendaciones.
* **Datos (`datos.py`):** Carga la información de `conocimiento.json` en una base de datos SQLite (definida en `esquema.sql`) y permite consultar las hipótesis y las respuestas disponibles.

**Archivos adicionales:**
* `traza.json`: Guarda el historial de los cálculos para explicar cómo se obtuvo el resultado.
* `test_motor.py`: Contiene pruebas automáticas que verifican el funcionamiento del sistema.
