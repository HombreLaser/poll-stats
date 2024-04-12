import { Client } from "./client.js";


export class FormRegistrationController {
    constructor(route) {
        this.client = new Client(route);
        this.form = document.getElementById("form-registration");
        this.field_button = document.getElementById("new-field-button");
        this.init();
    }

    init() {
        this.listenForNewFields();
    }

    listenForNewFields() {
        this.field_button.addEventListener("click", this.connect.bind(this));
    }

    connect(event) {
        event.preventDefault();
        console.log("Connected!");
    }
}