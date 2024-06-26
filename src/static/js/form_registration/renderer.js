export class Renderer {
  constructor(client, field_button, form, update_form=false) {
    this.update_form = update_form;
    this.client = client;
    this.field_button = field_button;
    this.form = form;
    this.last_rendered_field = null;
    this.open_field_counter = 0;
    this.selection_field_counter = 0;
    this.options_counter = document.querySelectorAll("input[name^=option").length;
  }

  disableButton(button, event, func) {
    button.classList.remove("btn-primary");
    button.classList.add("btn-secondary");
    button.setAttribute("disabled", true);
    button.removeEventListener(event, func, true);
  }

  enableButton(button, event, func) {
    button.classList.remove("btn-secondary");
    button.classList.add("btn-primary");
    button.removeAttribute("disabled");
    button.addEventListener(event, func);
  }

  addOption(event) {
    event.preventDefault();
    this.options_counter += 1;
    var new_option_button = event.target;
    var options_container = new_option_button.parentElement
                                             .parentElement
                                             .querySelector(".options-container");

    this.client.getOption().then((option) => {
      const new_option = option.querySelector(".options");
      this.setOptionFieldNames(options_container, option);
      options_container.appendChild(new_option);
      this.listenForOptionDeletion(options_container, new_option, new_option_button);
    });

    if(options_container.children.length >= 3) {
      this.disableButton(new_option_button, "click", this.addOption);

      return;
    }
  }

  changeField(event) {
    const selected_index = event.target.selectedIndex;
    const selected_value = event.target.options[selected_index].value;
    var current_field_container = event.target.parentElement.parentElement;

    this.client.get(selected_value).then((field) => {
      this.setLastRenderedField(field);
      this.decreaseRelevantCounter(current_field_container);
      this.increaseCounter(field.getAttribute("class"));
      this.setFieldNames(field);
      current_field_container.replaceWith(field);
      field.querySelector(".form-select").selectedIndex = selected_index;
      this.listenForFieldTypeSelection(field);
      this.listenForFieldDeletion(field);

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
      this.increaseCounter("open");
      this.setLastRenderedField(field);
      this.setFieldNames(field);
      this.form.insertBefore(field, this.field_button);
      this.listenForFieldTypeSelection(field);
      this.listenForFieldDeletion(field);
    });
  }

  listenForFieldDeletion(field) {
    field.getElementsByClassName('btn btn-danger remove-question')[0]
         .addEventListener("click", (event) => {
           event.preventDefault();
           field.remove();
         });
  }

  listenForOptionDeletion(options_container, option, add_option_button) {
    option.getElementsByClassName("btn btn-danger remove-option")[0]
          .addEventListener("click", (event) => {
            event.preventDefault();
            option.remove();
            
            if(options_container.children.length <= 3)
              this.enableButton(add_option_button, "click", this.addOption);
          });
  }

  listenForFieldTypeSelection(field) {
    const select_field_id = field.querySelector(".form-select").id;
    this.form.elements[select_field_id].addEventListener("change", (event) => {
      this.changeField(event);
    });
  }

  increaseCounter(counter_to_increase) {
    if(counter_to_increase == "open")
      this.open_field_counter += 1;
    else
      this.selection_field_counter += 1;
  }

  decreaseRelevantCounter(field) {
    if(field.getAttribute("class") == "open")
      this.open_field_counter -= 1;
    else
      this.selection_field_counter -= 1;
  }

  setLastRenderedField(field) {
    this.last_rendered_field = field;
  }

  setFieldNames(field_container) {
    const type = field_container.getAttribute("class");
    const counter = type == "open" ? this.open_field_counter : this.selection_field_counter;

    if(this.update_form)
      var new_content_field_name = `new_${type}[content][${counter}]`;
    else
      var new_content_field_name = `${type}[content][${counter}]`;

    field_container.children[0].children[0].setAttribute("name", new_content_field_name);
  }

  setOptionFieldNames(options_container, options) {
    const input_name_regex_results = /((new_)?selection)\[content\]\[(\d+)\]/.exec(options_container.parentElement.children[0].children[0].name);
    const selection_id = input_name_regex_results[3];
    const selection_type = input_name_regex_results[1];

    if(this.update_form)
      var name = `new_option[${this.options_counter}][${selection_type}][${selection_id}]`;
    else
      var name = `option[${this.options_counter}][${selection_type}][${selection_id}]`;

    const container = options.querySelector(".options");
    container.children[0].children[0].setAttribute("name", name + "[content]");
    container.children[1].children[0].setAttribute("name",  name + "[score]");
  }

  renderErrors(errors) {
    const elements = Array.from(this.form.elements);
    const question_regex = /(open|selection)\[(content|type)\]\[\d\]/;
    var option_errors_index = 0;
    var question_errors_index = 0;

    // Errores en el campo de nombre de formulario.
    if('form' in errors)
      this.renderErrorsInField(elements[0], errors.form);

    for(const element of elements.slice(1)) {
      if(element.nodeName != "INPUT" || element.id == "submit-button")
        continue;

      if(question_regex.exec(element.name)) {
        this.renderErrorsInField(element, errors.questions[question_errors_index]);
        ++question_errors_index;

        continue;
      }

      if(errors?.options?.length > 0)
        this.renderErrorsInField(element, errors.options[question_errors_index - 1][option_errors_index]);

      ++option_errors_index;
    }
  }

  renderErrorsInField(field, errors) {
    if(!errors)
      return;
    
    field.setAttribute("class", field.getAttribute("class") + " is-invalid");
    const errors_list = this.createErrorList(errors);
    field.parentElement.appendChild(errors_list);
  }

  createErrorList(errors) {
    const list = document.createElement("ul");
    list.setAttribute("class", "text-danger no-bullets");

    for(const attribute of ['content', 'name', 'options']) {
      if(!(attribute in errors))
        continue;

      for(const error of errors[attribute]) {
        const error_element = document.createElement("li");
        error_element.innerText = error;
        list.appendChild(error_element);
      }
    }

    return list;
  }
}