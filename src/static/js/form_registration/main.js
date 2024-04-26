import { FormRegistrationController } from "./form_registration_controller.js";
import { FormUpdateController } from "./form_update_controller.js";


export function new_main(route) {
	const token = document.head.querySelector("[name~=token][content]").content;

	new FormRegistrationController(route, token);
}

export function edit_main(route) {
	const token = document.head.querySelector("[name~=token][content]").content;

	new FormUpdateController(route, token);
}