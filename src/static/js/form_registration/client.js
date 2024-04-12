export class Client {
    constructor(route) {
        this.route = route;
        this.parser = new DOMParser();
    }

    fromResponse(body) {
        return this.parser.parseFromString(body, "text/html");
    }

    async get(field_type) {
        const response = await fetch(`${this.route}?field_type=${field_type}`, {
            method: 'GET',
            mode: 'same-origin',
            credentials: 'same-origin'
        });

        return response.text().then(this.fromResponse.bind(this));
    }
}