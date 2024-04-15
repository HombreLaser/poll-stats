import { FormParser } from "./form_parser.js";


export class Client {
    constructor(route) {
        this.route = route;
        this.parser = new DOMParser();
    }

    htmlFromResponse(body) {
        return this.parser.parseFromString(body, "text/html");
    }

    fromResponse(body, field_type) {
        return this.htmlFromResponse(body).querySelector(`.${field_type}`);
    }

    submit(submitted_form) {
        const form = new FormData(submitted_form);
        const form_parser = new FormParser(form);
        form_parser.parse();
        console.log("Submitted?")
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