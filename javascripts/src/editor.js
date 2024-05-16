import { EditorView, basicSetup } from "codemirror";
import { keymap } from "@codemirror/view";
import { sql, SQLDialect } from "@codemirror/lang-sql";

const sqlite = SQLDialect.define({
    keywords:
    "and as asc between by case cast count current_date current_time current_timestamp desc distinct each else escape except exists explain filter first for from full generated group having if in index inner intersect into isnull join last left like limit not null or order outer over pragma primary query raise range regexp right rollback row select set table then to union unique using values view virtual when where",
    // https://www.sqlite.org/datatype3.html
    types: "null integer real text blob",
    builtin: "",
    operatorChars: "*+-%<>!=&|/~",
    identifierQuotes: '`"',
    specialVar: "@:?$",
});

export function editorFromTextArea(textarea, conf = {}) {
    let view = new EditorView({
	doc: textarea.value,
	extensions: [
	    keymap.of([
		{
		    key: "Shift-Enter",
		    run: function () {
			textarea.value = view.state.doc.toString();
			textarea.form.submit();
			return true;
		    },
		},
		{
		    key: "Meta-Enter",
		    run: function () {
			textarea.value = view.state.doc.toString();
			textarea.form.submit();
			return true;
		    },
		},
	    ]),
	    basicSetup,
	    EditorView.lineWrapping,
	    sql({
		dialect: sqlite,
		schema: conf.schema,
		tables: conf.tables,
		defaultTableName: conf.defaultTableName,
		defaultSchemaName: conf.defaultSchemaName,
	    }),
	],
    });

    let editorDOM = view.contentDOM.closest(".cm-editor");
    let observer = new ResizeObserver(function () {
	view.requestMeasure();
    });
    observer.observe(editorDOM, { attributes: true });

    textarea.parentNode.insertBefore(view.dom, textarea);
    textarea.style.display = "none";
    if (textarea.form) {
	textarea.form.addEventListener("submit", () => {
	    textarea.value = view.state.doc.toString();
	});
    }
    return view;
}
