# Formularios

## Responsable:

Todo lo referente a formularios: controlador, vistas, lógica. Es posible asignar este ticket a dos personas debido a 
su complejidad.

* Controlador de formularios: new, patch, index, get, create. El método create NO recibe un Web Form, recibe JSON
  mediante una petición AJAX hecha en el javascript incluido en new.
* Vistas a crear (referirse al mockup). El formulario renderizado en new y edit es dinámico.
* La vista de un formulario particular presentará al usuario con la opción de publicar. Al publicarlo, ya no podrá
  ser editado y se incluirá un campo donde se mostrará el URL del formulario a compartir. 
* Al ser publicado, la vista de un formulario particular cambiará el botón de "Publicar" por uno que diga "Dejar de recibir respuestas".
* Las preguntas creadas tendrán un peso o puntaje (TODO: qué intervalos tomar en cuenta).

Ticket relacionado: [creación de respuestas](./creacion_respuestas.md)
Ticket relacionado: [creación de modelo de formulario](./modelo_form.md)