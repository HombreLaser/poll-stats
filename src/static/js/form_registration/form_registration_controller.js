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

    disableButton(button, event, func) {
        button.classList.remove("btn-primary");
        button.classList.add("btn-secondary");
        button.setAttribute("disabled", true);
        button.removeEventListener(event, func, true);
    }

    addOption(event) {
        event.preventDefault();
        var new_option_button = event.target;
        var options_container = new_option_button.parentElement
                                                 .parentElement
                                                 .querySelector(".options-container");

        this.client.getOption().then((option) => {
            options_container.appendChild(option.querySelector(".options"));
        });

        if(options_container.children.length >= 3) {
            this.disableButton(new_option_button, "click", this.addOption);

            return;
        }
    }

    changeField(event) {
        const selected_index = event.target.selectedIndex;
        const selected_value = event.target.options[selected_index].value;
    
        this.client.get(selected_value).then((field) => {
            event.target.parentElement.parentElement.replaceWith(field);
            field.querySelector(".form-select").selectedIndex = selected_index;
            this.listenForFieldTypeSelection(field);

            if(selected_value == "selection") {
                this.addOption = this.addOption.bind(this);
                field.getElementsByClassName("btn btn-primary add-option")[0]
                     .addEventListener("click", this.addOption);
            }
        });
    }

    renderField(event) {
        event.preventDefault();
        this.client.get("open").then((field) => {
            this.form.insertBefore(field, this.field_button);
            this.listenForFieldTypeSelection(field);
        });
    }
}