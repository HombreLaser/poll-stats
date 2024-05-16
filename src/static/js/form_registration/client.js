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

    async submit(submitted_form, method="POST") {
	const form = new FormData(submitted_form);

	const response = await fetch(submitted_form.action, {
            headers: {
		"X-CSRF-Token": token
            },
            method: method,
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

    async modify_status(endpoint) {
	const form_id = window.location.pathname.split('/')[3];
	const response = await fetch(
	    window.location.href.replace("/edit", endpoint),
	    {
		headers: {
		    "X-CSRF-Token": token
		},
		method: "POST",
		mode: "same-origin",
		credentials: "same-origin",
		redirect: "follow"
	    }
	);

	return response;
    }

    async publish(event) {
	event.preventDefault();
	const response = await this.modify_status("/publish");

	if(response.status == 200)
	    window.location = response.url;
    }

    async close(event) {
	event.preventDefault();
	const response = await this.modify_status("/close");
	
	if(response.status == 200)
	    window.location = response.url;
    }
}
