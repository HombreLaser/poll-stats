# poll-stats
PIA de la clase de administración de proyectos de software.


## Programas que necesitas tener
- Instala [MariaDB](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.2&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&mirror=gigenet) o [MySQL](https://dev.mysql.com/downloads/workbench/).
- Asegúrate de tener instalado [Python](https://www.python.org/downloads/) a una versión 
    ```
        $ python --version
        > 3.11.X
    ```
- Asegúrate de tener instalado el sistema de gestión de paquetes PIP a la versión 
    ```
        $ pip --version
        24.x
    ```

_Nota: Lo anterior mencionado te servirá para no tener problemas al ejecutar el proyecto. Para utilizar MariaDB en windows lo puedes hacer desde la terminal Client o desde el gestor gráfico de HeidiSQL_ 

# Configuración
Posteriormente de instalar MariaDB o Mysql, configura el servidor de base de datos y crea una base de datos llamada poll_stats ayúdate del siguiente comando:

`CREATE DATABASE poll_stats;`

Si te configuraste como un super usuario, o un usuario con todos los privilegios, no necesitas asignarte privilegios para esta base de datos.

En la raíz del proyecto, copia `config.example.toml` y renómbralo a `config.toml`. Deberías ver algo como esto:

```toml
    [database]
    user = 'tu_usuario'
    password = 'tu_contraseña'

    [flask]
    APPLICATION_ROOT = "http://localhost:5000"
    SECRET_KEY = "texto_muy_largo"
```

En user, escribe tu usuario de mysql/Mariadb, en password tu contraseña. Para el secret key, abre una terminal y ejecuta el siguiente comando:

`python -c "import secrets; print(secrets.token_hex(32))"`

Copia y asigna el texto generado a SECRET_KEY.

Deja APPLICATION_ROOT sin cambiar.

# Ejecutando el proyecto
Abre la terminal en la raíz del proyecto y ejecuta los siguientes comandos para crear un entorno virtual e instalar las dependencias.
Recuerda que tendrás que ejecutar `env/bin/activate` cada que abras una terminal en el directorio del proyecto y quieras trabajar en él.

Si tienes "**Linux**" realiza lo siguiente

```toml
    # Genera un entorno virtual en ./env
    python -m venv env
    # Activa el entorno virtual
    source env/bin/activate
    # Instala las dependencias del proyecto.
    pip install -r requirements.txt
```

Si tienes "**Windows**" realiza lo siguiente

```toml
    # Genera un entorno virtual en ./env
    python -m venv env
    # Activa el entorno virtual
        - # En el simbolo del sistema
            env\Scripts\activate.bat
        - # En "PowerShell"
            .\env\Scripts\Activate.ps1
    # Instala las dependencias del proyecto.
    pip install -r requirements.txt
```

_Nota: Para verificar que se haya activado correctamente el entorno virtual, verás el nombre `(env)` en la línea de comandos. Cuando deeses desactivar el entorno virtual usa el comando `deactivate`._

Ya que tengas las dependencias y el entorno virtual listo, ejecuta las migraciones:

`flask --app main db upgrade`

Ya que hayas ejecutado las migraciones, tu base de datos está lista. Para iniciar la aplicación, escribe en la terminal:

`flask --app main run`

## Crea un usuario maestro
Cuando creas un usuario maestro puedes invitar a más miembros a que formen parte de tu red, para esto se necesita ejecutar el siguiente comando

```toml
    u = models.UserAccount(email='maestro@example.org', first_name='Nombre', last_name='Apellido')
    u.password = 'contraseña'
    u.role = 'master'
    db.session.add(u)
    db.session.commit()
```