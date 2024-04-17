export class FormParser {
  constructor(form) {
    this.form = form;
  }

  parse() {
    const open_field_regex = /^open/;
    const entries_iterator = this.form.entries();
    var entries = [];
    var open_field_counter = 0;
    let current = entries_iterator.next();

    while(!current.done) {
      if(open_field_regex.exec(current.value[0])) {
        // Una pregunta abierta.
        open_field_counter++;
        const matcher = new RegExp(`^open_(content|type)_${open_field_counter}$`);
        var match = matcher.exec(current.value[0]);

        while(match != null && !current.done) {
          if(match[1] == "content") {
            entries.push(
              {
                content: current.value[1],
                type: "open"
              }
            );
          }

          current = entries_iterator.next();

          if(!current.done)
            match = matcher.exec(current.value[0]);
        }
      } else {
          var field = { content: current.value[1], type: "selection" };
          const option_matcher = /^(content|score)_(\d)$/;
          current = entries_iterator.next();
          // Saltamos type
          current = entries_iterator.next()
          var match = option_matcher.exec(current.value[0]);
          var options = [];

          while(match != null && !current.done) {
            const content = current.value[1];
            current = entries_iterator.next();
            const score = current.value[1];

            options.push(
              {
                content: content,
                score: score
              }
            );

            current = entries_iterator.next();
            
            if(!current.done)
              match = option_matcher.exec(current.value[0]);
          }

          field.options = options;
          entries.push(field);
      }
    }

    return entries;
  }
}