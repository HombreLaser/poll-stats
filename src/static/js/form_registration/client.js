export class Client {
  constructor(route, token) {
    this.route = route;
    this.token = token;
    this.parser = new DOMParser();
  }

  htmlFromResponse(body) {
    return this.parser.parseFromString(body, "text/html");
  }

  fromResponse(body, field_type) {
    return this.htmlFromResponse(body).querySelector(`.${field_type}`);
  }

  async submit(submitted_form) {
    const form = new FormData(submitted_form);

    const response = await fetch(submitted_form.action, {
        headers: {
            "X-CSRF-Token": token
        },
        method: "POST",
        body: form,
        mode: "same-origin",
        credentials: "same-origin",
        redirect: "follow"
    });

    return response;
  }

  async get(field_type) {
    const body = await fetch(
        `${this.route}?field_type=${field_type}`,
        {
            method: "GET",
            mode: "same-origin",
            credentials: "same-origin"
        }
    ).then((response) => { return response.text() });

    return this.fromResponse(body, field_type);
  }

  async getOption() {
    const body = await fetch(
      `${this.route}/selection/option`,
      {
          method: "GET",
          mode: "same-origin",
          credentials: "same-origin"
      }
    ).then((response) => { return response.text() });

    return this.htmlFromResponse(body);
  }
}