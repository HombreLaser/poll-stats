import { editorFromTextArea } from "./editor.js";

function main() {
    window.addEventListener("DOMContentLoaded", () => {
	const sql_input = document.querySelector("textarea#sql-editor");

	if(sql_input) {
	    var editor = (window.editor = editorFromTextArea(sql_input, {}));
	}
    });
}

main();
