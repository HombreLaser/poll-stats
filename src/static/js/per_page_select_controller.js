class PerPageSelectController {
    constructor() {
        this.query_params = this.getQueryParams();
        this.select_button = document.getElementById("per-page-select");
        this.setSelectedValue();
        console.log('Hello!')
    }

    setSelectedValue() {
        const elements_per_page = this.query_params.get("per_page");

        if(!elements_per_page)
            return;

        this.select_button.selectedIndex = Array.from(this.select_button.options).findIndex((option) => {
            return option.value == elements_per_page;
        });
    }

    getQueryParams() {
        var previous_query_params;

        try {
            previous_query_params = new URLSearchParams((new URL(document.referrer)).search);
        } catch(error) {
            return new URLSearchParams();
        }

        if(previous_query_params.get("per_page") == null) 
            return new URLSearchParams(window.location.search);
        
        return previous_query_params;
    }
}

new PerPageSelectController();