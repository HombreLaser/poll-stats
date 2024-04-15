import { Client } from "./client.js";
import { Renderer } from "./renderer.js";


export class FormRegistrationController {
  constructor(route) {
    this.client = new Client(route);
    this.form = document.getElementById("form-registration");
    this.field_button = document.getElementById("new-field-button");
    this.renderer = new Renderer(this.client, this.field_button, this.form);
    this.listenForNewFields();
    this.listenForSubmit();
  }

  listenForNewFields() {
    this.field_button.addEventListener("click", (event) => {
      this.renderer.renderField(event);
    });
  }

  listenForSubmit() {
    this.form.addEventListener("submit", this.submit.bind(this));
  }

  submit(event) {
    event.preventDefault();
    this.client.submit(event.target);
  }
}