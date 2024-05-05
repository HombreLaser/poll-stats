# Reportes estadísticos

## Responsable: Juan José

Procesamiento de respuestas, generación de reportes estadísticos.

- [X] Procesamiento de respuestas 
- [ ] Generación de la vista del reporte estadístico.

Crear un endpoint que sirva JSON para ser consumido por javascript via fetch.
Crea un archivo `api_reports_controller.py` en src/controllers/api/.

Importa `Blueprint` de flask y crea un blueprint. Con ese blueprint puedes registrar 
una ruta, que será usada por el javascript en el frontend. Importa el modelo form y 
el objeto db para poder extraerlo de la base de datos.

```python
from flask import Blueprint
from src.database.models import Form
from src.database import db


api_reports_blueprint = Blueprint('api_reports_controller', __name__)

@api_reports_blueprint.get('/api/reports/<int:form_id>')
def index(form_id):
	# Extrae el formulario con su llave primaria.
	# No olvides checar si es None y regresar un 404 
	# con return tu_json_con_el_mensaje_de_error, 404
	form = db.session.get(Form, form_id)
```

Guarda el reporte en un diccionario y retórnalo: flask se encargará de servirlo como un JSON.

Para que puedas usar tu ruta en la app, regístrala, importándola en src/controllers/api/__init__.py:

```python
import src.controllers.api.api_reports_controller
```
