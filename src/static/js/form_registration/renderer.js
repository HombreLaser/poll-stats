export class Renderer {
  constructor(client, field_button, form) {
    this.client = client;
    this.field_button = field_button;
    this.form = form;
    this.last_rendered_field = null;
    this.open_field_counter = 0;
    this.selection_field_counter = 0;
    this.options_counter = 0;
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
      this.setOptionFieldNames(option);
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
    option.getElementsByClassName("btn btn-danger remove-question")[0]
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
    const new_content_field_name = `${type}_content_${counter}`;
    const new_type_name = `${type}_type_${counter}`;

    field_container.children[0].children[0].setAttribute("name", new_content_field_name);
    field_container.children[1].children[0].setAttribute("name", new_type_name);
  }

  setOptionFieldNames(options) {
    var options_container = options.querySelector(".options");

    options_container.children[0].children[0].setAttribute("name", `content_${this.options_counter}`);
    options_container.children[1].children[0].setAttribute("name", `score_${this.options_counter}`);
  }
}