export class Client {
    constructor(route) {
        this.route = route;
        this.parser = new DOMParser();
    }

    fromResponse(body, field_type) {
        return this.parser.parseFromString(body, "text/html").querySelector(`.${field_type}`);
    }

    async get(field_type) {
        const body = await fetch(
            `${this.route}?field_type=${field_type}`,
            {
                method: 'GET',
                mode: 'same-origin',
                credentials: 'same-origin'
            }
        ).then((response) => { return response.text() });

        return this.fromResponse(body, field_type);
    }
}