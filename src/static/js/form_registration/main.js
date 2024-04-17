import { FormRegistrationController } from "./form_registration_controller.js";


export function main(route) {
    const token = document.head.querySelector("[name~=token][content]").content;

    new FormRegistrationController(route, token);
}