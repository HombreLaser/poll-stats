import { Controller } from "./controller.js";


export class FormRegistrationController extends Controller {
  async submit(event) {
    event.preventDefault();
    const response = await this.client.submit(event.target);
    await this.processResponse(response);
  }
}