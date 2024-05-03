# poll-stats
PIA de la clase de administración de proyectos de software

# Configuración
Instala [MariaDB](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.2&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&mirror=gigenet) o MySQL.

Una vez que tengas configurada el servidor de base de datos, crea una base de datos llamada poll_stats:

`CREATE DATABASE poll_stats;`

Si te configuraste como un super usuario, o un usuario con todos los privilegios, no necesitas asignarte privilegios para esta base
de datos.

En la raíz del proyecto, copia `config.example.toml` y renómbralo a `config.toml`. Deberías ver algo como esto:

```toml
[database]
user = 'tu_usuario'
password = 'tu_contraseña'

[flask]
APPLICATION_ROOT = "http://localhost:5000"
SECRET_KEY = "texto_muy_largo"
```

En user, escribe tu usuario de mysql/mariadb, en password tu contraseña. Para el secret key, abre una terminal y ejecuta:

`python -c "import secrets; print(secrets.token_hex(32))"`

Copia y asigna el texto generado a SECRET_KEY.
Deja APPLICATION_ROOT sin cambiar.

# Ejecutando el proyecto

Abre la terminal en la raíz del proyecto y ejecuta los siguientes comandos para crear un entorno virtual e instalar las dependencias.
Recuerda que tendrás que ejecutar `source env/bin/activate` cada que abras una terminal en el directorio del proyecto y quieras trabajar
en él.

```
# Genera un entorno virtual en ./env
python -m venv env
# Activa el entorno virtual
source env/bin/activate
# Instala las dependencias del proyecto.
pip install -r requirements.txt
```
Ya que tengas las dependencias y el entorno virtual listo, ejecuta las migraciones:

`flask --app main db upgrade`

Ya que hayas ejecutado las migraciones, tu base de datos está lista. Para iniciar la aplicación, escribe en la terminal:

`flask --app main run`
