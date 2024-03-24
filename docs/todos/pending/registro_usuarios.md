# Añadir registro de usuarios

## Responsable:

El usuario maestro puede añadir nuevos usuarios en la plataforma. Al añadir un usuario, se generará un
URL de invitación que al ser accedido, te pedirá asignar una contraseña a este nuevo usuario.

Esta feature engloba los siguientes requisitos:

* Definición de un modelo Invitation (consultar el diagrama entidad-relación para más detalles: tiene una
  relación con UserAccount).
* Controlador de registros: sólo tendrá dos métodos, new y create. New renderizará el formulario que le
  pedirá al usuario la nueva contraseña. Create será el endpoint para la petición POST.
  * El método create seguirá la siguiente lógica: en el usuario creado por maestro se actualizará su campo
    activated a true, la invitación cambiará su status a used.
* Cuando un usuario se registre, no se podrá volver a acceder al URL de invitación generado (Añadir un constraint
  que cheque el status de la invitación).
