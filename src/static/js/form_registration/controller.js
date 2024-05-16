import { Client  } from "./client.js";
import { Renderer } from "./renderer.js";


export class Controller {
    constructor(route, token, update_form=false) {
	this.client = new Client(route, token);
	this.form = document.getElementById("form-registration");
	this.field_button = document.getElementById("new-field-button");
	this.renderer = new Renderer(this.client, this.field_button, this.form, update_form);
	this.listenForNewFields();
	this.listenForSubmit();
    }

    listenForSubmit() {
	if(this.form)
	    this.form.addEventListener("submit", this.submit.bind(this));
    }
    
    listenForNewFields() {
	if(this.field_button) {
	    this.field_button.addEventListener("click", (event) => {
		this.renderer.renderField(event);
	    });
	}
    }

    async processResponse(response) {
	if(response.status == 200) {
	    const body = await response.text();
	    const flash_message = this.client.htmlFromResponse(body).getElementById("flash-message");
	    window.location = response.url;
	    return;
	}

	const errors = await response.json();

	this.renderer.renderErrors(errors);
    }
}
