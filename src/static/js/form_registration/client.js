import { FormParser } from "./form_parser.js";


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
        const form_parser = new FormParser(form);
        const entries = form_parser.parse();

        await fetch(submitted_form.action, {
            headers: {
                "X-CSRF-Token": token,
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify(entries),
            mode: "same-origin",
            credentials: "same-origin",
            redirect: "follow"
        }).then((response) => {
            if(response.redirected)
                window.location = response.url;
        });
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