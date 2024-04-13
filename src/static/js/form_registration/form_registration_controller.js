import { Client } from "./client.js";


export class FormRegistrationController {
    constructor(route) {
        this.client = new Client(route);
        this.select_button_ids = [];
        this.form = document.getElementById("form-registration");
        this.field_button = document.getElementById("new-field-button");
        this.listenForNewFields();
    }

    listenForNewFields() {
        this.field_button.addEventListener("click", this.renderField.bind(this));
    }

    listenForFieldTypeSelection(field) {
        const select_field_id = field.querySelector(".form-select").id;
        this.form.elements[select_field_id].addEventListener("change", this.changeField.bind(this));
    }

    changeField(event) {
        const selected_index = event.target.selectedIndex;
        const selected_value = event.target.options[selected_index].value;
    
        this.client.get(selected_value).then((field) => {
            event.target.parentElement.parentElement.replaceWith(field);
            field.querySelector(".form-select").selectedIndex = selected_index;
            this.listenForFieldTypeSelection(field);
        });
    }

    renderField(event) {
        event.preventDefault();
        this.client.get("open").then((field) => {
            this.form.insertBefore(field, this.form.firstChild);
            this.listenForFieldTypeSelection(field);
        });
    }
}