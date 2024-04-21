import { FormRegistrationController } from "./form_registration_controller.js";
import { FormPatchController } from "./form_patch_controller.js";


export function new_main(route) {
	const token = document.head.querySelector("[name~=token][content]").content;

	new FormRegistrationController(route, token);
}

export function edit_main(route) {
	const token = document.head.querySelector("[name~=token][content]").content;

	new FormPatchController(route, token);
}