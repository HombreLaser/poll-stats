# El usuario maestro puede crear usuarios (normales).

## Responsable: Luis Sebastian

El usuario maestro puede registrar nuevos usuarios. (Revisar [este ticket](./registro_usuarios.md) para la
lógica de las invitaciones y la activación de usuarios). Requiere:

* Controlador de usuarios en maestro. Métodos: new, edit, create, index. Edit quedará inhabilitado cuando el
  usuario registrado haya sido activado por la invitación (añadir esta lógica después del ticket de registro
  de usuarios).
* Formulario de registro de usuario.
* Índice de usuarios registrados.