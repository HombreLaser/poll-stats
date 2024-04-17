from wtforms import Field


class ListField(Field):
    widget = None

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist
        else:
            self.data = []


class OptionsField(Field):
    widget = None

    def process_formdata(self, valuelist):
        self.data = []
       
        for option in valuelist:
            self.data.append({
                'content': option.content.data,
                'score': option.score.data
            })
