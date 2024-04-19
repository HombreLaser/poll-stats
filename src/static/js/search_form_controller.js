class SearchFormController {
    constructor() {
        this.params = ["per_page", "order_by", "order"];
        this.query_params = this.getQueryParams();
        this.elements = [
            { "per_page": document.getElementById("per-page-select") }, 
            { "order_by": document.getElementById("order-by-select") },
            { "order": document.getElementById("order-method-select") }
        ];
        this.setSelectedValues();
    }

    setSelectedValues() {
        for(var object of this.elements) {
            for(const [param, element] of Object.entries(object)) {
                const query_param = this.query_params.get(param);
                
                if(!query_param)
                    continue;

                element.selectedIndex = Array.from(element.options).findIndex((option) => {
                    return option.value == query_param;
                });
            }
        }
    }

    getQueryParams() {
        const current_query_params = new URLSearchParams(window.location.search);
        var previous_query_params;
        var query_params = new URLSearchParams();

        try {
            previous_query_params = new URLSearchParams((new URL(document.referrer)).search);
        } catch(error) {
            return new URLSearchParams();
        }

        for(const param of this.params) {
            if(previous_query_params.get(param) == null) {
                if(current_query_params.get(param) != null)
                    query_params.append(param, current_query_params.get(param));
            } else
                query_params.append(param, previous_query_params.get(param));
        }

        return query_params;
    }
}

new SearchFormController();