import { Controller } from "./controller.js";


export class FormPatchController extends Controller {
  constructor(route, token) {
    super(route, token);
    this.prepareFields();
    this.old_form_data = (new FormParser(new FormData(this.form))).parseByIds();
    this.disableButtons();
    this.listenForNewOptions();
    this.listenForFieldDeletions();
  }

  async submit(event) {
    event.preventDefault();
    const response = this.client.patch(event.target, this.current_form_data);
    this.processResponse(response);
  }

  disableButtons() {
    for(const button of document.getElementsByClassName("btn btn-primary add-option")) {
      const options_container = button.parentElement.parentElement
                                      .querySelector(".options-container");

      if(options_container.children.length >= 3)
        this.renderer.disableButton(button, "click", this.renderer.addOption);                      
    }
  }

  listenForNewOptions() {
    for(const button of document.getElementsByClassName("btn btn-primary add-option")) {
      button.addEventListener("click", this.renderer.addOption.bind(this.renderer));
    }
  }

  listenForFieldDeletions() {
    const fields = this.form.querySelectorAll("div[class^=open_],div[class^=selection_]");

    for(const field of fields) {
      this.renderer.listenForFieldDeletion(field);
    }
  }

  prepareFields() {
    const id_regex = /(open|selection|options)_(\d)/;
    this.open_question_ids = [];
    this.selection_question_ids = [];
    this.option_ids = [];

    document.querySelectorAll("div[class^=open_]").forEach((elem) => {
      this.open_question_ids.push(
        id_regex.exec(elem.getAttribute("class").split(' ')[0])[2]
      );
      this.prepare(elem, "open", this.open_question_ids.slice(-1));
    });

    document.querySelectorAll("div[class^=selection_]").forEach((elem) => {
      this.selection_question_ids.push(
        id_regex.exec(elem.getAttribute("class").split(' ')[0])[2]
      );
      this.prepare(elem, "selection", this.selection_question_ids.slice(-1));
    });

    document.querySelectorAll("div[class^=options_]").forEach((elem) => {
      this.option_ids.push(
        id_regex.exec(elem.getAttribute("class").split(' ')[0])[2]
      );
      this.prepareOptionField(elem, this.option_ids.slice(-1));
    });
  }

  prepare(field, type, id) {
    field.children[0].children[0].setAttribute("name", `${type}_content_id_${id}`);
    field.children[1].children[0].setAttribute("name", `${type}_type_id_${id}`);
  }

  prepareOptionField(field, id) {
    field.children[0].children[0].setAttribute("name", `option_content_${id}`);
    field.children[1].children[0].setAttribute("name", `option_score_${id}`);
  }
}