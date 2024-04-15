export class FormParser {
  constructor(form) {
    this.form = form;
  }

  parse() {
    const open_field_regex = /^open/;
    const selection_field_regex = /^selection/;
    const entries_iterator = this.form.entries();
    let current = entries_iterator.next();

    while(!current.done) {
      if(open_field_regex.exec(current.value[0]))
        console.log("I'm in");
      else
        console.log("I'm not in!!! What??");

      current = entries_iterator.next();
    }
  }
}